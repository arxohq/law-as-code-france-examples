# Law as Code in Practice: French Family Benefits — case packages

> **First of all, a demonstration.** These case packages show what modelling legislation with Arxo can
> do: fictional families' files answered by executable French family-benefit canons, with the source of
> every answer. They do not claim legal accuracy or completeness, they are not an implementation by or
> for the Cnaf or any French authority, and their answers are not legal advice. For a real file, rely
> on the official texts and the competent bodies.

The ten case packages of the book *Law as Code in Practice: French Family Benefits*
(Law as Code by Country · Volume 1). Each folder holds one fictional file: the facts, the legal date,
the readings it selects, saved questions (`queries/`) and declared scenarios (`tests/`). The rules are
not copied here: `law.lock` pins the French canons by exact version and hash, and `law install` fetches
them from the canon repository [`arxohq/arxo-cnaf`](https://github.com/arxohq/arxo-cnaf).

Published with the book at https://books.arxo.io; the canons are in the public repository
[`arxohq/arxo-cnaf`](https://github.com/arxohq/arxo-cnaf).

## Run an example

You need the `law` command-line tool, version 0.2.2 or later (`npm i -g @arxo/cli`); it executes
`law.core/0.2.11`.

```sh
git clone https://github.com/arxohq/arxo-cnaf.git
git clone https://github.com/arxohq/law-as-code-france-examples.git examples
cd examples/prime-naissance-moreau
law install --registry arxo=../../arxo-cnaf/registry
law ask . --case PlafondEgal --query-json queries/montant.json --out "$(mktemp -d)"
law test . --json
```

`law install` never picks versions: it restores exactly what `law.lock` pins and checks every hash.
`check.py` in each folder is the authors' check inside the Arxo repository and is not needed to run
the examples.

## Chapters and folders

| Chapter | Folder |
|---|---|
| 0, 4 | `famille-trois-enfants-loyer/` |
| 1 | `editions-2021/` |
| 2, 5, 17, 18 | `prime-naissance-moreau/` |
| 3, 14 | `cohorte-revalorisation/` |
| 6 | `foyer-coefficient-k/` |
| 7 | `douzieme-sans-arrondi/` |
| 9 | `logement-decent-garnier/` |
| 11 | `famille-dans-le-temps/` |
| 12, 13 | `recours-remise-fontaine/` |
| 12 | `recours-indu-cra/` |

`famille-dans-le-temps/` declares no scenarios: Chapter 11 asks its monthly files one by one with
`law ask`.

## Chapters 3, 8 and 10: the scenarios of the canons

These chapters run scenarios of the canons themselves. In `arxo-cnaf` every canon is a folder of
`packages/` with its dependencies pinned inside it — nothing to install:

```sh
cd arxo-cnaf/packages/fr.apl
law test . --file tests/finish-lecture-pp.lawtest --json
```

| Chapter | Canon (`arxo-cnaf/packages/…`) | Scenario file |
|---|---|---|
| 3 | `fr.css.revalorisation` | `tests/bmaf-chaine-2026.lawtest` |
| 8 | `fr.apl` | `tests/finish-lecture-pp.lawtest` |
| 10 | `fr.pf.paje` | `tests/devoir-declarer-satisfait.lawtest`, `tests/devoir-declarer-envoi-tardif.lawtest` |

In the book's commands the path `corpus/laws/fr/<canon>` of the Arxo repository is this folder. The
maintenance example of Chapter 10 (`fr.pf.maintenance`) runs only from a checkout of the Arxo
repository.

## The saved answer of Chapter 17

`prime-naissance-moreau/runs/plafond-egal/` is the answer of `PlafondEgal` to `montant` (€919, established),
saved with `--out`:

| Fingerprint | Value |
|---|---|
| program (`manifest.programHash`) | `sha256:d7740308956c4a9b279537698f7af3d448a2abb9b54e2f676fc16eacfaaf29aa` |
| case (`manifest.caseHash`) | `sha256:8134b82a55a7e45ccce7732f00c1659c5b1ff91e98abc16a25590339591a9f92` |
| result (`resultHash`) | `sha256:3b041b7e8d987baafb0425b9fb2c0286f11c4d79c8eaa5519db62a2051e64ac2` |
| semantics | `law.core/0.2.11` |

```sh
cp -R runs/plafond-egal /tmp/plafond-egal
law eval /tmp/plafond-egal
shasum -a 256 runs/plafond-egal/result.json /tmp/plafond-egal/result.json
```

Recorded on 12 October 2026 with `law` 0.2.1 built from the Arxo repository at commit `ba9c096f1d`. Checked
again the same day with the released `law` 0.2.2 from fresh clones of both repositories: the same three
fingerprints, and the replay byte for byte identical to the saved `result.json`.

## Licence

Apache License 2.0 (`LICENSE`). The one pinned third-party text keeps its own terms — see `NOTICE`.
