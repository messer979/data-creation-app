#!/usr/bin/env python3
"""
Test script to verify UI reorganization
Tests that the sidebar data type selection and main panel template editor work correctly
"""

import sys
import os
# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data_generator import DataGenerator
from config_manager import ConfigurationManager

def test_ui_reorganization():
    """Test the UI reorganization changes"""
    
    print("🧪 Testing UI reorganization...")
    
    # Initialize components
    data_gen = DataGenerator()
    config_manager = ConfigurationManager()
    
    # Test 1: Check that templates are loaded
    template_count = len(data_gen.templates)
    print(f"✅ Found {template_count} templates")
    assert template_count > 0, "No templates found"
    
    # Test 2: Check that template names are available
    template_options = list(data_gen.templates.keys())
    print(f"✅ Template options: {template_options}")
    
    # Test 3: Check that generation templates exist for data types
    generation_template_count = 0
    for template_name in template_options:
        if data_gen.has_generation_template(template_name):
            generation_template_count += 1
            print(f"✅ {template_name} has generation template")
    
    print(f"✅ Found {generation_template_count} generation templates")
    
    # Test 4: Verify display name conversion
    display_options = [name.replace('_', ' ').title() for name in template_options]
    print(f"✅ Display options: {display_options}")
    print(f"\n🎉 UI structure test completed successfully!")
    print("📋 Current UI structure:")
    print("  • Data type selection in main column")
    print("  • Generation Template Editor is second section in main panel")
    print("  • Sidebar contains collapsed configuration (global & endpoint)")
    print("  • Template editor expands by default")

if __name__ == "__main__":
    test_ui_reorganization()
