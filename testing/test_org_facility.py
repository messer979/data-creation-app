#!/usr/bin/env python3
"""
Test script for organization and facility functionality
"""

from components.config_manager import ConfigurationManager

def test_org_facility():
    """Test organization and facility functionality"""
    print("Testing ConfigurationManager organization and facility features...")
    
    # Create config manager instance
    cm = ConfigurationManager()
    
    # Test default values
    print(f"Default Organization: {cm.get_selected_organization()}")
    print(f"Default Facility: {cm.get_selected_facility()}")
    
    # Test setting new values
    cm.set_selected_organization("test_org")
    cm.set_selected_facility("test_facility")
    
    print(f"Updated Organization: {cm.get_selected_organization()}")
    print(f"Updated Facility: {cm.get_selected_facility()}")
    
    # Test headers for a template
    headers = cm.get_headers_for_template("facility")
    print(f"Headers for facility template: {headers}")
    
    # Verify organization and facility are in headers
    assert 'SelectedOrganization' in headers
    assert 'SelectedFacility' in headers
    assert headers['SelectedOrganization'] == "test_org"
    assert headers['SelectedFacility'] == "test_facility"
    
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_org_facility()
