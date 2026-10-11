# WITNESS — couple en résidence autonomie, coefficient K (calcul à la main)

Réplique indépendante, en fractions exactes, de la réponse du canon pour le
dossier `CoupleResidenceAutonomie`. Elle part du texte : CCH D. 832-24
(Af = K × (E − E0), minoration, montant représentatif des contributions
sociales), D. 832-25 (N et K), D. 832-26 (E0), D. 832-27 (dépense nette
minimale) et l'arrêté du 27 septembre 2019, articles 27 à 32. Seules les
valeurs du barème sont lues dans les paramètres épinglés du canon
(`corpus/laws/fr/apl/bareme/`, éditions applicables en mars 2026) ; aucune règle
du canon n'est importée.

## Faits (dossier fictif)

Couple sans personne à charge, logement-foyer conventionné de type général
(résidence autonomie), zone II, métropole ; redevance 495 EUR par mois ;
ressources du ménage 12 500 EUR par an ; mois du droit : mars 2026 ; APL.

## Valeurs épinglées (mars 2026)

| valeur | montant | ancre |
|---|---:|---|
| plafond d'équivalence de loyer E, zone II, couple (art. 27) | 532,35 | ARR_ART27_ED2025_10 |
| parts N, couple sans personne à charge (D. 832-25 1°) | 1,8 | CCH_D832_25_ED2023_12 |
| tranches E0 (art. 31, a) premier alinéa) | 1 948,10 / 2 678,71 / 3 896,18 / 5 357,44 / 6 331,29 × N ; 4 / 10,4 / 21,6 / 26,4 / 32 / 48 % | ARR_ART31_ED2025_10 |
| forfait E0, premier alinéa (art. 31) | 45,57 × N | ARR_ART31_ED2025_10 |
| r et cm (art. 30) | 1 217,26 ; 13 393,40 | ARR_ART30_ED2025_10 |
| plafond de K, 1° (D. 832-25) | 0,95 | CCH_D832_25_ED2023_12 |
| minoration forfaitaire APL foyer (art. 28) | 5,00 | ARR_ART28_ED2025_10 |
| dépense nette minimale (art. 32) | 26,68 | ARR_ART32_ED2025_10 |
| seuil de versement APL foyer (art. 29) | 10,00 | ARR_ART29_ED2025_10 |
| CRDS (ordonnance 96-50, art. 19) | 0,5 % | ORD9650_ART19_ED2020_01 |

## Étapes

1. R = 12 500 (ressources « arrondies à la centaine d'euros supérieure »).
2. E = min(495, 532,35) = **495**.
3. E0 : bornes × 1,8 = 3 506,58 / 4 821,678 / 7 013,124 / 9 643,392 / 11 396,322 ;
   tranches 140,2632 + 136,770192 + 473,352336 + 694,390752 + 560,9376 +
   (12 500 − 11 396,322) × 48 % = 529,76544 ; somme 2 535,47952 ; forfait
   45,57 × 1,8 = 82,026 ; E0 = 2 617,50552 / 12 = **218,12546** (quotient fini).
4. K (formule 1°, lue dans R. 351-61, voir ci-dessous) :
   (R − r × N) / (cm × N) = (12 500 − 2 191,068) / 24 108,12 = 0,427612… ;
   K = 0,95 − 0,427612… = 0,522387… , « arrondi à deux décimales par défaut »
   → **0,52** (au plus égal à 0,95).
5. Af = 0,52 × (495 − 218,12546) = 0,52 × 276,87454 = **143,9747608**.
   Avec K = 0,53 (arrondi par excès) on aurait 146,7435062 : le canon ne le
   déduit pas.
6. Minoration : 143,9747608 − 5 = 138,9747608 ; dépense nette
   495 − 138,9747608 = 356,03 > 26,68 : pas d'abattement.
7. Contributions sociales : c = 0,5 % × 138,9747608 = 0,694873804 ;
   ⌊138,9747608 − 0,694873804⌋ = 138 ; 138 + 0,694873804 = **138,694873804**
   ≥ 10 : versée (`aide_mensuelle`).
8. Précompte de la CRDS par l'organisme payeur :
   138,694873804 × 0,995 = **138,00139943498** (`aide_nette_precompte_crds`).

Canon (lawc et oracle lawref, `tests/foyer-coefficient-k.lawtest`) : E0, Af,
aide mensuelle et montant net `TRUE_ONLY` ; Af avec K = 0,53 `NEITHER` ; les
règles `NombreParts`, `CoefficientPriseEnChargeAPLGeneral`, `AideFoyerFormuleAPL`
s'appliquent.

## Lecture de K

Le texte de D. 832-25 (1° et 2°) n'existe dans Légifrance et dans les données
LEGI que sous forme d'image (« Vous pouvez consulter l'intégralité du texte
avec ses images »). Le canon lit l'algèbre dans les articles qu'a abrogés, le
1er septembre 2019, le même décret qui a créé D. 832-25, et dont le texte est
dans le dump : R. 351-61 « K = 0,95-((R-(r X N))/ (CM X N)) », au plus égal à
0,95, « arrondi à deux décimales par défaut » (cas général), et R. 351-61-1
« K = 0,9-(R/ (CM X N)) » (foyers de jeunes travailleurs et résidences
sociales). La règle `CoefficientPriseEnChargeAPLGeneral` porte les deux ancres,
D. 832-25 et R. 351-61 ; `check.py` le vérifie dans le programme de la réponse.
C'est une lecture, pas une citation de D. 832-25 : les six valeurs de K des
exemples Catala la confirment (voir le README du canon, « Коэффициент K »).
