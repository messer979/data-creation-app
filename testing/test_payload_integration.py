#!/usr/bin/env python3
"""
Integration test for payload wrapping with actual configuration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_generator import DataGenerator
from config_manager import ConfigurationManager

def test_integration():
    """Test payload wrapping integration with ConfigurationManager"""
    
    print("🔧 Testing Payload Wrapping Integration")
    print("=" * 50)
    
    # Create instances
    data_gen = DataGenerator()
    config_manager = ConfigurationManager()
    
    # Sample data
    test_data = [
        {"ItemId": "TEST001", "Description": "Test Item"}
    ]
    
    # Test with different templates from configuration.json
    templates_to_test = ['facility', 'item', 'vendor', 'ilpn']
    
    for template_name in templates_to_test:
        print(f"\n📋 Testing template: {template_name}")
        
        # Get configuration for this template
        config = config_manager.get_template_config(template_name)
        
        print(f"   Configuration: type={config.get('type')}, dataWrapper={config.get('dataWrapper')}")
        
        # Test payload wrapping
        wrapped_payload = data_gen._wrap_payload(test_data, config)
        
        print(f"   Original data: {test_data}")
        print(f"   Wrapped payload: {wrapped_payload}")
        
        # Verify expected wrapping based on configuration
        payload_type = config.get('type')
        data_wrapper = config.get('dataWrapper', False)
        
        if payload_type == 'xint' and data_wrapper:
            expected = {"Payload": {"data": test_data}}
            assert wrapped_payload == expected, f"Expected xint+dataWrapper format for {template_name}"
            print(f"   ✅ Correctly wrapped as xint+dataWrapper: {{'Payload': {{'data': [records]}}}}")
        elif payload_type == 'xint':
            expected = {"Payload": test_data}
            assert wrapped_payload == expected, f"Expected xint format for {template_name}"
            print(f"   ✅ Correctly wrapped as xint: {{'Payload': [records]}}")
        elif data_wrapper:
            expected = {"data": test_data}
            assert wrapped_payload == expected, f"Expected dataWrapper format for {template_name}"
            print(f"   ✅ Correctly wrapped as dataWrapper: {{'data': [records]}}")
        else:
            assert wrapped_payload == test_data, f"Expected no wrapping for {template_name}"
            print(f"   ✅ No wrapping applied: [records]")
    
    print(f"\n✅ All integration tests passed!")
    print(f"\nConfiguration-based wrapping is working correctly!")


if __name__ == "__main__":
    test_integration()
