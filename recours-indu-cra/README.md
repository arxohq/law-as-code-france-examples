# Overpayment appeal: is recovery suspended?

[All examples](../README.md#browse-the-cases) · Book chapter 12

**How do appeal facts and conflicting evidence affect a recovery claim?**

> Fictional teaching example from an independent Arxo model; not a Cnaf implementation or a legal decision. See the [demonstration limits](../README.md).

## Facts and assumptions

Three fictional files — `AppelPendant`, `SansAppel` and `DossierDivergent` — use a teaching debt of €600, procedural facts and evidence. The model concerns recovery while an appeal is pending.

Inspect the [dated case files](cases/) and [registered cases](law.toml).

## Run the example

Complete the root [Quick start](../README.md#quick-start) first. From the
`examples` repository root, run:

```sh
cd recours-indu-cra
law install --registry arxo=../../arxo-cnaf/registry
result_dir="$(mktemp -d)"
law ask . --case AppelPendant \
  --query-json queries/AppelPendant-cra-appelpendant.json \
  --out "$result_dir"
printf 'Saved answer: %s/result.json\n' "$result_dir"
law test . --json
```

The scenario check should exit with code `0` and report no failed scenarios.

## Expected answer

`COMPUTED / TRUE_ONLY`: the claim that recovery is suspended is supported.

Open `$result_dir/result.json`: read `results` for the status and follow
`proofGraph` for the derivation. See [how to read an answer](../README.md#how-to-read-an-answer).

## Try another case

```sh
law ask . --case SansAppel --query-json queries/SansAppel-cra-sansappel.json
law ask . --case DossierDivergent --query-json queries/DossierDivergent-truth.json
law ask . --case AppelPendant --query-json queries/AppelPendant-argumentation.json
```

Without an appeal, recovery of €600 is `TRUE_ONLY`. The divergent file’s claimed recovery is `FALSE_ONLY`. Each file also has an argumentation query; the [query plan](queries/plan.json) lists all six questions.

## Sources and limits

Arguments and priorities concern recovery during an appeal, not a CRA decision on the debt’s merits. CSS L. 845-2 concerns prior recourse to the CRA; L. 845-3 concerns suspension. Housing-debt remission under CCH R. 825-3 is a separate procedure, not a universal appeal deadline.

Follow the [manual calculation and source references](sources/WITNESS.md).

<details>
<summary>Calculation details and recorded context</summary>

The [browser scene](https://french-benefits.law.arxo.io/overpayment-appeal/) was recorded on 9 October 2026 and has its own evidence release. The author checked six questions and the declared scenarios on `law` 0.1.12 on 11 October; this historical execution record is not legal qualification.

</details>

Need help running the commands? See [Troubleshooting](../README.md#troubleshooting).
