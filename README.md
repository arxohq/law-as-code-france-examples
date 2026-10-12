# French Family Benefits — Executable Examples

Explore ten fictional family files: run the rules, compare answers, and trace
their reasoning to published French legal sources.

**[Run your first example](#quick-start)** ·
**[Browse the cases](#browse-the-cases)** ·
**[Read the book](https://books.arxo.io/)**

> **First of all, a demonstration.** These case packages show what modelling legislation with Arxo can
> do: fictional families' files answered by executable French family-benefit canons, with the source of
> every answer. They do not claim legal accuracy or completeness, they are not an implementation by or
> for the Cnaf or any French authority, and their answers are not legal advice. For a real file, rely
> on the official texts and the competent bodies.

These examples accompany *Law as Code in Practice: French Family Benefits*
(Law as Code by Country · Volume 1). You can start without reading the book.
For a browser introduction, open [French Benefits Lab](https://french-benefits.law.arxo.io/)
— no installation. The lab has its own recorded evidence release; its cases
and version are separate from this reproduction kit.

## Your first answer

**Does the model establish a birth grant when income is exactly at the ceiling?**
The Moreau example compares equality, an excess of one cent, and missing income.
Here is a readable summary of its [saved equality answer](prime-naissance-moreau/runs/plafond-egal/result.json),
not literal terminal output:

```text
Case:          PlafondEgal
Legal date:    15 July 2025
Claim tested:  Birth grant of €919
Answer:        Established — TRUE_ONLY
```

**These are teaching parameters:** a €400 family-benefit calculation base
(BMAF) and a €30,000 base ceiling. They are not the published annual amounts
for this family. The [manual calculation](prime-naissance-moreau/sources/WITNESS.md)
shows how the model obtains the €35,841 ceiling and €919 grant.

## Quick start

You need **Git, Node.js 20+ and npm**. The pinned CLI below is the released
**`law` 0.2.2**, available through npm for macOS arm64 and Linux x64.
Commands use a POSIX shell (macOS Terminal or a Linux shell).
Python and a checkout of the Arxo engine are not needed.

### 1. Install the command-line tool

```sh
npm install -g @arxo/cli@0.2.2
law --version
```

The version should start with `law 0.2.2`.

### 2. Get the cases and their pinned rules

Run the two clones from the same parent directory:

```sh
git clone https://github.com/arxohq/arxo-cnaf.git
git clone https://github.com/arxohq/law-as-code-france-examples.git examples
cd examples/prime-naissance-moreau
law install --registry arxo=../../arxo-cnaf/registry
```

A **canon** is a package containing a legal model. The examples hold facts
and questions; their rules come from [arxo-cnaf](https://github.com/arxohq/arxo-cnaf).
`law install` restores the exact versions and hashes in `law.lock`.

### 3. Ask a question and check the scenarios

```sh
result_dir="$(mktemp -d)"
law ask . --case PlafondEgal \
  --query-json queries/montant.json \
  --out "$result_dir"
printf 'Saved answer: %s/result.json\n' "$result_dir"

law test . --json
```

The answer has `evaluationStatus: COMPUTED` and `truthStatus: TRUE_ONLY`.
The scenario check should exit with code `0` and report no failed scenarios.
The successful scenario report includes:

```json
{"ok": true, "passed": 7, "failed": 0, "total": 7}
```

These checks compare execution with the model's declared expectations.

Open `$result_dir/result.json` in your editor. `results` contains the answer,
`proofGraph` contains its derivation, and `manifest` records the legal date
and execution fingerprints. Keep the other files beside it: together they
form the replay bundle. [How to read an answer](#how-to-read-an-answer)
explains the statuses.

**Next:** follow the [Moreau guide](prime-naissance-moreau/README.md#try-another-case)
to compare the one-cent excess and the missing-income file.

## Browse the cases

Choose a question; each guide includes facts, commands, expected answers and limits.
Chapter numbers follow the book.

| Question | Example | Chapters |
|---|---|---|
| Does income exactly at the ceiling qualify? | [Moreau birth grant](prime-naissance-moreau/) — start here | 2, 5, 17, 18 |
| How do several benefits apply to one family? | [Garnier: three children and rent](famille-trois-enfants-loyer/) | 0, 4 |
| Which edition applies before and after a change? | [December 2020 and January 2021](editions-2021/) | 1 |
| How do parameters affect several households? | [Revaluation cohort](cohorte-revalorisation/) | 3, 14 |
| How is the housing-aid coefficient calculated? | [Housing aid and K](foyer-coefficient-k/) | 6 |
| What happens when the text does not specify rounding? | [Division by twelve](douzieme-sans-arrondi/) | 7 |
| When must a person decide before a right is established? | [Decent housing](logement-decent-garnier/) | 9 |
| How do deductions and recovery change payments over time? | [One family, 2024–2026](famille-dans-le-temps/) | 11 |
| What deadlines follow a request to remit a housing debt? | [Fontaine debt remission](recours-remise-fontaine/) | 12, 13 |
| Is debt recovery suspended during an appeal? | [Overpayment appeal](recours-indu-cra/) | 12 |

`famille-dans-le-temps` has saved questions but no declared scenarios.
Its guide runs the monthly files with `law ask`.

## How to read an answer

A saved proposition query tests a particular claim, such as “this grant is €919”.
A truth status describes support for that claim in the model:

| Status | Meaning |
|---|---|
| `TRUE_ONLY` | The claim is supported; its negation is not. |
| `FALSE_ONLY` | The claim's negation is supported; the claim is not. |
| `BOTH` | Both the claim and its negation are supported; inspect the conflict. |
| `NEITHER` | Neither is supported. This alone does not mean rejection. |

Also read `evaluationStatus`: `COMPUTED` means evaluation completed;
`REQUIRES_JUDGMENT` asks for an authority's judgment; `RUNTIME_ERROR` means
execution could not complete. An `INEXACT_DIVISION` issue in the rounding
example is an expected refusal to invent a rounding choice.

Follow `results[].proof` into `proofGraph`. Applied rules and `sourceAnchors`
show the reasoning and legal references; the saved bundle supplies the program
needed to resolve those references. Sources attached to an applied rule need
not appear directly on the top-level result.

## Find your way around a case

| Path | Use it to… |
|---|---|
| `README.md` | Understand the example and run its first question |
| `cases/*.lawcase` | Inspect the dated facts and any named readings |
| `queries/*.json` | See the exact claim or explanation being requested |
| `tests/*.lawtest` | Inspect declared expectations, when present |
| `law.toml` | Find registered case names and scenario files |
| `law.lock` | Identify the exact pinned dependencies |
| `sources/` | Inspect supporting material and manual calculations, when present |

The `check.py` files are author checks tied to paths in the Arxo engine
repository. Use the public `law ask` and `law test` commands in these guides.

## Reproduce the remaining book chapters

Chapters 3, 8 and 10 also run scenarios directly in the canon repository.
From `examples/prime-naissance-moreau`, this runs Chapter 8:

```sh
cd ../../arxo-cnaf/packages/fr.apl
law test . --file tests/finish-lecture-pp.lawtest --json
```

The canon folders already contain pinned dependencies for these scenarios.

| Chapter | Canon | Scenario file |
|---|---|---|
| 3 | [fr.css.revalorisation](https://github.com/arxohq/arxo-cnaf/tree/main/packages/fr.css.revalorisation) | `tests/bmaf-chaine-2026.lawtest` |
| 8 | [fr.apl](https://github.com/arxohq/arxo-cnaf/tree/main/packages/fr.apl) | `tests/finish-lecture-pp.lawtest` |
| 10 | [fr.pf.paje](https://github.com/arxohq/arxo-cnaf/tree/main/packages/fr.pf.paje) | `tests/devoir-declarer-satisfait.lawtest`, `tests/devoir-declarer-envoi-tardif.lawtest` |

A book command using `corpus/laws/fr/<canon>` refers to that canon's
`arxo-cnaf/packages/…` folder here. Chapter 10's maintenance example
(`fr.pf.maintenance`) requires the Arxo engine repository.

## Verify the recorded answer

Chapter 17's [saved bundle](prime-naissance-moreau/runs/plafond-egal/) can be
replayed without installing the canons. Run this from `prime-naissance-moreau`:

```sh
replay_dir="$(mktemp -d)"
cp -R runs/plafond-egal/. "$replay_dir/"
law eval "$replay_dir"
shasum -a 256 runs/plafond-egal/result.json "$replay_dir/result.json"
```

The two SHA-256 values should match. The temporary directory keeps the
recorded bundle intact and gives each replay a fresh destination.

<details>
<summary>Recorded fingerprints and execution provenance</summary>

| Fingerprint | Value |
|---|---|
| program (`manifest.programHash`) | `sha256:d7740308956c4a9b279537698f7af3d448a2abb9b54e2f676fc16eacfaaf29aa` |
| case (`manifest.caseHash`) | `sha256:8134b82a55a7e45ccce7732f00c1659c5b1ff91e98abc16a25590339591a9f92` |
| result (`resultHash`) | `sha256:3b041b7e8d987baafb0425b9fb2c0286f11c4d79c8eaa5519db62a2051e64ac2` |
| semantics | `law.core/0.2.11` |

Recorded on 12 October 2026 with `law` 0.2.1 built from Arxo commit
`ba9c096f1d`. Checked again that day with released `law` 0.2.2 from fresh
clones: the same three fingerprints and a byte-for-byte identical replay.

The commands in all ten guides were checked on 12 October 2026 with
released `law` 0.2.2: 37 saved questions matched the documented outcomes,
38 declared case scenarios passed, and the four canon scenario files above
passed their 10 scenarios. The recorded Chapter 17 answer replayed byte for byte.

</details>

## Troubleshooting

| Symptom | Recovery |
|---|---|
| `law: command not found` | Open a new shell after installation. Check `npm prefix -g` and add its `bin` directory to your `PATH`. |
| npm installation fails | Check `node --version` (20+) and that your platform is macOS arm64 or Linux x64. A permissions error needs a user-writable npm prefix. |
| Registry directory is missing | From an example folder, check `ls ../../arxo-cnaf/registry`. Clone both repositories into the same parent directory, or supply the actual registry path. |
| A dependency cannot be loaded | Run `law install --registry arxo=../../arxo-cnaf/registry` inside that example folder. |
| `NEITHER` despite a completed query | Check the claim, the dated facts and selected readings. Compare with the guide's expected answer; do not interpret `NEITHER` as automatic denial. |
| No scenarios in the family-over-time example | Run its saved monthly questions; that package declares no scenarios. |

## Licence

Code and model: [Apache License 2.0](LICENSE). The pinned third-party text
retains its own terms; see [NOTICE](NOTICE).
