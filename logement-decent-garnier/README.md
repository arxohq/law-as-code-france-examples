# La décence du logement des Garnier : qui décide, et ce qui suit chaque réponse

Trois dossiers d'une famille fictive sur le canon épinglé `fr.apl` (`0.1.0`), avec
la politique de délais publique `fr.pf.cmg::CMG_MOIS_CALENDAIRE`. Mêmes faits de
logement que le dossier `prestations-versement/examples/famille-trois-enfants-loyer` :
Nadia et Thomas Garnier, trois enfants à charge, perçoivent les allocations
familiales ; depuis le 14 mars 2026 ils louent à un bailleur privé une maison de
cinq pièces en zone II, 1 320 EUR par mois, ressources 24 600 EUR par an ; demande
d'ALF le 20 mars. Le paquet-cas sert la leçon 9 du cours *Law as Code in Practice:
French Family Benefits (CNAF)*.

L'article L. 822-9 du code de la construction et de l'habitation exige un
logement décent pour ouvrir droit à l'aide. La décence est appréciée par
l'organisme payeur : dans `fr.apl`, c'est le canal de jugement
`logement_decent` (`authority OrganismePayeur`), et non un fait du dossier.

| Dossier (`--case`) | Date | Réponse de l'organisme |
|---|---|---|
| `DecenceEnAttente` | 15 avril 2026 | pas encore de réponse |
| `DecenceReconnue` | 15 avril 2026 | logement décent (`origin adjudicated`) |
| `NonDecenceConstatee` | 15 mai 2026 | logement non décent, constat du 28 avril 2026 (`origin adjudicated` et `constat_non_decence`) |

## Ce que répond le canon

| Question | `DecenceEnAttente` | `DecenceReconnue` | `NonDecenceConstatee` |
|---|---|---|---|
| droit ouvert (`droit_ouvert`) | `NEITHER`, `REQUIRES_JUDGMENT`, demande `logement_decent` → `OrganismePayeur` | `TRUE_ONLY` — `DroitOuvert`, L. 822-2 et L. 822-9 | `NEITHER`, `COMPUTED`, sans demande |
| aide calculée, 189,95295 EUR (`aide_mensuelle`) | `TRUE_ONLY` | `TRUE_ONLY` | `TRUE_ONLY` |
| allocation conservée (`conservation_en_cours`) | `NEITHER` | `NEITHER` | `TRUE_ONLY` — `ConservationDeclencheeALF`, L. 843-1 |
| loyer dû réduit, 1 130,04705 EUR (`loyer_du_reduit`) | `NEITHER` | `NEITHER` | `TRUE_ONLY` — `LoyerReduitConservation`, L. 843-1 |
| positions actives | ménage : pièces justificatives, interdiction du cumul des logements (R. 821-1) ; bailleur : attestation de décence (R. 823-2) | + caisse : verser l'aide due (`VerserAideTheoriqueDue`) | caisse : notifier le constat au propriétaire (L. 843-1), informer le locataire (R. 843-3) et le propriétaire des aides (R. 843-4) ; ménage : immunité contre la résiliation du bail (L. 843-1) ; bailleur : attestation (R. 823-2) |

Dans `NonDecenceConstatee` le même acte de l'organisme est saisi deux fois :
comme réponse négative au jugement de décence, et comme constat daté de
L. 843-1 qui déclenche la conservation. L'allocation conservée
(`allocation_due_conservation`) est le montant communiqué au locataire ; le
dossier reprend le calcul de la leçon 4 (189,95295 EUR), avec toutes ses
décimales. La caisse n'est tenue de verser l'aide que dans
`DecenceReconnue`.

## Lancer

Le paquet-cas est membre du workspace : les dépendances se résolvent par nom.

```sh
python3 corpus/laws/fr/apl/examples/logement-decent-garnier/check.py --law <binaire law>
```

`check.py` pose neuf questions et trois questions de positions, vérifie le
statut, les règles appliquées, la demande adressée à l'organisme et les
positions actives ou absentes, puis lance `law test` sur le jumeau
`tests/logement-decent-garnier.lawtest`.

**Piège (11 octobre 2026).** Une copie locale de dépendances hors git,
`examples/recours-remise-fontaine/deps/`, fait échouer un nouvel abaissement de
`fr.apl` (`LDC-E8704` : la découverte des ressources descend dans les
paquets-cas imbriqués). Dans un checkout propre, le dossier s'exécute.
