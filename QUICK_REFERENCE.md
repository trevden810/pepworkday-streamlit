# Quick Reference Guide

## 🚀 Essential Commands

### Setup & Installation
```bash
# Clone and setup
git clone https://github.com/your-username/pepworkday-streamlit.git
cd pepworkday-streamlit
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### Testing
```bash
# Quick test run
python run_tests.py

# With coverage
python run_tests.py --coverage

# Specific categories
python run_tests.py --unit
python run_tests.py --csv
python run_tests.py --integration
```

### Development
```bash
# Code formatting
black app.py data_loader.py tests/

# Linting
flake8 app.py data_loader.py tests/

# Install dev dependencies
pip install pytest pytest-cov black flake8
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application |
| `data_loader.py` | Data processing functions |
| `.streamlit/config.toml` | App configuration |
| `.streamlit/secrets.toml` | Sensitive credentials |
| `tests/test_data_loader.py` | Test suite |
| `requirements.txt` | Dependencies |

## 🔧 Configuration

### Secrets Template
```toml
[database]
postgres_host = "localhost"
postgres_username = "user"
postgres_password = "password"

[api_keys]
openai_api_key = "sk-your-key"
mapbox_token = "pk.your-token"

[environment]
mode = "development"
debug = true
```

### Environment Variables
```bash
export STREAMLIT_ENV=development
export DEBUG=true
export DB_HOST=localhost
export DB_PORT=5432
```

## 🚀 Deployment

### Streamlit Cloud
1. Push to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Configure secrets
5. Deploy

### Docker
```bash
# Build and run
docker build -t pepworkday-streamlit .
docker run -p 8501:8501 pepworkday-streamlit
```

## 🐛 Troubleshooting

### Common Issues
- **Import errors**: Check virtual environment activation
- **Secrets not found**: Verify `.streamlit/secrets.toml` exists
- **Port in use**: Use `--server.port 8502`
- **Cache issues**: Clear with `st.cache_data.clear()`

### Debug Mode
```python
# Enable in secrets.toml
[environment]
debug = true

# Or set environment variable
export DEBUG=true
```

## 📊 Data Processing

### Key Functions
```python
# Load data
df = load_data()
raw_df = create_raw_df()

# Process data
jobs_data = get_jobs_per_driver(raw_df)
miles_data = get_miles_per_driver(raw_df)
combined = get_combined_analysis(raw_df)

# Get statistics
stats = get_summary_stats(combined)
```

### CSV Operations
```python
# Load CSV
df = load_csv("data/file.csv")

# Merge data
merged = merge_data(df1, df2, on='id', how='inner')
```

## 🎯 URLs & Links

- **Local App**: http://localhost:8501
- **Streamlit Cloud**: https://share.streamlit.io
- **Documentation**: https://docs.streamlit.io
- **Community**: https://discuss.streamlit.io

## 📞 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@pepworkday.com
- **Docs**: README.md, TESTING_GUIDE.md, STREAMLIT_DEPLOYMENT_GUIDE.md
