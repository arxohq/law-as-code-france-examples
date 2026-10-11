# WITNESS — famille Garnier, avril et mai 2026 (calcul à la main)

Réplique indépendante, en fractions exactes, des réponses du canon pour les
trois dossiers de la famille Garnier. Elle part du texte : CSS L. 521-1,
D. 521-1, D. 521-3 et R. 521-4 (allocations familiales), ordonnance 96-50
art. 14 et 19 (CRDS), CCH D. 823-16 et D. 823-17 (aide au logement, secteur
locatif), R. 823-10 et R. 823-13 (dates), R. 823-2 et R. 823-3 (pièces et
changements), l'arrêté du 27 septembre 2019, chapitre III. Les valeurs du
barème du logement sont lues dans les paramètres épinglés de `fr.apl`
(éditions applicables en avril 2026) ; la BMAF et les plafonds de ressources
des AF sont des montants publiés que `fr.pf.af` reçoit en entrée (décision D-81),
cités ici dans les instructions épinglées de la DSS. Aucune règle du canon
n'est importée.

## Faits (dossier fictif)

Nadia Garnier (allocataire) et Thomas Garnier, en couple ; trois enfants à
charge : Inès (née le 3 novembre 2010, 15 ans), Hugo (21 juin 2015), Léa
(9 février 2021). Depuis le 14 mars 2026, la famille loue à un bailleur privé
une maison de cinq pièces en zone II, 1 320 EUR par mois ; demande d'aide au
logement le 20 mars 2026 ; ressources du ménage 24 600 EUR par an. En mai 2026,
Thomas perd son emploi le 18 ; la famille le déclare et demande la révision de
l'aide.

## Allocations familiales, avril 2026

| valeur | montant | source épinglée |
|---|---:|---|
| BMAF au 1er avril 2026 | 478,16 | DSS/2B/2026/46, `revalorisation/sources/dss-2026-46.txt:177` |
| plafond de base, 1re tranche ; majoration par enfant | 66 652 ; 6 664 | DSS/2B/2025/177, `dss-2025-177.txt:188-191` |

1. Plafond de la 1re tranche pour trois enfants : 66 652 + 3 × 6 664 = 86 644 ;
   24 600 ≤ 86 644 : **tranche 1** (D. 521-1 I 1°, montant maximal).
2. Base AF, trois enfants : 32 % + 41 % = 73 % de la BMAF ;
   73 % × 478,16 = 349,0568.
3. Majoration pour âge (Inès, 14 ans et plus, famille de trois enfants) :
   16 % × 478,16 = 76,5056.
4. **Lecture `ArrondiLignesDss` (D-83)** : chaque ligne du barème DSS est
   arrondie au centime (« 3 enfants 73 % 349,06 », « 16 % 76,51 »,
   `dss-2026-46.txt:192` et `:208`), le total est la somme des lignes :
   349,06 + 76,51 = **425,57** (`montant_mensuel_af` et `af_montant_du`).
   Arrondir le total exact donnerait 425,56 : le canon ne le déduit pas sous
   cette lecture.
5. **Sans lecture** (dossier `Garnier2026AvrilTexteSeul`) : le mensuel est le
   produit exact **425,5624** ; la règle `MontantDu` du canon arrondit le total
   dû au centime, demi supérieur : **425,56**.
6. CRDS précomptée (0,5 %, ordonnance 96-50 art. 14 et 19) et montant net :
   425,57 × 0,005 = 2,12785 ; net **423,44215** ; sans lecture,
   425,56 − 2,1278 = **423,4322**.

## Allocation de logement familiale, avril 2026

| valeur | montant | ancre |
|---|---:|---|
| plafond de loyer, zone II, 1 personne à charge ; par personne en plus (art. 7) | 399,89 ; 58,21 | ARR_ART07_ED2025_10 |
| forfait de charges ; par personne à charge (art. 9) | 60,59 ; 13,74 | ARR_ART09_ED2025_10 |
| P0 : 8,5 % de L + C, au moins (art. 13) | 39,56 | ARR_ART13_ED2025_10 |
| TF, trois personnes à charge (art. 14) | 0,0201 | ARR_ART14_ED2025_10 |
| LR : 399,89 + 58,21 par personne à charge au-delà d'une (art. 14) | 516,31 | ARR_ART14_ED2025_10 |
| R0, trois personnes à charge (art. 15) | 9 498 | ARR_ART15_ED2025_10 |
| coefficients de dégressivité et de suppression, zone II (art. 10) | 2,5 ; 3,1 | ARR_ART10_ED2025_10 |
| minoration forfaitaire (art. 11) ; seuil de versement ALF (art. 12) | 5,00 ; 10,00 | ARR_ART11/12_ED2025_10 |

1. Plafond : 399,89 + 2 × 58,21 = 516,31 ; L = min(1 320, 516,31) = **516,31**.
2. C = 60,59 + 3 × 13,74 = **101,81**.
3. P0 = max(8,5 % × 618,12, 39,56) = max(52,5402, 39,56) = **52,5402**.
4. RL = 516,31 / 516,31 = 1,0000 ; TL = 0,45 % × 0,30 + 0,68 % × 0,25 = 0,00305 ;
   Tp = 0,0201 + 0,00305 = 0,02315.
5. R = 24 600 ; R − R0 = 15 102 ; Pp = 52,5402 + 0,02315 × 15 102 = **402,1515**
   (lecture `PpPlancherFinal` : Pp ≥ P0, ici sans effet).
6. Af = 516,31 + 101,81 − 402,1515 = **215,9685**.
7. Dégressivité (D. 823-16) : plafond de dégressivité 516,31 × 2,5 = 1 290,775,
   plafond de suppression 516,31 × 3,1 = 1 600,561 ; le loyer 1 320 dépasse le
   premier : 215,9685 × (1 600,561 − 1 320) / (1 600,561 − 1 290,775)
   = 215,9685 × 280,561 / 309,786 = 195,594178976… (quotient sans écriture
   décimale finie).
   - **Lecture `ArrondiCentimeHalfUp` (D-82)** : arrondi au centime, **195,59**.
   - **Sans lecture** : refus `INEXACT_DIVISION` ; l'aide n'a pas de montant.
8. Minoration : 195,59 − 5 = **190,59**.
9. Contributions sociales, D. 823-16 : c = 0,5 % × 190,59 = 0,95295 ;
   ⌊190,59 − 0,95295⌋ = ⌊189,63705⌋ = 189 ; 189 + 0,95295 = **189,95295**
   (pas de RLS, bailleur privé). Sans ce pas, 190,59 : non déduit.
10. 189,95295 ≥ 10 : versée, `aide_mensuelle` = **189,95295**.
11. Précompte de la CRDS : 189,95295 × 0,995 = **189,00318525**.

## Dates et positions

- Conditions réunies le 14 mars 2026, demande le 20 mars 2026, hors des
  dérogations de R. 823-11 : l'aide est due à compter du premier jour du mois
  suivant, **1er avril 2026** (R. 823-10).
- Changement du 18 mai 2026 modifiant les droits : il prend effet le
  **1er juin 2026** (R. 823-13).
- Positions actives en avril : le ménage doit joindre les pièces justificatives
  de la demande (R. 823-2, `JoindrePiecesJustificatives`) ; la caisse doit payer
  au ménage les allocations familiales nettes dues (`PayerAfNet`) et informer
  l'allocataire de ses droits (L. 583-1, `InformerAllocataires`). En mai : le
  ménage doit justifier le changement avec sa demande de révision (R. 823-3,
  `JustifierChangements`).

Canon (lawc et oracle lawref, `tests/famille-trois-enfants-loyer.lawtest`) :
toutes les valeurs ci-dessus `TRUE_ONLY` dans le dossier qui les porte ; 425,56
sous la lecture DSS, 425,57 sans elle et 190,59 sont `NEITHER` ; l'aide sans
lecture est `RUNTIME_ERROR` avec `INEXACT_DIVISION` ; les quatre positions sont
`ACTIVE`.

Pour comparaison (réplique seulement) : la lecture d'OpenFisca —
round2((round2(195,594…) − 5) × 0,995), sans pas de l'euro inférieur — donnerait
189,64 EUR au lieu de 189,00318525.
