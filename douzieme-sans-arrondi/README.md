# Diviser par douze sans règle d'arrondi : refus, puis lecture nommée

Deux dossiers aux mêmes faits sur le canon épinglé `fr.apl@0.1.0` (APL,
secteur logement-foyer). Une personne seule, sans personne à charge, vit dans
un logement-foyer conventionné de type général en zone II ; redevance 430 EUR,
ressources 9 600 EUR par an, mois du droit mars 2026. Le paquet-cas ne porte que
ces faits et les questions ; les règles et le barème viennent du canon.

L'article D. 832-26 du code de la construction et de l'habitation calcule
l'équivalence de loyer minimale E0 : « Le résultat est majoré du produit d'un
montant forfaitaire par le nombre de parts “ N ”, le total étant ensuite divisé
par douze » (version applicable en mars 2026). Ici le
total vaut 1 977,17096 EUR et son douzième, 164,764246666… EUR, n'a pas
d'écriture décimale finie. Le texte ne dit pas comment l'arrondir.

## Les deux dossiers

| Dossier (`--case`) | Lecture choisie | E0 | Aide mensuelle |
|---|---|---|---|
| `ResidentSansLecture` | aucune lecture d'arrondi | refus `RUNTIME_ERROR`, `INEXACT_DIVISION` | pas de montant (`NEITHER`), même refus |
| `ResidentLectureD82` | `fr.apl::ArrondiCentimeHalfUp` (D-82, pratique de la CNAF : au centime, demi supérieur) | **164,76 EUR** `TRUE_ONLY` | **132,664624 EUR** `TRUE_ONLY` ; après CRDS 132,00130088 EUR |

Avec la lecture, Af = K × (E − E0) = 0,52 × (430 − 164,76) = 137,9248 EUR ; les
règles appliquées sont `EquivalenceLoyerMinimaleArrondie` et
`ArrondiIntermediaireCentime`, ancrées à D. 832-26 : la réponse dit quelle
lecture a tranché. Sans lecture, le canon ne choisit pas à la place du texte :
il refuse de diviser et nomme la cause. Le calcul à la main, tranche par
tranche, est dans [`sources/WITNESS.md`](sources/WITNESS.md).

Le même silence se retrouve ailleurs : la moyenne trimestrielle de l'article
R. 262-7 du code de l'action sociale et des familles (lecture
`MoyenneArrondieCentime` de `fr.minima.ressources`) et le douzième du complément
dégressif de D. 521-1 II du code de la sécurité sociale (lecture
`ArrondiLignesDss` de `fr.pf.af`). Ce paquet montre un seul de ces points.

## Lancer depuis la racine du dépôt

Le paquet-cas est membre du workspace : les dépendances se résolvent par nom
parmi les membres, sans `law.lock` ni `deps/`. Utilisez un binaire `law` déjà
construit (le lanceur `./law` recompile le moteur à chaque appel).

```sh
LAW_BIN=<binaire law> ./law ask corpus/laws/fr/apl/examples/douzieme-sans-arrondi \
  --case ResidentSansLecture \
  --query-json corpus/laws/fr/apl/examples/douzieme-sans-arrondi/queries/equivalence-loyer-minimale.json

LAW_BIN=<binaire law> ./law ask corpus/laws/fr/apl/examples/douzieme-sans-arrondi \
  --case ResidentLectureD82 \
  --query-json corpus/laws/fr/apl/examples/douzieme-sans-arrondi/queries/equivalence-loyer-minimale.json

python3 corpus/laws/fr/apl/examples/douzieme-sans-arrondi/check.py --law <binaire law>
```

`check.py` pose six questions (deux sans lecture, quatre avec), vérifie le
statut, le code `INEXACT_DIVISION` du refus, les règles appliquées, K = 0,52
dans le graphe de preuve et l'ancre D. 832-26 de la règle sous lecture, puis
lance `law test` sur le jumeau `tests/douzieme-sans-arrondi.lawtest`.

**État d'exécution, 10 octobre 2026.** `check.py --law <law>` passe 7/7
avec le binaire `law` construit depuis le commit d25481bde0 : les 6 questions
`law ask` et l'étape `law test` (code de sortie 0). Le jumeau `.lawtest` est
exécuté par `law test` : `[tests].world` commence par ce paquet-cas lui-même,
suivi du canon `fr.apl`.

## Limites

La lecture D-82 repose sur la pratique de la CNAF, non sur le texte : c'est un
choix nommé du dossier, pas une règle du canon. `PpPlancherFinal` est choisi
dans les deux dossiers seulement parce que le groupe `SensMinimumPp` du canon
exige un choix ; il n'entre pas dans ce calcul.
