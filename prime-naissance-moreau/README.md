# Prime à la naissance — trois dossiers Moreau

Famille fictive distincte des Garnier: grossesse, juillet 2025. Les valeurs
BMAF 400 EUR et plafond de base 30000 EUR reprennent des tests pédagogiques;
elles ne représentent pas les montants annuels publiés pour cette famille.

Trois dossiers: égalité au plafond, dépassement d’un centime, ressources absentes.
Les faits sont case_input; aucune appréciation d’un organisme n’est simulée.

```sh
python3 check.py --law <chemin-absolu-vers-law> --out <nouveau-dossier>
law ask . --case RessourcesAbsentes --query-json queries/droit.json --out <nouveau-dossier>
law test . --json
```

Exécution locale dans le checkout: les canons français ne sont pas encore publiés
pour une installation indépendante. Réplique arithmétique: sources/WITNESS.md.
