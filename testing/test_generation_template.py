#!/usr/bin/env python3
"""
Test script to verify generation template processing functionality
"""

import json
import os
from template_generator import TemplateGenerator
from data_generator import DataGenerator

def test_generation_template_processing():
    """Test if generation templates are processed correctly"""
    print("=== Testing Generation Template Processing ===\n")
    
    # Initialize template generator
    template_gen = TemplateGenerator()
    
    # Test 1: Check if generation templates are loaded
    print("1. Testing generation template loading...")
    available_templates = template_gen.get_available_templates()
    print(f"   Available generation templates: {available_templates}")
    
    if not available_templates:
        print("   ❌ FAIL: No generation templates loaded")
        return False
    else:
        print(f"   ✅ SUCCESS: Loaded {len(available_templates)} generation templates")
    
    # Test 2: Check template info retrieval
    print("\n2. Testing template info retrieval...")
    for template_name in available_templates[:2]:  # Test first 2 templates
        template_info = template_gen.get_template_info(template_name)
        if template_info:
            print(f"   ✅ {template_name}: {list(template_info.keys())}")
        else:
            print(f"   ❌ {template_name}: Failed to retrieve template info")
    
    # Test 3: Test data generation with a simple template
    print("\n3. Testing data generation...")
    try:
        # Load data generator to get base templates
        data_gen = DataGenerator()
        
        # Test with item template if available
        if 'item' in available_templates and 'item' in data_gen.templates:
            print("   Testing item template generation...")
            
            base_template = data_gen.templates['item']
            generation_template = template_gen.get_template_info('item')
            
            print(f"   Base template keys: {list(base_template.keys())[:5]}...")
            print(f"   Generation template sections: {list(generation_template.keys())}")
            
            # Generate 2 test records
            records = template_gen.generate_records('item', 2, base_template)
            
            if records and len(records) == 2:
                print(f"   ✅ SUCCESS: Generated {len(records)} records")
                
                # Check first record for expected changes
                record1 = records[0]
                record2 = records[1]
                
                # Check dynamic fields (should be different)
                if 'ItemId' in record1 and 'ItemId' in record2:
                    if record1['ItemId'] != record2['ItemId']:
                        print(f"   ✅ Dynamic fields working: {record1['ItemId']} vs {record2['ItemId']}")
                    else:
                        print(f"   ❌ Dynamic fields not working: {record1['ItemId']} == {record2['ItemId']}")
                
                # Check static fields (should be same)
                if 'Style' in record1 and 'Style' in record2:
                    if record1['Style'] == record2['Style']:
                        print(f"   ✅ Static fields working: {record1['Style']}")
                    else:
                        print(f"   ❌ Static fields not working: {record1['Style']} != {record2['Style']}")
                
                # Check random fields (should exist)
                if 'Volume' in record1:
                    print(f"   ✅ Random fields working: Volume = {record1['Volume']}")
                else:
                    print(f"   ❌ Random fields not working: Volume not found")
                
                # Check linked fields
                if 'PrimaryBarCode' in record1:
                    print(f"   ✅ Linked fields working: PrimaryBarCode = {record1['PrimaryBarCode']}")
                else:
                    print(f"   ❌ Linked fields not working: PrimaryBarCode not found")
                
                return True
            else:
                print(f"   ❌ FAIL: Expected 2 records, got {len(records) if records else 0}")
                return False
                
    except Exception as e:
        print(f"   ❌ FAIL: Exception during generation: {e}")
        return False

if __name__ == "__main__":
    success = test_generation_template_processing()
    if success:
        print("\n🎉 Generation template processing is working correctly!")
    else:
        print("\n💥 Generation template processing has issues!")
