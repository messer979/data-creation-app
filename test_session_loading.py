#!/usr/bin/env python3
"""
Test script to check if templates are loading in session-only mode
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

# Mock streamlit module
class MockStreamlit:
    def __init__(self):
        self.session_state = MockSessionState()
    
    def error(self, msg):
        print(f"ERROR: {msg}")

# Replace streamlit import
sys.modules['streamlit'] = MockStreamlit()
import streamlit as st

# Now test the managers
from templates.session_base_template_manager import SessionBaseTemplateManager
from data_creation.template_generator import TemplateGenerator

def test_session_managers():
    print("Testing Session-Only Template Loading...")
    print("=" * 50)
    
    # Test SessionBaseTemplateManager
    print("\n1. Testing SessionBaseTemplateManager:")
    base_manager = SessionBaseTemplateManager()
    print(f"   - Base templates count: {len(base_manager.base_templates)}")
    print(f"   - Base templates: {list(base_manager.base_templates.keys())}")
    
    # Test TemplateGenerator
    print("\n2. Testing TemplateGenerator:")
    template_gen = TemplateGenerator()
    print(f"   - Generation templates count: {len(template_gen.generation_templates)}")
    print(f"   - Generation templates: {list(template_gen.generation_templates.keys())}")
    
    # Check what's actually in session state
    print("\n3. Session State Contents:")
    for key, value in st.session_state._state.items():
        if isinstance(value, dict):
            print(f"   - {key}: {len(value)} items - {list(value.keys())}")
        else:
            print(f"   - {key}: {type(value).__name__}")
    
    # Check if example base templates directory exists
    base_templates_dir = "templates/base_templates"
    if os.path.exists(base_templates_dir):
        json_files = [f for f in os.listdir(base_templates_dir) if f.endswith('.json')]
        print(f"\n4. Available base template files ({len(json_files)}):")
        for file in json_files:
            print(f"   - {file}")
    else:
        print(f"\n4. Base templates directory not found: {base_templates_dir}")
    
    # Check if generation templates directory exists
    gen_templates_dir = "templates/generation_templates"
    if os.path.exists(gen_templates_dir):
        json_files = [f for f in os.listdir(gen_templates_dir) if f.endswith('.json')]
        print(f"\n5. Available generation template files ({len(json_files)}):")
        for file in json_files:
            print(f"   - {file}")
    else:
        print(f"\n5. Generation templates directory not found: {gen_templates_dir}")

if __name__ == "__main__":
    test_session_managers()
