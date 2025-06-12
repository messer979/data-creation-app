#!/usr/bin/env python3
"""
Test script to verify Bearer token handling in ConfigurationManager
"""

import sys
import os
import json

# Add the components directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'components'))

from config_manager import ConfigurationManager

def test_bearer_token_handling():
    """Test that tokens are properly handled with and without Bearer prefix"""
    
    print("🧪 Testing Bearer token handling...")
    
    # Create a temporary config file for testing
    test_config = {
        "description": "Test configuration",
        "version": "1.0",
        "base_url": "https://test.example.com",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer TEST_TOKEN",
            "SelectedOrganization": "TEST_ORG",
            "SelectedLocation": "TEST_LOC"
        },
        "endpoints": {
            "test_endpoint": {
                "endpoint": "/test",
                "method": "POST",
                "description": "Test endpoint"
            }
        }
    }
    
    # Write test config
    with open('test_config.json', 'w') as f:
        json.dump(test_config, f)
    
    try:
        # Initialize config manager with test config
        config_manager = ConfigurationManager('test_config.json')
        
        # Test 1: Token with Bearer prefix
        print("Test 1: Setting token with Bearer prefix")
        config_manager.set_shared_token("Bearer ALREADY_HAS_BEARER")
        token = config_manager.get_shared_token()
        assert token == "Bearer ALREADY_HAS_BEARER", f"Expected 'Bearer ALREADY_HAS_BEARER', got '{token}'"
        print("✅ Token with Bearer prefix handled correctly")
        
        # Test 2: Token without Bearer prefix
        print("Test 2: Setting token without Bearer prefix")
        config_manager.set_shared_token("RAW_TOKEN_NO_BEARER")
        token = config_manager.get_shared_token()
        assert token == "Bearer RAW_TOKEN_NO_BEARER", f"Expected 'Bearer RAW_TOKEN_NO_BEARER', got '{token}'"
        print("✅ Token without Bearer prefix handled correctly")
        
        # Test 3: Import configuration with Bearer token
        print("Test 3: Importing configuration with Bearer token")
        import_config = {
            "base_url": "https://imported.example.com",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer IMPORTED_TOKEN",
                "SelectedOrganization": "IMPORTED_ORG",
                "SelectedLocation": "IMPORTED_LOC"
            },
            "endpoints": {}
        }
        
        success = config_manager._import_full_config(import_config)
        assert success, "Import should succeed"
        assert config_manager.get_shared_token() == "Bearer IMPORTED_TOKEN"
        assert config_manager.get_selected_organization() == "IMPORTED_ORG"
        assert config_manager.get_selected_location() == "IMPORTED_LOC"
        assert config_manager.get_base_url() == "https://imported.example.com"
        print("✅ Import with Bearer token handled correctly")
        
        # Test 4: Import configuration without Bearer token
        print("Test 4: Importing configuration without Bearer token")
        import_config_no_bearer = {
            "base_url": "https://nobearertest.example.com",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "RAW_IMPORTED_TOKEN",
                "SelectedOrganization": "NO_BEARER_ORG",
                "SelectedLocation": "NO_BEARER_LOC"
            },
            "endpoints": {}
        }
        
        success = config_manager._import_full_config(import_config_no_bearer)
        assert success, "Import should succeed"
        # The token should now have Bearer prefix added
        token = config_manager.get_shared_token()
        assert token == "Bearer RAW_IMPORTED_TOKEN", f"Expected 'Bearer RAW_IMPORTED_TOKEN', got '{token}'"
        print("✅ Import without Bearer token handled correctly")
        
        # Test 5: Export preserves correct structure
        print("Test 5: Testing export structure")
        exported = config_manager.export_full_config()
        exported_data = json.loads(exported)
        
        assert "base_url" in exported_data
        assert "headers" in exported_data
        assert "endpoints" in exported_data
        assert exported_data["headers"]["Authorization"] == "Bearer RAW_IMPORTED_TOKEN"
        assert exported_data["headers"]["Content-Type"] == "application/json"
        print("✅ Export structure is correct")
        
        print("\n🎉 All Bearer token handling tests passed!")
        
    finally:
        # Clean up test file
        if os.path.exists('test_config.json'):
            os.remove('test_config.json')

if __name__ == "__main__":
    test_bearer_token_handling()
