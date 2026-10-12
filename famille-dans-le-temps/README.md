# One family over time: payments from 2024 to 2026

[All examples](../README.md#browse-the-cases) · Book chapter 11

**How do contributions, recovery, debt carry-over and a supplied prescription finding affect payments?**

> Fictional teaching example from an independent Arxo model; not a Cnaf implementation or a legal decision. See the [demonstration limits](../README.md).

## Facts and assumptions

Six monthly snapshots of a fictional household, with seven saved questions. Gross AF, ARS and PAJE birth-grant amounts, RSA allocation and activity-bonus amounts are supplied inputs before recovery.

Inspect the [dated case files](cases/) and [registered cases](law.toml).

## Run the example

Complete the root [Quick start](../README.md#quick-start) first. From the
`examples` repository root, run:

```sh
cd famille-dans-le-temps
law install --registry arxo=../../arxo-cnaf/registry
result_dir="$(mktemp -d)"
law ask . --case Famille2024_03 \
  --query-json queries/af-net-2024-03.json \
  --out "$result_dir"
printf 'Saved answer: %s/result.json\n' "$result_dir"
```

This package declares no scenarios. Use the monthly questions below for verification.

## Expected answer

`COMPUTED / TRUE_ONLY`: the net family-allowance claim of **€199** is supported.

Open `$result_dir/result.json`: read `results` for the status and follow
`proofGraph` for the derivation. See [how to read an answer](../README.md#how-to-read-an-answer).

## Try another case

| Case | Saved question | Established amount |
|---|---|---|
| `Famille2024_03` | [af-net-2024-03](queries/af-net-2024-03.json) | €199 |
| `Famille2024_08` | [ars-net-2024-08](queries/ars-net-2024-08.json) | €398 |
| `Famille2025_07` | [prime-net-2025-07](queries/prime-net-2025-07.json) | €995 |
| `Famille2025_12` | [af-rec-2025-12](queries/af-rec-2025-12.json) | €238.80 |
| `Famille2026_03` | [af-presc-2026-03](queries/af-presc-2026-03.json) | €318.40 |
| `Famille2026_03` | [rsa-carry-2026-03](queries/rsa-carry-2026-03.json) | €420 |
| `Famille2026_06` | [pa-rec-2026-06](queries/pa-rec-2026-06.json) | €210 |

```sh
law ask . --case Famille2025_12 --query-json queries/af-rec-2025-12.json
law ask . --case Famille2026_03 --query-json queries/rsa-carry-2026-03.json
```

All seven saved amount claims expect `COMPUTED / TRUE_ONLY`.

## Sources and limits

This package does not execute the complete housing → RSA → activity-bonus chain. Deductions of €79.60, €180 and €70 and facts permitting debt carry-over are supplied; deduction rates are not calculated here. March’s `action_prescrite` is a supplied prescription conclusion, not a calculation of debt age. The caller links identities; no automatic joining is claimed.

Follow the [manual calculation and source references](sources/WITNESS.md).

<details>
<summary>Calculation details and recorded context</summary>

The author recorded seven passing monthly questions on `law` 0.1.12 on 11 October 2026. The separate engine-workspace scenario `dossier-pa-cascade-2026-06.lawtest` was not included in that case acceptance. This public package declares no scenarios: inspect the seven saved answers rather than expecting `law test` to check them.

</details>

Need help running the commands? See [Troubleshooting](../README.md#troubleshooting).
