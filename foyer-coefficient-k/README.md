# Le coefficient K de l'article D. 832-25, sur un dossier de logement-foyer

Un dossier fictif sur le canon épinglé `fr.apl@0.1.0` (aide personnalisée au
logement, secteur logement-foyer). Un couple de retraités sans personne à
charge vit dans une résidence autonomie conventionnée de type général, en
zone II ; la redevance est de 495 EUR par mois et les ressources du ménage de
12 500 EUR par an ; le mois du droit est mars 2026. Le paquet-cas ne porte que
ces faits et les questions enregistrées : les règles, la lecture de K et toutes
les valeurs du barème viennent du canon.

La formule de K de l'article D. 832-25 du code de la construction et de
l'habitation n'est publiée dans Légifrance que sous forme d'image. Le canon la
lit dans le texte des articles abrogés R. 351-61 et R. 351-61-1 du même code,
présents dans les données LEGI ; la règle qui calcule K porte les deux ancres.

## Questions et réponses

| Question (`queries/`) | Réponse du canon | Règle appliquée |
|---|---|---|
| `equivalence-loyer-minimale` — E0 = 218,12546 EUR | `TRUE_ONLY` | D. 832-26 (`EquivalenceLoyerMinimale`) |
| `aide-formule` — Af = K × (E − E0) = 143,9747608 EUR, avec N = 1,8 et K = 0,52 dans le graphe de preuve | `TRUE_ONLY` | D. 832-24, D. 832-25 et R. 351-61 (`AideFoyerFormuleAPL`, `CoefficientPriseEnChargeAPLGeneral`, `NombreParts`) |
| `aide-formule-k-053` — Af = 146,7435062 EUR, celui d'un K arrondi par excès (0,53) | `NEITHER` | — |
| `aide-mensuelle` — 138,694873804 EUR | `TRUE_ONLY` | D. 832-24, arrêté art. 28 et 29 (`ContributionsSocialesFoyerAPL`, `AideFoyerVersee`) |
| `aide-nette-crds` — 138,00139943498 EUR après précompte de la CRDS | `TRUE_ONLY` | ordonnance 96-50, art. 14 III et 19 (`PrecompteCRDSMetropole`) |

K = 0,95 − (R − r × N) / (cm × N) = 0,95 − (12 500 − 1 217,26 × 1,8) /
(13 393,40 × 1,8) = 0,5224…, « arrondi à deux décimales par défaut » : 0,52.
Af = 0,52 × (495 − 218,12546) = 143,9747608 EUR ; après la minoration de 5 EUR
et le montant représentatif des contributions sociales arrondi à l'euro
inférieur, l'aide mensuelle est de 138,694873804 EUR. Le calcul à la main,
tranche par tranche, est dans [`sources/WITNESS.md`](sources/WITNESS.md).

## Lancer depuis la racine du dépôt

Le paquet-cas est membre du workspace : les dépendances se résolvent par nom
parmi les membres, sans `law.lock` ni `deps/`. Le lanceur `./law` à la racine
recompile le moteur à chaque appel ; utilisez un binaire déjà construit.

```sh
LAW_BIN=<binaire law> ./law ask corpus/laws/fr/apl/examples/foyer-coefficient-k \
  --case CoupleResidenceAutonomie \
  --query-json corpus/laws/fr/apl/examples/foyer-coefficient-k/queries/aide-formule.json \
  --out corpus/laws/fr/apl/examples/foyer-coefficient-k/runs/aide-formule

python3 corpus/laws/fr/apl/examples/foyer-coefficient-k/check.py --law <binaire law>
```

`check.py` pose les cinq questions, vérifie le statut, les règles appliquées,
la valeur de K et de N dans le graphe de preuve et les ancres de la règle de K
(D. 832-25 et R. 351-61) dans le programme de la réponse, puis lance `law test`
sur le jumeau `tests/foyer-coefficient-k.lawtest`, déclaré dans le `law.toml`
de ce paquet. Le jumeau vérifie K à travers Af : un littéral décimal d'un
`.lawtest` est abaissé en `Number` et ne se compare pas à une valeur `Decimal`
(limite connue du canon, D-42).

**État d'exécution, 10 octobre 2026.** `check.py --law <law>` passe 6/6
avec le binaire `law` construit depuis le commit d25481bde0 : les 5 questions
`law ask` et l'étape `law test` (code de sortie 0). Le jumeau `.lawtest` est
exécuté par `law test` : `[tests].world` commence par ce paquet-cas lui-même,
suivi du canon `fr.apl`.

## Limites

La lecture de K par R. 351-61 / R. 351-61-1 est une lecture : l'identité entre
l'image de D. 832-25 et la formule de l'article abrogé ne se vérifie pas sur les
octets de l'image. La lecture `PpPlancherFinal` est choisie seulement parce que
le groupe `SensMinimumPp` du canon exige un choix dans chaque dossier ; elle
n'entre pas dans le calcul du logement-foyer.
