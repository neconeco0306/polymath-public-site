#!/usr/bin/env python3
"""Exploratory KIC 10797460 light-curve period search (not an exoplanet validator).

Usage: python period_search.py path/to/10797460.csv > period_search_output.json
Public third-party source: https://github.com/buildwithanuragpandey/stelsion-dataset
Verify immutable Git blob identity before working; SHA1 is a content identifier, not a source-authenticity guarantee.
"""
from __future__ import annotations
import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from statistics import median

SOURCE_BLOB = 'f7185dd055fc7993469bb788816be6f592751a38'


def git_sha1(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def load(path: Path):
    data = path.read_bytes()
    if git_sha1(data) != SOURCE_BLOB:
        raise ValueError('source Git blob SHA1 mismatch; refuse silently changed data')
    rows = []
    reader = csv.reader(data.decode('utf-8-sig').splitlines())
    if next(reader) != ['time', 'flux']:
        raise ValueError('unexpected CSV header')
    for parts in reader:
        if len(parts) != 2:
            continue
        t, y = map(float, parts)
        if math.isfinite(t) and math.isfinite(y) and y > 0:
            rows.append((t, y))
    return rows


def detrend(rows):
    start = rows[0][0]
    bins = defaultdict(list)
    for t, y in rows:
        bins[math.floor((t - start) / 2)].append(y)
    centers = {key: median(v) for key, v in bins.items()}
    return [(t, (y / centers[math.floor((t-start)/2)]-1)*1e6)
            for t, y in rows if abs((y / centers[math.floor((t-start)/2)]-1)*1e6) < 4000]


def fold(period: float, rows, origin: float, bins: int=120):
    sums = [0.0]*bins
    counts = [0]*bins
    for t, ppm in rows:
        f = (t - origin) / period
        b = math.floor((f - math.floor(f)) * bins)
        sums[b] += ppm
        counts[b] += 1
    return sums, counts


def evaluate(period, rows, origin, chosen=None, bins=120):
    sums, counts = fold(period, rows, origin, bins)
    def bin_depth(i):
        j = (i+1) % bins
        n = counts[i] + counts[j]
        return (-((sums[i]+sums[j])/n) if n else float('nan'), n)
    if chosen is not None:
        depth, n = bin_depth(chosen)
        return {'period': period, 'bin': chosen, 'depth_ppm': depth, 'n': n}
    best = {'period': period, 'bin': -1, 'depth_ppm': float('-inf'), 'n': 0}
    for i in range(bins):
        depth, n = bin_depth(i)
        if n >= 160 and depth > best['depth_ppm']:
            best = {'period': period, 'bin': i, 'depth_ppm': depth, 'n': n}
    return best


def grid(start, stop, step, rows, origin):
    count = round((stop - start)/step)
    return sorted((evaluate(start+i*step, rows, origin) for i in range(count+1)),
                  key=lambda z: z['depth_ppm'], reverse=True)


def main(path: Path):
    rows = load(path)
    origin = rows[0][0]
    halfway = (origin + rows[-1][0])/2
    clean = detrend(rows)
    first = [r for r in clean if r[0] < halfway]
    last = [r for r in clean if r[0] >= halfway]
    coarse = grid(3, 20, .02, first, origin)
    refined = []
    for x in coarse[:12]:
        refined += grid(max(3,x['period']-.06), min(20,x['period']+.06), .001, first, origin)
    refined.sort(key=lambda z: z['depth_ppm'],reverse=True)
    distinct=[]
    for candidate in refined:
        if all(abs(candidate['period']-other['period']) > .08 for other in distinct):
            distinct.append(candidate)
        if len(distinct) >= 10:break
    # Harmonic selection is POST HOC. It was performed after looking at an early holdout result.
    # This exercise is therefore not a preregistered blind/confirmatory search.
    harmonic = grid(9.425, 9.525, .0002, first, origin)[0]
    control_periods = [9.4, 9.45, 9.47, 9.488015, 9.5, 9.52, 9.6, 10.2, 18.973, harmonic['period']]
    controls = []
    for p in control_periods:
        a = evaluate(p, first, origin)
        b = evaluate(p, last, origin, chosen=a['bin'])
        controls.append({'period':p, 'train':a,'holdout_at_train_phase':b})
    return {'source_blob':SOURCE_BLOB,'total_rows':len(rows),'retained_rows':len(clean),
            'train_rows':len(first),'holdout_rows':len(last),'method':'local 2-day median, |ppm| <4000; 120 phase bins; 2-bin box minimum',
            'first_coarse':coarse[:12], 'refined_distinct':distinct,
            'harmonic_selected_posthoc':harmonic,
            'heldout_at_training_phase':evaluate(harmonic['period'],last,origin,chosen=harmonic['bin']),
            'controls':controls,
            'classification':'EXPLORATORY; NOT INDEPENDENT; NOT NEW PLANET'}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python period_search.py 10797460.csv')
    print(json.dumps(main(Path(sys.argv[1])),indent=2,ensure_ascii=False))
