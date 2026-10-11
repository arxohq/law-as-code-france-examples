# WITNESS — famille dans le temps (hand computation)

Household: Camille (allocataire) + Mehdi; Lina (b. 2018-05-10), Yanis
(b. 2021-11-02), Chloe (b. 2025-06-20). Every brut below is a
caller-stated owner-chain value, NOT derived: the dossier routes stated
bruts through the payment stage; deriving AF/ARS/PAJE/RSA from
household facts is the neighbours' job. CRDS rate 0.5 % (Ord. 96-50
art. 14, pinned in fr.apl). No rounding rule exists at PF payment
stage (B-PV-ARRONDI): products stay exact.

## March 2024 — AF + housing (Famille2024_03)

- AF brut stated 200.00. CRDS = 200.00 x 0.005 = 1.00.
  Net = 200.00 - 1.00 = 199.00 -> `af-net-2024-03` TRUE_ONLY.
- Housing net stated 344.00 (fr.apl.versement chain, read-only here).

## August 2024 — ARS (Famille2024_08)

- ARS Lina stated 400.00. CRDS = 400.00 x 0.005 = 2.00.
  Net = 400.00 - 2.00 = 398.00 -> `ars-net-2024-08` TRUE_ONLY.
- Household total stated 400.00 >= 15 EUR floor (D. 543-2): paid.

## July 2025 — PAJE prime (Famille2025_07)

- Prime stated 1000.00. CRDS = 1000.00 x 0.005 = 5.00.
  Net = 1000.00 - 5.00 = 995.00 -> `prime-net-2025-07` TRUE_ONLY.
- July AF brut stated 320.00 (three children). Net = 318.40
  (routed, not queried).

## December 2025 — AF recovery (Famille2025_12)

- Echeance: brut 320.00 -> CRDS 1.60 -> 318.40.
- Debt: indu 500.00 + RSA carry 0 = 500.00 (no fraud stated).
- Deduction amount fund-stated 79.60 (Money). Deduction = min(79.60, 500.00)
  = min(79.60, 500.00) = 79.60.
- Net = 318.40 - 79.60 = 238.80 -> `af-rec-2025-12` TRUE_ONLY.

## March 2026 — prescription + RSA carry (Famille2026_03)

- AF thread: echeance 318.40 (brut 320.00); the 2021 indu is
  time-barred (action_prescrite supplied as a finding; not derived here):
  no deduction, full 318.40 -> `af-presc-2026-03` TRUE_ONLY.
- RSA thread: allocation stated 600.00; debt = own indu 0 +
  PF carry 300.00 + PA carry 0 = 300.00 (no fraud stated);
  deduction amount fund-stated 180.00 (Money). Deduction =
  min(180.00, 300.00) = 180.00. Net = 600.00 - 180.00 = 420.00
  -> `rsa-carry-2026-03` TRUE_ONLY.
- PA thread: none in this snapshot — the PA checkpoint lives in
  Famille2026_06 (June 2026) since the FINISH-W2 linkage
  (B-PV-PA closed).

## June 2026 — PA recovery checkpoint, given-PA regression (Famille2026_06)

- Served quarterly amount STATED 280.00 (owner chain, post
  minimum-payment floor). This case proves payment/recovery
  arithmetic ONLY from a supplied echeance — it does NOT derive
  the logement → forfait → RSA → PA chain: the cascade trace
  below is stated values (D-26 contract), not rule outputs.
  Cascade trace: housing net 344.00 (March 2024, stage 1) feeds
  the R. 262-9 housing flat-rate inside quarterly resources
  (stage 2); the RSA allocation 600.00 (March 2026, stage 3) is
  paid through this layer (net 420.00 after the PF carry); paid
  RSA nets enter PA resources for the reviewed quarter (R. 842-3,
  actually received — not the due average), from which the
  neighbour serves 280.00 (stage 4). The 3-month resource sum is
  a stated-assumption proxy here: this snapshot states one
  served quarter, not three paid months.
- Debt: own PA indu 150.00 + RSA carry 60.00 = 210.00 (no fraud
  stated). Deduction amount fund-stated70.00 (Money). Deduction = min(70.00, 210.00) = 70.00.
- Net = 280.00 - 70.00 = 210.00 -> `pa-rec-2026-06` TRUE_ONLY.
- The JOINED derivation (each stage computed by public neighbour
  rules from case inputs: aid 344.00 -> capped 72.00 -> RSA
  allocation 372.00 -> paid nets 312.00 -> PA resources 612.00 ->
  DERIVED due 167.55 -> net 134.04) runs in
  `tests/dossier-pa-cascade-2026-06.lawtest` and its positions
  twin. No normative end-to-end calculation is claimed from the
  stated 280.00 in this case.
- Cross-identity linkage (menage / minima Personne / Demandeur)
  stays caller-side per IDENTITY/NO-LEDGER: the case states each
  stage's inputs equal to the previous stage's witnessed outputs;
  no rule joins the identities.

## Foreign cross-check (structure only, S4 survey)

- Leximpact/2024 gross+CRDS+net triples (PPA/AF/ARS/ASF/CF/PAJE;
  PPA 19 is the largest group) confirm the shape
  CRDS-applies/net=brut-CRDS at ±1 EUR; cents are never anchored
  to them.
- mes-aides cases are gross-only 2014-2015 law: usable for brut
  plausibility, not for payment-stage expectations.
- No foreign suite covers retenues, the 10 % indemnity, the fraud
  uplift, floors as standalone assertions, or prescription bars:
  the December 2025 and March 2026 checkpoints have no foreign
  counterpart by construction.

## Method note (apply-canon, without-guide)

No `fr` package publishes a task guide, so no author's route was
followed: the order of questions (CRDS checkpoints, then recovery,
then prescription/carry) is the agent's; only the answers are the
canon's. No passage journal is kept — a journal pins a route.
In THIS case the housing -> forfait -> RSA -> PA cascade is
staged as stated owner-chain values plus this hand arithmetic
(D-26 contract); the joined in-world derivation (stages 2-4
computed, stage 1 via the minima input contract, caller-side
identity per IDENTITY) runs in
`tests/dossier-pa-cascade-2026-06.lawtest` since the FINISH-W2
cascade follow-up. No rule joins the identities; nothing here
claims a normative end-to-end calculation from the stated 280.00.

Update11.10.2026: fixed Money levy inputs replace obsolete rate inputs, with
explicit lawful carry-over facts; all seven expected answers unchanged and
passed with law0.1.12. Rates are not computed in this case.
