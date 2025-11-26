#!/usr/bin/env python3

import os
import yaml
from pathlib import Path

def normalize_name(name):
    """Normalize attribute name for comparison (lowercase, stripped)."""
    return str(name).strip().lower()

def main():
    print("🔍 S4A Dictionary - Missing Attributes Analysis")
    print("━" * 60)
    
    project_root = Path(__file__).parent.parent
    
    # 1. Load existing attributes
    existing_attributes = set()
    attributes_dir = project_root / 'data/attributes'
    if attributes_dir.exists():
        for yaml_file in attributes_dir.glob('*.yaml'):
            with open(yaml_file, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                    if data and 'name' in data:
                        existing_attributes.add(normalize_name(data['name']))
                except Exception as e:
                    print(f"Error reading {yaml_file}: {e}")

    print(f"✅ Found {len(existing_attributes)} existing attributes definitions.")

    # 2. Scan for used attributes
    used_attributes = {} # name -> list of usage locations

    # Scan Objects
    objects_dir = project_root / 'data/objects'
    if objects_dir.exists():
        for yaml_file in objects_dir.glob('*.yaml'):
            with open(yaml_file, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                    if not data: continue
                    
                    obj_name = data.get('Name', yaml_file.stem)
                    
                    # Core Attributes
                    if 'CoreAttributes' in data and data['CoreAttributes']:
                        for attr in data['CoreAttributes']:
                            if 'Name' in attr:
                                name = normalize_name(attr['Name'])
                                if name not in used_attributes: used_attributes[name] = []
                                used_attributes[name].append(f"Object: {obj_name}")

                    # System Perspectives
                    if 'SystemPerspectives' in data and data['SystemPerspectives']:
                        for persp_id, persp_data in data['SystemPerspectives'].items():
                            if 'RelevantAttributes' in persp_data and persp_data['RelevantAttributes']:
                                for attr in persp_data['RelevantAttributes']:
                                    if 'Name' in attr:
                                        name = normalize_name(attr['Name'])
                                        if name not in used_attributes: used_attributes[name] = []
                                        used_attributes[name].append(f"Perspective: {persp_id}")

                except Exception as e:
                    print(f"Error reading object {yaml_file}: {e}")

    # Scan Views
    views_dir = project_root / 'data/views'
    if views_dir.exists():
        for yaml_file in views_dir.glob('*.yaml'):
            with open(yaml_file, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                    if not data: continue
                    
                    view_title = data.get('Title', yaml_file.stem)
                    
                    if 'IncludedAttributes' in data and data['IncludedAttributes']:
                        for attr in data['IncludedAttributes']:
                            name = ""
                            if isinstance(attr, dict):
                                name = attr.get('Name', '')
                            else:
                                name = str(attr)
                            
                            if name:
                                norm_name = normalize_name(name)
                                if norm_name not in used_attributes: used_attributes[norm_name] = []
                                used_attributes[norm_name].append(f"View: {view_title}")

                except Exception as e:
                    print(f"Error reading view {yaml_file}: {e}")

    # 3. Compare and Report
    missing_count = 0
    print("\n❌ Missing Attributes (Used but not defined in data/attributes/):")
    print("━" * 60)
    
    sorted_missing = sorted([name for name in used_attributes.keys() if name not in existing_attributes])
    
    for name in sorted_missing:
        missing_count += 1
        locations = used_attributes[name]
        # Limit locations display
        loc_str = ", ".join(locations[:3])
        if len(locations) > 3:
            loc_str += f" (+{len(locations)-3} more)"
            
        print(f"• {name.title()} (Used in: {loc_str})")

    print("━" * 60)
    print(f"Total missing attributes: {missing_count}")

if __name__ == "__main__":
    main()
