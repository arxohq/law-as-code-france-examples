# Housing aid: follow the coefficient K

[All examples](../README.md#browse-the-cases) · Book chapter 6

**How does the model obtain K = 0.52 and use it in the housing-aid formula?**

> Fictional teaching example from an independent Arxo model; not a Cnaf implementation or a legal decision. See the [demonstration limits](../README.md).

## Facts and assumptions

A fictional retired couple with no dependants lives in a conventioned residence autonomie of the general type, zone II. Monthly fee: €495; annual resources: €12,500; entitlement month: March 2026. Rules and parameters come from the pinned `fr.apl` canon.

Inspect the [dated case files](cases/) and [registered cases](law.toml).

## Run the example

Complete the root [Quick start](../README.md#quick-start) first. From the
`examples` repository root, run:

```sh
cd foyer-coefficient-k
law install --registry arxo=../../arxo-cnaf/registry
result_dir="$(mktemp -d)"
law ask . --case CoupleResidenceAutonomie \
  --query-json queries/aide-formule.json \
  --out "$result_dir"
printf 'Saved answer: %s/result.json\n' "$result_dir"
law test . --json
```

The scenario check should exit with code `0` and report no failed scenarios.

## Expected answer

`COMPUTED / TRUE_ONLY`: **Af = €143.9747608**. The proof graph contains **N = 1.8** and **K = 0.52**.

Open `$result_dir/result.json`: read `results` for the status and follow
`proofGraph` for the derivation. See [how to read an answer](../README.md#how-to-read-an-answer).

## Try another case

```sh
law ask . --case CoupleResidenceAutonomie --query-json queries/aide-formule-k-053.json
law ask . --case CoupleResidenceAutonomie --query-json queries/aide-mensuelle.json
law ask . --case CoupleResidenceAutonomie --query-json queries/aide-nette-crds.json
```

The claim using K = 0.53 is `NEITHER`. The monthly-aid claim of **€138.694873804** and the after-CRDS claim of **€138.00139943498** are `TRUE_ONLY`.

## Sources and limits

D. 832-25 publishes K’s formula as an image. The canon’s reading uses repealed R. 351-61 and R. 351-61-1; identity with the image is not established by checking image bytes. `PpPlancherFinal` is selected because the canon’s `SensMinimumPp` group requires a choice; it does not enter this housing-residence calculation.

Follow the [manual calculation and source references](sources/WITNESS.md).

<details>
<summary>Calculation details and recorded context</summary>

K = 0.95 − (R − r × N) / (cm × N)
= 0.95 − (12,500 − 1,217.26 × 1.8) / (13,393.40 × 1.8)
= 0.5224…, rounded down to two decimals: **0.52**.

E0 = **€218.12546** (D. 832-26). Af = 0.52 × (495 − 218.12546)
= **€143.9747608** (D. 832-24 and D. 832-25). The €5 reduction and
contributions produce the monthly amount above (order, articles 28 and 29).
CRDS references ordinance 96-50, articles 14 III and 19.

The declared scenario tests K through Af: the original author check notes
that a decimal literal lowered as `Number` does not compare directly with
`Decimal` in this canon’s test setup.

</details>

Need help running the commands? See [Troubleshooting](../README.md#troubleshooting).
