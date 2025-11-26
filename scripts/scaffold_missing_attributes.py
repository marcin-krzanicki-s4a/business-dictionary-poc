#!/usr/bin/env python3

import os
import yaml
from pathlib import Path
import re

def normalize_name(name):
    return str(name).strip().lower()

def to_kebab_case(name):
    name = str(name).strip().lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)
    return name.strip('-')

def main():
    print("🛠️  S4A Dictionary - Scaffolding Missing Attributes")
    print("━" * 60)
    
    project_root = Path(__file__).parent.parent
    attributes_dir = project_root / 'data/attributes'
    attributes_dir.mkdir(exist_ok=True)

    # 1. Load existing attributes
    existing_attributes = set()
    existing_ids = set()
    
    for yaml_file in attributes_dir.glob('*.yaml'):
        with open(yaml_file, 'r') as f:
            try:
                data = yaml.safe_load(f)
                if data:
                    if 'name' in data:
                        existing_attributes.add(normalize_name(data['name']))
                    if 'id' in data:
                        existing_ids.add(data['id'])
            except:
                pass

    # 2. Scan for used attributes
    used_attributes = set()

    # Scan Objects
    objects_dir = project_root / 'data/objects'
    if objects_dir.exists():
        for yaml_file in objects_dir.glob('*.yaml'):
            with open(yaml_file, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                    if not data: continue
                    
                    if 'CoreAttributes' in data and data['CoreAttributes']:
                        for attr in data['CoreAttributes']:
                            if 'Name' in attr: used_attributes.add(attr['Name'])

                    if 'SystemPerspectives' in data and data['SystemPerspectives']:
                        for persp_data in data['SystemPerspectives'].values():
                            if 'RelevantAttributes' in persp_data and persp_data['RelevantAttributes']:
                                for attr in persp_data['RelevantAttributes']:
                                    if 'Name' in attr: used_attributes.add(attr['Name'])
                except: pass

    # Scan Views
    views_dir = project_root / 'data/views'
    if views_dir.exists():
        for yaml_file in views_dir.glob('*.yaml'):
            with open(yaml_file, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                    if not data: continue
                    
                    if 'IncludedAttributes' in data and data['IncludedAttributes']:
                        for attr in data['IncludedAttributes']:
                            if isinstance(attr, dict): used_attributes.add(attr.get('Name', ''))
                            else: used_attributes.add(str(attr))
                except: pass

    # 3. Create missing files
    created_count = 0
    next_id_num = 100 # Start generating IDs from 100 to avoid conflicts
    
    for name in sorted(used_attributes):
        if not name: continue
        
        norm_name = normalize_name(name)
        if norm_name in existing_attributes:
            continue
            
        # Generate unique ID
        while f"ATTR-{next_id_num:03d}" in existing_ids:
            next_id_num += 1
        new_id = f"ATTR-{next_id_num:03d}"
        existing_ids.add(new_id)
        
        # Create YAML content
        file_name = to_kebab_case(name) + ".yaml"
        file_path = attributes_dir / file_name
        
        data = {
            'id': new_id,
            'name': name, # Keep original casing
            'description': f"Attribute representing {name}.",
            'dataType': 'String', # Default
            'source': 'Auto-generated',
            'status': 'draft'
        }
        
        with open(file_path, 'w') as f:
            yaml.dump(data, f, sort_keys=False)
            
        print(f"✅ Created {file_name} ({new_id})")
        created_count += 1

    print("━" * 60)
    print(f"🎉 Created {created_count} new attribute files.")

if __name__ == "__main__":
    main()
