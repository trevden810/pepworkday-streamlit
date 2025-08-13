#!/usr/bin/env python3
"""
Debug script to check Samsara API request parameters.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import requests
from urllib.parse import urlencode


def debug_samsara_request():
    """Debug Samsara API request."""
    print("=" * 60)
    print("Debugging Samsara API Request")
    print("=" * 60)
    
    # Load secrets
    try:
        st.secrets.load_if_toml_exists()
    except Exception as e:
        print(f"Warning: Could not load Streamlit secrets: {e}")
        return
    
    # Get Samsara configuration
    base_url = st.secrets["samsara"]["base_url"]
    api_token = st.secrets["samsara"]["api_token"]
    group_id = st.secrets.get("samsara", {}).get("group_id", None)
    
    print(f"Base URL: {base_url}")
    print(f"API Token: {api_token[:20]}...")
    print(f"Group ID: {group_id}")
    
    # Test URL construction
    url = f"{base_url}/fleet/vehicles/stats"
    print(f"\nURL: {url}")
    
    # Test parameters
    params = {
        "types": ["vehicleInfo"]
    }
    
    if group_id and group_id != "your-group-id":
        params["groupId"] = group_id
    
    print(f"Parameters: {params}")
    
    # Test URL encoding
    encoded_params = urlencode(params, doseq=True)
    print(f"Encoded parameters: {encoded_params}")
    
    # Test headers
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    print(f"Headers: {headers}")
    
    # Make the request
    print("\nMaking request...")
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text[:200]}...")
    except Exception as e:
        print(f"Request failed with error: {str(e)}")


if __name__ == "__main__":
    debug_samsara_request()
