# Streamlit Community Cloud Deployment Guide

This guide provides step-by-step instructions for deploying your Streamlit application to Streamlit Community Cloud.

## 📁 Project Structure

Your project should have the following structure:
```
pepworkday-streamlit/
├── .streamlit/
│   ├── config.toml          # App configuration (commit to repo)
│   └── secrets.toml         # Sensitive data (DO NOT commit)
├── app.py                   # Main Streamlit application
├── data_loader.py           # Data loading functions
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
└── README.md               # Project documentation
```

## 🔐 Security Setup

### 1. Create .gitignore file
Ensure your `.gitignore` includes:
```gitignore
# Streamlit secrets
.streamlit/secrets.toml

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Data files (if sensitive)
*.csv
*.xlsx
*.db
```

### 2. Configure secrets.toml
Edit `.streamlit/secrets.toml` with your actual credentials:
```toml
[database]
postgres_host = "your-actual-host.com"
postgres_username = "your_username"
postgres_password = "your_password"

[api_keys]
openai_api_key = "sk-your-actual-api-key"
```

### 3. Update your app.py to use secrets
```python
import streamlit as st

# Access secrets in your app
db_host = st.secrets["database"]["postgres_host"]
api_key = st.secrets["api_keys"]["openai_api_key"]
```

## 📦 Dependencies Setup

### 1. Create requirements.txt
```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
altair>=5.0.0
```

### 2. Generate from your environment
```bash
pip freeze > requirements.txt
```

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository

1. **Commit your code to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Streamlit deployment"
   git push origin main
   ```

2. **Verify .streamlit/secrets.toml is NOT committed:**
   ```bash
   git status
   # Should not show secrets.toml as staged
   ```

### Step 2: Deploy to Streamlit Community Cloud

1. **Visit Streamlit Community Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App:**
   - Click "New app"
   - Select your repository: `pepworkday-streamlit`
   - Set branch: `main`
   - Set main file path: `app.py`
   - Choose app URL (optional custom subdomain)

3. **Configure Secrets:**
   - In the app dashboard, click "Settings" → "Secrets"
   - Copy the contents of your local `.streamlit/secrets.toml`
   - Paste into the secrets editor
   - Click "Save"

### Step 3: Advanced Configuration

1. **Custom Domain (Optional):**
   - In app settings, add your custom domain
   - Configure DNS CNAME record pointing to your Streamlit app

2. **Environment Variables:**
   - Use secrets for sensitive data
   - Use config.toml for non-sensitive settings

## 🔧 Configuration Examples

### Database Connection Example
```python
import streamlit as st
import psycopg2

@st.cache_resource
def init_connection():
    return psycopg2.connect(
        host=st.secrets["database"]["postgres_host"],
        port=st.secrets["database"]["postgres_port"],
        database=st.secrets["database"]["postgres_database"],
        user=st.secrets["database"]["postgres_username"],
        password=st.secrets["database"]["postgres_password"]
    )

conn = init_connection()
```

### API Key Usage Example
```python
import streamlit as st
import openai

# Configure OpenAI
openai.api_key = st.secrets["api_keys"]["openai_api_key"]

def get_ai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

## 🐛 Troubleshooting

### Common Issues:

1. **Import Errors:**
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **Secrets Not Found:**
   - Verify secrets are properly configured in Streamlit Cloud
   - Check for typos in secret keys

3. **App Won't Start:**
   - Check logs in Streamlit Cloud dashboard
   - Verify main file path is correct

4. **Performance Issues:**
   - Use `@st.cache_data` for data processing
   - Use `@st.cache_resource` for database connections
   - Optimize data loading and processing

### Debug Mode:
```python
import streamlit as st

# Enable debug mode for development
if st.secrets.get("environment", {}).get("debug", False):
    st.write("Debug info:", st.secrets)
```

## 📊 Monitoring and Maintenance

### 1. App Analytics
- Monitor usage in Streamlit Cloud dashboard
- Track performance metrics
- Review error logs

### 2. Updates and Maintenance
- Push updates to GitHub to auto-deploy
- Monitor resource usage
- Update dependencies regularly

### 3. Backup Strategy
- Keep local backups of secrets
- Document configuration changes
- Version control all non-sensitive files

## 🔗 Useful Links

- [Streamlit Community Cloud](https://share.streamlit.io)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)
- [Configuration Options](https://docs.streamlit.io/library/advanced-features/configuration)

## 📞 Support

If you encounter issues:
1. Check the [Streamlit Community Forum](https://discuss.streamlit.io)
2. Review the [GitHub Issues](https://github.com/streamlit/streamlit/issues)
3. Consult the [Streamlit Documentation](https://docs.streamlit.io)
