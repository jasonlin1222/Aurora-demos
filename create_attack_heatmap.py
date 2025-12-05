#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from mitreattack.stix20 import MitreAttackData


def get_technique_info(technique_id, mitre_attack_data):
    """Get technique name and tactics from MITRE ATT&CK ID."""
    try:
        technique = mitre_attack_data.get_object_by_attack_id(
            technique_id, "attack-pattern"
        )
        if technique:
            tactics = []
            if hasattr(technique, "kill_chain_phases"):
                tactics = [
                    phase.phase_name.replace("-", " ").title()
                    for phase in technique.kill_chain_phases
                ]
            return technique.name, tactics
        return technique_id, []
    except:
        return technique_id, []


def load_required_techniques():
    """Load required techniques from EDR gaps CSV files (extracted from Excel sheets)."""
    techniques_by_category = {
        "well_covered": set(),
        "moderately_covered": set(), 
        "poorly_covered": set()
    }
    
    # Map CSV files to categories
    csv_files = {
        "well_covered": "well_covered.csv",
        "moderately_covered": "moderately_covered.csv",
        "poorly_covered": "poorly_covered.csv"
    }
    
    try:
        for category, csv_file in csv_files.items():
            df = pd.read_csv(csv_file)
            for column in df.columns:
                for technique in df[column].dropna():
                    if technique.strip():
                        techniques_by_category[category].add(technique.strip())
        
        # Combine all techniques for backward compatibility
        all_techniques = set()
        for category_set in techniques_by_category.values():
            all_techniques.update(category_set)
            
        return all_techniques, techniques_by_category
    except Exception as e:
        print(f"Error loading required techniques: {e}")
        return set(), {"well_covered": set(), "moderately_covered": set(), "poorly_covered": set()}


def calculate_coverage_stats(technique_counts, required_techniques, expected_categories):
    """Calculate coverage statistics comparing expected categories vs actual detection status."""
    
    def get_technique_count(technique, technique_counts):
        """Get count for a technique, including sub-techniques."""
        # Check for exact match first
        if technique in technique_counts:
            return technique_counts[technique]
        else:
            # Check for sub-techniques (e.g., T1059.001, T1059.003 for T1059)
            count = 0
            for detected_technique in technique_counts:
                if detected_technique.startswith(technique + "."):
                    count += technique_counts[detected_technique]
            return count
    
    # Get expected categories from CSV files
    expected_well = expected_categories["well_covered"]
    expected_mod = expected_categories["moderately_covered"] 
    expected_poor = expected_categories["poorly_covered"]
    
    all_required = set()
    for category_set in expected_categories.values():
        all_required.update(category_set)
    
    # Calculate actual detection status for each technique
    detected_techniques = set()
    missing_techniques = set()
    technique_detection_counts = {}
    
    for technique in all_required:
        count = get_technique_count(technique, technique_counts)
        technique_detection_counts[technique] = count
        if count > 0:
            detected_techniques.add(technique)
        else:
            missing_techniques.add(technique)
    
    # Calculate coverage match accuracy
    well_covered_detected = len(expected_well & detected_techniques)
    well_covered_missing = len(expected_well & missing_techniques)
    
    mod_covered_detected = len(expected_mod & detected_techniques)
    mod_covered_missing = len(expected_mod & missing_techniques)
    
    poor_covered_detected = len(expected_poor & detected_techniques)
    poor_covered_missing = len(expected_poor & missing_techniques)
    
    # Calculate overall detection rates
    total_expected_well = len(expected_well)
    total_expected_mod = len(expected_mod)
    total_expected_poor = len(expected_poor)
    
    return {
        "total_required": len(all_required),
        "total_detected": len(detected_techniques),
        "total_missing": len(missing_techniques),
        "expected_well_covered": total_expected_well,
        "expected_moderately_covered": total_expected_mod,
        "expected_poorly_covered": total_expected_poor,
        "well_covered_detected": well_covered_detected,
        "well_covered_missing": well_covered_missing,
        "mod_covered_detected": mod_covered_detected,
        "mod_covered_missing": mod_covered_missing,
        "poor_covered_detected": poor_covered_detected,
        "poor_covered_missing": poor_covered_missing,
        "detected_techniques": detected_techniques,
        "missing_techniques": missing_techniques,
        "expected_categories": expected_categories,
        "technique_detection_counts": technique_detection_counts
    }


def main():
    # Load MITRE ATT&CK data
    print("Loading MITRE ATT&CK data...")
    mitre_attack_data = MitreAttackData("enterprise-attack.json")

    # Load required techniques from EDR gaps files
    print("Loading required techniques from EDR gaps CSV files...")
    required_techniques, expected_categories = load_required_techniques()
    print(f"Found {len(required_techniques)} total required techniques")
    print(f"  Expected well covered: {len(expected_categories['well_covered'])}")
    print(f"  Expected moderately covered: {len(expected_categories['moderately_covered'])}")
    print(f"  Expected poorly covered: {len(expected_categories['poorly_covered'])}")

    # Load CSV data
    df = pd.read_csv("attack_chains_analysis.csv")

    # Extract all techniques
    all_techniques = []
    for ids_sequence in df["ids_sequence"]:
        if ids_sequence != "No IDs found":
            techniques = [t.strip() for t in ids_sequence.split(",")]
            all_techniques.extend(techniques)

    # Count technique frequencies
    technique_counts = Counter(all_techniques)

    # Group techniques by tactics
    tactics_techniques = {}
    print("\nAll covered attack techniques grouped by tactics:")
    print("=" * 60)

    for technique_id in sorted(technique_counts.keys()):
        technique_name, tactics = get_technique_info(technique_id, mitre_attack_data)

        if not tactics:
            tactics = ["Other"]

        for tactic in tactics:
            if tactic not in tactics_techniques:
                tactics_techniques[tactic] = []
            tactics_techniques[tactic].append(
                {
                    "id": technique_id,
                    "name": technique_name,
                    "count": technique_counts[technique_id],
                }
            )

    # Print grouped techniques
    for tactic in sorted(tactics_techniques.keys()):
        print(f"\n{tactic.upper()}:")
        print("-" * len(tactic))
        for tech in sorted(
            tactics_techniques[tactic], key=lambda x: x["count"], reverse=True
        ):
            print(f"  {tech['id']}: {tech['name']} (used {tech['count']} times)")

    # Get all techniques sorted by frequency
    all_techniques_sorted = technique_counts.most_common()
    techniques, counts = zip(*all_techniques_sorted)

    # Get technique names for visualization
    technique_labels = []
    for tech_id in techniques:
        name, tactics = get_technique_info(tech_id, mitre_attack_data)
        # Truncate long names for display
        if len(name) > 30:
            name = name[:27] + "..."
        technique_labels.append(f"{tech_id}\n{name}")

    # Create visualization - Full heatmap
    plt.figure(figsize=(20, 12))

    # Create a bar chart that looks like a heatmap
    colors = plt.cm.YlOrRd([count / max(counts) for count in counts])
    bars = plt.bar(range(len(techniques)), counts, color=colors)

    # Add labels
    plt.title(
        "MITRE ATT&CK Technique Frequency Heatmap", fontsize=16, fontweight="bold"
    )
    plt.xlabel("Techniques", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(
        range(len(techniques)), technique_labels, rotation=90, ha="right", fontsize=6
    )

    # Add value labels on bars
    for i, bar in enumerate(bars):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            str(counts[i]),
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    plt.tight_layout()
    plt.savefig("attack_heatmap.png", dpi=300, bbox_inches="tight")
    plt.show()

    # Create Top 10 visualization
    plt.figure(figsize=(15, 10))

    # Get top 10 techniques
    top_10_techniques = all_techniques_sorted[:10]
    top_10_ids, top_10_counts = zip(*top_10_techniques)

    # Get technique names for top 10
    top_10_labels = []
    for tech_id in top_10_ids:
        name, tactics = get_technique_info(tech_id, mitre_attack_data)
        if len(name) > 25:
            name = name[:22] + "..."
        top_10_labels.append(f"{tech_id}\n{name}")

    # Create horizontal bar chart for top 10
    colors_top10 = plt.cm.Reds([count / max(top_10_counts) for count in top_10_counts])
    bars = plt.barh(range(len(top_10_ids)), top_10_counts, color=colors_top10)

    # Customize the plot
    plt.title(
        "Top 10 Most Frequent MITRE ATT&CK Techniques", fontsize=16, fontweight="bold"
    )
    plt.xlabel("Frequency", fontsize=12)
    plt.ylabel("Techniques", fontsize=12)
    plt.yticks(range(len(top_10_ids)), top_10_labels, fontsize=8)

    # Add value labels on bars
    for i, bar in enumerate(bars):
        plt.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            str(top_10_counts[i]),
            ha="left",
            va="center",
            fontweight="bold",
            fontsize=9,
        )

    # Invert y-axis to show highest frequency at top
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("top_10_attack_techniques.png", dpi=300, bbox_inches="tight")
    plt.show()

    # Calculate coverage statistics
    coverage_stats = calculate_coverage_stats(technique_counts, required_techniques, expected_categories)
    
    # Print gap analysis
    print(f"\n{'='*80}")
    print(f"EDR COVERAGE ANALYSIS - EXPECTED vs ACTUAL DETECTION")
    print(f"{'='*80}")
    
    print(f"\nOverall Statistics:")
    print(f"Total required techniques: {coverage_stats['total_required']}")
    print(f"Total detected techniques: {coverage_stats['total_detected']}")
    print(f"Total missing techniques: {coverage_stats['total_missing']}")
    
    # Calculate percentages
    total_req = coverage_stats['total_required']
    if total_req > 0:
        detected_pct = (coverage_stats['total_detected'] / total_req) * 100
        missing_pct = (coverage_stats['total_missing'] / total_req) * 100
        
        print(f"\nOverall Detection Rate: {coverage_stats['total_detected']}/{total_req} ({detected_pct:.1f}%)")
        print(f"Overall Missing Rate: {coverage_stats['total_missing']}/{total_req} ({missing_pct:.1f}%)")
        
        print(f"\nEXPECTED Coverage Categories (from EDR gaps assessment):")
        expected_well_pct = (coverage_stats['expected_well_covered'] / total_req) * 100
        expected_mod_pct = (coverage_stats['expected_moderately_covered'] / total_req) * 100  
        expected_poor_pct = (coverage_stats['expected_poorly_covered'] / total_req) * 100
        print(f"• Expected well covered:              {coverage_stats['expected_well_covered']:2d} techniques ({expected_well_pct:5.1f}%)")
        print(f"• Expected moderately covered:        {coverage_stats['expected_moderately_covered']:2d} techniques ({expected_mod_pct:5.1f}%)")
        print(f"• Expected poorly covered:            {coverage_stats['expected_poorly_covered']:2d} techniques ({expected_poor_pct:5.1f}%)")
        
        print(f"\nDETECTION SUCCESS by Expected Category:")
        well_success_pct = (coverage_stats['well_covered_detected'] / coverage_stats['expected_well_covered']) * 100 if coverage_stats['expected_well_covered'] > 0 else 0
        mod_success_pct = (coverage_stats['mod_covered_detected'] / coverage_stats['expected_moderately_covered']) * 100 if coverage_stats['expected_moderately_covered'] > 0 else 0
        poor_success_pct = (coverage_stats['poor_covered_detected'] / coverage_stats['expected_poorly_covered']) * 100 if coverage_stats['expected_poorly_covered'] > 0 else 0
        
        print(f"• Well covered techniques detected:   {coverage_stats['well_covered_detected']}/{coverage_stats['expected_well_covered']} ({well_success_pct:5.1f}%)")
        print(f"• Moderately covered techniques detected: {coverage_stats['mod_covered_detected']}/{coverage_stats['expected_moderately_covered']} ({mod_success_pct:5.1f}%)")
        print(f"• Poorly covered techniques detected: {coverage_stats['poor_covered_detected']}/{coverage_stats['expected_poorly_covered']} ({poor_success_pct:5.1f}%)")
    
    # Show missing techniques by expected category
    if coverage_stats['missing_techniques']:
        print(f"\nMISSING TECHNIQUES by Expected Coverage Category:")
        print("-" * 60)
        
        expected_well = expected_categories["well_covered"]
        expected_mod = expected_categories["moderately_covered"]
        expected_poor = expected_categories["poorly_covered"]
        missing = coverage_stats['missing_techniques']
        
        well_missing = expected_well & missing
        mod_missing = expected_mod & missing
        poor_missing = expected_poor & missing
        
        if well_missing:
            print(f"\nExpected WELL COVERED but MISSING ({len(well_missing)} techniques):")
            for technique in sorted(well_missing):
                name, tactics = get_technique_info(technique, mitre_attack_data)
                tactic_str = ", ".join(tactics) if tactics else "Unknown"
                print(f"• {technique}: {name} [{tactic_str}]")
        
        if mod_missing:
            print(f"\nExpected MODERATELY COVERED but MISSING ({len(mod_missing)} techniques):")
            for technique in sorted(mod_missing):
                name, tactics = get_technique_info(technique, mitre_attack_data)
                tactic_str = ", ".join(tactics) if tactics else "Unknown"
                print(f"• {technique}: {name} [{tactic_str}]")
        
        if poor_missing:
            print(f"\nExpected POORLY COVERED but MISSING ({len(poor_missing)} techniques):")
            for technique in sorted(poor_missing):
                name, tactics = get_technique_info(technique, mitre_attack_data)
                tactic_str = ", ".join(tactics) if tactics else "Unknown"
                print(f"• {technique}: {name} [{tactic_str}]")

    # Print summary
    print(f"\n{'='*80}")
    print(f"DETECTION SUMMARY")
    print(f"{'='*80}")
    print(f"Total unique techniques detected: {len(technique_counts)}")
    print(f"Total technique occurrences: {sum(technique_counts.values())}")

    print(f"\nTop 10 most frequent techniques:")
    for i, (technique, count) in enumerate(all_techniques_sorted[:10], 1):
        name, tactics = get_technique_info(technique, mitre_attack_data)
        tactic_str = ", ".join(tactics) if tactics else "Other"
        print(f"{i}. {technique}: {name} [{tactic_str}] ({count} times)")


if __name__ == "__main__":
    main()
