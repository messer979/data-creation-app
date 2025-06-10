#!/usr/bin/env python3
"""
Test the integration between UI configuration and payload wrapping
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.config_manager import ConfigurationManager
from data_creation.data_generator import DataGenerator
import json

def test_ui_config_integration():
    """Test that UI configuration changes properly affect payload wrapping"""
    
    print("🧪 Testing UI configuration integration with payload wrapping...")
    
    # Initialize configuration manager
    config_manager = ConfigurationManager()
    
    # Test data
    test_records = [
        {"id": 1, "name": "Test Item 1"},
        {"id": 2, "name": "Test Item 2"}
    ]
    
    # Test different configuration scenarios
    test_scenarios = [
        {
            "name": "None/False - Raw array",
            "config": {"endpoint": "/test", "type": None, "dataWrapper": False},
            "expected": test_records
        },
        {
            "name": "None/True - Data wrapper only",
            "config": {"endpoint": "/test", "type": None, "dataWrapper": True},
            "expected": {"data": test_records}
        },
        {
            "name": "xint/False - Payload wrapper only",
            "config": {"endpoint": "/test", "type": "xint", "dataWrapper": False},
            "expected": {"Payload": test_records}
        },
        {
            "name": "xint/True - Both wrappers",
            "config": {"endpoint": "/test", "type": "xint", "dataWrapper": True},
            "expected": {"Payload": {"data": test_records}}
        }
    ]
    
    # Create data generator
    data_generator = DataGenerator()
    
    for scenario in test_scenarios:
        print(f"\n📋 Testing: {scenario['name']}")
        
        # Update template configuration
        config_manager.update_template_config("test_template", scenario["config"])
        
        # Get the updated configuration
        template_config = config_manager.get_template_config("test_template")
        
        # Test payload wrapping
        wrapped_payload = data_generator._wrap_payload(test_records, template_config)
        
        # Verify result
        expected = scenario["expected"]
        if wrapped_payload == expected:
            print(f"   ✅ PASS: Got expected result")
            print(f"      Expected: {json.dumps(expected, indent=2)}")
        else:
            print(f"   ❌ FAIL: Result doesn't match expected")
            print(f"      Expected: {json.dumps(expected, indent=2)}")
            print(f"      Got:      {json.dumps(wrapped_payload, indent=2)}")
            return False
    
    print(f"\n🎉 All UI configuration integration tests passed!")
    return True

def test_config_persistence():
    """Test that configuration changes persist in session"""
    
    print("\n🧪 Testing configuration persistence...")
    
    # Initialize configuration manager
    config_manager = ConfigurationManager()
    
    # Set a custom configuration
    test_config = {
        "endpoint": "/custom/endpoint",
        "type": "xint",
        "dataWrapper": True,
        "description": "Custom test configuration"
    }
    
    # Update and save
    config_manager.update_template_config("persistence_test", test_config)
    
    # Retrieve the configuration
    retrieved_config = config_manager.get_template_config("persistence_test")
    
    # Verify all fields are present
    for key, value in test_config.items():
        if retrieved_config.get(key) != value:
            print(f"   ❌ FAIL: {key} not persisted correctly")
            print(f"      Expected: {value}")
            print(f"      Got:      {retrieved_config.get(key)}")
            return False
    
    print(f"   ✅ PASS: Configuration persisted correctly")
    return True

if __name__ == "__main__":
    success = True
    
    try:
        success &= test_ui_config_integration()
        success &= test_config_persistence()
        
        if success:
            print(f"\n🎉 All tests passed! UI configuration integration is working correctly.")
        else:
            print(f"\n❌ Some tests failed!")
            
    except Exception as e:
        print(f"\n💥 Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        success = False
    
    exit(0 if success else 1)
