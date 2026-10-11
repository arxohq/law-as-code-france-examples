#!/usr/bin/env python3
"""Regression of case famille-dans-le-temps: six household snapshots x
saved questions, tabled expectations.

WHAT THIS CHECKS. Famille2024_03 carries March 2024 (AF brut 200.00 ->
net 199.00; housing net 344.00 read-only); Famille2024_08 carries the
2024 rentree (ARS 400.00 -> net 398.00); Famille2025_07 carries Chloe's
birth prime (1000.00 -> net 995.00); Famille2025_12 carries AF recovery
(December echeance 318.40, indu 500 at rate 0.25 -> net 238.80);
Famille2026_03 carries the prescribed 2021 indu (full 318.40) and the
RSA carry (allocation 600.00, PF indu 300 at rate 0.30 -> net 420.00);
Famille2026_06 carries PA recovery from a STATED served 280.00
(given-PA regression: own indu 150.00 + RSA carry 60.00 at rate
0.25 -> net 210.00; the joined derivation runs separately in
tests/dossier-pa-cascade-2026-06.lawtest and is not claimed here).
Bruts are caller-stated owner-chain values (evidence only; see
sources/WITNESS.md).

    python3 corpus/laws/fr/prestations-versement/examples/famille-dans-le-temps/check.py
    python3 corpus/laws/fr/prestations-versement/examples/famille-dans-le-temps/check.py --json

RUN STATUS (06.10.2026): not run in this environment — `law ask` needs
materialized deps for the case package (law.lock is git-ignored; the
repo ./law wrapper would start a build). The same six checkpoints run
green as .lawtest in the #dossier family (70/70 lawc direct run).
FINISH-W2 adds the seventh checkpoint (pa-rec-2026-06 + dossier-pa
lawtest); its run is pending the reviewer.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
PACKAGE = "corpus/laws/fr/prestations-versement/examples/famille-dans-le-temps"

#: (case, query) -> expected §62 status.
EXPECTED = {
    ("Famille2024_03", "af-net-2024-03"): "TRUE_ONLY",
    ("Famille2024_08", "ars-net-2024-08"): "TRUE_ONLY",
    ("Famille2025_07", "prime-net-2025-07"): "TRUE_ONLY",
    ("Famille2025_12", "af-rec-2025-12"): "TRUE_ONLY",
    ("Famille2026_03", "af-presc-2026-03"): "TRUE_ONLY",
    ("Famille2026_03", "rsa-carry-2026-03"): "TRUE_ONLY",
    ("Famille2026_06", "pa-rec-2026-06"): "TRUE_ONLY",
}


#: Path to the launcher; run_all.sh passes the built binary via --law.
LAW = [str(ROOT / "law")]
OUTPUT = None


def ask(case: str, query: str) -> dict:
    result = subprocess.run(
        [LAW[0], "ask", PACKAGE, "--case", case,
         "--query-json", f"{PACKAGE}/queries/{query}.json"] + (["--out", str(OUTPUT / case / query)] if OUTPUT else []),
        cwd=ROOT, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": {"code": "NO_JSON",
                          "stderr": result.stderr[-2000:]}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--law", default=None)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    global OUTPUT
    OUTPUT = args.out.resolve() if args.out else None
    if args.law:
        LAW[0] = args.law
    rows = []
    failed = 0
    for (case, query), expected in EXPECTED.items():
        answer = ask(case, query)
        results = answer.get("results") or []
        status = results[0].get("truthStatus", "?") if len(results) == 1 else answer.get("error", {}).get("code", "?")
        computed = len(results) == 1 and results[0].get("evaluationStatus") == "COMPUTED"
        ok = status == expected and computed
        failed += not ok
        rows.append({"case": case, "query": query, "expected": expected,
                     "got": status, "ok": ok})
    if args.json:
        print(json.dumps({"failed": failed, "rows": rows}, indent=2,
                         ensure_ascii=False))
    else:
        for row in rows:
            mark = "PASS" if row["ok"] else "FAIL"
            print(f"{mark}: {row['case']} {row['query']} "
                  f"(expected {row['expected']}, got {row['got']})")
        print(f"{len(rows) - failed}/{len(rows)} dossier questions pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
