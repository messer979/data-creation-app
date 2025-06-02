#!/usr/bin/env python3
"""
Simple test to verify generation template processing
"""

try:
    from template_generator import TemplateGenerator
    from data_generator import DataGenerator
    import json
    
    print("=== Generation Template Test ===")
    
    # Initialize generators
    template_gen = TemplateGenerator()
    data_gen = DataGenerator()
    
    # Check available templates
    templates = template_gen.get_available_templates()
    print(f"Available generation templates: {templates}")
    
    # Test item generation
    if 'item' in templates and 'item' in data_gen.templates:
        base_template = data_gen.templates['item']
        generation_template = template_gen.get_template_info('item')
        
        print(f"\nBase template ItemId: {base_template.get('ItemId', 'Not found')}")
        print(f"Generation template sections: {list(generation_template.keys())}")
        
        # Generate 2 records
        records = template_gen.generate_records('item', 2, base_template)
        print(f"\nGenerated {len(records)} records")
        
        if len(records) >= 2:
            record1, record2 = records[0], records[1]
            
            print(f"\nRecord 1:")
            print(f"  ItemId: {record1.get('ItemId', 'Not found')}")
            print(f"  Style: {record1.get('Style', 'Not found')}")
            print(f"  Volume: {record1.get('Volume', 'Not found')}")
            print(f"  PrimaryBarCode: {record1.get('PrimaryBarCode', 'Not found')}")
            
            print(f"\nRecord 2:")
            print(f"  ItemId: {record2.get('ItemId', 'Not found')}")
            print(f"  Style: {record2.get('Style', 'Not found')}")
            print(f"  Volume: {record2.get('Volume', 'Not found')}")
            print(f"  PrimaryBarCode: {record2.get('PrimaryBarCode', 'Not found')}")
            
            # Verify functionality
            print(f"\n=== Verification ===")
            print(f"Dynamic fields working: {record1.get('ItemId') != record2.get('ItemId')}")
            print(f"Static fields working: {record1.get('Style') == record2.get('Style')}")
            print(f"Random fields present: {'Volume' in record1}")
            print(f"Linked fields present: {'PrimaryBarCode' in record1}")
            
            if all([
                record1.get('ItemId') != record2.get('ItemId'),  # Dynamic
                record1.get('Style') == record2.get('Style'),   # Static
                'Volume' in record1,                             # Random
                'PrimaryBarCode' in record1                      # Linked
            ]):
                print("\n✅ SUCCESS: Generation template processing is working correctly!")
            else:
                print("\n❌ ISSUES: Some generation template features are not working properly")
        else:
            print("❌ FAIL: Could not generate enough records for testing")
    else:
        print("❌ FAIL: Item template not available for testing")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
