#!/usr/bin/env python3
"""
End-to-end test to verify payload wrapping works through the complete flow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_generator import DataGenerator
from config_manager import ConfigurationManager

def test_end_to_end_payload_wrapping():
    """Test the complete flow from data generation to API payload wrapping"""
    print("🧪 Testing End-to-End Payload Wrapping...")
    
    # Initialize components
    data_gen = DataGenerator()
    config_manager = ConfigurationManager()
    
    # Test data (simulating generated records)
    test_data = [
        {"id": 1, "name": "Test Item 1"},
        {"id": 2, "name": "Test Item 2"}
    ]
    
    # Test different template configurations
    test_configs = [
        {
            "name": "No wrapping",
            "config": {},
            "expected_structure": "list"
        },
        {
            "name": "dataWrapper only",
            "config": {"dataWrapper": True},
            "expected_structure": "data_wrapper"
        },
        {
            "name": "xint type only", 
            "config": {"type": "xint"},
            "expected_structure": "payload_wrapper"
        },
        {
            "name": "Both xint and dataWrapper",
            "config": {"type": "xint", "dataWrapper": True},
            "expected_structure": "both_wrappers"
        }
    ]
    
    print("\n" + "="*60)
    for test_config in test_configs:
        print(f"\n📋 Testing: {test_config['name']}")
        print(f"Config: {test_config['config']}")
        
        # Use the _wrap_payload method directly
        wrapped_payload = data_gen._wrap_payload(test_data, test_config['config'])
        
        print(f"Result: {wrapped_payload}")
        
        # Validate structure
        if test_config['expected_structure'] == 'list':
            assert isinstance(wrapped_payload, list), "Expected list structure"
            assert wrapped_payload == test_data, "Expected original data"
            
        elif test_config['expected_structure'] == 'data_wrapper':
            assert isinstance(wrapped_payload, dict), "Expected dict structure"
            assert 'data' in wrapped_payload, "Expected 'data' key"
            assert wrapped_payload['data'] == test_data, "Expected data in 'data' key"
            
        elif test_config['expected_structure'] == 'payload_wrapper':
            assert isinstance(wrapped_payload, dict), "Expected dict structure"
            assert 'Payload' in wrapped_payload, "Expected 'Payload' key"
            assert wrapped_payload['Payload'] == test_data, "Expected data in 'Payload' key"
            
        elif test_config['expected_structure'] == 'both_wrappers':
            assert isinstance(wrapped_payload, dict), "Expected dict structure"
            assert 'Payload' in wrapped_payload, "Expected 'Payload' key"
            assert isinstance(wrapped_payload['Payload'], dict), "Expected nested dict"
            assert 'data' in wrapped_payload['Payload'], "Expected 'data' key in Payload"
            assert wrapped_payload['Payload']['data'] == test_data, "Expected data in nested structure"
        
        print("✅ Test passed!")
    
    print("\n" + "="*60)
    print("🎉 All end-to-end payload wrapping tests passed!")

if __name__ == "__main__":
    test_end_to_end_payload_wrapping()
