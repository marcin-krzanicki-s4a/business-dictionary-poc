#!/usr/bin/env python3

import os
import yaml
from pathlib import Path

def main():
    print("🎨 S4A Dictionary - Populating Attributes with Sample Data")
    print("━" * 60)
    
    project_root = Path(__file__).parent.parent
    attributes_dir = project_root / 'data/attributes'
    
    # Define rules for populating data based on attribute name keywords
    # Priority: Exact match > Keyword match
    
    rules = {
        # Exact matches
        'iata-designator': {
            'dataType': 'String',
            'format': '^[A-Z0-9]{2}$',
            'minLength': 2,
            'maxLength': 2,
            'example': 'LH',
            'description': 'Two-character alphanumeric code assigned by IATA to the airline.'
        },
        'icao-indicator': {
            'dataType': 'String',
            'format': '^[A-Z]{3}$',
            'minLength': 3,
            'maxLength': 3,
            'example': 'DLH',
            'description': 'Three-letter code assigned by ICAO to the airline.'
        },
        'airport-code-iata': {
            'dataType': 'String',
            'format': '^[A-Z]{3}$',
            'minLength': 3,
            'maxLength': 3,
            'example': 'LHR',
            'description': 'Three-letter IATA airport code.'
        },
        'flight-status': {
            'dataType': 'Enum',
            'values': [
                {'label': 'Scheduled', 'description': 'Flight is planned.'},
                {'label': 'Active', 'description': 'Flight is currently in the air.'},
                {'label': 'Landed', 'description': 'Flight has arrived.'},
                {'label': 'Cancelled', 'description': 'Flight has been cancelled.'},
                {'label': 'Delayed', 'description': 'Flight is delayed.'}
            ],
            'example': 'Active',
            'description': 'Current operational status of the flight.'
        },
        'operating-status': {
            'dataType': 'Enum',
            'values': [
                {'label': 'Normal', 'description': 'Operating normally.'},
                {'label': 'Closed', 'description': 'Temporarily closed.'},
                {'label': 'Restricted', 'description': 'Operating with restrictions.'}
            ],
            'example': 'Normal'
        },
        'ticketnumber': {
            'dataType': 'String',
            'format': '^[0-9]{13}$',
            'minLength': 13,
            'maxLength': 13,
            'example': '1762345678901',
            'description': '13-digit unique ticket number.'
        },
        'ticket-number': { # Duplicate handling
            'dataType': 'String',
            'format': '^[0-9]{13}$',
            'minLength': 13,
            'maxLength': 13,
            'example': '1762345678901',
            'description': '13-digit unique ticket number.'
        },
        'qnh': {
            'dataType': 'Integer',
            'unit': 'hPa',
            'minValue': 900,
            'maxValue': 1100,
            'example': 1013,
            'description': 'Atmospheric pressure adjusted to sea level.'
        },
        'notams': {
            'dataType': 'String',
            'maxLength': 1000,
            'example': 'RWY 27 CLSD DUE WX',
            'description': 'Notice to Airmen - important flight information.'
        },
        'delays': {
            'dataType': 'Integer',
            'unit': 'minutes',
            'minValue': 0,
            'example': 45,
            'description': 'Flight delay duration in minutes.'
        },
        'flight-aircraft-tailnumber': {
            'dataType': 'String',
            'format': '^[A-Z0-9-]{5,10}$',
            'minLength': 5,
            'maxLength': 10,
            'example': 'N12345',
            'description': 'Aircraft registration/tail number.'
        },
        'active-runway-configuration': {
            'dataType': 'String',
            'format': '^[0-9]{2}[LCR]?$',
            'minLength': 2,
            'maxLength': 3,
            'example': '27L',
            'description': 'Active runway designation (e.g., 27L for left runway).'
        },
        'nearest-lounge': {
            'dataType': 'String',
            'maxLength': 100,
            'example': 'Platinum Lounge - Terminal A',
            'description': 'Name/location of the nearest passenger lounge.'
        },
        'flight-route': {
            'dataType': 'String',
            'maxLength': 500,
            'example': 'JFK-LAX-SFO',
            'description': 'Flight route as sequence of airport codes.'
        },
        'hvac-status': {
            'dataType': 'Enum',
            'values': [
                {'label': 'Normal', 'description': 'HVAC operating normally.'},
                {'label': 'Maintenance', 'description': 'HVAC under maintenance.'},
                {'label': 'Fault', 'description': 'HVAC system fault.'}
            ],
            'example': 'Normal',
            'description': 'Heating, ventilation, and air conditioning status.'
        },
        'current-weather': {
            'dataType': 'String',
            'maxLength': 200,
            'example': 'Clear skies, 22°C, wind 5kt from 270°',
            'description': 'Current weather conditions summary.'
        },
        'arrival-airport': {
            'dataType': 'String',
            'format': '^[A-Z]{3}$',
            'minLength': 3,
            'maxLength': 3,
            'example': 'LAX',
            'description': 'IATA code of the arrival airport.'
        },
        'crewmanifest': {
            'dataType': 'String',
            'maxLength': 1000,
            'example': 'Captain: John Smith, First Officer: Jane Doe, Flight Attendants: 4',
            'description': 'List of crew members assigned to the flight.'
        },
        'departure-airport': {
            'dataType': 'String',
            'format': '^[A-Z]{3}$',
            'minLength': 3,
            'maxLength': 3,
            'example': 'JFK',
            'description': 'IATA code of the departure airport.'
        },
        
        # Keyword matches (checked if no exact match)
        'keywords': [
            {
                'keys': ['time', 'date', 'schedule'],
                'data': {
                    'dataType': 'DateTime',
                    'format': 'ISO 8601',
                    'example': '2023-10-25T14:30:00Z',
                    'description': 'Timestamp in UTC.'
                }
            },
            {
                'keys': ['count', 'passengers', 'seats'],
                'data': {
                    'dataType': 'Integer',
                    'minValue': 0,
                    'example': 150
                }
            },
            {
                'keys': ['weight', 'load'],
                'data': {
                    'dataType': 'Decimal',
                    'unit': 'kg',
                    'precision': 2,
                    'minValue': 0.0,
                    'example': 23.5
                }
            },
            {
                'keys': ['distance', 'range', 'length'],
                'data': {
                    'dataType': 'Decimal',
                    'unit': 'km',
                    'precision': 1,
                    'minValue': 0.0,
                    'example': 1500.0
                }
            },
            {
                'keys': ['temperature'],
                'data': {
                    'dataType': 'Decimal',
                    'unit': 'Celsius',
                    'precision': 1,
                    'example': 21.5
                }
            },
            {
                'keys': ['speed', 'velocity'],
                'data': {
                    'dataType': 'Integer',
                    'unit': 'knots',
                    'minValue': 0,
                    'example': 450
                }
            },
            {
                'keys': ['price', 'cost', 'fare'],
                'data': {
                    'dataType': 'Decimal',
                    'unit': 'USD',
                    'precision': 2,
                    'minValue': 0.0,
                    'example': 199.99
                }
            },
            {
                'keys': ['id', 'code'],
                'data': {
                    'dataType': 'String',
                    'minLength': 1,
                    'maxLength': 50,
                    'example': 'ID-12345'
                }
            },
            {
                'keys': ['name', 'surname'],
                'data': {
                    'dataType': 'String',
                    'minLength': 1,
                    'maxLength': 100,
                    'example': 'John Doe'
                }
            },
            {
                'keys': ['description', 'note', 'comment'],
                'data': {
                    'dataType': 'String',
                    'maxLength': 500,
                    'example': 'Sample text description.'
                }
            },
            {
                'keys': ['percent', 'progress', 'rate'],
                'data': {
                    'dataType': 'Decimal',
                    'unit': '%',
                    'minValue': 0,
                    'maxValue': 100,
                    'example': 75.5
                }
            }
        ]
    }

    updated_count = 0
    
    for yaml_file in attributes_dir.glob('*.yaml'):
        with open(yaml_file, 'r') as f:
            try:
                data = yaml.safe_load(f)
            except:
                continue
        
        if not data: continue
        
        # Only update files marked as Auto-generated or Draft with minimal info
        if data.get('source') != 'Auto-generated':
            continue
            
        name_key = yaml_file.stem.lower()
        original_name = data.get('name', '')
        
        new_data = data.copy()
        new_data['status'] = 'active' # Promote to active since we are adding data
        new_data['source'] = 'Inferred'
        
        # Apply rules
        applied = False
        
        # 1. Exact Match
        if name_key in rules:
            new_data.update(rules[name_key])
            applied = True
        else:
            # 2. Keyword Match
            for rule in rules['keywords']:
                if any(k in name_key for k in rule['keys']):
                    new_data.update(rule['data'])
                    applied = True
                    break
        
        if applied:
            # Preserve ID and Name if they were overwritten (though update() shouldn't overwrite if not in rule)
            new_data['id'] = data['id']
            new_data['name'] = original_name
            
            with open(yaml_file, 'w') as f:
                yaml.dump(new_data, f, sort_keys=False)
            
            print(f"✅ Updated {yaml_file.name}")
            updated_count += 1
        else:
            print(f"⚠️  No rule matched for {yaml_file.name}, skipping update.")

    print("━" * 60)
    print(f"🎉 Updated {updated_count} attribute files with sample data.")

if __name__ == "__main__":
    main()
