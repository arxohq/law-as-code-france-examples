# Law as Code in Practice: French Family Benefits — case packages

The ten case packages of the book *Law as Code in Practice: French Family Benefits*
(Law as Code by Country · Volume 1). Each folder holds one fictional file: the facts, the legal date,
the readings it selects, saved questions (`queries/`) and declared scenarios (`tests/`). The rules are
not copied here: `law.lock` pins the French canons by exact version and hash in the Arxo registry, and
`law install` fetches them.

**Status: private staging.** The canons are published in the private registry `arxohq/registry-staging`
with the layout of the public Arxo registry. Both repositories become public with the book.

## Run an example

```sh
git clone git@github.com:arxohq/registry-staging.git registry
git clone git@github.com:arxohq/law-as-code-france-examples.git examples
cd examples/prime-naissance-moreau
law install --registry arxo=../../registry
law ask . --case PlafondEgal --query-json queries/montant.json --out "$(mktemp -d)"
law test . --json
```

`law install` never picks versions: it restores exactly what `law.lock` pins and checks every hash.
The `law` tool must execute `law.core/0.2.11`. `check.py` in each folder is the authors' check inside
the Arxo repository and is not needed to run the examples.

## Chapters and folders

| Chapter | Folder |
|---|---|
| 0, 4 | `famille-trois-enfants-loyer/` |
| 1 | `editions-2021/` |
| 2, 5, 17, 18 | `prime-naissance-moreau/` |
| 3, 14 | `cohorte-revalorisation/` |
| 6 | `foyer-coefficient-k/` |
| 7 | `douzieme-sans-arrondi/` |
| 9 | `logement-decent-garnier/` |
| 11 | `famille-dans-le-temps/` |
| 12, 13 | `recours-remise-fontaine/` |
| 12 | `recours-indu-cra/` |
