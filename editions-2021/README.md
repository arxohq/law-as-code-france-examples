# Housing-aid resources: December 2020 and January 2021

[All examples](../README.md#browse-the-cases) · Book chapter 1

**Which legal edition and resource inputs apply on each side of the January 2021 change?**

> Fictional teaching example from an independent Arxo model; not a Cnaf implementation or a legal decision. See the [demonstration limits](../README.md).

## Facts and assumptions

Two fictional tenants: one file in December 2020 and another in January 2021. The supplied facts differ to meet each edition’s input requirements; this is not a change of date alone.

Inspect the [dated case files](cases/) and [registered cases](law.toml).

## Run the example

Complete the root [Quick start](../README.md#quick-start) first. From the
`examples` repository root, run:

```sh
cd editions-2021
law install --registry arxo=../../arxo-cnaf/registry
result_dir="$(mktemp -d)"
law ask . --case TenantDecembre \
  --query-json queries/TenantDecembre-resources-tenantdecembre.json \
  --out "$result_dir"
printf 'Saved answer: %s/result.json\n' "$result_dir"
law test . --json
```

The scenario check should exit with code `0` and report no failed scenarios.

## Expected answer

`COMPUTED / TRUE_ONLY`: the model establishes **€12,000** of resources for the December file.

Open `$result_dir/result.json`: read `results` for the status and follow
`proofGraph` for the derivation. See [how to read an answer](../README.md#how-to-read-an-answer).

## Try another case

```sh
law ask . --case TenantJanvier \
  --query-json queries/TenantJanvier-resources-tenantjanvier.json
```

The January file establishes **€16,200**, also `COMPUTED / TRUE_ONLY`. Compare the two [case files](cases/) and their dates, then follow the applied rules and edition references in each proof graph.

## Sources and limits

The questions concern resources taken into account, not the amount of housing aid. The two outputs do not isolate the effect of changing the legal date with all other facts held constant.

Follow the [manual calculation and source references](sources/WITNESS.md).

Need help running the commands? See [Troubleshooting](../README.md#troubleshooting).
