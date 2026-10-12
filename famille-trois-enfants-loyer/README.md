# Garnier: three children, rent and several benefits

[All examples](../README.md#browse-the-cases) · Book chapters 0 and 4

**Which amounts, duties and dates does the model establish for one household?**

> Fictional teaching example from an independent Arxo model; not a Cnaf implementation or a legal decision. See the [demonstration limits](../README.md).

## Facts and assumptions

Nadia and Thomas Garnier have three children: Inès (15), Hugo (10) and Léa (5).
Since 14 March 2026 they rent a five-room house from a private landlord in
zone II for €1,320 per month. Annual household resources are €24,600.
The pinned canons supply the rules, housing parameters and named readings;
family-benefit base and ceilings are inputs referenced to captured DSS instructions.

| Case | Legal date | Selected readings |
|---|---|---|
| `Garnier2026Avril` | 15 April 2026 | `fr.pf.af::ArrondiLignesDss`, `fr.apl::ArrondiCentimeHalfUp`, `fr.apl::PpPlancherFinal` |
| `Garnier2026AvrilTexteSeul` | 15 April 2026 | `fr.apl::PpPlancherFinal` only |
| `Garnier2026Mai` | 26 May 2026 | Same readings as April; Thomas lost his job on 18 May |

Inspect the [dated case files](cases/) and [registered cases](law.toml).

## Run the example

Complete the root [Quick start](../README.md#quick-start) first. From the
`examples` repository root, run:

```sh
cd famille-trois-enfants-loyer
law install --registry arxo=../../arxo-cnaf/registry
result_dir="$(mktemp -d)"
law ask . --case Garnier2026Avril \
  --query-json queries/al-mensuelle.json \
  --out "$result_dir"
printf 'Saved answer: %s/result.json\n' "$result_dir"
law test . --json
```

The scenario check should exit with code `0` and report no failed scenarios.

## Expected answer

`COMPUTED / TRUE_ONLY`: the monthly housing-allowance claim of
**€189.95295** is established under the selected readings. This is the
model's amount with its retained decimal precision.

Open `$result_dir/result.json`: read `results` for the status and follow
`proofGraph` for the derivation. See [how to read an answer](../README.md#how-to-read-an-answer).

## Try another case

```sh
law ask . --case Garnier2026Avril --query-json queries/positions.json
law ask . --case Garnier2026AvrilTexteSeul --query-json queries/al-mensuelle.json
```

The first query exposes active duties. Without the housing rounding reading,
expect `RUNTIME_ERROR`, `INEXACT_DIVISION`: the proportional reduction does
not have an exact finite decimal result. Compare the May [questions](queries/)
for the duty to justify the change and its effect date, **1 June 2026**.

## Sources and limits

The family-allowance and housing rounding readings are selected model choices;
they are not rounding rules supplied by the text or verified statements of
Cnaf practice. D. 521-1 supplies percentages of BMAF; the captured DSS tables
print cent-rounded rows. D. 823-16 calls for proportional reduction but does
not specify how to round that proportion. Its separate floor-to-euro step
is in the text and applies in every file.

- The model can calculate housing aid without establishing entitlement. The
  duty `VerserAideTheoriqueDue` requires a decency judgment; this example
  does not supply it. Explore the [decent-housing example](../logement-decent-garnier/)
  for the authority responses.
- Deadlines select `fr.pf.cmg::CMG_MOIS_CALENDAIRE` (calendar months without
  carry-over), matching the form of the unexported `fr.apl::APL_MOIS_CIVIL`.
- The caller links the family-benefit recipient (`fr.pf.core::Personne`) and
  housing household (`fr.apl::Menage`); no rule automatically joins them.
- May's resources are not recalculated. That file shows the change-related
  duty and effect date, not a new benefit amount.

Follow the [manual calculations and source references](sources/WITNESS.md).

<details>
<summary>Other expected answers, applied rules and recorded context</summary>

| Question | Model answer | Applied rule and source |
|---|---|---|
| AF resource band | Band 1 | `Bande1` — CSS D. 521-1 I 1° |
| AF under DSS row reading | €349.06 + €76.51 = **€425.57**, `TRUE_ONLY`; €425.56 is `NEITHER` | `MontantMensuelLignes`, `ArrondiLignesMetropole` — D. 521-1; `MontantDu` — L. 521-1 |
| AF after CRDS | **€423.44215** | `RetenueCRDSAF`, `NetApresCRDSAF` — ordinance 96-50, articles 14 and 19 |
| Personal contribution Pp | **€402.1515** | `ParticipationPersonnelle` — CCH D. 823-17 |
| Housing aid after reduction and contributions | **€189.95295**; €190.59 without floor-to-euro step is `NEITHER` | `DegressiviteProportionnelleArrondie`, `ArrondiIntermediaireCentime`, `MinorationForfaitaireAppliquee`, `ArrondiContributionsSociales` — D. 823-16, order articles 10 and 11 |
| Monthly housing allowance | **€189.95295** | `AideVerseeAllocationFamiliale`, `AideMensuelleMetropole` — order article 12, D. 823-16 |
| Housing allowance after CRDS | **€189.00318525** | `PrecompteCRDSMetropole` — ordinance 96-50, articles 14 III and 19 |
| Housing entitlement start | **1 April 2026** | `OuvertureApresConditions` — R. 823-10 |
| April duties | Household supplies supporting documents; fund pays net AF and informs the recipient | `JoindrePiecesJustificatives` — R. 823-2; `PayerAfNet` — L. 521-1 and ordinance 96-50; `InformerAllocataires` — L. 583-1 |
| AF without the row reading | Exact monthly €425.5624; total due **€425.56**, net €423.4322; €425.57 is `NEITHER` | `MontantMensuel` — D. 521-1; `MontantDu` rounds the total to cents |
| May change takes effect | **1 June 2026** | `EffetChangementDroits` — R. 823-13 |
| May household duty | Justify the change with the revision request | `JustifierChangements` — R. 823-3 |

April's positions also include the fund's `PayerAllocationsFamilialesDues`
and liberty `AiderRecouvrementCreances` (CSS L. 581-1), which the original
author check did not require. In May, `JoindrePiecesJustificatives` remains
active alongside `JustifierChangements`.

Answers expose input origins, parameters, operations and rule sources,
illustrating the explanation elements described in CRPA R. 311-3-1-2.
That text is not pinned in this example; check it on Légifrance. Exposing
these elements does not establish a decision's legal compliance.

On 10 October 2026, the author recorded 20/20 checks with an engine binary
from Arxo commit `d25481bde0`: 19 questions and the declared scenario run.
This is historical execution provenance, not legal qualification.

</details>

Need help running the commands? See [Troubleshooting](../README.md#troubleshooting).
