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

# Set up the page configuration
st.set_page_config(page_title='PEP Workday - Fleet Management Dashboard', layout='wide')

# Add role selection to the sidebar
st.sidebar.header('User Role Selection')
user_role = st.sidebar.selectbox(
    'Select your role',
    ['CSR', 'Dispatcher', 'Operations Manager']
)

# Add a simple alert system
def show_alerts():
    """Display alerts based on data conditions."""
    # In a real implementation, these would be based on actual data conditions
    alerts = []
    
    # Example alerts (in a real app, these would be dynamic based on data)
    if user_role == 'Dispatcher':
        alerts.append(("warning", "Driver John Smith is running 30 minutes behind schedule"))
        alerts.append(("info", "New job assignment available for Driver Jane Doe"))
    elif user_role == 'Operations Manager':
        alerts.append(("error", "Truck #245 requires immediate maintenance"))
        alerts.append(("warning", "Capacity at 85% for tomorrow's schedule"))
        alerts.append(("info", "New driver certification completed"))
    elif user_role == 'CSR':
        alerts.append(("info", "Customer ABC Corp has a scheduled job today"))
        alerts.append(("warning", "Job #603142 requires a callback"))
    
    # Display alerts
    if alerts:
        st.sidebar.header("Alerts")
        for alert_type, message in alerts:
            if alert_type == "error":
                st.sidebar.error(f"🚨 {message}")
            elif alert_type == "warning":
                st.sidebar.warning(f"⚠️ {message}")
            elif alert_type == "info":
                st.sidebar.info(f"ℹ️ {message}")

# Show alerts in the sidebar
show_alerts()

# Set the title based on the selected role
if user_role == 'CSR':
    st.title('PEP Workday - Customer Service Dashboard')
elif user_role == 'Dispatcher':
    st.title('PEP Workday - Dispatch Dashboard')
elif user_role == 'Operations Manager':
    st.title('PEP Workday - Operations Management Dashboard')
else:
    st.title('PEP Workday - Fleet Management Dashboard')


# Initialize tabs at the top
tab1, tab2, tab3, tab4 = st.tabs(["Jobs Overview", "Fleet Map", "Assignments", "Analytics"])


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
            # Also clear session state to force reload
            if 'df' in st.session_state:
                del st.session_state.df
            if 'raw_df' in st.session_state:
                del st.session_state.raw_df
            
            # Force fresh API calls
            api_success = True
            try:
                # Get fresh Samsara data
                samsara_df = load_samsara_fleet_data()
                if samsara_df is not None and not samsara_df.empty:
                    st.sidebar.success("✅ Successfully pulled Samsara data")
                else:
                    st.sidebar.warning("⚠️ Samsara data pull returned no data")
                    api_success = False
                
                # Get fresh FileMaker data if job_id exists and FileMaker is selected
                if data_source == 'FileMaker Job Data' and 'job_id' in locals():
                    fm_df = load_filemaker_data(job_id)
                    if fm_df is not None and not fm_df.empty:
                        st.sidebar.success(f"✅ Successfully pulled FileMaker data for job {job_id}")
                    else:
                        st.sidebar.warning("⚠️ FileMaker data pull returned no data")
                        api_success = False
                
                if api_success:
                    st.success("✅ All API data refreshed successfully")
                else:
                    st.warning("⚠️ Some API calls returned no data. Using available data.")
                
                # Mark data as not loaded to force reload
                if 'data_loaded' in st.session_state:
                    del st.session_state.data_loaded
                
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"❌ API pull failed: {str(e)}")
                st.error("Failed to refresh API data. Please check your connection and credentials.")

# Load data based on selection with improved error handling and lazy loading
df = None
raw_df = None

# Only load data when needed (lazy loading)
data_loaded = st.session_state.get('data_loaded', False)
current_data_source = st.session_state.get('data_source', None)

# Check if we need to load data (either first time or data source changed)
if not data_loaded or current_data_source != data_source:
    st.session_state.data_loaded = True
    st.session_state.data_source = data_source
    st.session_state.df = None
    st.session_state.raw_df = None

# Load data if not already in session state
if 'df' not in st.session_state or st.session_state.df is None:
    if data_source == 'FileMaker Job Data':
        with st.spinner('Loading FileMaker data...'):
            try:
                df = load_filemaker_data(job_id) if 'job_id' in locals() else load_data()
                if df is not None and not df.empty:
                    st.success(f"✅ Loaded FileMaker data for job {job_id}")
                    st.session_state.df = df
                    # Create sample raw_df with driver and miles data for visualization
                    st.session_state.raw_df = create_sample_df()  # Using sample for now, could convert actual data
                else:
                    st.warning("⚠️ No data found for this job ID or failed to load FileMaker data, using sample data")
                    st.session_state.df = load_data()
                    st.session_state.raw_df = create_sample_df()
            except Exception as e:
                st.error(f"❌ Error loading FileMaker data: {str(e)}")
                st.info("Using sample data as fallback")
                st.session_state.df = load_data()
                st.session_state.raw_df = create_sample_df()
    elif data_source == 'Samsara Fleet Data':
        with st.spinner('Loading Samsara fleet data...'):
            try:
                samsara_df = load_samsara_fleet_data()
                if samsara_df is not None and not samsara_df.empty:
                    st.success("✅ Loaded Samsara fleet data")
                    st.session_state.df = samsara_df
                    # Convert Samsara data to format compatible with existing visualizations
                    st.session_state.raw_df = convert_samsara_to_driver_format(samsara_df)
                else:
                    st.warning("⚠️ No Samsara data available or failed to load, using sample data")
                    st.session_state.df = load_data()
                    st.session_state.raw_df = create_sample_df()
            except Exception as e:
                st.error(f"❌ Error loading Samsara data: {str(e)}")
                st.info("Using sample data as fallback")
                st.session_state.df = load_data()
                st.session_state.raw_df = create_sample_df()
    elif data_source == 'Combined Data':
        with st.spinner('Loading combined fleet data...'):
            try:
                combined_df = load_combined_fleet_data()
                if combined_df is not None and not combined_df.empty:
                    st.success("✅ Loaded combined fleet data")
                    st.session_state.df = combined_df
                    # Convert combined data to format compatible with existing visualizations
                    st.session_state.raw_df = convert_combined_to_driver_format(combined_df)
                else:
                    st.warning("⚠️ No combined data available or failed to load, using sample data")
                    st.session_state.df = load_data()
                    st.session_state.raw_df = create_sample_df()
            except Exception as e:
                st.error(f"❌ Error loading combined data: {str(e)}")
                st.info("Using sample data as fallback")
                st.session_state.df = load_data()
                st.session_state.raw_df = create_sample_df()
    else:
        # Sample data
        st.session_state.df = load_data()
        st.session_state.raw_df = create_sample_df()

# Use data from session state
df = st.session_state.df
raw_df = st.session_state.raw_df

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
    # Jobs Overview Tab - Customized based on user role
    if user_role == 'CSR':
        st.header("Today's Jobs")
        st.markdown("Quick access to customer and job information for today's jobs.")
        
        # Add a search box for job/customer lookup
        search_term = st.text_input("Search jobs by ID, customer, or address", "")
        
        # Filter data based on search term if provided
        if search_term and df is not None:
            # Try to filter the dataframe based on search term
            filtered_df = df[df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)]
            if not filtered_df.empty:
                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.info("No jobs found matching your search criteria.")
        elif df is not None:
            # Show today's jobs (for now, showing all data)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No job data available")
            
    elif user_role == 'Dispatcher':
        st.header("Job Dispatch Overview")
        st.markdown("View job details and status for all active jobs.")
        
        # Job data display
        if df is not None:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No job data available")
            
    elif user_role == 'Operations Manager':
        st.header("Live Schedule")
        st.markdown("View and manage the live schedule for all jobs.")
        
        # Show schedule view
        if df is not None:
            # For now, showing the same data but with different context
            st.dataframe(df, use_container_width=True)
            st.markdown("Use the controls below to block parts of the schedule or adjust capacity planning.")
        else:
            st.warning("No schedule data available")
    else:
        # Default view
        st.header("Job Dispatch Overview")
        
        # Job data display
        if df is not None:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No job data available")

with tab2:
    # Fleet Map Tab - Customized based on user role
    if user_role == 'Dispatcher':
        st.header("Technician Locations")
        st.markdown("Live map showing technician locations and job details.")
        
        if df is not None and 'latitude' in df.columns and 'longitude' in df.columns:
            # Create a more detailed map with job information
            map_data = df[['latitude', 'longitude']].copy()
            if 'job_id' in df.columns:
                map_data['job_id'] = df['job_id']
            if 'driver' in df.columns:
                map_data['driver'] = df['driver']
            if 'status' in df.columns:
                map_data['status'] = df['status']
            
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
                        data=map_data,
                        get_position='[longitude, latitude]',
                        get_color='[200, 30, 0, 160]',
                        get_radius=200,
                        pickable=True,
                        auto_highlight=True,
                    ),
                ],
                tooltip={
                    "html": "<b>Job ID:</b> {job_id}<br/><b>Driver:</b> {driver}<br/><b>Status:</b> {status}",
                    "style": {"backgroundColor": "steelblue", "color": "white"}
                }
            ))
        else:
            st.warning("Location data not available")
    elif user_role == 'Operations Manager':
        st.header("Fleet Locations")
        st.markdown("Live map showing fleet locations with capacity planning indicators.")
        
        if df is not None and 'latitude' in df.columns and 'longitude' in df.columns:
            # Create a map with capacity planning indicators
            map_data = df[['latitude', 'longitude']].copy()
            if 'driver' in df.columns:
                map_data['driver'] = df['driver']
            if 'truck_id' in df.columns:
                map_data['truck_id'] = df['truck_id']
            # Add a simple capacity indicator (for now, just showing all vehicles)
            map_data['capacity'] = 100  # Placeholder for capacity percentage
            
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
                        data=map_data,
                        get_position='[longitude, latitude]',
                        get_color='[200, 30, 0, 160]',
                        get_radius=200,
                        pickable=True,
                        auto_highlight=True,
                    ),
                ],
                tooltip={
                    "html": "<b>Truck ID:</b> {truck_id}<br/><b>Driver:</b> {driver}<br/><b>Capacity:</b> {capacity}%",
                    "style": {"backgroundColor": "steelblue", "color": "white"}
                }
            ))
        else:
            st.warning("Location data not available")
    else:
        # Default view
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
    # Assignments Tab - Customized based on user role
    if user_role == 'Dispatcher':
        st.header("Driver Assignments")
        st.markdown("Assign drivers to jobs and manage current assignments.")
        
        if df is not None:
            # Show assignment interface
            st.subheader("Current Assignments")
            # Filter to show only relevant columns for assignments
            assignment_cols = [col for col in ['job_id', 'driver', 'truck_id', 'status'] if col in df.columns]
            if assignment_cols:
                st.dataframe(df[assignment_cols], use_container_width=True)
            else:
                st.dataframe(df, use_container_width=True)
            
            # Add assignment controls
            st.subheader("Assign Driver to Job")
            with st.form("assignment_form"):
                job_id = st.selectbox("Select Job", df['job_id'].unique() if 'job_id' in df.columns else [])
                driver = st.selectbox("Select Driver", df['driver'].unique() if 'driver' in df.columns else [])
                truck_id = st.selectbox("Select Truck", df['truck_id'].unique() if 'truck_id' in df.columns else [])
                submitted = st.form_submit_button("Assign")
                if submitted:
                    st.success(f"Assigned {driver} with truck {truck_id} to job {job_id}")
        else:
            st.warning("Assignment data not available")
            
    elif user_role == 'Operations Manager':
        st.header("Capacity Planning")
        st.markdown("Manage resource allocation and view flagged issues.")
        
        if df is not None:
            # Show capacity planning interface
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Resource Allocation")
                # Show a simple capacity chart
                if 'driver' in df.columns:
                    driver_counts = df['driver'].value_counts()
                    st.bar_chart(driver_counts)
                
                # Add controls to block parts of the schedule
                st.subheader("Schedule Blocking")
                with st.form("block_schedule"):
                    block_date = st.date_input("Date to block")
                    block_reason = st.text_input("Reason for blocking")
                    block_submitted = st.form_submit_button("Block Schedule")
                    if block_submitted:
                        st.success(f"Blocked schedule for {block_date} due to: {block_reason}")
            
            with col2:
                st.subheader("Flagged Issues")
                # Show flagged issues (for now, just showing all data as potential issues)
                st.dataframe(df, use_container_width=True)
                
                # Add a way to flag new issues
                st.subheader("Flag New Issue")
                with st.form("flag_issue"):
                    issue_job_id = st.selectbox("Select Job", df['job_id'].unique() if 'job_id' in df.columns else [])
                    issue_description = st.text_area("Issue Description")
                    issue_priority = st.select_slider("Priority", options=["Low", "Medium", "High", "Critical"])
                    flag_submitted = st.form_submit_button("Flag Issue")
                    if flag_submitted:
                        st.success(f"Flagged issue for job {issue_job_id} with priority {issue_priority}")
        else:
            st.warning("Capacity planning data not available")
    else:
        # Default view
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
