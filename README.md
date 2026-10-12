# Law as Code in Practice: French Family Benefits — case packages

The ten case packages of the book *Law as Code in Practice: French Family Benefits*
(Law as Code by Country · Volume 1). Each folder holds one fictional file: the facts, the legal date,
the readings it selects, saved questions (`queries/`) and declared scenarios (`tests/`). The rules are
not copied here: `law.lock` pins the French canons by exact version and hash in the Arxo registry, and
`law install` fetches them.

**Status: private staging.** The canons are published in the private registry `arxohq/registry-staging`
with the layout of the public Arxo registry. Both repositories become public with the book.

## Run an example

```sh
git clone git@github.com:arxohq/registry-staging.git registry
git clone git@github.com:arxohq/law-as-code-france-examples.git examples
cd examples/prime-naissance-moreau
law install --registry arxo=../../registry
law ask . --case PlafondEgal --query-json queries/montant.json --out "$(mktemp -d)"
law test . --json
```

`law install` never picks versions: it restores exactly what `law.lock` pins and checks every hash.
The `law` tool must execute `law.core/0.2.11`. `check.py` in each folder is the authors' check inside
the Arxo repository and is not needed to run the examples.

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

## Chapters 3, 8 and 10: the scenarios of the canons

These chapters run scenarios of the canons themselves. The registry publishes each canon's sources with its
pinned legal texts and a lock for this registry: copy it out, install, run.

```sh
cp -R registry/p/fr.apl/0.1.0/src fr-apl
cd fr-apl
law install --registry arxo=../registry
law test . --file tests/finish-lecture-pp.lawtest --json
```

| Chapter | Canon (`registry/p/…/0.1.0/src`) | Scenario file |
|---|---|---|
| 3 | `fr.css.revalorisation` | `tests/bmaf-chaine-2026.lawtest` |
| 8 | `fr.apl` | `tests/finish-lecture-pp.lawtest` |
| 10 | `fr.pf.paje` | `tests/devoir-declarer-satisfait.lawtest`, `tests/devoir-declarer-envoi-tardif.lawtest` |

In the book's commands the path `corpus/laws/fr/<canon>` of the Arxo repository is this copied folder. On
12 October 2026 all four files passed from the registry.

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

Recorded on 12 October 2026 with `law` 0.2.1 built from the Arxo repository at commit `ba9c096f1d`; on that
day the replay was byte for byte identical to the saved `result.json`.
