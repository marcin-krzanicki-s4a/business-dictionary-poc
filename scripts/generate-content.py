#!/usr/bin/env python3

"""
S4A Business Dictionary - Content Generator
Automatically generates Hugo content files (.md) from YAML data files
Usage: python3 scripts/generate-content.py
"""

import os
import yaml
import sys
from pathlib import Path

def main():
    print("🚀 S4A Dictionary Content Generator")
    print("━" * 80)
    
    # Get project root (parent of scripts directory)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    os.chdir(project_root)
    
    counters = {
        'objects': 0,
        'views': 0,
        'perspectives': 0,
        'attributes': 0
    }
    
    # Generate Attribute content files
    print("\n🏷️  Generating Attribute content files...")
    print("━" * 80)
    
    attributes_dir = Path('data/attributes')
    content_attributes_dir = Path('content/attributes')
    content_attributes_dir.mkdir(parents=True, exist_ok=True)
    
    # Simulation Data - Aviation Domain Logic
    def get_origin_data(attr_name_lower):
        # Weather Data
        if any(x in attr_name_lower for x in ['weather', 'temp', 'wind', 'visibility', 'qnh', 'rvr']):
            return {
                'system': 'Met Office API',
                'type': 'External',
                'entity': 'METAR/TAF Service',
                'refresh': 'Hourly'
            }
        
        # Passenger / Ticket Data
        if any(x in attr_name_lower for x in ['passenger', 'ticket', 'surname', 'name', 'seat', 'bag', 'loyalty']):
            return {
                'system': 'Amadeus DCS',
                'type': 'External',
                'entity': 'PNR_Record',
                'refresh': 'Real-time'
            }
            
        # Flight Operations
        if any(x in attr_name_lower for x in ['flight', 'route', 'aircraft', 'tail', 'fuel', 'crew']):
            return {
                'system': 'AODB (Airport Ops DB)',
                'type': 'Internal',
                'entity': 'FLIGHT_OPS_DAILY',
                'refresh': 'Real-time'
            }
            
        # Infrastructure / Airport
        if any(x in attr_name_lower for x in ['runway', 'gate', 'belt', 'stand', 'terminal', 'lounge']):
            return {
                'system': 'Airport BMS / Tower',
                'type': 'Internal',
                'entity': 'INFRA_STATUS_REALTIME',
                'refresh': 'Real-time'
            }
            
        # Financial
        if any(x in attr_name_lower for x in ['price', 'fare', 'cost', 'revenue']):
            return {
                'system': 'SAP ERP',
                'type': 'Internal',
                'entity': 'FI_CO_PA',
                'refresh': 'Daily'
            }

        # Default / Fallback
        return {
            'system': 'Data Lake',
            'type': 'Internal',
            'entity': 'RAW_INGESTION_LAYER',
            'refresh': 'Daily'
        }

    for yaml_file in attributes_dir.glob('*.yaml'):
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        
        attr_id = data.get('id', '')
        attr_name = data.get('name', yaml_file.stem)
        attr_type = data.get('dataType', 'String')
        attr_desc = data.get('description', '').replace('"', '\\"')
        
        # Simulate Data Origin based on Name
        origin = get_origin_data(attr_name.lower())
        
        content_file = content_attributes_dir / f"{yaml_file.stem}.md"
        
        with open(content_file, 'w') as f:
            f.write(f"""---
title: "{attr_name}"
id: "{attr_id}"
dataType: "{attr_type}"
description: "{attr_desc}"
sourceSystem: "{origin['system']}"
sourceType: "{origin['type']}"
sourceEntity: "{origin['entity']}"
refreshRate: "{origin['refresh']}"
---
""")
        
        print(f"  ✅ Generated: {content_file} (from {yaml_file.name})")
        counters['attributes'] += 1

    # Generate Object content files
    print("\n📦 Generating Object content files...")
    print("━" * 80)
    
    objects_dir = Path('data/objects')
    content_objects_dir = Path('content/objects')
    content_objects_dir.mkdir(parents=True, exist_ok=True)
    
    for yaml_file in objects_dir.glob('*.yaml'):
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        
        object_id = yaml_file.stem
        object_slug = object_id.lower()
        object_name = data.get('Name', object_id)
        
        content_file = content_objects_dir / f"{object_slug}.md"
        
        with open(content_file, 'w') as f:
            f.write(f"""---
title: "{object_name}"
description: "Definition of the {object_name} business object."
---
""")
        
        print(f"  ✅ Generated: {content_file} (from {object_id}.yaml)")
        counters['objects'] += 1
    
    # Generate View content files
    print("\n🖼️  Generating View content files...")
    print("━" * 80)
    
    views_dir = Path('data/views')
    content_views_dir = Path('content/views')
    content_views_dir.mkdir(parents=True, exist_ok=True)
    
    for yaml_file in views_dir.glob('*.yaml'):
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        
        view_id = yaml_file.stem
        view_description = data.get('Description', '')
        
        # Create title from view ID (e.g., AirlineOperations_DashboardView -> Airline Operations Dashboard View)
        view_title = view_id.replace('_', ' ')
        
        content_file = content_views_dir / f"{view_id}.md"
        
        with open(content_file, 'w') as f:
            f.write(f"""---
title: "{view_title}"
description: "{view_description}"
---
""")
        
        print(f"  ✅ Generated: {content_file} (from {view_id}.yaml)")
        counters['views'] += 1
    
    # Generate Perspective content files
    print("\n🔍 Generating Perspective content files...")
    print("━" * 80)
    
    content_perspectives_dir = Path('content/perspectives')
    content_perspectives_dir.mkdir(parents=True, exist_ok=True)
    
    for yaml_file in objects_dir.glob('*.yaml'):
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        
        object_id = yaml_file.stem
        object_slug = object_id.lower()
        
        system_perspectives = data.get('SystemPerspectives', {})
        
        for perspective_name in system_perspectives.keys():
            # Create slug for perspective (e.g., "Route Management" -> "route-management")
            perspective_slug = perspective_name.lower().replace(' ', '-')
            
            # Create filename (e.g., "airline-route-management.md")
            filename = f"{object_slug}-{perspective_slug}.md"
            
            content_file = content_perspectives_dir / filename
            
            with open(content_file, 'w') as f:
                f.write(f"""---
title: "{perspective_name}"
object_id: "{object_id}"
perspective_id: "{perspective_name}"
---
""")
            
            print(f"  ✅ Generated: {content_file} ({object_id} -> {perspective_name})")
            counters['perspectives'] += 1
    
    # Summary
    print("\n" + "━" * 80)
    print("✨ Content generation complete!")
    print("\n📊 Summary:")
    print(f"   • Objects:      {counters['objects']} files generated")
    print(f"   • Views:        {counters['views']} files generated")
    print(f"   • Perspectives: {counters['perspectives']} files generated")
    print(f"   • Attributes:   {counters['attributes']} files generated")
    print(f"   • Total:        {sum(counters.values())} files")
    print("\n💡 Next steps:")
    print("   1. Review generated files in content/ directories")
    print("   2. Run 'hugo server' to preview changes")
    print("   3. Run 'hugo build' to build the site")
    print()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
