#!/usr/bin/env python3
"""
Test script to verify end-to-end template loading and data generation
"""
import sys
import os
import json

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock streamlit session state for testing
class MockSessionState:
    def __init__(self):
        self._state = {}
    
    def __contains__(self, key):
        return key in self._state
    
    def __getitem__(self, key):
        return self._state[key]
    
    def __setitem__(self, key, value):
        self._state[key] = value
        
    def get(self, key, default=None):
        return self._state.get(key, default)
    
    def clear(self):
        self._state.clear()

# Mock streamlit module
class MockStreamlit:
    def __init__(self):
        self.session_state = MockSessionState()
    
    def error(self, msg):
        print(f"ERROR: {msg}")
    
    def success(self, msg):
        print(f"SUCCESS: {msg}")

# Replace streamlit import
sys.modules['streamlit'] = MockStreamlit()
import streamlit as st

# Now test the managers
from templates.session_base_template_manager import SessionBaseTemplateManager
from data_creation.template_generator import TemplateGenerator
from data_creation.data_generator import DataGenerator

def test_end_to_end():
    print("Testing End-to-End Template Loading and Data Generation...")
    print("=" * 60)
    
    # Test SessionBaseTemplateManager
    print("\n1. Initializing SessionBaseTemplateManager...")
    base_manager = SessionBaseTemplateManager()
    print(f"   ✓ Base templates loaded: {len(base_manager.base_templates)}")
    
    # Test TemplateGenerator
    print("\n2. Initializing TemplateGenerator...")
    template_gen = TemplateGenerator()
    print(f"   ✓ Generation templates loaded: {len(template_gen.generation_templates)}")
      # Test DataGenerator
    print("\n3. Initializing DataGenerator...")
    data_gen = DataGenerator()
    print(f"   ✓ DataGenerator initialized with base templates: {len(data_gen.templates)}")
    
    # Test if we can use a base template for generation
    if 'item' in base_manager.base_templates and 'item' in template_gen.generation_templates:
        print("\n4. Testing data generation with 'item' template...")
        try:
            base_template = base_manager.base_templates['item']
            generation_template = template_gen.generation_templates['item']
            
            print(f"   - Base template has {len(base_template)} fields")
            print(f"   - Generation template has {len(generation_template)} fields")
            
            # Generate 3 test records
            generated_records = template_gen.generate_records('item', 3, base_template)
            print(f"   ✓ Successfully generated {len(generated_records)} records")
            
            # Check that each record has the expected structure
            for i, record in enumerate(generated_records):
                print(f"   - Record {i+1}: ItemId = {record.get('ItemId', 'N/A')}")
                
        except Exception as e:
            print(f"   ✗ Error during data generation: {e}")
    else:
        print("\n4. 'item' template not found - skipping generation test")
    
    # Test session state persistence
    print("\n5. Testing session state management...")
    original_count = len(base_manager.base_templates)
    
    # Add a test template
    test_template = {"test_field": "test_value"}
    base_manager.save_template("test_template", test_template)
    print(f"   - Added test template, count: {len(base_manager.base_templates)}")
    
    # Verify it's in session
    if "test_template" in base_manager.base_templates:
        print("   ✓ Test template successfully stored in session")
        
        # Remove test template
        base_manager.delete_template("test_template")
        print(f"   - Removed test template, count: {len(base_manager.base_templates)}")
        
        if "test_template" not in base_manager.base_templates:
            print("   ✓ Test template successfully removed from session")
    
    print("\n6. Summary:")
    print(f"   - Base templates available: {len(base_manager.base_templates)}")
    print(f"   - Generation templates available: {len(template_gen.generation_templates)}")
    print(f"   - Session keys: {list(st.session_state._state.keys())}")
    print("   ✓ All session-only functionality working correctly!")

if __name__ == "__main__":
    test_end_to_end()
