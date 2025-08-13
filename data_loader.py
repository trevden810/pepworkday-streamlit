import pandas as pd
import streamlit as st
from typing import Optional
from filemaker_api import get_filemaker_job_data
from samsara_api import get_samsara_vehicles, get_samsara_drivers, get_recent_vehicle_stats

@st.cache_data
def load_data():
    """Load example data for demonstration purposes."""
    return pd.DataFrame({
        'column1': [1, 2, 3, 4],
        'column2': [10, 20, 30, 40]
    })

@st.cache_data
def load_large_dataset():
    """Load a more complex dataset (placeholder implementation)."""
    # In a real app, this might connect to a database or external API
    return pd.DataFrame({
        'id': range(100),
        'value': [i * 10 for i in range(100)]
    })

@st.cache_data
def load_csv(file_path):
    """Load CSV data from the specified file path using pandas."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return pd.DataFrame()

@st.cache_data
def merge_data(filemaker_df, samsara_df, on='id', how='inner'):
    """Merge FileMaker and Samsara CSV datasets using pandas."""
    merged_df = pd.merge(filemaker_df, samsara_df, on=on, how=how)
    return merged_df

@st.cache_data
def load_filemaker_data(job_id: str) -> Optional[pd.DataFrame]:
    """
    Load data from FileMaker API for a specific job ID.
    
    Args:
        job_id (str): Job ID to retrieve data for
        
    Returns:
        Optional[pd.DataFrame]: DataFrame with job data or None if failed
    """
    try:
        job_data = get_filemaker_job_data(job_id)
        
        if job_data and "fieldData" in job_data:
            # Convert the FileMaker response to a DataFrame
            field_data = job_data["fieldData"]
            df = pd.DataFrame([field_data])
            return df
        else:
            return None
            
    except Exception as e:
        st.error(f"Error loading FileMaker data: {str(e)}")
        return None

@st.cache_data
def load_samsara_fleet_data() -> Optional[pd.DataFrame]:
    """
    Load fleet data from Samsara API.
    
    Returns:
        Optional[pd.DataFrame]: DataFrame with fleet data or None if failed
    """
    try:
        # Get vehicles data
        vehicles_df = get_samsara_vehicles()
        
        if vehicles_df is not None:
            return vehicles_df
        else:
            return None
            
    except Exception as e:
        st.error(f"Error loading Samsara data: {str(e)}")
        return None

@st.cache_data
def load_combined_fleet_data() -> Optional[pd.DataFrame]:
    """
    Load combined fleet data from both FileMaker and Samsara APIs.
    
    Returns:
        Optional[pd.DataFrame]: DataFrame with combined data or None if failed
    """
    try:
        # Get Samsara data (vehicles)
        samsara_df = get_recent_vehicle_stats()
        
        if samsara_df is not None:
            # For now, we'll return just the Samsara data
            # In a real implementation, you would merge this with FileMaker data
            # based on your specific business logic
            return samsara_df
        else:
            return None
            
    except Exception as e:
        st.error(f"Error loading combined fleet data: {str(e)}")
        return None
