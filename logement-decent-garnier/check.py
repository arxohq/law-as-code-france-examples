#!/usr/bin/env python3
"""Пристойность жилья семьи Garnier: канал суждения L. 822-9 и консервация L. 843-1.

ЧТО ПРОВЕРЯЕТСЯ. Три дела одних фактов жилья (наём дома в зоне II за 1 320 €,
ALF, заявление 20.03.2026), которые различаются ответом органа о пристойности.
DecenceEnAttente — ответа нет: право `NEITHER` с evaluation status
`REQUIRES_JUDGMENT` и запросом fr.apl::logement_decent к OrganismePayeur; расчёт
пособия (189,95295 €) установлен; обязанности выплатить пособие нет.
DecenceReconnue — орган признал жильё пристойным (adjudicated): право
`TRUE_ONLY` по правилу DroitOuvert, касса обязана выплатить пособие
(VerserAideTheoriqueDue). NonDecenceConstatee — орган признал жильё
непристойным и 28.04.2026 констатировал это: право `NEITHER` без запроса судье,
консервация пособия (ConservationDeclencheeALF, L. 843-1), семья платит
1 320 − 189,95295 = 1 130,04705 € (LoyerReduitConservation), касса обязана
уведомить владельца и информировать стороны (L. 843-1, R. 843-3, R. 843-4),
семья защищена иммунитетом от расторжения найма, обязанности выплатить
пособие нет. Во всех делах владелец обязан подать справку о пристойности
(R. 823-2). Затем `law test` исполняет двойник §267
(tests/logement-decent-garnier.lawtest).

Пакет — член workspace (DECISION-0459). ЛОВУШКА 11.10.2026: локальная копия
зависимостей examples/recours-remise-fontaine/deps/ (вне git) ломает свежее
понижение fr.apl (LDC-E8704: discover_resources не пропускает вложенные
пакеты-дела). В чистом checkout дело исполняется; в общем дереве с этой копией —
только пока кэш workspace держит понижение fr.apl.

    python3 corpus/laws/fr/apl/examples/logement-decent-garnier/check.py --law <бинарь law>
"""
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
APL = "urn:fr:corpus:clir:apl#"
MENAGE = "urn:law:examples:fr:garnier:menage"
CAF = "urn:law:examples:fr:garnier:caf"
BAILLEUR = "urn:law:examples:fr:garnier:bailleur"

#: (дело, вопрос) → (evaluationStatus, truthStatus, правила, обязанные примениться).
EXPECTED = {
    ("DecenceEnAttente", "droit-ouvert"): ("REQUIRES_JUDGMENT", "NEITHER", []),
    ("DecenceEnAttente", "aide-mensuelle"): ("COMPUTED", "TRUE_ONLY", [APL + "AideMensuelleMetropole"]),
    ("DecenceEnAttente", "conservation"): ("COMPUTED", "NEITHER", []),
    ("DecenceReconnue", "droit-ouvert"): ("COMPUTED", "TRUE_ONLY", [APL + "DroitOuvert"]),
    ("DecenceReconnue", "aide-mensuelle"): ("COMPUTED", "TRUE_ONLY", [APL + "AideMensuelleMetropole"]),
    ("DecenceReconnue", "conservation"): ("COMPUTED", "NEITHER", []),
    ("NonDecenceConstatee", "droit-ouvert"): ("COMPUTED", "NEITHER", []),
    ("NonDecenceConstatee", "conservation"): ("COMPUTED", "TRUE_ONLY", [APL + "ConservationDeclencheeALF"]),
    ("NonDecenceConstatee", "loyer-reduit"): ("COMPUTED", "TRUE_ONLY", [APL + "LoyerReduitConservation"]),
}

#: (дело, вопрос) → запросы судье (отношение суждения, орган); пустой список — запросов нет.
JUDGMENTS = {
    ("DecenceEnAttente", "droit-ouvert"): [(APL + "logement_decent", APL + "OrganismePayeur")],
    ("DecenceReconnue", "droit-ouvert"): [],
    ("NonDecenceConstatee", "droit-ouvert"): [],
}

#: дело → (шаблон позиции, носитель), обязанные быть ACTIVE в ответе positions.
POSITIONS = {
    "DecenceEnAttente": [(APL + "JoindrePiecesJustificatives", MENAGE),
                         (APL + "DeposerAttestationBailleur", BAILLEUR)],
    "DecenceReconnue": [(APL + "VerserAideTheoriqueDue", CAF),
                        (APL + "JoindrePiecesJustificatives", MENAGE),
                        (APL + "DeposerAttestationBailleur", BAILLEUR)],
    "NonDecenceConstatee": [(APL + "NotifierProprietaireConstat", CAF),
                            (APL + "InformerLocataireConformite843", CAF),
                            (APL + "InformerProprietaireAides", CAF),
                            (APL + "NonResiliationBailNonDecence", MENAGE),
                            (APL + "DeposerAttestationBailleur", BAILLEUR)],
}

#: дело → шаблоны позиций, которых в ответе positions быть не должно.
ABSENT = {
    "DecenceEnAttente": [APL + "VerserAideTheoriqueDue"],
    "NonDecenceConstatee": [APL + "VerserAideTheoriqueDue"],
}


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
