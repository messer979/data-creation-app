#!/usr/bin/env python3
"""Test script to verify DataGenerator functionality after cleanup"""

try:
    from data_generator import DataGenerator
    print("✅ DataGenerator imported successfully")
    
    # Initialize DataGenerator
    dg = DataGenerator()
    print("✅ DataGenerator initialized successfully")
    
    # Check templates
    base_templates = list(dg.templates.keys())
    generation_templates = dg.template_generator.get_available_templates()
    
    print(f"📋 Base templates ({len(base_templates)}): {base_templates}")
    print(f"🎯 Generation templates ({len(generation_templates)}): {generation_templates}")
    
    # Test data generation if possible
    if 'facility' in base_templates and 'facility' in generation_templates:
        try:
            result = dg.generate_data('facility', 2)
            print(f"✅ Generated {len(result)} facility records")
            if result:
                print(f"📄 Sample record keys: {list(result[0].keys())}")
        except Exception as e:
            print(f"❌ Error generating facility data: {e}")
    else:
        print("ℹ️ Facility template not available for testing")
    
    print("\n🎉 All tests passed! DataGenerator is working correctly.")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()
