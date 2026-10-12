# Revaluation cohort: one base, several households

[All examples](../README.md#browse-the-cases) · Book chapters 3 and 14

**How do family size and the supplied calculation base affect family allowances?**

> Fictional teaching example from an independent Arxo model; not a Cnaf implementation or a legal decision. See the [demonstration limits](../README.md).

## Facts and assumptions

Four fictional households dated 15 April 2026: Martin has two children, Bernard three, Petit four and Durand one, without age supplements. All select the named reading `fr.pf.af::ArrondiLignesDss`. BMAF is supplied as an input; the revaluation coefficient is calculated in a separate canon.

Inspect the [dated case files](cases/) and [registered cases](law.toml).

## Run the example

Complete the root [Quick start](../README.md#quick-start) first. From the
`examples` repository root, run:

```sh
cd cohorte-revalorisation
law install --registry arxo=../../arxo-cnaf/registry
result_dir="$(mktemp -d)"
law ask . --case Martin \
  --query-json queries/Martin-amount.json \
  --out "$result_dir"
printf 'Saved answer: %s/result.json\n' "$result_dir"
law test . --json
```

The scenario check should exit with code `0` and report no failed scenarios.

## Expected answer

`COMPUTED / TRUE_ONLY`: the saved Martin claim of **€153.01** is established.

Open `$result_dir/result.json`: read `results` for the status and follow
`proofGraph` for the derivation. See [how to read an answer](../README.md#how-to-read-an-answer).

## Try another case

```sh
law ask . --case Bernard --query-json queries/Bernard-amount.json
law ask . --case Petit --query-json queries/Petit-amount.json
law ask . --case Durand --query-json queries/af-durand-droit.json
```

Bernard and Petit’s saved amount claims are `TRUE_ONLY`; Durand’s entitlement claim is `NEITHER`. The [query plan](queries/plan.json) lists seven comparisons and their expected statuses.

## Sources and limits

This package compares supplied parameters. It does not derive BMAF’s annual revaluation. For that calculation, follow the [Chapter 3 canon scenario](../README.md#reproduce-the-remaining-book-chapters).

Follow the [manual calculation and source references](sources/WITNESS.md).

Need help running the commands? See [Troubleshooting](../README.md#troubleshooting).
