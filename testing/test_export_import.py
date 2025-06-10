#!/usr/bin/env python3
"""
Test the export and import configuration functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.config_manager import ConfigurationManager
import json

def test_export_import_functionality():
    """Test that export and import works for both global and endpoint configurations"""
    
    print("🧪 Testing export/import configuration functionality...")
    
    # Initialize configuration manager
    config_manager = ConfigurationManager()
    
    # Test 1: Check what's currently being exported
    print("\n📋 Testing current export functionality...")
    
    # Get current exported config
    exported_config = config_manager.export_user_config()
    print(f"Current export result: {exported_config}")
    
    # Parse the exported config
    try:
        parsed_config = json.loads(exported_config)
        print(f"✅ Export produces valid JSON")
        print(f"📊 Exported {len(parsed_config)} configurations")
        
        # Show what's included
        for key in parsed_config.keys():
            print(f"   • {key}")
            
    except json.JSONDecodeError:
        print(f"❌ Export does not produce valid JSON!")
        return False
    
    # Test 2: Check if global config is included
    print(f"\n🌐 Checking if global configuration is included...")
    
    # Check for global settings
    current_base_url = config_manager.get_base_url()
    current_token = config_manager.get_shared_token()
    current_org = config_manager.get_selected_organization()
    current_facility = config_manager.get_selected_facility()
    
    print(f"Current global settings:")
    print(f"   • Base URL: {current_base_url}")
    print(f"   • Token: {current_token[:20]}..." if len(current_token) > 20 else f"   • Token: {current_token}")
    print(f"   • Organization: {current_org}")
    print(f"   • Facility: {current_facility}")
    
    # Check if these are in the exported config
    has_global_config = any(key in ['base_url', 'shared_token', 'selected_organization', 'selected_facility', 'global_settings'] 
                           for key in parsed_config.keys())
    
    if has_global_config:
        print(f"✅ Global configuration appears to be included in export")
    else:
        print(f"⚠️  Global configuration does NOT appear to be included in export")
        print(f"    Export only contains endpoint configurations")
    
    # Test 3: Test import functionality
    print(f"\n📥 Testing import functionality...")
    
    # Create a test configuration to import
    test_import_config = {
        "test_template": {
            "endpoint": "/test/import",
            "type": "xint",
            "dataWrapper": True,
            "description": "Test import configuration"
        }
    }
    
    # Import the test config
    import_success = config_manager.import_user_config(json.dumps(test_import_config))
    
    if import_success:
        print(f"✅ Import functionality works")
        
        # Verify the imported config
        imported_template_config = config_manager.get_template_config("test_template")
        if imported_template_config.get('endpoint') == "/test/import":
            print(f"✅ Imported configuration is accessible")
        else:
            print(f"❌ Imported configuration not found or incorrect")
            return False
    else:
        print(f"❌ Import functionality failed")
        return False
    
    # Test 4: Test round-trip (export then import)
    print(f"\n🔄 Testing round-trip (export then import)...")
    
    # Add some endpoint config
    config_manager.update_template_config("roundtrip_test", {
        "endpoint": "/roundtrip/test",
        "type": "none",
        "dataWrapper": False,
        "description": "Round trip test"
    })
    
    # Export
    exported_round_trip = config_manager.export_user_config()
    
    # Clear and import back
    config_manager.clear_all_user_config()
    import_round_trip_success = config_manager.import_user_config(exported_round_trip)
    
    if import_round_trip_success:
        # Check if the round trip config is back
        round_trip_config = config_manager.get_template_config("roundtrip_test")
        if round_trip_config.get('endpoint') == "/roundtrip/test":
            print(f"✅ Round-trip export/import works for endpoint configurations")
        else:
            print(f"❌ Round-trip failed for endpoint configurations")
            return False
    else:
        print(f"❌ Round-trip import failed")
        return False
    
    # Summary
    print(f"\n📋 Export/Import Analysis:")
    print(f"   ✅ Export produces valid JSON")
    print(f"   ✅ Import functionality works")
    print(f"   ✅ Round-trip works for endpoint configurations")
    
    if has_global_config:
        print(f"   ✅ Global configuration included in export")
    else:
        print(f"   ⚠️  Global configuration NOT included in export")
        print(f"       (only endpoint configurations are exported)")
    
    return True

def test_enhanced_export_import():
    """Test the new enhanced export/import functionality"""
    
    print(f"\n🔧 Testing enhanced export/import functionality...")
    
    config_manager = ConfigurationManager()
    
    # Set up some test configuration
    config_manager.set_base_url("https://test.example.com")
    config_manager.set_shared_token("test-token-12345")
    config_manager.set_selected_organization("TEST-ORG")
    config_manager.set_selected_facility("TEST-FAC")
    
    # Add some endpoint configuration
    config_manager.update_template_config("test_enhanced", {
        "endpoint": "/enhanced/test",
        "type": "xint",
        "dataWrapper": True,
        "description": "Enhanced test configuration"
    })
    
    # Test full export
    print(f"\n📦 Testing full configuration export...")
    full_export = config_manager.export_full_config()
    
    try:
        full_config = json.loads(full_export)
        print(f"✅ Full export produces valid JSON")
        
        # Check structure
        required_keys = ["version", "global_settings", "endpoint_configurations"]
        missing_keys = [key for key in required_keys if key not in full_config]
        
        if missing_keys:
            print(f"❌ Missing required keys in full export: {missing_keys}")
            return False
        
        print(f"✅ Full export has all required sections")
        
        # Check global settings
        global_settings = full_config["global_settings"]
        if (global_settings.get("base_url") == "https://test.example.com" and
            "test-token-12345" in global_settings.get("shared_token", "") and
            global_settings.get("selected_organization") == "TEST-ORG" and
            global_settings.get("selected_facility") == "TEST-FAC"):
            print(f"✅ Global settings exported correctly")
        else:
            print(f"❌ Global settings not exported correctly")
            print(f"   Expected base_url: https://test.example.com")
            print(f"   Got: {global_settings.get('base_url')}")
            return False
        
        # Check endpoint configurations
        endpoint_configs = full_config["endpoint_configurations"]
        if "test_enhanced" in endpoint_configs:
            test_config = endpoint_configs["test_enhanced"]
            if (test_config.get("endpoint") == "/enhanced/test" and
                test_config.get("type") == "xint" and
                test_config.get("dataWrapper") == True):
                print(f"✅ Endpoint configurations exported correctly")
            else:
                print(f"❌ Endpoint configurations not exported correctly")
                return False
        else:
            print(f"❌ Test endpoint configuration not found in export")
            return False
            
    except json.JSONDecodeError:
        print(f"❌ Full export does not produce valid JSON!")
        return False
    
    # Test full import
    print(f"\n📥 Testing full configuration import...")
    
    # Clear configuration
    config_manager.clear_all_user_config()
    
    # Import the full configuration
    import_success = config_manager.import_full_config(full_export)
    
    if import_success:
        print(f"✅ Full import completed successfully")
        
        # Verify global settings were imported
        if (config_manager.get_base_url() == "https://test.example.com" and
            "test-token-12345" in config_manager.get_shared_token() and
            config_manager.get_selected_organization() == "TEST-ORG" and
            config_manager.get_selected_facility() == "TEST-FAC"):
            print(f"✅ Global settings imported correctly")
        else:
            print(f"❌ Global settings not imported correctly")
            print(f"   Base URL: {config_manager.get_base_url()}")
            print(f"   Token: {config_manager.get_shared_token()}")
            print(f"   Org: {config_manager.get_selected_organization()}")
            print(f"   Facility: {config_manager.get_selected_facility()}")
            return False
        
        # Verify endpoint configuration was imported
        imported_config = config_manager.get_template_config("test_enhanced")
        if (imported_config.get("endpoint") == "/enhanced/test" and
            imported_config.get("type") == "xint" and
            imported_config.get("dataWrapper") == True):
            print(f"✅ Endpoint configuration imported correctly")
        else:
            print(f"❌ Endpoint configuration not imported correctly")
            return False
    else:
        print(f"❌ Full import failed")
        return False
    
    # Test backward compatibility with legacy format
    print(f"\n🔄 Testing backward compatibility with legacy format...")
    
    legacy_config = {
        "legacy_test": {
            "endpoint": "/legacy/test",
            "type": "none",
            "dataWrapper": False,
            "description": "Legacy format test"
        }
    }
    
    legacy_import_success = config_manager.import_user_config(json.dumps(legacy_config))
    
    if legacy_import_success:
        legacy_imported = config_manager.get_template_config("legacy_test")
        if legacy_imported.get("endpoint") == "/legacy/test":
            print(f"✅ Legacy format import works correctly")
        else:
            print(f"❌ Legacy format import failed")
            return False
    else:
        print(f"❌ Legacy format import failed")
        return False
    
    print(f"\n📋 Enhanced Export/Import Summary:")
    print(f"   ✅ Full configuration export works")
    print(f"   ✅ Full configuration import works")
    print(f"   ✅ Global settings export/import works")
    print(f"   ✅ Endpoint configurations export/import works")
    print(f"   ✅ Backward compatibility with legacy format maintained")
    
    return True

if __name__ == "__main__":
    success = True
    
    try:
        success &= test_export_import_functionality()
        success &= test_enhanced_export_import()
        
        if success:
            print(f"\n🎉 Export/Import analysis completed!")
        else:
            print(f"\n❌ Some tests failed!")
            
    except Exception as e:
        print(f"\n💥 Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        success = False
    
    exit(0 if success else 1)
