# WITNESS — « le total étant ensuite divisé par douze » sans règle d'arrondi (calcul à la main)

Réplique indépendante, en fractions exactes, des deux réponses du canon. Elle
part du texte : CCH D. 832-26 dans sa version applicable en mars 2026 (E0 « est
obtenue par application de pourcentages à des tranches de ressources, dont les
limites inférieures et supérieures initiales sont multipliées par le nombre de
parts “ N ” […]. Le résultat est majoré du produit d'un montant forfaitaire par
le nombre de parts “ N ”, le total étant ensuite divisé par douze »),
D. 832-24, D. 832-25, D. 832-27 et l'arrêté du 27 septembre 2019, articles 27
à 32. Seules les valeurs du barème sont lues dans
les paramètres épinglés du canon (`corpus/laws/fr/apl/bareme/`, mars 2026).

## Faits (dossier fictif)

Une personne seule, sans personne à charge, logement-foyer conventionné de type
général, zone II, métropole ; redevance 430 EUR ; ressources 9 600 EUR par an ;
mois du droit : mars 2026 ; APL.

## E0 : un douzième qui ne tombe pas juste

N = 1,4 (personne seule, D. 832-25 1°) ; R = 9 600. Bornes de l'article 31
(a) premier alinéa) multipliées par N : 2 727,34 / 3 750,194 / 5 454,652 /
7 500,416 / 8 863,806.

| tranche | montant |
|---|---:|
| 2 727,34 × 4 % | 109,0936 |
| (3 750,194 − 2 727,34) × 10,4 % | 106,376816 |
| (5 454,652 − 3 750,194) × 21,6 % | 368,162928 |
| (7 500,416 − 5 454,652) × 26,4 % | 540,081696 |
| (8 863,806 − 7 500,416) × 32 % | 436,2848 |
| (9 600 − 8 863,806) × 48 % | 353,37312 |
| somme | 1 913,37296 |
| forfait 45,57 × 1,4 | 63,798 |
| total | 1 977,17096 |

1 977,17096 / 12 = 24 714 637 / 150 000 = 164,764246666… EUR : le dénominateur
contient le facteur 3, le quotient n'a pas d'écriture décimale finie.
D. 832-26 ne dit pas comment l'arrondir.

## Dossier `ResidentSansLecture` — aucune lecture d'arrondi

Le canon divise exactement ou refuse : E0 n'est pas représentable, la réponse
est `RUNTIME_ERROR` avec le code `INEXACT_DIVISION`, et l'aide qui en dépend ne
reçoit pas de montant (`NEITHER`). Aucun arrondi silencieux n'est appliqué.

## Dossier `ResidentLectureD82` — lecture `fr.apl::ArrondiCentimeHalfUp`

Lecture nommée D-82 du canon (pratique de la CNAF, non le texte) : le quotient
inexact d'une division dont le texte ne fixe pas l'arrondi est arrondi au
centime, demi supérieur.

1. E0 = arrondi(164,764246…, 2) = **164,76**.
2. E = min(430, plafond art. 27 zone II personne seule 456,15) = 430.
3. K = 0,95 − ⌈(9 600 − 1 217,26 × 1,4) / (13 393,40 × 1,4)⌉ au centième
   = 0,95 − ⌈0,421094…⌉ = 0,95 − 0,43 = **0,52** (D. 832-25 lu par R. 351-61,
   « arrondi à deux décimales par défaut »).
4. Af = 0,52 × (430 − 164,76) = **137,9248**.
5. Minoration 5 EUR : 132,9248 ; dépense nette 430 − 132,9248 = 297,08 > 26,68 :
   pas d'abattement.
6. Contributions sociales : c = 0,664624 ; ⌊132,9248 − 0,664624⌋ = 132 ;
   132 + 0,664624 = **132,664624** ≥ 10 : versée.
7. Après précompte de la CRDS : 132,664624 × 0,995 = **132,00130088**.

Pour comparaison (réplique seulement, le canon ne le calcule pas) : avec le
quotient exact, Af = 0,52 × (430 − 164,764246…) = 137,922591…, soit 0,0022 EUR
de moins ; l'aide versée après le pas de l'euro inférieur reste 132 EUR plus
la contribution représentative.

Canon (lawc et oracle lawref, `tests/douzieme-sans-arrondi.lawtest`) : sans
lecture, `RUNTIME_ERROR` et `INEXACT_DIVISION` pour E0 et pour l'aide ; avec la
lecture D-82, E0, Af, l'aide mensuelle et le montant net `TRUE_ONLY`, par les
règles `EquivalenceLoyerMinimaleArrondie` et `ArrondiIntermediaireCentime`
(ancrées à D. 832-26).
