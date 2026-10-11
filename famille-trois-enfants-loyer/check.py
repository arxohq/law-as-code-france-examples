#!/usr/bin/env python3
"""Семья с тремя детьми и наймом: AF по строкам DSS, жилищная помощь, сроки, позиции.

ЧТО ПРОВЕРЯЕТСЯ. Три дела одной вымышленной семьи Garnier. Garnier2026Avril
(прочтения ArrondiLignesDss, ArrondiCentimeHalfUp, PpPlancherFinal): полоса 1,
AF по строкам таблицы DSS 349,06 + 76,51 = 425,57 € (не 425,56 € округлённого
итога), AF после CRDS 423,44215 €, ALF: Pp 402,1515 €, пропорция D. 823-16 до
сантима и шаг к нижнему евро — 189,95295 € (не 190,59 €), после CRDS
189,00318525 €, право с 01.04.2026 (R. 823-10), позиции: ménage обязан
приложить документы (R. 823-2), касса обязана платить AF нетто и информировать.
Garnier2026AvrilTexteSeul (только PpPlancherFinal): AF-произведение 425,5624 €,
итог к выплате 425,56 € (правило MontantDu округляет итог), ALF — отказ
INEXACT_DIVISION. Garnier2026Mai: изменение 18.05.2026 действует с 01.06.2026
(R. 823-13), ménage обязан подтвердить изменение (R. 823-3). Каждое правило
«почему» проверяется вместе с якорем статьи. Ожидания — ответ канона, сверенный
с репликой на дробях (sources/WITNESS.md). Затем `law test` исполняет двойник
§267 (tests/famille-trois-enfants-loyer.lawtest).

Пакет — член workspace (DECISION-0459): зависимости разрешаются по имени среди
членов, `law.lock` и `deps/` не нужны. Корневой `./law` без LAW_BIN собирает
движок на каждый вызов — передайте готовый бинарь через `--law`.

    python3 corpus/laws/fr/prestations-versement/examples/famille-trois-enfants-loyer/check.py --law <бинарь law>
    python3 corpus/laws/fr/prestations-versement/examples/famille-trois-enfants-loyer/check.py --law <бинарь law> --json

RUN STATUS (10.10.2026): PASS 20/20 — `check.py --law <law>` с бинарём
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
AF = "urn:fr:corpus:clir:pf-af#"
APL = "urn:fr:corpus:clir:apl#"
PV = "urn:fr:corpus:clir:prestations-versement#"
CORE = "urn:fr:corpus:clir:pf-core#"
MENAGE = "urn:law:examples:fr:garnier:menage"
CAF = "urn:law:examples:fr:garnier:caf"

#: (дело, вопрос) → (evaluationStatus, truthStatus, правила, обязанные примениться).
EXPECTED = {
    ("Garnier2026Avril", "af-bande-1"): ("COMPUTED", "TRUE_ONLY", [AF + "Bande1"]),
    ("Garnier2026Avril", "af-mensuel-lignes"): ("COMPUTED", "TRUE_ONLY", [AF + "MontantMensuelLignes", AF + "ArrondiLignesMetropole"]),
    ("Garnier2026Avril", "af-du-lignes"): ("COMPUTED", "TRUE_ONLY", [AF + "MontantDu"]),
    ("Garnier2026Avril", "af-du-arrondi-total"): ("COMPUTED", "NEITHER", []),
    ("Garnier2026Avril", "af-net-crds"): ("COMPUTED", "TRUE_ONLY", [PV + "RetenueCRDSAF", PV + "NetApresCRDSAF"]),
    ("Garnier2026Avril", "al-participation"): ("COMPUTED", "TRUE_ONLY", [APL + "ParticipationPersonnelle"]),
    ("Garnier2026Avril", "al-apres-contributions"): ("COMPUTED", "TRUE_ONLY", [APL + "DegressiviteProportionnelleArrondie", APL + "ArrondiIntermediaireCentime", APL + "MinorationForfaitaireAppliquee", APL + "ArrondiContributionsSociales"]),
    ("Garnier2026Avril", "al-sans-arrondi-euro"): ("COMPUTED", "NEITHER", []),
    ("Garnier2026Avril", "al-mensuelle"): ("COMPUTED", "TRUE_ONLY", [APL + "AideVerseeAllocationFamiliale", APL + "AideMensuelleMetropole"]),
    ("Garnier2026Avril", "al-nette-crds"): ("COMPUTED", "TRUE_ONLY", [APL + "PrecompteCRDSMetropole"]),
    ("Garnier2026Avril", "al-droit-commence"): ("COMPUTED", "TRUE_ONLY", [APL + "OuvertureApresConditions"]),
    ("Garnier2026AvrilTexteSeul", "af-mensuel-exact"): ("COMPUTED", "TRUE_ONLY", [AF + "MontantMensuel"]),
    ("Garnier2026AvrilTexteSeul", "af-du-arrondi-total"): ("COMPUTED", "TRUE_ONLY", [AF + "MontantDu"]),
    ("Garnier2026AvrilTexteSeul", "af-du-lignes"): ("COMPUTED", "NEITHER", []),
    ("Garnier2026AvrilTexteSeul", "af-net-crds-arrondi-total"): ("COMPUTED", "TRUE_ONLY", [PV + "RetenueCRDSAF", PV + "NetApresCRDSAF"]),
    ("Garnier2026AvrilTexteSeul", "al-mensuelle"): ("RUNTIME_ERROR", "NEITHER", []),
    ("Garnier2026Mai", "al-changement-effet"): ("COMPUTED", "TRUE_ONLY", [APL + "EffetChangementDroits"]),
}

#: (дело, вопрос) → коды issue, обязанные прозвучать в ответе.
ISSUES = {
    ("Garnier2026AvrilTexteSeul", "al-mensuelle"): ["INEXACT_DIVISION"],
}

#: (дело, вопрос) → (предикат, значение), выведенное в proof-графе ответа.
PROOF_VALUES = {
}

#: (дело, вопрос) → (правило, якорь статьи в редакции, действующей в месяце права) в программе запроса (request.json).
ANCHORS = {
    ("Garnier2026Avril", "af-mensuel-lignes"): [(AF + "MontantMensuelLignes", AF + "CSS_D521_1_ED2026_03"), (AF + "ArrondiLignesMetropole", AF + "CSS_D521_1_ED2026_03")],
    ("Garnier2026Avril", "af-net-crds"): [(PV + "RetenueCRDSAF", APL + "ORD9650_ART19_ED2020_01")],
    ("Garnier2026Avril", "al-apres-contributions"): [(APL + "DegressiviteProportionnelleArrondie", APL + "CCH_D823_16_ED2023_12"), (APL + "ArrondiContributionsSociales", APL + "CCH_D823_16_ED2023_12")],
    ("Garnier2026Avril", "al-droit-commence"): [(APL + "OuvertureApresConditions", APL + "CCH_R823_10_ED2023_12")],
    ("Garnier2026Mai", "al-changement-effet"): [(APL + "EffetChangementDroits", APL + "CCH_R823_13_ED2023_12")],
}

#: дело → (шаблон позиции, носитель), обязанные быть ACTIVE в ответе positions.
POSITIONS = {
    "Garnier2026Avril": [(APL + "JoindrePiecesJustificatives", MENAGE), (PV + "PayerAfNet", CAF), (CORE + "InformerAllocataires", CAF)],
    "Garnier2026Mai": [(APL + "JustifierChangements", MENAGE)],
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
