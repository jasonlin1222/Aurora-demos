#!/usr/bin/env python3

import pandas as pd
from collections import Counter

# Load attack chains data
df = pd.read_csv('attack_chains_analysis.csv')

# Extract all techniques
all_techniques = []
for ids_sequence in df['ids_sequence']:
    if ids_sequence != 'No IDs found':
        techniques = [t.strip() for t in ids_sequence.split(',')]
        all_techniques.extend(techniques)

# Count technique frequencies
technique_counts = Counter(all_techniques)

# Load required techniques
required_df = pd.read_csv('EDR_gaps_technique_IDs.csv')
required_techniques = set()
for column in required_df.columns:
    for technique in required_df[column].dropna():
        if technique.strip():
            required_techniques.add(technique.strip())

print(f'Total required techniques: {len(required_techniques)}')
print(f'Total detected techniques: {len(technique_counts)}')

# Calculate coverage manually
well_covered = set()
moderately_covered = set()
poorly_covered = set()

for technique in required_techniques:
    if technique in technique_counts:
        count = technique_counts[technique]
        if count >= 5:
            well_covered.add(technique)
        elif count >= 2:
            moderately_covered.add(technique)
        else:
            poorly_covered.add(technique)

missing = required_techniques - set(technique_counts.keys())

total_req = len(required_techniques)
well_pct = (len(well_covered) / total_req) * 100 if total_req > 0 else 0
mod_pct = (len(moderately_covered) / total_req) * 100 if total_req > 0 else 0
poor_pct = (len(poorly_covered) / total_req) * 100 if total_req > 0 else 0
missing_pct = (len(missing) / total_req) * 100 if total_req > 0 else 0

print(f'Well covered: {len(well_covered)} ({well_pct:.1f}%)')
print(f'Moderately covered: {len(moderately_covered)} ({mod_pct:.1f}%)')
print(f'Poorly covered: {len(poorly_covered)} ({poor_pct:.1f}%)')
print(f'Missing: {len(missing)} ({missing_pct:.1f}%)')
print(f'Total percentages: {well_pct + mod_pct + poor_pct + missing_pct:.1f}%')

# Show what's in each category
print(f'\nRequired techniques with coverage:')
for technique in sorted(required_techniques):
    if technique in technique_counts:
        count = technique_counts[technique]
        print(f'{technique}: {count} times')
    else:
        print(f'{technique}: missing')