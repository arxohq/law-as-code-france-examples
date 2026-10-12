# Moreau: a birth grant at the income ceiling

[All examples](../README.md#browse-the-cases) · Book chapters 2, 5, 17 and 18

**Does equality qualify, and what changes when income exceeds the ceiling by one cent or is missing?**

> Fictional teaching example from an independent Arxo model; not a Cnaf implementation or a legal decision. See the [demonstration limits](../README.md).

## Facts and assumptions

A fictional family, distinct from the Garnier family, with a pregnancy in July 2025. The €400 BMAF (family-benefit calculation base) and €30,000 base ceiling are teaching inputs taken from canon scenarios, not published annual amounts for this family. The resulting ceiling is €35,841.

Inspect the [dated case files](cases/) and [registered cases](law.toml).

## Run the example

Complete the root [Quick start](../README.md#quick-start) first. From the
`examples` repository root, run:

```sh
cd prime-naissance-moreau
law install --registry arxo=../../arxo-cnaf/registry
result_dir="$(mktemp -d)"
law ask . --case PlafondEgal \
  --query-json queries/montant.json \
  --out "$result_dir"
printf 'Saved answer: %s/result.json\n' "$result_dir"
law test . --json
```

The scenario check should exit with code `0` and report no failed scenarios.

## Expected answer

`COMPUTED / TRUE_ONLY`: the claim that the birth grant is **€919** is established. This is the model’s answer using the teaching parameters above.

Open `$result_dir/result.json`: read `results` for the status and follow
`proofGraph` for the derivation. See [how to read an answer](../README.md#how-to-read-an-answer).

## Try another case

| Case | Income | Expected answer to `droit.json` |
|---|---|---|
| `PlafondEgal` | €35,841 | `TRUE_ONLY` — entitlement established |
| `PlafondDepasse` | €35,841.01 | `NEITHER` — entitlement not derived |
| `RessourcesAbsentes` | not supplied | `NEITHER` — no ceiling comparison can be established |

```sh
law ask . --case PlafondDepasse --query-json queries/droit.json
law ask . --case RessourcesAbsentes --query-json queries/pourquoi-droit.json
```

The explanation for missing income identifies `ressources_annuelles`.
`NEITHER` does not by itself mean that a negative entitlement claim is proven.

## Sources and limits

All facts are supplied case inputs; no authority judgment is simulated. The saved [Chapter 17 bundle](runs/plafond-egal/) records the equality answer; see [replay instructions](../README.md#verify-the-recorded-answer).

Follow the [manual calculation and source references](sources/WITNESS.md).

<details>
<summary>Calculation details and recorded context</summary>

Ceiling: 30,000 × 11947/10000 = €35,841. Grant: 400 × 22975/10000 = €919. The canon references CSS L. 531-2 (2020 edition), D. 531-2 (2021 edition) and D. 531-3-1 (2018 edition).

</details>

Need help running the commands? See [Troubleshooting](../README.md#troubleshooting).
