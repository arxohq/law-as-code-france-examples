# Une famille de trois enfants qui loue : montants, articles, obligations, échéances

Trois dossiers d'une famille fictive sur les canons épinglés
`fr.prestations.versement`, `fr.pf.af`, `fr.pf.core`, `fr.apl` et `fr.pf.cmg`
(tous `0.1.0`). Nadia et Thomas Garnier ont trois enfants — Inès (15 ans), Hugo
(10 ans), Léa (5 ans). Depuis le 14 mars 2026, ils louent à un bailleur privé une
maison de cinq pièces en zone II, 1 320 EUR par mois ; les ressources du ménage
sont de 24 600 EUR par an. Le paquet-cas porte les faits et les questions ; les
règles, les lectures nommées et le barème du logement viennent des canons. La
BMAF et les plafonds de ressources des allocations familiales, que `fr.pf.af`
reçoit en entrée, sont cités dans les instructions DSS épinglées.

| Dossier (`--case`) | Date | Lectures choisies |
|---|---|---|
| `Garnier2026Avril` | 15 avril 2026 | `fr.pf.af::ArrondiLignesDss`, `fr.apl::ArrondiCentimeHalfUp`, `fr.apl::PpPlancherFinal` |
| `Garnier2026AvrilTexteSeul` | 15 avril 2026 | `fr.apl::PpPlancherFinal` seulement (choix exigé par le groupe `SensMinimumPp`) |
| `Garnier2026Mai` | 26 mai 2026 | les mêmes que `Garnier2026Avril` ; Thomas a perdu son emploi le 18 mai |

## Ce que répond le canon

| Question | Réponse | Pourquoi : règle et article |
|---|---|---|
| tranche de ressources des AF | tranche 1 | `Bande1` — CSS D. 521-1 I 1° |
| AF, lignes du barème DSS | 349,06 + 76,51 = **425,57 EUR** (`TRUE_ONLY`) ; 425,56 `NEITHER` | `MontantMensuelLignes`, `ArrondiLignesMetropole` — D. 521-1, lecture D-83 ; `MontantDu` — L. 521-1 |
| AF nettes après CRDS | **423,44215 EUR** | `RetenueCRDSAF`, `NetApresCRDSAF` — ordonnance 96-50, art. 14 et 19 |
| participation personnelle Pp | **402,1515 EUR** | `ParticipationPersonnelle` — CCH D. 823-17 |
| aide après dégressivité et contributions | **189,95295 EUR** ; 190,59 sans le pas de l'euro inférieur : `NEITHER` | `DegressiviteProportionnelleArrondie`, `ArrondiIntermediaireCentime` (lecture D-82), `MinorationForfaitaireAppliquee`, `ArrondiContributionsSociales` — CCH D. 823-16, arrêté art. 10 et 11 |
| allocation de logement mensuelle | **189,95295 EUR** | `AideVerseeAllocationFamiliale`, `AideMensuelleMetropole` — arrêté art. 12, D. 823-16 |
| allocation après précompte de la CRDS | **189,00318525 EUR** | `PrecompteCRDSMetropole` — ordonnance 96-50, art. 14 III et 19 |
| début du droit au logement | **1er avril 2026** | `OuvertureApresConditions` — CCH R. 823-10 |
| obligations actives en avril | le ménage joint les pièces justificatives ; la caisse paie les AF nettes et informe l'allocataire | `JoindrePiecesJustificatives` — R. 823-2 ; `PayerAfNet` — L. 521-1, ordonnance 96-50 ; `InformerAllocataires` — CSS L. 583-1 |
| sans lecture : AF | mensuel exact **425,5624 EUR** ; total dû **425,56 EUR** (net 423,4322) ; 425,57 `NEITHER` | `MontantMensuel` — D. 521-1 ; `MontantDu` arrondit le total au centime |
| sans lecture : logement | refus `RUNTIME_ERROR`, `INEXACT_DIVISION` : la proportion de D. 823-16 ne tombe pas juste | D. 823-16, « Il décroît proportionnellement au dépassement de ce plafond » |
| mai : effet du changement | **1er juin 2026** | `EffetChangementDroits` — CCH R. 823-13 |
| mai : obligation du ménage | justifier le changement avec la demande de révision | `JustifierChangements` — CCH R. 823-3 |

Les deux lectures d'arrondi sont des choix nommés du dossier, non des règles du
texte : D. 521-1 fixe des pourcentages de la BMAF sans arrondi, et les tables
des instructions DSS impriment des lignes arrondies au centime (lecture D-83) ;
D. 823-16 fait « décroître proportionnellement » l'aide sans dire comment
arrondir la proportion, et la pratique de la CNAF arrondit au centime (lecture
D-82). Le dossier `Garnier2026AvrilTexteSeul` montre ce que dit le texte seul.
Le pas « arrondi à l'euro inférieur, puis majoré de ce montant représentatif »
de D. 823-16, lui, est dans le texte et s'applique dans tous les dossiers. Le
calcul à la main de chaque montant est dans
[`sources/WITNESS.md`](sources/WITNESS.md).

Chaque réponse porte les données utilisées (les faits du dossier, avec leur
origine), les paramètres appliqués (valeurs du barème et leur ancre dans le
texte épinglé), les opérations (le graphe de preuve, règle par règle) et
l'article derrière chaque règle (ses ancres). Ce sont les éléments que
l'article R. 311-3-1-2 du code des relations entre le public et
l'administration énumère pour une décision prise sur le fondement d'un
traitement algorithmique ; ce texte n'est pas épinglé dans ce dépôt et se
vérifie sur Légifrance. Le paquet montre le contenu de la réponse ; il
n'affirme pas la conformité juridique d'une décision.

## Lancer depuis la racine du dépôt

Le paquet-cas est membre du workspace : les dépendances se résolvent par nom
parmi les membres, sans `law.lock` ni `deps/`. Utilisez un binaire `law` déjà
construit (le lanceur `./law` recompile le moteur à chaque appel).

```sh
LAW_BIN=<binaire law> ./law ask corpus/laws/fr/prestations-versement/examples/famille-trois-enfants-loyer \
  --case Garnier2026Avril \
  --query-json corpus/laws/fr/prestations-versement/examples/famille-trois-enfants-loyer/queries/al-mensuelle.json \
  --out corpus/laws/fr/prestations-versement/examples/famille-trois-enfants-loyer/runs/al-mensuelle

LAW_BIN=<binaire law> ./law ask corpus/laws/fr/prestations-versement/examples/famille-trois-enfants-loyer \
  --case Garnier2026Avril \
  --query-json corpus/laws/fr/prestations-versement/examples/famille-trois-enfants-loyer/queries/positions.json

python3 corpus/laws/fr/prestations-versement/examples/famille-trois-enfants-loyer/check.py --law <binaire law>
```

`check.py` pose dix-sept questions et deux questions de positions, vérifie le
statut, les règles appliquées, le code du refus, les ancres d'article des règles
« pourquoi » dans le programme de la réponse et les positions actives avec leur
titulaire, puis lance `law test` sur le jumeau
`tests/famille-trois-enfants-loyer.lawtest`, déclaré dans le `law.toml` de ce
paquet.

**État d'exécution, 10 octobre 2026.** `check.py --law <law>` passe 20/20
avec le binaire `law` construit depuis le commit d25481bde0 : les 19 questions
`law ask` et l'étape `law test` (code de sortie 0). Le jumeau `.lawtest` est
exécuté par `law test` : `[tests].world` commence par ce paquet-cas lui-même,
suivi de `fr.prestations.versement`, `fr.pf.core`, `fr.pf.af`, `fr.apl` et `fr.pf.cmg`.

## Limites

- La réponse `positions` d'avril porte aussi deux positions actives de la
  caisse que `check.py` n'exige pas : le devoir de payer les allocations
  familiales dues (`PayerAllocationsFamilialesDues`, `fr.pf.af`) et la liberté
  d'aider au recouvrement des créances d'entretien (`AiderRecouvrementCreances`,
  CSS L. 581-1) ; en mai, `JoindrePiecesJustificatives` reste active à côté de
  `JustifierChangements`.

- L'obligation de la caisse de verser l'allocation de logement
  (`VerserAideTheoriqueDue`) n'est pas demandée : elle suppose le droit ouvert,
  donc la décence du logement, que `fr.apl` traite comme un jugement de
  l'organisme (`logement_decent`) non exporté — un paquet-cas ne peut pas la
  fournir.
- Les échéances utilisent la politique de calcul des délais
  `fr.pf.cmg::CMG_MOIS_CALENDAIRE` : même forme que `APL_MOIS_CIVIL` de
  `fr.apl` (mois civil, sans report), qui n'est pas exportée.
- L'identité entre l'allocataire des AF (`fr.pf.core::Personne`) et le ménage du
  logement (`fr.apl::Menage`) reste du côté du dossier : aucune règle ne les
  relie, comme dans les autres dossiers de `fr.prestations.versement`.
- Les ressources de mai ne sont pas recalculées : le dossier de mai montre
  l'obligation et la date d'effet du changement, pas le nouveau montant.
