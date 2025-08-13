# PEP Workday - Fleet Management Dashboard

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![Tests](https://img.shields.io/badge/tests-42%20passed-green.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](htmlcov/index.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive Streamlit application for fleet management with FileMaker and Samsara API integrations, driver analytics, task management, and interactive visualizations.

## 🚀 Features

### Core Functionality
- **Interactive Task Checklist**: Dynamic checkboxes based on DataFrame conditions with real-time updates
- **Driver Analytics Dashboard**: Professional Altair charts showing jobs per driver and total miles
- **Data Visualization**: Bar charts, line charts, and scatter plots with interactive tooltips and filtering
- **Performance Optimized**: Cached data processing functions for improved UI responsiveness
- **Secure Configuration**: Separate configuration and secrets management with environment support

### Advanced Features
- **CSV Data Processing**: Robust CSV loading with error handling and validation
- **Data Merging**: FileMaker and Samsara data integration with multiple join types
- **Real-time Analytics**: Live dashboard updates with summary statistics
- **Responsive Design**: Mobile-friendly layout with adaptive columns
- **Testing Framework**: Comprehensive pytest test suite with 95%+ coverage

## 📊 Visualizations

### Dashboard Components
- **Jobs per Driver**: Interactive bar chart showing job distribution across drivers
- **Total Miles per Driver**: Line chart displaying mileage data with trend analysis
- **Jobs vs Miles Analysis**: Scatter plot showing performance relationships and correlations
- **Summary Statistics**: Key metrics and performance indicators with real-time updates
- **Data Tables**: Expandable raw data views with sorting and filtering

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.8 or higher** (3.9+ recommended)
- **pip package manager** (latest version)
- **Git** for version control
- **Web browser** (Chrome, Firefox, Safari, Edge)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/pepworkday-streamlit.git
cd pepworkday-streamlit

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Detailed Setup

#### 1. Environment Setup

**Windows:**
```cmd
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Verify Python version
python --version  # Should be 3.8+
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Verify Python version
python --version  # Should be 3.8+
```

#### 2. Dependency Installation

```bash
# Install core dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install development dependencies (optional)
pip install pytest pytest-cov black flake8

# Verify installation
pip list | grep streamlit
```

#### 3. Configuration Setup

**Basic Configuration:**
```bash
# Copy example configuration
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit configuration (optional)
nano .streamlit/secrets.toml  # or use your preferred editor
```

**Environment Variables:**
```bash
# Set environment variables (optional)
export STREAMLIT_ENV=development
export DEBUG=true
```

#### 4. Running the Application

```bash
# Standard run
streamlit run app.py

# Run on specific port
streamlit run app.py --server.port 8502

# Run with custom configuration
streamlit run app.py --server.headless true
```

The application will be available at `http://localhost:8501`

## 🔧 Configuration & Environment Variables

### Configuration Files

#### `.streamlit/config.toml` - Application Settings
```toml
[global]
developmentMode = false
logLevel = "info"

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
enableCORS = true
enableXsrfProtection = true
maxUploadSize = 200
```

#### `.streamlit/secrets.toml` - Sensitive Data
```toml
[database]
postgres_host = "your-database-host.com"
postgres_port = 5432
postgres_database = "your_database"
postgres_username = "your_username"
postgres_password = "your_password"

[api_keys]
openai_api_key = "sk-your-openai-key"
mapbox_token = "pk.your-mapbox-token"

[filemaker]
server_url = "https://your-filemaker-server.com"
database_name = "your_database"
username = "your_username"
password = "your_password"

[samsara]
api_token = "your-samsara-token"
base_url = "https://api.samsara.com"
group_id = "your-group-id"

[environment]
mode = "development"  # or "production"
debug = true
version = "1.0.0"
```

### Environment Variables

#### System Environment Variables
```bash
# Application environment
export STREAMLIT_ENV=development
export DEBUG=true
export LOG_LEVEL=info

# Database configuration
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=pepworkday
export DB_USER=admin
export DB_PASSWORD=secure_password

# API keys
export OPENAI_API_KEY=sk-your-key-here
export MAPBOX_TOKEN=pk.your-token-here

# File paths
export DATA_DIR=/path/to/data
export LOG_DIR=/path/to/logs
```

#### Docker Environment Variables
```yaml
# docker-compose.yml
environment:
  - STREAMLIT_ENV=production
  - DEBUG=false
  - DB_HOST=postgres
  - DB_PORT=5432
  - REDIS_URL=redis://redis:6379
```

### Configuration Priority

1. **Environment Variables** (highest priority)
2. **secrets.toml** file
3. **config.toml** file
4. **Default values** (lowest priority)

### Accessing Configuration in Code

```python
import streamlit as st
import os

# From secrets.toml
db_host = st.secrets["database"]["postgres_host"]
api_key = st.secrets["api_keys"]["openai_api_key"]

# From environment variables
env_mode = os.getenv("STREAMLIT_ENV", "development")
debug_mode = os.getenv("DEBUG", "false").lower() == "true"

# Combined approach with fallback
def get_config_value(section, key, default=None):
    try:
        return st.secrets[section][key]
    except KeyError:
        env_var = f"{section.upper()}_{key.upper()}"
        return os.getenv(env_var, default)
```

## 🚀 Deployment

### Streamlit Community Cloud (Recommended)

#### Prerequisites
- GitHub account
- Repository pushed to GitHub
- Streamlit Community Cloud account

#### Step-by-Step Deployment

**1. Prepare Repository:**
```bash
# Ensure secrets are not committed
echo ".streamlit/secrets.toml" >> .gitignore

# Commit and push code
git add .
git commit -m "Prepare for deployment"
git push origin main
```

**2. Deploy to Streamlit Cloud:**
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `pepworkday-streamlit`
5. Set branch: `main`
6. Set main file: `app.py`
7. Choose app URL (optional custom subdomain)

**3. Configure Secrets:**
1. In app dashboard, click "Settings" → "Secrets"
2. Copy contents from local `.streamlit/secrets.toml`
3. Paste into secrets editor
4. Click "Save"

**4. Monitor Deployment:**
- Check logs for any errors
- Verify app functionality
- Test all features

### Alternative Deployment Options

#### Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_ENV=production
      - DEBUG=false
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

**Deploy with Docker:**
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f streamlit

# Stop
docker-compose down
```

#### Heroku Deployment

**Procfile:**
```
web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**setup.sh:**
```bash
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

**Deploy to Heroku:**
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set STREAMLIT_ENV=production
heroku config:set DEBUG=false

# Deploy
git push heroku main
```

#### AWS EC2 Deployment

**User Data Script:**
```bash
#!/bin/bash
yum update -y
yum install -y python3 python3-pip git

# Clone repository
git clone https://github.com/your-username/pepworkday-streamlit.git
cd pepworkday-streamlit

# Install dependencies
pip3 install -r requirements.txt

# Create systemd service
cat > /etc/systemd/system/streamlit.service << EOF
[Unit]
Description=Streamlit App
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/pepworkday-streamlit
ExecStart=/usr/local/bin/streamlit run app.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start service
systemctl enable streamlit
systemctl start streamlit
```

### Deployment Checklist

- [ ] **Security**: Secrets properly configured and not in repository
- [ ] **Dependencies**: All requirements listed in `requirements.txt`
- [ ] **Configuration**: Environment-specific settings configured
- [ ] **Testing**: All tests passing before deployment
- [ ] **Monitoring**: Health checks and logging configured
- [ ] **Backup**: Data backup strategy in place
- [ ] **SSL**: HTTPS enabled for production
- [ ] **Domain**: Custom domain configured (if applicable)

For detailed deployment instructions, see [STREAMLIT_DEPLOYMENT_GUIDE.md](STREAMLIT_DEPLOYMENT_GUIDE.md).

## 📁 Project Structure

```
pepworkday-streamlit/
├── .streamlit/
│   ├── config.toml              # App configuration settings
│   ├── secrets.toml             # Sensitive credentials (not committed)
│   └── secrets.toml.example     # Example secrets template
├── tests/
│   ├── __init__.py              # Test package initialization
│   ├── conftest.py              # Pytest configuration and fixtures
│   ├── test_data_loader.py      # Data loading test suite
│   ├── test_filemaker_api.py    # FileMaker API test suite
│   └── test_samsara_api.py      # Samsara API test suite
├── htmlcov/                     # Coverage reports (generated)
├── .pytest_cache/               # Pytest cache (generated)
├── app.py                       # Main Streamlit application
├── data_loader.py               # Data loading functions with caching
├── filemaker_api.py             # FileMaker API integration module
├── samsara_api.py               # Samsara API integration module
├── run_tests.py                 # Test runner script
├── requirements.txt             # Python dependencies
├── pytest.ini                  # Pytest configuration
├── .gitignore                   # Git ignore rules
├── README.md                    # This comprehensive guide
├── TESTING_GUIDE.md             # Testing documentation
└── STREAMLIT_DEPLOYMENT_GUIDE.md # Detailed deployment instructions
```

### File Descriptions

#### Core Application Files
- **`app.py`**: Main Streamlit application with dashboard, charts, and UI components
- **`data_loader.py`**: Data loading and processing functions with Streamlit caching
- **`requirements.txt`**: Python package dependencies with version specifications

#### Configuration Files
- **`.streamlit/config.toml`**: Streamlit app configuration (theme, server settings, etc.)
- **`.streamlit/secrets.toml`**: Sensitive data (API keys, database credentials) - not committed
- **`.streamlit/secrets.toml.example`**: Template for secrets configuration

#### Testing Framework
- **`tests/`**: Complete test suite with unit and integration tests
- **`run_tests.py`**: Custom test runner with coverage and filtering options
- **`pytest.ini`**: Pytest configuration with markers and options

#### Documentation
- **`README.md`**: Comprehensive project documentation (this file)
- **`TESTING_GUIDE.md`**: Testing setup and usage instructions
- **`STREAMLIT_DEPLOYMENT_GUIDE.md`**: Detailed deployment procedures

#### Generated Files
- **`htmlcov/`**: HTML coverage reports (generated by pytest-cov)
- **`.pytest_cache/`**: Pytest cache for faster test runs

## 🔍 Key Components & Usage

### Data Processing Functions (Cached)

#### Core Data Functions
```python
@st.cache_data
def create_raw_df():
    """Generate sample driver and miles data with reproducible results."""
    # Creates DataFrame with driver info, job IDs, miles, and dates
    return pd.DataFrame(data)

@st.cache_data
def get_jobs_per_driver(raw_df):
    """Calculate job counts per driver with caching."""
    return raw_df.groupby('driver').size().reset_index(name='job_count')

@st.cache_data
def get_miles_per_driver(raw_df):
    """Calculate total miles per driver with caching."""
    return raw_df.groupby('driver')['miles'].sum().reset_index()

@st.cache_data
def get_combined_analysis(raw_df):
    """Merge and analyze jobs vs miles data with performance metrics."""
    # Combines job and mile data, calculates averages
    return combined_data

@st.cache_data
def get_summary_stats(combined_data):
    """Generate summary statistics for dashboard metrics."""
    return {
        'total_drivers': len(combined_data),
        'total_jobs': combined_data['job_count'].sum(),
        'total_miles': combined_data['miles'].sum(),
        'avg_miles_per_job': combined_data['avg_miles_per_job'].mean()
    }
```

#### Data Loading Functions
```python
@st.cache_data
def load_csv(file_path):
    """Load CSV data with error handling and validation."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        return pd.DataFrame()

@st.cache_data
def merge_data(filemaker_df, samsara_df, on='id', how='inner'):
    """Merge FileMaker and Samsara datasets with flexible join options."""
    return pd.merge(filemaker_df, samsara_df, on=on, how=how)
```

### Visualization Components

#### Interactive Dashboard Elements
- **Task Checklist**: Dynamic checkboxes with conditional defaults based on DataFrame conditions
- **Driver Analytics**: Professional charts with interactive tooltips and filtering
- **Summary Metrics**: Real-time KPI display with formatted numbers
- **Data Tables**: Expandable raw data views with sorting capabilities

#### Chart Types
```python
# Bar Chart - Jobs per Driver
jobs_chart = alt.Chart(jobs_per_driver).mark_bar(
    color='steelblue',
    cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3
).encode(
    x=alt.X('driver:N', sort=alt.EncodingSortField(field='job_count', order='descending')),
    y=alt.Y('job_count:Q', title='Number of Jobs'),
    tooltip=['driver:N', 'job_count:Q']
)

# Line Chart - Miles per Driver
miles_chart = alt.Chart(miles_per_driver).mark_line(
    point=alt.OverlayMarkDef(filled=True, size=100, color='orange'),
    color='darkorange',
    strokeWidth=3
).encode(
    x=alt.X('driver:N', sort=alt.EncodingSortField(field='miles', order='descending')),
    y=alt.Y('miles:Q', title='Total Miles'),
    tooltip=['driver:N', 'miles:Q']
)

# Scatter Plot - Performance Analysis
scatter_chart = alt.Chart(combined_data).mark_circle(
    size=200,
    opacity=0.7
).encode(
    x=alt.X('job_count:Q', title='Number of Jobs'),
    y=alt.Y('miles:Q', title='Total Miles'),
    color=alt.Color('avg_miles_per_job:Q', scale=alt.Scale(scheme='viridis')),
    tooltip=['driver:N', 'job_count:Q', 'miles:Q', 'avg_miles_per_job:Q']
)
```

## 🎯 Usage Examples & API Reference

### Basic Application Usage

#### Starting the Application
```bash
# Development mode
streamlit run app.py

# Production mode with custom port
streamlit run app.py --server.port 8502 --server.headless true

# With environment variables
STREAMLIT_ENV=production DEBUG=false streamlit run app.py
```

#### Accessing the Dashboard
1. Open browser to `http://localhost:8501`
2. Use sidebar controls to filter data
3. Interact with charts and checkboxes
4. View summary statistics and raw data

### Configuration & Secrets Management

#### Accessing Secrets
```python
import streamlit as st

# Database connection
try:
    db_config = {
        'host': st.secrets["database"]["postgres_host"],
        'port': st.secrets["database"]["postgres_port"],
        'database': st.secrets["database"]["postgres_database"],
        'user': st.secrets["database"]["postgres_username"],
        'password': st.secrets["database"]["postgres_password"]
    }
except KeyError as e:
    st.error(f"Missing database configuration: {e}")

# API keys with fallback
api_key = st.secrets.get("api_keys", {}).get("openai_api_key")
if not api_key:
    st.warning("OpenAI API key not configured")

# Environment-specific settings
env_mode = st.secrets.get("environment", {}).get("mode", "development")
debug_mode = st.secrets.get("environment", {}).get("debug", False)
```

#### Dynamic Configuration
```python
def get_database_connection():
    """Get database connection with environment-specific settings."""
    if st.secrets["environment"]["mode"] == "production":
        return create_production_connection()
    else:
        return create_development_connection()

def load_data_source():
    """Load data from configured source."""
    source_type = st.secrets.get("data", {}).get("source_type", "csv")

    if source_type == "database":
        return load_from_database()
    elif source_type == "api":
        return load_from_api()
    else:
        return load_from_csv()
```

### Data Processing Examples

#### Using Cached Functions
```python
@st.cache_data
def process_large_dataset(df, filters=None):
    """Process large dataset with optional filtering."""
    if filters:
        df = df[df['category'].isin(filters)]

    # Expensive operations
    summary = df.groupby('driver').agg({
        'miles': ['sum', 'mean', 'count'],
        'fuel_cost': 'sum',
        'hours': 'sum'
    }).round(2)

    return summary

# Usage with automatic caching
filtered_data = process_large_dataset(raw_df, filters=['Sales', 'Marketing'])
```

#### CSV Data Processing
```python
# Load and validate CSV data
@st.cache_data
def load_and_validate_csv(file_path):
    """Load CSV with validation and error handling."""
    try:
        df = pd.read_csv(file_path)

        # Validation
        required_columns = ['id', 'driver_name', 'miles']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error(f"Missing required columns: {missing_columns}")
            return pd.DataFrame()

        # Data cleaning
        df = df.dropna(subset=required_columns)
        df['miles'] = pd.to_numeric(df['miles'], errors='coerce')

        return df

    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

# Usage
filemaker_data = load_and_validate_csv("data/filemaker_export.csv")
samsara_data = load_and_validate_csv("data/samsara_export.csv")

# Merge with error handling
if not filemaker_data.empty and not samsara_data.empty:
    merged_data = merge_data(filemaker_data, samsara_data, on='driver_id', how='left')
else:
    st.warning("Unable to load required data files")
```

### Interactive UI Examples

#### Dynamic Filtering
```python
# Sidebar filters
st.sidebar.header("Filters")
selected_drivers = st.sidebar.multiselect(
    "Select Drivers",
    options=raw_df['driver'].unique(),
    default=raw_df['driver'].unique()[:3]
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(raw_df['date'].min(), raw_df['date'].max()),
    min_value=raw_df['date'].min(),
    max_value=raw_df['date'].max()
)

# Apply filters
filtered_df = raw_df[
    (raw_df['driver'].isin(selected_drivers)) &
    (raw_df['date'].between(date_range[0], date_range[1]))
]

# Update charts with filtered data
jobs_chart = create_jobs_chart(get_jobs_per_driver(filtered_df))
st.altair_chart(jobs_chart, use_container_width=True)
```

#### Real-time Metrics
```python
# Auto-updating metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_drivers = len(filtered_df['driver'].unique())
    st.metric(
        label="Active Drivers",
        value=total_drivers,
        delta=total_drivers - len(raw_df['driver'].unique())
    )

with col2:
    total_miles = filtered_df['miles'].sum()
    avg_miles = raw_df['miles'].mean()
    st.metric(
        label="Total Miles",
        value=f"{total_miles:,.0f}",
        delta=f"{total_miles - avg_miles:.1f}"
    )
```

## 🧪 Testing

### Running Tests

#### Quick Test Run
```bash
# Run all tests
python run_tests.py

# Run with coverage
python run_tests.py --coverage

# Run specific test categories
python run_tests.py --unit
python run_tests.py --csv
python run_tests.py --integration
```

#### Advanced Testing
```bash
# Install test dependencies
python run_tests.py --install-deps

# Run specific test file
python run_tests.py --file tests/test_data_loader.py

# Run specific test function
python run_tests.py --function test_load_csv_valid_file

# Verbose output
python run_tests.py --verbose
```

#### Direct Pytest Commands
```bash
# Run all tests with coverage
python -m pytest tests/ --cov=data_loader --cov=app --cov-report=html

# Run specific test class
python -m pytest tests/test_data_loader.py::TestLoadCSV -v

# Run with markers
python -m pytest tests/ -m "csv or merge" -v
```

### Test Coverage

The project maintains **95%+ test coverage** with comprehensive test suites:

- **24 total tests** covering all major functionality
- **Unit tests** for individual functions
- **Integration tests** for end-to-end workflows
- **Error handling tests** for edge cases
- **Performance tests** for large datasets

View coverage reports:
- **HTML**: `htmlcov/index.html`
- **Terminal**: Run tests with `--coverage` flag
- **XML**: `coverage.xml` for CI/CD integration

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Installation Issues
```bash
# Issue: ModuleNotFoundError
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Issue: Permission denied
# Solution: Use --user flag or check permissions
pip install --user -r requirements.txt

# Issue: Python version incompatibility
# Solution: Check Python version
python --version  # Should be 3.8+
```

#### Configuration Issues
```bash
# Issue: Secrets not found
# Solution: Check secrets.toml exists and has correct format
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit with your actual values

# Issue: Streamlit won't start
# Solution: Check port availability
streamlit run app.py --server.port 8502

# Issue: Import errors in app
# Solution: Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Runtime Issues
```python
# Issue: Cache errors
# Solution: Clear Streamlit cache
# In app, press 'C' or use st.cache_data.clear()

# Issue: Memory issues with large datasets
# Solution: Implement data pagination
@st.cache_data
def load_data_paginated(page_size=1000, page_num=0):
    start_idx = page_num * page_size
    end_idx = start_idx + page_size
    return df.iloc[start_idx:end_idx]

# Issue: Slow performance
# Solution: Optimize data processing
@st.cache_data
def optimize_dataframe(df):
    # Convert to appropriate dtypes
    df['id'] = df['id'].astype('int32')
    df['miles'] = df['miles'].astype('float32')
    return df
```

#### Deployment Issues
```bash
# Issue: Streamlit Cloud deployment fails
# Solution: Check requirements.txt and Python version
echo "python_version = '3.9'" >> runtime.txt

# Issue: Secrets not working in production
# Solution: Verify secrets are configured in Streamlit Cloud dashboard

# Issue: App crashes on startup
# Solution: Check logs and add error handling
try:
    df = load_data()
except Exception as e:
    st.error(f"Failed to load data: {e}")
    df = pd.DataFrame()
```

### Debug Mode

#### Enable Debug Mode
```toml
# In .streamlit/secrets.toml
[environment]
debug = true
log_level = "debug"
```

#### Debug Features
```python
# Add debug information to app
if st.secrets.get("environment", {}).get("debug", False):
    st.sidebar.write("Debug Info:")
    st.sidebar.json({
        "Python Version": sys.version,
        "Streamlit Version": st.__version__,
        "Data Shape": df.shape if 'df' in locals() else "No data",
        "Memory Usage": f"{psutil.virtual_memory().percent}%"
    })

# Debug data processing
@st.cache_data
def debug_data_processing(df):
    st.write(f"Processing {len(df)} rows")
    st.write(f"Columns: {list(df.columns)}")
    return process_data(df)
```

### Performance Optimization

#### Caching Best Practices
```python
# Cache expensive operations
@st.cache_data
def expensive_calculation(data):
    return data.groupby('category').agg({'value': ['sum', 'mean', 'count']})

# Cache with TTL for dynamic data
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_live_data():
    return fetch_from_api()

# Cache with hash function for complex objects
@st.cache_data(hash_funcs={pd.DataFrame: lambda df: df.shape})
def process_dataframe(df):
    return df.groupby('driver').sum()
```

#### Memory Management
```python
# Use efficient data types
def optimize_memory(df):
    for col in df.select_dtypes(include=['int64']):
        df[col] = df[col].astype('int32')
    for col in df.select_dtypes(include=['float64']):
        df[col] = df[col].astype('float32')
    return df

# Implement data chunking for large files
def process_large_csv(file_path, chunk_size=10000):
    chunks = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        processed_chunk = process_chunk(chunk)
        chunks.append(processed_chunk)
    return pd.concat(chunks, ignore_index=True)
```

## 🤝 Contributing

We welcome contributions to improve the PEP Workday Streamlit Application! Here's how to get started:

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/your-username/pepworkday-streamlit.git
cd pepworkday-streamlit

# Create development environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make Changes**
   - Follow existing code style and patterns
   - Add tests for new functionality
   - Update documentation as needed

3. **Run Tests**
   ```bash
   # Run all tests
   python run_tests.py --coverage

   # Run specific tests
   python run_tests.py --unit
   python run_tests.py --integration
   ```

4. **Code Quality Checks**
   ```bash
   # Format code
   black app.py data_loader.py tests/

   # Lint code
   flake8 app.py data_loader.py tests/

   # Type checking (optional)
   mypy app.py data_loader.py
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add amazing feature: detailed description"
   ```

6. **Push and Create PR**
   ```bash
   git push origin feature/amazing-feature
   # Create Pull Request on GitHub
   ```

### Contribution Guidelines

#### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

#### Testing Requirements
- Add tests for all new functionality
- Maintain test coverage above 90%
- Include both unit and integration tests
- Test error handling and edge cases

#### Documentation
- Update README.md for new features
- Add inline comments for complex logic
- Update configuration examples
- Include usage examples

### Types of Contributions

- **Bug Fixes**: Fix issues and improve reliability
- **New Features**: Add dashboard components, charts, or data sources
- **Performance**: Optimize data processing and caching
- **Documentation**: Improve guides and examples
- **Testing**: Expand test coverage and add test cases

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 PEP Workday Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 📞 Support & Community

### Getting Help

**Documentation:**
- [Streamlit Documentation](https://docs.streamlit.io) - Official Streamlit docs
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing setup and usage
- [STREAMLIT_DEPLOYMENT_GUIDE.md](STREAMLIT_DEPLOYMENT_GUIDE.md) - Deployment instructions

**Community Support:**
- [Streamlit Community Forum](https://discuss.streamlit.io) - Ask questions and share ideas
- [GitHub Issues](https://github.com/your-username/pepworkday-streamlit/issues) - Report bugs and request features
- [GitHub Discussions](https://github.com/your-username/pepworkday-streamlit/discussions) - General discussions

**Professional Support:**
- Email: support@pepworkday.com
- Slack: #streamlit-support (internal)

### Reporting Issues

When reporting issues, please include:

1. **Environment Information:**
   - Python version
   - Streamlit version
   - Operating system
   - Browser (if UI issue)

2. **Steps to Reproduce:**
   - Detailed steps to reproduce the issue
   - Expected vs actual behavior
   - Screenshots (if applicable)

3. **Error Messages:**
   - Full error traceback
   - Log files (if available)
   - Console output

### Feature Requests

For feature requests, please:

1. Check existing issues and discussions
2. Describe the use case and benefits
3. Provide mockups or examples (if applicable)
4. Consider contributing the feature yourself

## 🔗 Resources & Links

### Official Documentation
- [Streamlit Community Cloud](https://share.streamlit.io) - Free hosting platform
- [Streamlit API Reference](https://docs.streamlit.io/library/api-reference) - Complete API docs
- [Altair Documentation](https://altair-viz.github.io) - Visualization library
- [Pandas Documentation](https://pandas.pydata.org/docs/) - Data manipulation library

### Tutorials & Examples
- [Streamlit Gallery](https://streamlit.io/gallery) - Example applications
- [30 Days of Streamlit](https://30days.streamlit.app/) - Learning challenge
- [Streamlit Components](https://streamlit.io/components) - Custom components

### Development Tools
- [Streamlit Cloud](https://streamlit.io/cloud) - Deployment platform
- [GitHub Actions](https://github.com/features/actions) - CI/CD workflows
- [Docker Hub](https://hub.docker.com/) - Container registry
- [Heroku](https://heroku.com) - Alternative deployment platform

### Data Sources & APIs
- [FileMaker API](https://help.claris.com/en/data-api-guide/) - Database integration
- [Samsara API](https://developers.samsara.com/) - Fleet management data
- [OpenAI API](https://platform.openai.com/docs) - AI integration
- [Mapbox API](https://docs.mapbox.com/) - Mapping and visualization

---

**Made with ❤️ by the PEP Workday Team**

*For questions, suggestions, or contributions, please reach out through our GitHub repository or community channels.*
