#!/usr/bin/env python3
"""Render the recorded Moreau proof, grouping its five case assertions."""
from pathlib import Path
from decimal import Decimal
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "prime-naissance-moreau/runs/plafond-egal"
result = json.loads((RUN / "result.json").read_text())
ir = json.loads((RUN / "request.json").read_text())["ir"]
nodes = {n["id"]: n for n in result["proofGraph"]["nodes"]}
rules = {n["rule"].split("#")[-1]: n for n in nodes.values() if "rule" in n}
ir_nodes = {n["id"]: n for n in ir["nodes"]}
query = nodes[result["proofGraph"]["roots"][0]]
ancestors = set()

def visit(node_id):
    if node_id in ancestors:
        return
    ancestors.add(node_id)
    for premise in nodes[node_id].get("premises", []):
        visit(premise)

visit(query["id"])
inputs = [n for n in nodes.values() if n["id"] in ancestors and n["kind"] == "assertion"]
selected = [rules[name] for name in ["PlafondPrimeConstruit", "DroitPrimeNaissance", "MontantPrimeNaissance", "PrimeNaissanceAttribuee"]]
if {n["id"] for n in inputs + selected + [query]} != ancestors:
    raise ValueError("Recorded proof structure changed; review the diagram grouping")

def value(node):
    return next(a["value"] for a in reversed(node["conclusion"]["args"]) if "value" in a)

def money(raw):
    return "€" + format(Decimal(raw), ",f").rstrip("0").rstrip(".") if "." in raw else "€" + format(int(raw), ",")

input_by_predicate = {n["conclusion"]["predicate"].split("#")[-1]: n for n in inputs}
base = money(value(input_by_predicate["plafond_base_taux_plein"]))
income = money(value(input_by_predicate["ressources_annuelles"]))
bmaf = money(value(input_by_predicate["bmaf_applicable"]))
exam = value(input_by_predicate["date_examen_situation"])
ceiling = money(value(selected[0]))
amount = money(value(selected[2]))
status = query["conclusion"]["truthStatus"]

parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="720" height="846" viewBox="0 0 720 846" role="img" aria-labelledby="title desc">',
         '<title id="title">Moreau: the recorded proof of a '+amount+' birth grant</title>',
         '<desc id="desc">Five supplied inputs feed four applied rules: construct the ceiling, establish entitlement, compute the amount, and attribute the grant at the examination date. The query is '+status+'. Source anchors are resolved from the recorded program.</desc>',
         '<metadata>'+escape(json.dumps({"resultHash": result["resultHash"], "programHash": result["manifest"]["programHash"], "proofHash": result["proofGraph"]["proofHash"], "nodes": sorted(ancestors)}))+'</metadata>',
         '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#1b5277"/></marker></defs>',
         '<rect width="720" height="846" rx="12" fill="#fffaf3"/>']

def text(x, y, content, size=22, color="#172a3d", mono=False, weight="400"):
    font = "ui-monospace, SFMono-Regular, Consolas, monospace" if mono else "-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    parts.append(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(content)}</text>')

text(40, 42, "Follow the recorded answer", 30, weight="700")
text(40, 70, "PlafondEgal · legal date "+result["manifest"]["legalTime"], 18, "#42586b")
parts.append('<rect x="60" y="94" width="600" height="90" rx="8" fill="#f1e8dc"/>')
text(80, 123, "Teaching inputs: base "+base+" · income "+income, 22)
text(80, 150, "BMAF "+bmaf+" · expected child", 22)
text(80, 175, "Examination date: "+exam+" · five inputs grouped", 18, "#42586b")

ys = [224, 354, 484, 614, 744]
node_y = {n["id"]: y for n, y in zip(selected+[query], ys)}
# Each line corresponds to a real premise edge. Assertion edges share a rail.
for node, y in zip(selected+[query], ys):
    for premise in node.get("premises", []):
        if nodes[premise]["kind"] == "assertion":
            continue
        parent_y = node_y[premise]
        if y - parent_y == 130:
            parts.append(f'<path d="M360 {parent_y+90} V{y-6}" stroke="#1b5277" stroke-width="2" fill="none" marker-end="url(#arrow)"/>')
        else:
            parts.append(f'<path d="M660 {parent_y+45} H692 V{y+45} H666" stroke="#1b5277" stroke-width="2" fill="none" marker-end="url(#arrow)"/>')
    if any(nodes[p]["kind"] == "assertion" for p in node.get("premises", [])):
        parts.append(f'<path d="M60 139 H28 V{y+45} H54" stroke="#1b5277" stroke-width="1.5" fill="none" marker-end="url(#arrow)"/>')

labels = ["Ceiling constructed: "+ceiling, "Entitlement established", "Grant amount: "+amount, "Grant attributed: "+amount, "Answer: "+status+" · "+amount]
for n,y,label in zip(selected+[query],ys,labels):
    fill = "#e5eef4" if n is query else "#ffffff"
    parts.append(f'<rect x="60" y="{y}" width="600" height="90" rx="8" fill="{fill}" stroke="#b4c4cf"/>')
    text(80,y+29,label,26,weight="600")
    if n is query:
        text(80,y+59,"The claim in queries/montant.json is supported.",20)
    else:
        text(80,y+54,n["rule"].split("#")[-1],20,mono=True)
        anchors = n.get("sourceAnchors") or ir_nodes[n["rule"]].get("anchors", [])
        articles = list(dict.fromkeys(ir_nodes[a]["locator"].replace("article/", "CSS ") for a in anchors))
        text(80,y+79," · ".join(articles),20,"#42586b")
parts.append('</svg>')
destination = ROOT / "assets/moreau-proof.svg"
destination.write_text("\n".join(parts)+"\n")
print(destination)
