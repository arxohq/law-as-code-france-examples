#!/usr/bin/env python3
"""Case structure and serial native checks with an explicitly selected binary.
--draft-check never evaluates law and does not qualify an engine result.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile
import tomllib
P=Path(__file__).resolve().parent

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--law',required=True,type=Path)
    a.add_argument('--draft-check',action='store_true')
    args=a.parse_args()
    if not args.law.is_file():raise ValueError('Provide the saved engine binary')
    m=tomllib.loads((P/'law.toml').read_text())
    plan=json.loads((P/'queries/plan.json').read_text())
    names={c['name'] for c in m['cases']}
    if names!={r['case'] for r in plan}:raise ValueError('Case/query coverage differs')
    for c in m['cases']:
        source=(P/c['path']).read_text()
        if f"case {c['name']} {{" not in source:raise ValueError('Case name differs')
        if not re.search(r'origin case_input;',source):raise ValueError('Missing facts')
    suites='\n'.join((P/f).read_text() for t in m['tests'] for f in t['suites'])
    for row in plan:
        q=json.loads((P/'queries'/row['file']).read_text())
        if q['queryId'] not in suites and q['kind']=='truth':raise ValueError('Missing test twin')
    if args.draft_check:
        print(f"DRAFT ONLY: {len(names)} fictional cases; native execution not checked")
        return 0
    with tempfile.TemporaryDirectory(prefix='cnaf-case-') as tmp:
        for i,row in enumerate(plan):
            out=Path(tmp)/str(i)
            proc=subprocess.run([str(args.law.resolve()),'ask',str(P),'--case',row['case'],'--query-json',str(P/'queries'/row['file']),'--out',str(out)],capture_output=True,text=True)
            if proc.returncode:raise RuntimeError(proc.stderr[-1500:]+proc.stdout[-1500:])
            result=json.loads((out/'result.json').read_text())
            answers=result.get('results',[])
            if any(r.get('evaluationStatus')!='COMPUTED' for r in answers) or any(x.get('severity')=='error' for x in result.get('issues',[])):raise RuntimeError('Native refusal; exit zero does not qualify the answer')
            if row.get('truth') and (len(answers)!=1 or answers[0].get('truthStatus')!=row['truth']):raise RuntimeError('Proposed expectation does not match')
        proc=subprocess.run([str(args.law.resolve()),'test',str(P),'--json'],capture_output=True,text=True)
        if proc.returncode:raise RuntimeError(proc.stderr[-1500:]+proc.stdout[-1500:])
    print('Native checks passed; compare proof and source anchors before promotion')
    return 0
if __name__=='__main__':raise SystemExit(main())
