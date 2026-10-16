#!/usr/bin/env python3
"""Exploratory challenge control; a false-positive folder label is NOT an authoritative NASA classification.

Usage: python control_scan.py path/to/10419211.csv > control_out.json
Compares binned periodic dips; this score is not a planet probability.
"""
from __future__ import annotations
import csv
import json
import math
import sys
from pathlib import Path
from period_search import detrend, evaluate, grid, git_sha1

EXPECTED_BLOB='5d8e5679f873faf79e21643f71f21d3cce2ffd94'

def load_data(path: Path):
    raw=path.read_bytes()
    if git_sha1(raw)!=EXPECTED_BLOB:
        raise ValueError('Git blob mismatch: refuse altered control CSV')
    rd=csv.reader(raw.decode('utf-8-sig').splitlines())
    if next(rd)!=['time','flux']:
        raise ValueError('unexpected header')
    out=[]
    for row in rd:
        if len(row)!=2:continue
        t,y=map(float,row)
        if math.isfinite(t) and math.isfinite(y) and y>0:out.append((t,y))
    return out

def run(rows):
    origin=rows[0][0]
    cleaned=detrend(rows)
    cutoff=(origin+rows[-1][0])/2
    train=[r for r in cleaned if r[0]<cutoff]
    heldout=[r for r in cleaned if r[0]>=cutoff]
    coarse=grid(3,20,.02,train,origin)
    refined=[]
    for entry in coarse[:10]:
        p=entry['period']
        refined.extend(grid(max(3,p-.04),min(20,p+.04),.001,train,origin))
    refined.sort(key=lambda v:v['depth_ppm'],reverse=True)
    independent=[]
    for row in refined:
        if all(abs(row['period']-a['period'])>.08 for a in independent):
            independent.append(row)
        if len(independent)>=8:break
    return {'status':'EXPLORATORY / NOT A PLANET CLASSIFIER','origin':origin,
            'raw_rows':len(rows),'retained_rows':len(cleaned),
            'train_rows':len(train),'holdout_rows':len(heldout),
            'coarse':coarse[:10],
            'refined':[{**a,'heldout':evaluate(a['period'],heldout,origin,a['bin'])} for a in independent],
            'source_blob_sha1':EXPECTED_BLOB,
            'interpretation':'A recurring brightness dip does not independently establish an exoplanet.'}

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: python control_scan.py 10419211.csv')
    print(json.dumps(run(load_data(Path(sys.argv[1]))),indent=2,ensure_ascii=False))
