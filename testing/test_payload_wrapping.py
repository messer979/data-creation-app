#!/usr/bin/env python3
"""
Test script for payload wrapping logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_creation.data_generator import DataGenerator

def test_payload_wrapping():
    """Test the payload wrapping logic with different configurations"""
    
    # Create a DataGenerator instance
    data_gen = DataGenerator()
    
    # Sample data
    test_data = [
        {"id": 1, "name": "Test Item 1"},
        {"id": 2, "name": "Test Item 2"}
    ]
    
    print("🧪 Testing Payload Wrapping Logic")
    print("=" * 50)
    
    # Test 1: No configuration (no wrapping)
    print("\n1. No configuration (should return original data):")
    result1 = data_gen._wrap_payload(test_data, None)
    print(f"   Result: {result1}")
    assert result1 == test_data, "No configuration should return original data"
    
    # Test 2: Empty configuration (no wrapping)
    print("\n2. Empty configuration (should return original data):")
    result2 = data_gen._wrap_payload(test_data, {})
    print(f"   Result: {result2}")
    assert result2 == test_data, "Empty configuration should return original data"
    
    # Test 3: Only dataWrapper=True
    print("\n3. Only dataWrapper=True (should wrap in {'data': [records]}):")
    config3 = {"dataWrapper": True}
    result3 = data_gen._wrap_payload(test_data, config3)
    expected3 = {"data": test_data}
    print(f"   Result: {result3}")
    assert result3 == expected3, f"Expected {expected3}, got {result3}"
    
    # Test 4: Only type="xint"
    print("\n4. Only type='xint' (should wrap in {'Payload': [records]}):")
    config4 = {"type": "xint"}
    result4 = data_gen._wrap_payload(test_data, config4)
    expected4 = {"Payload": test_data}
    print(f"   Result: {result4}")
    assert result4 == expected4, f"Expected {expected4}, got {result4}"
    
    # Test 5: Both type="xint" and dataWrapper=True
    print("\n5. Both type='xint' and dataWrapper=True (should wrap in {'Payload': {'data': [records]}}):")
    config5 = {"type": "xint", "dataWrapper": True}
    result5 = data_gen._wrap_payload(test_data, config5)
    expected5 = {"Payload": {"data": test_data}}
    print(f"   Result: {result5}")
    assert result5 == expected5, f"Expected {expected5}, got {result5}"
    
    # Test 6: type="array" and dataWrapper=True
    print("\n6. type='array' and dataWrapper=True (should wrap in {'data': [records]}):")
    config6 = {"type": "array", "dataWrapper": True}
    result6 = data_gen._wrap_payload(test_data, config6)
    expected6 = {"data": test_data}
    print(f"   Result: {result6}")
    assert result6 == expected6, f"Expected {expected6}, got {result6}"
    
    # Test 7: dataWrapper=False (should return original data)
    print("\n7. dataWrapper=False (should return original data):")
    config7 = {"dataWrapper": False}
    result7 = data_gen._wrap_payload(test_data, config7)
    print(f"   Result: {result7}")
    assert result7 == test_data, "dataWrapper=False should return original data"
    
    print("\n✅ All payload wrapping tests passed!")
    print("\nPayload Wrapping Logic Summary:")
    print("- No config or empty config: [records]")
    print("- dataWrapper=True only: {'data': [records]}")
    print("- type='xint' only: {'Payload': [records]}")
    print("- type='xint' + dataWrapper=True: {'Payload': {'data': [records]}}")
    print("- Other combinations: Follow individual rules")


if __name__ == "__main__":
    test_payload_wrapping()
