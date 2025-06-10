#!/usr/bin/env python3
"""Test script to verify whitespace handling in all field type patterns"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from data_creation.template_functions import generate_random_value

def test_whitespace_handling():
    """Test that all field type patterns handle whitespace correctly"""
    
    print("🧪 Testing whitespace handling in field type patterns...")
    
    # Test cases with various whitespace patterns
    test_cases = [
        # Float patterns
        ("float(1,50)", "float with no spaces"),
        ("float( 1 , 50 )", "float with spaces around values"),
        ("float(1, 50)", "float with space after comma"),
        ("float( 1, 50 )", "float with leading/trailing spaces"),
        ("float(1.5, 10.2, 3)", "float with precision and spaces"),
        ("float( 1.5 , 10.2 , 3 )", "float with precision and extra spaces"),
        
        # Int patterns
        ("int(10,100)", "int with no spaces"),
        ("int( 10 , 100 )", "int with spaces around values"),
        ("int(10, 100)", "int with space after comma"),
        ("int( 10, 100 )", "int with leading/trailing spaces"),
        
        # String patterns
        ("string(12)", "string with no spaces"),
        ("string( 12 )", "string with spaces around value"),
        
        # DateTime patterns
        ("datetime(future)", "datetime with no spaces"),
        ("datetime( future )", "datetime with spaces around value"),
        ("datetime( now )", "datetime now with spaces"),
        ("datetime( past )", "datetime past with spaces"),
        
        # Choice patterns
        ("choice(A,B,C)", "choice with no spaces"),
        ("choice( A , B , C )", "choice with spaces around values"),
        ("choice(A, B, C)", "choice with spaces after commas"),
        ("choice( A, B, C )", "choice with leading/trailing spaces"),
        ("choice(DEMO-FAC-01, CM_STORE_000001, CM_STORE_000002)", "choice with complex values and spaces"),
    ]
    
    print(f"\n📋 Testing {len(test_cases)} different whitespace patterns...")
    
    for field_type, description in test_cases:
        try:
            value = generate_random_value(field_type)
            print(f"✅ {description}: '{field_type}' → {value} ({type(value).__name__})")
            
            # Basic validation based on field type
            if field_type.startswith('float('):
                assert isinstance(value, float), f"Expected float, got {type(value)}"
            elif field_type.startswith('int('):
                assert isinstance(value, int), f"Expected int, got {type(value)}"
            elif field_type.startswith('string('):
                assert isinstance(value, str), f"Expected str, got {type(value)}"
            elif field_type.startswith('datetime('):
                assert isinstance(value, str), f"Expected str (ISO datetime), got {type(value)}"
            elif field_type.startswith('choice('):
                assert isinstance(value, str), f"Expected str (choice), got {type(value)}"
                
        except Exception as e:
            print(f"❌ {description}: '{field_type}' → ERROR: {e}")
            raise
    
    print(f"\n🎉 All whitespace handling tests passed!")
    print("✨ Field type patterns now properly handle whitespace in all formats!")

if __name__ == "__main__":
    test_whitespace_handling()
