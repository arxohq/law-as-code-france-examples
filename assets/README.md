# README visuals

`banner.png` was generated with the built-in ImageGen tool on 12 October
2026, using the published [book cover](https://books.arxo.io/law-as-code-france/)
as a style reference. The [prompt](banner-prompt.txt) records the adaptation
brief. The banner is editorial artwork and carries no execution evidence.

`moreau-proof.svg` is generated from the recorded Chapter 17 bundle:

```sh
python3 tools/render-readme-proof.py
```

The script reads `result.json` for proof nodes, premise edges, amounts,
status and legal date, and `request.json` for the pinned rules' source
anchors. Five supplied assertions are grouped into one input block; every
displayed edge corresponds to a premise edge, with grouped assertion edges
sharing a rail. An unrelated payment-regime branch is outside the query's
ancestors and is omitted. The script rejects a changed ancestor structure.

The saved bundle's hashes are embedded in SVG metadata. The diagram is a
view of that recorded answer, not an independent calculation or a claim
of legal qualification.
