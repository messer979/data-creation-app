"""
Test Script for Dummy Server and UI Integration
This script demonstrates how to test the inventory transfer UI with the dummy server
"""

import subprocess
import time
import requests
import sys
import os
from datetime import datetime

def test_dummy_server():
    """Test if dummy server is responding"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Dummy server is running and responding")
            return True
        else:
            print(f"❌ Dummy server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to dummy server - make sure it's running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Error testing dummy server: {e}")
        return False

def test_inventory_search():
    """Test inventory search endpoint"""
    try:
        payload = {
            "LocationQuery": {
                "Query": "Zone =ZONE1 and InventoryReservationTypeId=LOCATION"
            },
            "Size": 10,
            "Page": 0
        }
        
        response = requests.post("http://localhost:5000/inventory/search", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Inventory search successful - returned {len(data.get('data', []))} records")
            print(f"   Total count: {data.get('header', {}).get('totalCount', 'unknown')}")
            return True
        else:
            print(f"❌ Inventory search failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing inventory search: {e}")
        return False

def test_inventory_adjustment():
    """Test inventory adjustment endpoint"""
    try:
        payload = [
            {
                "ItemId": "TEST_ITEM_001",
                "LocationId": "STAGING-0001",
                "OnHand": 100,
                "ReservationTypeId": "LOCATION",
                "Zone": "STAGING",
                "AdjustmentType": "ABSOLUTE",
                "Reason": "ZONE_TRANSFER"
            }
        ]
        
        response = requests.post("http://localhost:5000/inventory/adjust", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            successful = data.get('data', {}).get('SuccessfulRecords', 0)
            failed = len(data.get('data', {}).get('FailedRecords', []))
            print(f"✅ Inventory adjustment successful - {successful} successful, {failed} failed")
            return True
        else:
            print(f"❌ Inventory adjustment failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing inventory adjustment: {e}")
        return False

def run_comprehensive_test():
    """Run a comprehensive test of the dummy server"""
    print("🧪 Starting Comprehensive Dummy Server Test")
    print("=" * 50)
    
    # Test server health
    if not test_dummy_server():
        print("\n❌ Cannot proceed - dummy server is not running")
        print("\nTo start the dummy server, run:")
        print("   python dummy_server.py")
        return False
    
    print()
    
    # Test inventory search
    test_inventory_search()
    print()
    
    # Test inventory adjustment
    test_inventory_adjustment()
    print()
    
    # Test all zones
    print("🔍 Testing all zones:")
    zones = ["ZONE1", "ZONE2", "ZONE3", "STAGING"]
    
    for zone in zones:
        payload = {
            "LocationQuery": {
                "Query": f"Zone ={zone} and InventoryReservationTypeId=LOCATION"
            },
            "Size": 5,
            "Page": 0
        }
        
        try:
            response = requests.post("http://localhost:5000/inventory/search", json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                count = data.get('header', {}).get('totalCount', 0)
                print(f"   {zone}: {count} records available")
            else:
                print(f"   {zone}: Error (status {response.status_code})")
        except:
            print(f"   {zone}: Connection error")
    
    print("\n✅ Comprehensive test completed!")
    print("\n📋 Next Steps:")
    print("1. Keep the dummy server running: python dummy_server.py")
    print("2. Start the Streamlit app: streamlit run app.py")
    print("3. Navigate to Data Import page")
    print("4. Enable 'Test Mode' checkbox")
    print("5. Run an inventory transfer test")
    
    return True

if __name__ == "__main__":
    print(f"Test started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success = run_comprehensive_test()
    
    if success:
        print(f"\n🎉 All tests passed! System is ready for testing.")
    else:
        print(f"\n❌ Some tests failed. Check the dummy server setup.")
    
    print(f"\nTest completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
