# Division by twelve: a missing rounding choice

[All examples](../README.md#browse-the-cases) · Book chapter 7

**What happens when a required division has no finite decimal result and the text supplies no rounding rule?**

> Fictional teaching example from an independent Arxo model; not a Cnaf implementation or a legal decision. See the [demonstration limits](../README.md).

## Facts and assumptions

Two files with the same facts: a single person with no dependants, conventioned general-type housing residence in zone II, €430 monthly fee, €9,600 annual resources, March 2026. The total used for E0 is €1,977.17096; divided by twelve it is €164.764246666… .

Inspect the [dated case files](cases/) and [registered cases](law.toml).

## Run the example

Complete the root [Quick start](../README.md#quick-start) first. From the
`examples` repository root, run:

```sh
cd douzieme-sans-arrondi
law install --registry arxo=../../arxo-cnaf/registry
result_dir="$(mktemp -d)"
law ask . --case ResidentLectureD82 \
  --query-json queries/equivalence-loyer-minimale.json \
  --out "$result_dir"
printf 'Saved answer: %s/result.json\n' "$result_dir"
law test . --json
```

The scenario check should exit with code `0` and report no failed scenarios.

## Expected answer

`COMPUTED / TRUE_ONLY`: **E0 = €164.76** under the selected reading `fr.apl::ArrondiCentimeHalfUp`.

Open `$result_dir/result.json`: read `results` for the status and follow
`proofGraph` for the derivation. See [how to read an answer](../README.md#how-to-read-an-answer).

## Try another case

```sh
law ask . --case ResidentSansLecture \
  --query-json queries/equivalence-loyer-minimale.json
law ask . --case ResidentLectureD82 --query-json queries/aide-mensuelle.json
```

Without a rounding reading, expect `RUNTIME_ERROR`, `INEXACT_DIVISION` and `NEITHER`: the model refuses to invent an exact decimal result. With the named reading, the monthly-aid claim **€132.664624** is `TRUE_ONLY`. The refusal is an intended outcome of this example; it is not an installation failure.

## Sources and limits

The selected rounding reading is an explicit model choice, not a rounding rule stated by D. 832-26 or a verified statement of Cnaf practice. `PpPlancherFinal` is selected in both files because `SensMinimumPp` requires a choice; it does not enter this calculation.

Follow the [manual calculation and source references](sources/WITNESS.md).

<details>
<summary>Calculation details and recorded context</summary>

With the selected reading, Af = 0.52 × (430 − 164.76) = **€137.9248**;
after deductions, monthly aid is **€132.664624**, and after CRDS
**€132.00130088**. The proof uses `EquivalenceLoyerMinimaleArrondie` and
`ArrondiIntermediaireCentime`, anchored to D. 832-26.

Related division choices occur in CASF R. 262-7 (`MoyenneArrondieCentime`,
`fr.minima.ressources`) and CSS D. 521-1 II (`ArrondiLignesDss`, `fr.pf.af`).
This package demonstrates only the housing-residence example.

</details>

Need help running the commands? See [Troubleshooting](../README.md#troubleshooting).
