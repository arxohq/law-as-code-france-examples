# Decent housing: when an authority must decide

[All examples](../README.md#browse-the-cases) · Book chapter 9

**Can the model establish entitlement before the paying body has judged the dwelling decent?**

> Fictional teaching example from an independent Arxo model; not a Cnaf implementation or a legal decision. See the [demonstration limits](../README.md).

## Facts and assumptions

Nadia and Thomas Garnier have three dependent children. Since 14 March 2026 they rent a five-room house in zone II for €1,320 monthly, with €24,600 annual resources; the ALF application is dated 20 March. Three files vary the supplied authority judgment. These are the housing facts of the [Garnier benefits example](../famille-trois-enfants-loyer/).

Inspect the [dated case files](cases/) and [registered cases](law.toml).

## Run the example

Complete the root [Quick start](../README.md#quick-start) first. From the
`examples` repository root, run:

```sh
cd logement-decent-garnier
law install --registry arxo=../../arxo-cnaf/registry
result_dir="$(mktemp -d)"
law ask . --case DecenceEnAttente \
  --query-json queries/droit-ouvert.json \
  --out "$result_dir"
printf 'Saved answer: %s/result.json\n' "$result_dir"
law test . --json
```

The scenario check should exit with code `0` and report no failed scenarios.

## Expected answer

`REQUIRES_JUDGMENT / NEITHER`: the model requests `logement_decent` from `OrganismePayeur`. The housing-aid amount can be calculated while entitlement remains unresolved.

Open `$result_dir/result.json`: read `results` for the status and follow
`proofGraph` for the derivation. See [how to read an answer](../README.md#how-to-read-an-answer).

## Try another case

```sh
law ask . --case DecenceReconnue --query-json queries/droit-ouvert.json
law ask . --case NonDecenceConstatee --query-json queries/conservation.json
law ask . --case NonDecenceConstatee --query-json queries/loyer-reduit.json
```

Recognition gives `TRUE_ONLY` for entitlement. Non-decency gives `TRUE_ONLY` for conservation and for reduced rent of **€1,130.04705**. The computed housing-aid amount **€189.95295** is supported in all three files; only `DecenceReconnue` activates the duty to pay it.

## Sources and limits

The judgment is an authority response, not an ordinary case-input assertion (CCH L. 822-9). In `NonDecenceConstatee`, the same fictional act is supplied both as a negative judgment and as a dated finding of 28 April 2026; the latter triggers conservation under L. 843-1.

<details>
<summary>Calculation details and recorded context</summary>

Pending judgment: supporting documents, the ban on combining housing claims
(R. 821-1) and the landlord’s decency attestation (R. 823-2) remain active.
Recognition adds `VerserAideTheoriqueDue`. A non-decency finding adds duties
to notify the owner (L. 843-1), inform the tenant (R. 843-3) and owner
(R. 843-4), and the household’s immunity against lease termination (L. 843-1).
Inspect [positions.json](queries/positions.json) in each file.
The cases use `fr.pf.cmg::CMG_MOIS_CALENDAIRE` for calendar-month deadlines.

</details>

Need help running the commands? See [Troubleshooting](../README.md#troubleshooting).
