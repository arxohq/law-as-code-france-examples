# Fontaine: a housing-debt remission request

[All examples](../README.md#browse-the-cases) · Book chapters 12 and 13

**Which deadlines and duties follow a request to remit an undisputed housing debt?**

> Fictional teaching example from an independent Arxo model; not a Cnaf implementation or a legal decision. See the [demonstration limits](../README.md).

## Facts and assumptions

A fictional Fontaine family with three children, €40,000 resources and no age supplements; family allowances are €349.06. This is a separate family from the Garnier file with €425.57 allowances. The supplied request date is 15 April 2026.

Inspect the [dated case files](cases/) and [registered cases](law.toml).

## Run the example

Complete the root [Quick start](../README.md#quick-start) first. From the
`examples` repository root, run:

```sh
cd recours-remise-fontaine
law install --registry arxo=../../arxo-cnaf/registry
result_dir="$(mktemp -d)"
law ask . --case FontaineRemise \
  --query-json queries/FontaineRemise-remise-receipt.json \
  --out "$result_dir"
printf 'Saved answer: %s/result.json\n' "$result_dir"
law test . --json
```

The scenario check should exit with code `0` and report no failed scenarios.

## Expected answer

`COMPUTED / TRUE_ONLY`: acknowledgement is due by **30 April 2026** under the case’s deadline interpretation.

Open `$result_dir/result.json`: read `results` for the status and follow
`proofGraph` for the derivation. See [how to read an answer](../README.md#how-to-read-an-answer).

## Try another case

```sh
law ask . --case FontaineRemise --query-json queries/FontaineRemise-remise-decision.json
law ask . --case FontaineRemise --query-json queries/FontaineRemise-positions.json
```

The decision-notification deadline of **15 June 2026** is `TRUE_ONLY`. The [query plan](queries/plan.json) also covers €349.06 family allowances and suspension of €600 activity-bonus recovery.

## Sources and limits

CCH R. 825-3 concerns remission where the basis of the debt is undisputed. The model treats filing on 15 April as receipt when deriving the 15-day and two-month deadlines; no separate receipt fact is supplied. Neither deadline grants remission. RAPO is the required prior stage before court proceedings; CRA is the participating commission. Keep this file’s facts separate from Garnier’s.

Follow the [manual calculation and source references](sources/WITNESS.md).

<details>
<summary>Calculation details and recorded context</summary>

[notification.fr.txt](resources/documents/notification.fr.txt) is a demonstration
document attached by content hash. Attachment does not turn its prose into
adjudicated facts. Chapter 13 discusses the four CRPA explanation headings;
[source text and provenance](sources/crpa/) accompany the example, but do
not add an executed CRPA rule. The notification has not been qualified by a
native-speaking lawyer as ready to send; absence of verbalization gaps does
not replace that review.

Historical recordings from 9 October 2026 used an earlier pin. On 11 October,
the author re-pinned the engine-workspace copy on `law` 0.1.12 and checked
that the five answers were preserved. Those earlier hashes are not hashes
of the public kit’s current pin. The public guide uses the committed
`law.lock` and leaves `pinned = true` in the manifest.

</details>

Need help running the commands? See [Troubleshooting](../README.md#troubleshooting).
