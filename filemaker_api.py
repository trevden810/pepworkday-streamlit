"""
FileMaker API Integration Module

This module provides functions to interact with the FileMaker Data API,
including authentication, data retrieval, and data creation.
"""

import requests
import streamlit as st
import json
from typing import Dict, List, Optional, Any


class FileMakerAPI:
    """FileMaker API client for interacting with FileMaker databases."""
    
    def __init__(self):
        """Initialize the FileMaker API client with configuration from secrets."""
        self.server_url = st.secrets["filemaker"]["server_url"]
        self.api_version = st.secrets["filemaker"]["api_version"]
        self.username = st.secrets["filemaker"]["username"]
        self.password = st.secrets["filemaker"]["password"]
        self.token = None
    
    def authenticate(self, database_name: str) -> bool:
        """
        Authenticate with the FileMaker Data API and obtain a session token.
        
        Args:
            database_name (str): Name of the FileMaker database
            
        Returns:
            bool: True if authentication was successful, False otherwise
        """
        auth_url = f"{self.server_url}/fmi/data/{self.api_version}/databases/{database_name}/sessions"
        
        try:
            response = requests.post(
                auth_url,
                auth=(self.username, self.password),
                headers={"Content-Type": "application/json"},
                json={}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data["response"]["token"]
                return True
            else:
                st.error(f"Authentication failed: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            st.error(f"Authentication request failed: {str(e)}")
            return False
    
    def find_record(self, database_name: str, layout: str, query: Dict) -> Optional[Dict]:
        """
        Find a record in FileMaker using a query.
        
        Args:
            database_name (str): Name of the FileMaker database
            layout (str): Layout name to search in
            query (Dict): Query parameters for the search
            
        Returns:
            Optional[Dict]: Found record data or None if not found
        """
        if not self.token:
            if not self.authenticate(database_name):
                return None
        
        find_url = f"{self.server_url}/fmi/data/{self.api_version}/databases/{database_name}/layouts/{layout}/_find"
        
        try:
            response = requests.post(
                find_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.token}"
                },
                json={"query": [query]}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data["response"]["data"]:
                    return data["response"]["data"][0]
                else:
                    st.warning("No records found matching the query")
                    return None
            else:
                st.error(f"Find record failed: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            st.error(f"Find record request failed: {str(e)}")
            return None
    
    def create_record(self, database_name: str, layout: str, field_data: Dict) -> Optional[str]:
        """
        Create a new record in FileMaker.
        
        Args:
            database_name (str): Name of the FileMaker database
            layout (str): Layout name to create record in
            field_data (Dict): Field data for the new record
            
        Returns:
            Optional[str]: Record ID of the created record or None if failed
        """
        if not self.token:
            if not self.authenticate(database_name):
                return None
        
        create_url = f"{self.server_url}/fmi/data/{self.api_version}/databases/{database_name}/layouts/{layout}/records"
        
        try:
            response = requests.post(
                create_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.token}"
                },
                json={"fieldData": field_data}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["response"]["recordId"]
            else:
                st.error(f"Create record failed: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            st.error(f"Create record request failed: {str(e)}")
            return None


@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_filemaker_job_data(job_id: str) -> Optional[Dict]:
    """
    Get comprehensive job data from FileMaker by job ID.
    
    Args:
        job_id (str): Job ID to search for
        
    Returns:
        Optional[Dict]: Structured job data with all requested fields or None if not found
    """
    fm_api = FileMakerAPI()
    database_name = st.secrets["filemaker"]["database_name"]
    layout = "jobs_api"
    
    query = {"_kp_job_id": job_id}
    record = fm_api.find_record(database_name, layout, query)
    
    if not record or "fieldData" not in record:
        return None
        
    field_data = record["fieldData"]
    
    # Structure all requested fields with fallback to None if missing
    return {
        "job_id": field_data.get("_kp_job_id"),
        "date": field_data.get("job_date"),
        "status": field_data.get("job_status"),
        "type": field_data.get("job_type"),
        "client_code": field_data.get("_kf_client_code_id"),
        "disposition": field_data.get("_kf_disposition"),
        "notification_id": field_data.get("_kf_notification_id"),
        "lead_id": field_data.get("_kf_lead_id"),
        "truck_id": field_data.get("_kf_trucks_id"),
        "people_required": field_data.get("people_required"),
        "product_weight": field_data.get("_kf_product_weight_id"),
        "miles_oneway": field_data.get("oneway_miles"),
        "location_load": field_data.get("location_load"),
        "location_return": field_data.get("location_return"),
        "address": field_data.get("address_C1"),
        "zip": field_data.get("zip_C1"),
        "city_id": field_data.get("_kf_city_id"),
        "state_id": field_data.get("_kf_state_id"),
        "notes_call_ahead": field_data.get("notes_call_ahead"),
        "notes_driver": field_data.get("notes_driver"),
        "raw_data": field_data  # Keep original data for reference
    }


@st.cache_data
def create_filemaker_job(field_data: Dict) -> Optional[str]:
    """
    Create a new job record in FileMaker.
    
    Args:
        field_data (Dict): Field data for the new job record
        
    Returns:
        Optional[str]: Record ID of the created job or None if failed
    """
    fm_api = FileMakerAPI()
    database_name = st.secrets["filemaker"]["pep_move_database"]
    layout = "table"  # You may need to adjust this based on your actual layout name
    
    return fm_api.create_record(database_name, layout, field_data)
