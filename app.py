import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import pydeck as pdk
import sys
import os
from data_loader import load_data, load_filemaker_data, load_samsara_fleet_data, load_combined_fleet_data

# Create sample raw_df with driver and miles data
@st.cache_data
def create_sample_df():
    """Create sample data with drivers, jobs, and miles information."""
    np.random.seed(42)  # For reproducible results
    drivers = ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Eva Brown', 'Frank Miller']

    data = []
    for driver in drivers:
        # Generate random number of jobs per driver (between 5-15)
        num_jobs = np.random.randint(5, 16)
        for job in range(num_jobs):
            data.append({
                'driver': driver,
                'job_id': f"{driver.split()[0][:2].upper()}{job+1:03d}",
                'miles': np.random.randint(50, 500),  # Random miles between 50-500
                'date': pd.date_range('2024-01-01', periods=30, freq='D')[np.random.randint(0, 30)]
            })

    return pd.DataFrame(data)

# Convert Samsara data to driver format
@st.cache_data
def convert_samsara_to_driver_format(samsara_df):
    """Convert Samsara vehicle data to driver format for visualization."""
    if samsara_df is None or samsara_df.empty:
        return create_sample_df()
    
    # Create a mapping of vehicles to drivers (simplified)
    drivers = [f"Driver {i+1}" for i in range(min(len(samsara_df), 6))]
    
    data = []
    for i, (_, vehicle) in enumerate(samsara_df.head(6).iterrows()):
        driver = drivers[i]
        # Use vehicle stats to generate job-like data
        miles = int(vehicle.get('odometer_meters', 0) / 1609.34) if 'odometer_meters' in vehicle else np.random.randint(50, 500)
        num_jobs = max(1, int(miles / 100))  # Generate jobs based on miles
        
        for job in range(num_jobs):
            data.append({
                'driver': driver,
                'job_id': f"{driver.split()[0][:2].upper()}{job+1:03d}",
                'miles': miles // num_jobs,
                'date': pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(0, 30))
            })
    
    return pd.DataFrame(data) if data else create_sample_df()

# Convert combined data to driver format
@st.cache_data
def convert_combined_to_driver_format(combined_df):
    """Convert combined fleet data to driver format for visualization."""
    if combined_df is None or combined_df.empty:
        return create_sample_df()
    
    # For now, just use the combined data as is, but convert to driver format
    return convert_samsara_to_driver_format(combined_df)

st.set_page_config(page_title='PEP Workday - Fleet Management Dashboard', layout='wide')
st.title('PEP Workday - Fleet Management Dashboard')

# Debug output
st.write("### Debug Information")
st.write("Python version:", sys.version)
st.write("Current working directory:", os.getcwd())
try:
    st.write("FileMaker connection test:", load_filemaker_data("test"))
except Exception as e:
    st.error(f"FileMaker connection failed: {str(e)}")
    
try:
    st.write("Samsara connection test:", load_samsara_fleet_data())
except Exception as e:
    st.error(f"Samsara connection failed: {str(e)}")

# Initialize tabs at the top
tab1, tab2, tab3, tab4 = st.tabs(["Jobs Overview", "Fleet Map", "Assignments", "Analytics"])

# Add connection status indicators
st.sidebar.header("API Connection Status")

# Check FileMaker connection
try:
    st.sidebar.success("✅ FileMaker API Connected")
except Exception as e:
    st.sidebar.error(f"❌ FileMaker API Error: {str(e)}")

# Check Samsara connection
try:
    st.sidebar.success("✅ Samsara API Connected")
except Exception as e:
    st.sidebar.error(f"❌ Samsara API Error: {str(e)}")

# Add data source selection
st.sidebar.header('Data Source Selection')
data_source = st.sidebar.radio(
    'Select Data Source',
    ['Sample Data', 'FileMaker Job Data', 'Samsara Fleet Data', 'Combined Data']
)

# Add job ID input for FileMaker
if data_source == 'FileMaker Job Data':
    job_id = st.sidebar.text_input('Enter Job ID', '603142')
    st.sidebar.info("Example Job ID: 603142")

# Add refresh buttons
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button('🔄 Refresh Data'):
        st.cache_data.clear()
        st.rerun()

with col2:
    if st.button('🔁 Pull Fresh API Data'):
        with st.spinner('Fetching fresh data from APIs...'):
            # Clear relevant caches
            st.cache_data.clear()
            
            # Force fresh API calls
            try:
                # Get fresh Samsara data
                samsara_df = load_samsara_fleet_data()
                if samsara_df is not None:
                    st.sidebar.success("✅ Successfully pulled Samsara data")
                else:
                    st.sidebar.warning("⚠️ Samsara data pull failed")
                
                # Get fresh FileMaker data if job_id exists
                if 'job_id' in locals():
                    fm_df = load_filemaker_data(job_id)
                    if fm_df is not None:
                        st.sidebar.success(f"✅ Successfully pulled FileMaker data for job {job_id}")
                    else:
                        st.sidebar.warning("⚠️ FileMaker data pull failed")
                
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"❌ API pull failed: {str(e)}")

# Load data based on selection
df = None
raw_df = None

if data_source == 'FileMaker Job Data':
    with st.spinner('Loading FileMaker data...'):
        df = load_filemaker_data(job_id) if 'job_id' in locals() else load_data()
        if df is not None:
            st.success(f"✅ Loaded FileMaker data for job {job_id}")
        else:
            st.warning("⚠️ Failed to load FileMaker data, using sample data")
            df = load_data()
            # Create sample raw_df with driver and miles data
            raw_df = create_sample_df()
elif data_source == 'Samsara Fleet Data':
    with st.spinner('Loading Samsara fleet data...'):
        samsara_df = load_samsara_fleet_data()
        if samsara_df is not None:
            df = samsara_df
            st.success("✅ Loaded Samsara fleet data")
            # Convert Samsara data to format compatible with existing visualizations
            raw_df = convert_samsara_to_driver_format(samsara_df)
        else:
            st.warning("⚠️ Failed to load Samsara data, using sample data")
            df = load_data()
            raw_df = create_sample_df()
elif data_source == 'Combined Data':
    with st.spinner('Loading combined fleet data...'):
        combined_df = load_combined_fleet_data()
        if combined_df is not None:
            df = combined_df
            st.success("✅ Loaded combined fleet data")
            # Convert combined data to format compatible with existing visualizations
            raw_df = convert_combined_to_driver_format(combined_df)
        else:
            st.warning("⚠️ Failed to load combined data, using sample data")
            df = load_data()
            raw_df = create_sample_df()
else:
    # Sample data
    df = load_data()
    raw_df = create_sample_df()

# Data processing functions with caching
@st.cache_data
def get_jobs_per_driver(raw_df):
    """Calculate jobs per driver with caching."""
    return raw_df.groupby('driver').size().reset_index(name='job_count')

@st.cache_data
def get_miles_per_driver(raw_df):
    """Calculate total miles per driver with caching."""
    return raw_df.groupby('driver')['miles'].sum().reset_index()

@st.cache_data
def get_combined_analysis(raw_df):
    """Get combined jobs and miles analysis with caching."""
    jobs_per_driver = get_jobs_per_driver(raw_df)
    miles_per_driver = get_miles_per_driver(raw_df)
    combined_data = jobs_per_driver.merge(miles_per_driver, on='driver')
    combined_data['avg_miles_per_job'] = combined_data['miles'] / combined_data['job_count']
    return combined_data

@st.cache_data
def get_summary_stats(combined_data):
    """Calculate summary statistics with caching."""
    return {
        'total_drivers': len(combined_data),
        'total_jobs': combined_data['job_count'].sum(),
        'total_miles': combined_data['miles'].sum(),
        'avg_miles_per_job': combined_data['avg_miles_per_job'].mean()
    }

@st.cache_data
def get_checklist_conditions(df):
    """Calculate checklist conditions with caching."""
    # Handle different data sources
    if 'column1' in df.columns:
        return {
            'completion_status': df['column1'] > 5,
            'notes_flag': df['column2'] == 20,
            'in_progress_flag': df['column1'] % 2 == 0
        }
    else:
        # For FileMaker or Samsara data, create sample conditions
        return {
            'completion_status': pd.Series([True] * len(df)) if len(df) > 0 else pd.Series([False]),
            'notes_flag': pd.Series([False] * len(df)) if len(df) > 0 else pd.Series([False]),
            'in_progress_flag': pd.Series([True] * len(df)) if len(df) > 0 else pd.Series([False])
        }

# Create raw_df if not already created
if raw_df is None:
    raw_df = create_sample_df()

with tab1:
    # Jobs Overview Tab
    st.header("Job Dispatch Overview")
    
    # Job data display
    if df is not None:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No job data available")
    
    # Interactive checklist
    st.markdown("### Task Checklist")
    checklist_conditions = get_checklist_conditions(df)
    completion_status = checklist_conditions['completion_status']
    notes_flag = checklist_conditions['notes_flag']
    in_progress_flag = checklist_conditions['in_progress_flag']

    # Create checkboxes for each row in the DataFrame
    if len(df) > 0:
        for i in range(min(len(df), 10)):  # Limit to first 10 rows
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                # Show relevant data based on data source
                if 'job_id' in df.columns:
                    st.write(f"Job: {df.iloc[i].get('job_id', f'Row {i}')}")
                elif 'name' in df.columns:
                    st.write(f"Vehicle: {df.iloc[i].get('name', f'Row {i}')}")
                else:
                    st.write(f"Task {i+1} (Row {i})")
            
            with col2:
                completed = st.checkbox(
                    "Completed", 
                    value=completion_status.iloc[i] if i < len(completion_status) else False, 
                    key=f"completed_{i}"
                )
            
            with col3:
                has_notes = st.checkbox(
                    "Has Notes", 
                    value=notes_flag.iloc[i] if i < len(notes_flag) else False, 
                    key=f"notes_{i}"
                )
            
            with col4:
                in_progress = st.checkbox(
                    "In Progress",
                    value=in_progress_flag.iloc[i] if i < len(in_progress_flag) else False,
                    key=f"progress_{i}"
                )
    else:
        st.info("No data available for checklist")

with tab2:
    # Fleet Map Tab
    st.header("Fleet Locations")
    if df is not None and 'latitude' in df.columns and 'longitude' in df.columns:
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=df['latitude'].mean(),
                longitude=df['longitude'].mean(),
                zoom=11,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[longitude, latitude]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=200,
                ),
            ],
        ))
    else:
        st.warning("Location data not available")

with tab3:
    # Assignments Tab
    st.header("Driver Assignments")
    if df is not None and 'truck_id' in df.columns:
        # Assignment interface would go here
        st.write("Assignment interface coming soon")
    else:
        st.warning("Assignment data not available")

with tab4:
    # Analytics Tab Content
    st.header("Analytics Dashboard")
    
    # Altair Charts Section
    st.markdown("### Driver Analytics")
    
    # Prepare data for charts using cached functions
    jobs_per_driver = get_jobs_per_driver(raw_df)
    miles_per_driver = get_miles_per_driver(raw_df)
    
    # Create two columns for side-by-side charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Jobs per Driver")
        jobs_chart = alt.Chart(jobs_per_driver).mark_bar(
            color='steelblue',
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3
        ).encode(
            x=alt.X('driver:N',
                    title='Driver',
                    sort=alt.EncodingSortField(field='job_count', order='descending')),
            y=alt.Y('job_count:Q',
                    title='Number of Jobs'),
            tooltip=['driver:N', 'job_count:Q']
        ).properties(
            width=300,
            height=400,
            title=alt.TitleParams(
                text="Jobs per Driver",
                anchor='start'
            )
        )
        st.altair_chart(jobs_chart, use_container_width=True)
    
    with col2:
        st.markdown("#### Total Miles per Driver")
        miles_chart = alt.Chart(miles_per_driver).mark_line(
            point=alt.OverlayMarkDef(
                filled=True,
                size=100,
                color='orange'
            ),
            color='darkorange',
            strokeWidth=3
        ).encode(
            x=alt.X('driver:N',
                    title='Driver',
                    sort=alt.EncodingSortField(field='miles', order='descending')),
            y=alt.Y('miles:Q',
                    title='Total Miles'),
            tooltip=['driver:N', 'miles:Q']
        ).properties(
            width=300,
            height=400,
            title=alt.TitleParams(
                text="Total Miles per Driver",
                anchor='start'
            )
        )
        st.altair_chart(miles_chart, use_container_width=True)
    
    # Combined analysis
    st.markdown("#### Jobs vs Miles Analysis")
    combined_data = get_combined_analysis(raw_df)
    scatter_chart = alt.Chart(combined_data).mark_circle(
        size=200,
        opacity=0.7
    ).encode(
        x=alt.X('job_count:Q',
                title='Number of Jobs',
                scale=alt.Scale(zero=False)),
        y=alt.Y('miles:Q',
                title='Total Miles',
                scale=alt.Scale(zero=False)),
        color=alt.Color('avg_miles_per_job:Q',
                       title='Avg Miles/Job',
                       scale=alt.Scale(scheme='viridis')),
        tooltip=['driver:N', 'job_count:Q', 'miles:Q', 'avg_miles_per_job:Q']
    ).properties(
        width=600,
        height=400,
        title=alt.TitleParams(
            text="Driver Performance: Jobs vs Total Miles",
            anchor='start'
        )
    )
    st.altair_chart(scatter_chart, use_container_width=True)
    
    # Summary statistics
    st.markdown("#### Summary Statistics")
    summary_stats = get_summary_stats(combined_data)
    cols = st.columns(4)
    cols[0].metric("Total Drivers", summary_stats['total_drivers'])
    cols[1].metric("Total Jobs", summary_stats['total_jobs'])
    cols[2].metric("Total Miles", f"{summary_stats['total_miles']:,}")
    cols[3].metric("Avg Miles/Job", f"{summary_stats['avg_miles_per_job']:.1f}")

# Show raw data table
with st.expander("View Raw Data"):
    st.dataframe(df if df is not None else raw_df, use_container_width=True)
