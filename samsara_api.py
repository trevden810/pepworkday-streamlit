"""
Samsara API Integration Module

This module provides functions to interact with the Samsara API,
including vehicle data, driver information, and fleet metrics.
"""

import requests
import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta


class SamsaraAPI:
    """Samsara API client for interacting with Samsara services."""
    
    def __init__(self):
        """Initialize the Samsara API client with configuration from secrets."""
        self.base_url = st.secrets["samsara"]["base_url"]
        self.api_token = st.secrets["samsara"]["api_token"]
        self.group_id = st.secrets.get("samsara", {}).get("group_id", None)
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def get_vehicles(self) -> Optional[List[Dict]]:
        """
        Get list of vehicles from Samsara.
        
        Returns:
            Optional[List[Dict]]: List of vehicle data or None if failed
        """
        url = f"{self.base_url}/fleet/vehicles"
        
        params = {}
        if self.group_id and self.group_id != "your-group-id":
            params["groupId"] = self.group_id
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                # Handle both "data" and "vehicles" response formats
                return data.get("data", data.get("vehicles", []))
            else:
                st.error(f"Get vehicles failed: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            st.error(f"Get vehicles request failed: {str(e)}")
            return None
    
    def get_vehicle_stats(self, vehicle_id: str, start_time: str, end_time: str) -> Optional[Dict]:
        """
        Get vehicle statistics for a specific time period.
        
        Args:
            vehicle_id (str): ID of the vehicle
            start_time (str): Start time in ISO 8601 format
            end_time (str): End time in ISO 8601 format
            
        Returns:
            Optional[Dict]: Vehicle statistics or None if failed
        """
        url = f"{self.base_url}/fleet/vehicles/stats/history"
        
        params = {
            "id": vehicle_id,
            "startTime": start_time,
            "endTime": end_time
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                st.error(f"Get vehicle stats failed: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            st.error(f"Get vehicle stats request failed: {str(e)}")
            return None
    
    def get_drivers(self) -> Optional[List[Dict]]:
        """
        Get list of drivers from Samsara.
        
        Returns:
            Optional[List[Dict]]: List of driver data or None if failed
        """
        url = f"{self.base_url}/fleet/drivers"
        
        params = {}
        if self.group_id:
            params["groupId"] = self.group_id
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("drivers", [])
            else:
                st.error(f"Get drivers failed: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            st.error(f"Get drivers request failed: {str(e)}")
            return None


@st.cache_data
def get_samsara_vehicles() -> Optional[pd.DataFrame]:
    """
    Get Samsara vehicles data as a DataFrame.
    
    Returns:
        Optional[pd.DataFrame]: DataFrame with vehicle data or None if failed
    """
    samsara_api = SamsaraAPI()
    vehicles = samsara_api.get_vehicles()
    
    if vehicles:
        # Convert to DataFrame for easier processing
        df = pd.DataFrame(vehicles)
        return df
    else:
        return None


@st.cache_data
def get_samsara_drivers() -> Optional[pd.DataFrame]:
    """
    Get Samsara drivers data as a DataFrame.
    
    Returns:
        Optional[pd.DataFrame]: DataFrame with driver data or None if failed
    """
    samsara_api = SamsaraAPI()
    drivers = samsara_api.get_drivers()
    
    if drivers:
        # Convert to DataFrame for easier processing
        df = pd.DataFrame(drivers)
        return df
    else:
        return None


@st.cache_data
def get_recent_vehicle_stats(hours: int = 24) -> Optional[pd.DataFrame]:
    """
    Get recent vehicle statistics for all vehicles.
    
    Args:
        hours (int): Number of hours to look back (default: 24)
        
    Returns:
        Optional[pd.DataFrame]: DataFrame with vehicle stats or None if failed
    """
    samsara_api = SamsaraAPI()
    vehicles = samsara_api.get_vehicles()
    
    if not vehicles:
        return None
    
    # Calculate time range
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    
    start_time_iso = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time_iso = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Collect stats for each vehicle
    all_stats = []
    
    for vehicle in vehicles:
        vehicle_id = vehicle.get("id")
        if vehicle_id:
            stats = samsara_api.get_vehicle_stats(
                vehicle_id, start_time_iso, end_time_iso
            )
            
            if stats:
                # Process stats data
                vehicle_stats = {
                    "vehicle_id": vehicle_id,
                    "name": vehicle.get("name", "Unknown"),
                    "vin": vehicle.get("vin", "Unknown"),
                    "odometer_meters": vehicle.get("odometerMeters", 0),
                    "engine_hours": vehicle.get("engineHours", 0),
                    "fuel_level_percent": vehicle.get("fuelPercent", 0)
                }
                
                # Add location data if available
                location_data = vehicle.get("locationData", {})
                if location_data:
                    vehicle_stats["latitude"] = location_data.get("latitude", None)
                    vehicle_stats["longitude"] = location_data.get("longitude", None)
                    vehicle_stats["location_time"] = location_data.get("time", None)
                
                all_stats.append(vehicle_stats)
    
    if all_stats:
        return pd.DataFrame(all_stats)
    else:
        return None
