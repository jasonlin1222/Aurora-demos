#!/usr/bin/env python3

import os
import yaml
import csv
from pathlib import Path

def extract_attack_chain_ids(yaml_file_path):
    """Extract attack IDs from a YAML attack chain file."""
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        
        ids = []
        attack_sequence = data.get('attack_action_sequence', [])
        
        for action in attack_sequence:
            action_ids = action.get('id', [])
            if action_ids:
                if isinstance(action_ids, list):
                    # Filter out None values and convert to strings
                    valid_ids = [str(id_val) for id_val in action_ids if id_val is not None]
                    ids.extend(valid_ids)
                elif action_ids is not None:
                    ids.append(str(action_ids))
        
        return ids
    except Exception as e:
        print(f"Error processing {yaml_file_path}: {e}")
        return []

def main():
    attacks_dir = Path("attacks")
    results = []
    
    if not attacks_dir.exists():
        print("Error: 'attacks' directory not found")
        return
    
    # Get all subdirectories in attacks folder
    attack_folders = [d for d in attacks_dir.iterdir() if d.is_dir()]
    attack_folders.sort()
    
    for attack_folder in attack_folders:
        attack_chain_file = attack_folder / "attack_chain.yml"
        
        if attack_chain_file.exists():
            folder_name = attack_folder.name
            ids = extract_attack_chain_ids(attack_chain_file)
            ids_sequence = ", ".join(ids) if ids else "No IDs found"
            
            results.append({
                'attack_folder': folder_name,
                'ids_sequence': ids_sequence
            })
            print(f"Processed: {folder_name} - {len(ids)} IDs found")
        else:
            print(f"Warning: No attack_chain.yml found in {attack_folder}")
    
    # Write results to CSV
    csv_filename = "attack_chains_analysis.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['attack_folder', 'ids_sequence']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\nAnalysis complete! Results saved to {csv_filename}")
    print(f"Total attack chains processed: {len(results)}")

if __name__ == "__main__":
    main()