#!/usr/bin/env python3
"""
Test script to check connectivity to FileMaker and Samsara APIs.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent))

# Set up Streamlit environment
os.environ["STREAMLIT_SERVER_PORT"] = "8502"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

import streamlit as st
from filemaker_api import FileMakerAPI, get_filemaker_job_data
from samsara_api import SamsaraAPI, get_samsara_vehicles, get_samsara_drivers


def test_filemaker_connection():
    """Test FileMaker API connection."""
    print("=" * 60)
    print("Testing FileMaker API Connection")
    print("=" * 60)
    
    try:
        fm_api = FileMakerAPI()
        print(f"FileMaker Server URL: {fm_api.server_url}")
        print(f"Username: {fm_api.username}")
        print(f"API Version: {fm_api.api_version}")
        
        # Test authentication
        print("\n1. Testing authentication...")
        database_name = st.secrets["filemaker"]["database_name"]
        success = fm_api.authenticate(database_name)
        
        if success:
            print("✅ Authentication successful!")
            print(f"Token: {fm_api.token[:20]}..." if fm_api.token else "No token")
        else:
            print("❌ Authentication failed!")
            return False
        
        # Test getting a specific job (using a common test job ID)
        print("\n2. Testing job data retrieval...")
        # Try to get job data for a test job ID
        job_data = get_filemaker_job_data("603142")  # Using the test job ID from unit tests
        
        if job_data:
            print("✅ Job data retrieval successful!")
            print(f"Job ID: {job_data.get('fieldData', {}).get('_kp_job_id', 'Unknown')}")
            print(f"Job Status: {job_data.get('fieldData', {}).get('job_status', 'Unknown')}")
        else:
            print("⚠️  Job data retrieval returned no results (this might be expected)")
        
        return True
        
    except Exception as e:
        print(f"❌ FileMaker API test failed with error: {str(e)}")
        return False


def test_samsara_connection():
    """Test Samsara API connection."""
    print("\n" + "=" * 60)
    print("Testing Samsara API Connection")
    print("=" * 60)
    
    try:
        samsara_api = SamsaraAPI()
        print(f"Samsara Base URL: {samsara_api.base_url}")
        print(f"API Token: {samsara_api.api_token[:20]}..." if samsara_api.api_token else "No token")
        print(f"Group ID: {samsara_api.group_id}")
        
        # Test getting vehicles
        print("\n1. Testing vehicle data retrieval...")
        vehicles = samsara_api.get_vehicles()
        
        if vehicles is not None:
            print(f"✅ Vehicle data retrieval successful!")
            print(f"Number of vehicles found: {len(vehicles)}")
            if vehicles:
                print(f"First vehicle: {vehicles[0].get('name', 'Unknown')} (ID: {vehicles[0].get('id', 'Unknown')})")
        else:
            print("❌ Vehicle data retrieval failed!")
            # Let's try to get more details about the error
            try:
                # Try again with more error details
                url = f"{samsara_api.base_url}/fleet/vehicles/stats"
                params = {}
                if samsara_api.group_id and samsara_api.group_id != "your-group-id":
                    params["groupId"] = samsara_api.group_id
                
                import requests
                response = requests.get(url, headers=samsara_api.headers, params=params)
                print(f"   Response Status Code: {response.status_code}")
                print(f"   Response Text: {response.text[:200]}...")
            except Exception as detailed_error:
                print(f"   Detailed error: {str(detailed_error)}")
            return False
        
        # Test getting drivers
        print("\n2. Testing driver data retrieval...")
        drivers = samsara_api.get_drivers()
        
        if drivers is not None:
            print(f"✅ Driver data retrieval successful!")
            print(f"Number of drivers found: {len(drivers)}")
            if drivers:
                print(f"First driver: {drivers[0].get('name', 'Unknown')} (ID: {drivers[0].get('id', 'Unknown')})")
        else:
            print("❌ Driver data retrieval failed!")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Samsara API test failed with error: {str(e)}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False


def main():
    """Main function to run all API connectivity tests."""
    print("API Connectivity Test Script")
    print("This script will test connectivity to FileMaker and Samsara APIs.")
    print("Make sure you have internet connectivity and valid credentials in .streamlit/secrets.toml")
    
    # Initialize Streamlit secrets (this is needed for the API modules to work)
    try:
        st.secrets.load_if_toml_exists()
    except Exception as e:
        print(f"Warning: Could not load Streamlit secrets: {e}")
        print("Make sure .streamlit/secrets.toml exists and is properly formatted.")
        return 1
    
    # Test FileMaker API
    fm_success = test_filemaker_connection()
    
    # Test Samsara API
    samsara_success = test_samsara_connection()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if fm_success and samsara_success:
        print("✅ All API connectivity tests passed!")
        return 0
    else:
        print("❌ Some API connectivity tests failed!")
        if not fm_success:
            print("   - FileMaker API connection failed")
        if not samsara_success:
            print("   - Samsara API connection failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
