#!/usr/bin/env python3
"""Дело фойе с коэффициентом K (D. 832-25, чтение по R. 351-61): ответ и итог.

ЧТО ПРОВЕРЯЕТСЯ. Одно вымышленное дело (CoupleResidenceAutonomie, март 2026
года) и пять сохранённых вопросов `law ask`: E0 = 218,12546 €, Af = K × (E − E0)
= 143,9747608 € с K = 0,52 и N = 1,8 в proof-графе, отказ вывести Af при K = 0,53
(«arrondi à deux décimales par défaut»), месячное пособие 138,694873804 € и
сумма после CRDS 138,00139943498 €. Правило K обязано нести якорь отменённой
R. 351-61 — это и есть чтение формулы, опубликованной картинкой. Ожидания —
ответ канона, сверенный с репликой на дробях (sources/WITNESS.md). Затем
`law test` исполняет двойник §267 (tests/foyer-coefficient-k.lawtest).
Значения Decimal (K, N) двойник проверяет через Af: литерал Decimal в .lawtest
понижается в Number (граница D-42 канона).

Пакет — член workspace (DECISION-0459): зависимости разрешаются по имени среди
членов, `law.lock` и `deps/` не нужны. Корневой `./law` без LAW_BIN собирает
движок на каждый вызов — передайте готовый бинарь через `--law`.

    python3 corpus/laws/fr/apl/examples/foyer-coefficient-k/check.py --law <бинарь law>
    python3 corpus/laws/fr/apl/examples/foyer-coefficient-k/check.py --law <бинарь law> --json

RUN STATUS (10.10.2026): PASS 6/6 — `check.py --law <law>` с бинарём
`law` из HEAD d25481bde0: все вопросы `law ask` и шаг `law test` (exit 0).
Двойник §267 исполняет `law test`: `[tests].world` начинается с самого
пакета-дела (DECISION-0127 §3, DECISION-0165 §1.2, DECISION-0382 п. 3).
Ворота `check_lawtest_suites.py --package` двойник не исполняют: снимка CLIR
у вложенного пакета-дела нет по построению (docs/PACKAGE-LAYOUT.ru.md,
NOT_LOWERED). Запись — docs/status/2026-10-10-fr-cnaf-current-engine-check.ru.md.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[5]
APL = "urn:fr:corpus:clir:apl#"

#: (дело, вопрос) → (evaluationStatus, truthStatus, правила, обязанные примениться).
EXPECTED = {
    ("CoupleResidenceAutonomie", "equivalence-loyer-minimale"): ("COMPUTED", "TRUE_ONLY", [APL + "EquivalenceLoyerMinimale"]),
    ("CoupleResidenceAutonomie", "aide-formule"): ("COMPUTED", "TRUE_ONLY", [APL + "AideFoyerFormuleAPL", APL + "CoefficientPriseEnChargeAPLGeneral", APL + "NombreParts"]),
    ("CoupleResidenceAutonomie", "aide-formule-k-053"): ("COMPUTED", "NEITHER", []),
    ("CoupleResidenceAutonomie", "aide-mensuelle"): ("COMPUTED", "TRUE_ONLY", [APL + "ContributionsSocialesFoyerAPL", APL + "AideFoyerVersee"]),
    ("CoupleResidenceAutonomie", "aide-nette-crds"): ("COMPUTED", "TRUE_ONLY", [APL + "PrecompteCRDSMetropole"]),
}

#: (дело, вопрос) → коды issue, обязанные прозвучать в ответе.
ISSUES = {
}

#: (дело, вопрос) → (предикат, значение), выведенное в proof-графе ответа.
PROOF_VALUES = {
    ("CoupleResidenceAutonomie", "aide-formule"): [(APL + "coefficient_prise_en_charge", "0.52"), (APL + "nombre_parts", "1.8")],
}

#: (дело, вопрос) → (правило, якорь статьи в редакции, действующей в месяце права) в программе запроса (request.json).
ANCHORS = {
    ("CoupleResidenceAutonomie", "aide-formule"): [(APL + "CoefficientPriseEnChargeAPLGeneral", APL + "CCH_R351_61"), (APL + "CoefficientPriseEnChargeAPLGeneral", APL + "CCH_D832_25_ED2023_12")],
}

#: дело → (шаблон позиции, носитель), обязанные быть ACTIVE в ответе positions.
POSITIONS = {
}


def run_json(command: list[str]) -> dict:
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"{' '.join(command)}\n{completed.stderr[-2000:]}") from error


def number(value) -> Fraction | None:
    """Числовое значение узла значения: «0.52», «13/25» — одно число."""
    try:
        return Fraction(str(value))
    except (ValueError, ZeroDivisionError):
        return None


def proof_values(result: dict, predicate: str) -> list[Fraction]:
    """Значения последнего аргумента выведенных литералов `predicate` в proof-графе."""
    found = []
    def walk(item):
        if isinstance(item, dict):
            if item.get("predicate") == predicate and item.get("args"):
                tail = item["args"][-1]
                if isinstance(tail, dict) and "value" in tail:
                    value = number(tail["value"])
                    if value is not None:
                        found.append(value)
            for child in item.values():
                walk(child)
        elif isinstance(item, list):
            for child in item:
                walk(child)
    walk(result.get("proofGraph") or {})
    return found


def ask(law: str, case: str, query: str, output: Path) -> dict:
    return run_json([law, "ask", str(PACKAGE), "--case", case,
                     "--query-json", str(PACKAGE / "queries" / f"{query}.json"),
                     "--out", str(output / case / query)])


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
        dumped = json.dumps(result, ensure_ascii=False)
        missing += [f"issue {code}" for code in ISSUES.get((case, query), []) if code not in dumped]
        if ANCHORS.get((case, query)):
            request = json.loads((output / case / query / "request.json").read_text(encoding="utf-8"))
            by_id = {node["id"]: node for node in request["ir"]["nodes"]}
            for rule, anchor in ANCHORS[(case, query)]:
                if anchor not in (by_id.get(rule, {}).get("anchors") or []) or anchor not in by_id:
                    missing.append(f"у {rule.rsplit('#', 1)[-1]} нет якоря {anchor.rsplit('#', 1)[-1]}")
        for predicate, value in PROOF_VALUES.get((case, query), []):
            if Fraction(value) not in proof_values(result, predicate):
                missing.append(f"в proof-графе нет {predicate.rsplit('#', 1)[-1]} = {value}")
        rows.append({"case": case, "query": query, "expected": [evaluation, truth],
                     "got": list(got), "missing": missing,
                     "ok": got == (evaluation, truth) and not missing})
    for case, positions in POSITIONS.items():
        result = ask(law, case, "positions", output)
        held = {(item.get("template"), item.get("holder"), item.get("status"))
                for item in result.get("positions") or []}
        missing = [f"{template.rsplit('#', 1)[-1]} @ {holder}" for template, holder in positions
                   if (template, holder, "ACTIVE") not in held]
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
                        help="не звать `law test` (бинарь движка без пользовательского CLI); "
                             "двойник тогда проверяет check_lawtest_suites.py --package")
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
