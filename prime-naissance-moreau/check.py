#!/usr/bin/env python3
"""Vérifie trois dossiers fictifs Moreau et les tests déclaratifs associés."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[5]
APL = "urn:fr:corpus:clir:pf-paje#"

#: (дело, вопрос) → (evaluationStatus, truthStatus, правила, обязанные примениться).
EXPECTED = {
    ("PlafondEgal", "droit"): ("COMPUTED", "TRUE_ONLY", [APL + "DroitPrimeNaissance"]),
    ("PlafondEgal", "montant"): ("COMPUTED", "TRUE_ONLY", [APL + "MontantPrimeNaissance"]),
    ("PlafondDepasse", "droit"): ("COMPUTED", "NEITHER", []),
    ("PlafondDepasse", "montant"): ("COMPUTED", "NEITHER", []),
    ("RessourcesAbsentes", "droit"): ("COMPUTED", "NEITHER", []),
    ("RessourcesAbsentes", "montant"): ("COMPUTED", "NEITHER", []),
    ("RessourcesAbsentes", "pourquoi-droit"): ("COMPUTED", "NEITHER", []),
}
JUDGMENTS = {}
POSITIONS = {}
ABSENT = {}


def run_json(command: list[str]) -> dict:
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"{' '.join(command)}\n{completed.stderr[-2000:]}") from error


def ask(law: str, case: str, query: str, output: Path) -> dict:
    result = run_json([law, "ask", str(PACKAGE), "--case", case,
                       "--query-json", str(PACKAGE / "queries" / f"{query}.json"),
                       "--out", str(output / case / query)])
    if "error" in result:
        raise RuntimeError(f"{case} {query}: {result['error']}")
    return result


def check(law: str, output: Path, law_test: bool = True) -> list[dict]:
    manifest = tomllib.loads((PACKAGE / "law.toml").read_text(encoding="utf-8"))
    registered = {entry["name"] for entry in manifest.get("cases", [])}
    named = {case for case, _ in EXPECTED} | set(POSITIONS)
    if registered != named:
        raise RuntimeError(f"состав дел {sorted(registered)} расходится с ожиданиями {sorted(named)}")
    rows = []
    for (case, query), (evaluation, truth, rules) in EXPECTED.items():
        result = ask(law, case, query, output)
        answer, = result["results"]
        got = (answer.get("evaluationStatus"), answer.get("truthStatus"))
        nodes = (result.get("proofGraph") or {}).get("nodes") or []
        missing = [rule for rule in rules
                   if not any(node.get("rule") == rule or f":apply:{rule}:" in node.get("id", "")
                              for node in nodes)]
        if (case, query) in JUDGMENTS:
            requests = sorted((item.get("predicate"), item.get("authority"))
                              for item in answer.get("judgmentRequests") or [])
            if requests != sorted(JUDGMENTS[(case, query)]):
                missing.append(f"запросы судье {requests} != {sorted(JUDGMENTS[(case, query)])}")
        if case == "RessourcesAbsentes" and query == "pourquoi-droit":
            inputs = [answer.get("value"), nodes]
            if not any("ressources_annuelles" in str(item) for item in inputs):
                missing.append("why_not: ressources_annuelles absent")
        rows.append({"case": case, "query": query, "expected": [evaluation, truth],
                     "got": list(got), "missing": missing,
                     "ok": got == (evaluation, truth) and not missing})
    for case, positions in POSITIONS.items():
        result = ask(law, case, "positions", output)
        held = {(item.get("template"), item.get("holder"), item.get("status"))
                for item in result.get("positions") or []}
        missing = [f"{template.rsplit('#', 1)[-1]} @ {holder}" for template, holder in positions
                   if (template, holder, "ACTIVE") not in held]
        missing += [f"лишняя {template.rsplit('#', 1)[-1]}" for template in ABSENT.get(case, [])
                    if any(t == template for t, _, _ in held)]
        rows.append({"case": case, "query": "positions", "expected": ["ACTIVE"] * len(positions),
                     "got": sorted(f"{t.rsplit('#', 1)[-1] if t else t}:{s}" for t, _, s in held),
                     "missing": missing, "ok": not missing})
    if not law_test:
        return rows
    completed = subprocess.run([law, "test", str(PACKAGE), "--json"], cwd=ROOT,
                               capture_output=True, text=True, check=False)
    rows.append({"case": "*", "query": "law test (tests/*.lawtest)", "expected": ["exit 0"],
                 "got": [f"exit {completed.returncode}"], "missing": [],
                 "ok": completed.returncode == 0})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--law", default=str(ROOT / "law"))
    parser.add_argument("--out", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-law-test", action="store_true",
                        help="не звать `law test` (бинарь движка без пользовательского CLI)")
    args = parser.parse_args()
    try:
        if args.out:
            rows = check(args.law, args.out.resolve(), not args.no_law_test)
        else:
            with tempfile.TemporaryDirectory(prefix=f"{PACKAGE.name}-") as temporary:
                rows = check(args.law, Path(temporary), not args.no_law_test)
    except (RuntimeError, ValueError, OSError, KeyError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    failed = sum(not row["ok"] for row in rows)
    if args.json:
        print(json.dumps({"failed": failed, "rows": rows}, indent=2, ensure_ascii=False))
    else:
        for row in rows:
            mark = "PASS" if row["ok"] else "FAIL"
            extra = f"; не хватает: {row['missing']}" if row["missing"] else ""
            print(f"{mark}: {row['case']} {row['query']} (ожидалось {row['expected']}, "
                  f"получено {row['got']}{extra})")
        print(f"{len(rows) - failed}/{len(rows)} проверок дела пройдено")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
