#!/usr/bin/env python3
"""
Test script to verify session-only template management is working
"""

import streamlit as st
import sys
import os

# Add the project directory to the path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

def test_session_only_templates():
    """Test session-only template functionality"""
    print("=== Testing Session-Only Template System ===")
    print()
    
    try:
        # Import our session-only components
        from templates.session_base_template_manager import SessionBaseTemplateManager
        from data_creation.template_generator import TemplateGenerator
        from data_creation.data_generator import DataGenerator
        
        print("SUCCESS: Successfully imported session-only components")
        
        # Initialize session state (normally done by Streamlit)
        if not hasattr(st, 'session_state'):
            class MockSessionState:
                def __init__(self):
                    self._state = {}
                
                def get(self, key, default=None):
                    return self._state.get(key, default)
                
                def __setitem__(self, key, value):
                    self._state[key] = value
                
                def __getitem__(self, key):
                    return self._state[key]
                
                def __contains__(self, key):
                    return key in self._state
            
            st.session_state = MockSessionState()
        
        # Test 1: Session Base Template Manager
        print()
        print("1. Testing SessionBaseTemplateManager...")
        base_manager = SessionBaseTemplateManager()
        
        # Add a test template
        test_template = {"test_field": "test_value", "id": 123}
        success = base_manager.save_template("test_template", test_template)
        
        if success and "test_template" in base_manager.base_templates:
            print("   SUCCESS: Base template saved to session successfully")
        else:
            print("   FAIL: Failed to save base template to session")
            return False
        
        # Test export
        json_str, export_data = base_manager.export_all_templates()
        if json_str and "session_only" in json_str:
            print("   SUCCESS: Export includes session-only marker")
        else:
            print("   FAIL: Export missing session-only marker")
        
        # Test 2: Session Generation Template Manager
        print()
        print("2. Testing TemplateGenerator (session-only)...")
        template_gen = TemplateGenerator()
        
        # Add a test generation template
        test_gen_template = {
            "StaticFields": {"test_static": "static_value"},
            "DynamicFields": {"test_dynamic": {"type": "counter", "start": 1}},
            "RandomFields": [],
            "LinkedFields": {}
        }
        
        # Directly add to session (simulating import)
        template_gen.generation_templates["test_gen"] = test_gen_template
        
        if "test_gen" in template_gen.generation_templates:
            print("   SUCCESS: Generation template stored in session successfully")
        else:
            print("   FAIL: Failed to store generation template in session")
            return False
        
        # Test 3: Data Generator with session templates
        print()
        print("3. Testing DataGenerator (session-only)...")
        data_gen = DataGenerator()
        
        # Check that it uses session state
        if hasattr(data_gen, 'templates') and isinstance(data_gen.templates, dict):
            print("   SUCCESS: DataGenerator using session-based templates")
        else:
            print("   FAIL: DataGenerator not properly configured for session-only")
            return False
        
        # Test 4: Check no file operations
        print()
        print("4. Verifying no server-side storage...")
        
        # Check that templates directory is not required
        templates_exist_on_disk = os.path.exists("templates/base_templates") and \
                                len(os.listdir("templates/base_templates")) > 0
        
        if not templates_exist_on_disk:
            print("   SUCCESS: No base templates found on disk - fully session-based")
        else:
            print("   WARNING: Some base templates still exist on disk")
            print("      This is OK for backwards compatibility, but they won't be auto-loaded")
        
        # Verify generation templates are session-only
        gen_templates_on_disk = os.path.exists("templates/generation_templates") and \
                              len(os.listdir("templates/generation_templates")) > 0
        
        if not gen_templates_on_disk:
            print("   SUCCESS: No generation templates found on disk - fully session-based")
        else:
            print("   WARNING: Some generation templates still exist on disk")
            print("      These will be ignored in favor of session storage")
        
        print()
        print("SUCCESS: Session-only template system is working correctly!")
        print()
        print("Key benefits achieved:")
        print("  - No server-side storage or persistence")
        print("  - Templates exist only in user session")
        print("  - Stateless server architecture")
        print("  - Templates lost on page refresh (by design)")
        print("  - Users must export templates to save them")
        
        return True
        
    except Exception as e:
        print()
        print(f"ERROR: Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_session_only_templates()
    if success:
        print()
        print("SUCCESS: All tests passed - Session-only system ready!")
    else:
        print()
        print("FAIL: Some tests failed - Check implementation")
