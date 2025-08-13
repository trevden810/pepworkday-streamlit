"""
Unit tests for the FileMaker API integration module.
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add the parent directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from filemaker_api import FileMakerAPI, get_filemaker_job_data, create_filemaker_job


class TestFileMakerAPI:
    """Test cases for the FileMakerAPI class."""
    
    def test_init(self, mock_streamlit):
        """Test FileMakerAPI initialization."""
        fm_api = FileMakerAPI()
        
        assert fm_api.server_url == "https://modd.mainspringhost.com"
        assert fm_api.api_version == "vLatest"
        assert fm_api.username == "trevor_api"
        assert fm_api.password == "XcScS2yRoTtMo7"
        assert fm_api.token is None
    
    def test_authenticate_success(self, mock_streamlit, monkeypatch):
        """Test successful authentication."""
        import requests
        import json
        
        # Mock the requests.post response
        class MockResponse:
            def __init__(self):
                self.status_code = 200
            
            def json(self):
                return {"response": {"token": "test-token-123"}}
        
        def mock_post(*args, **kwargs):
            return MockResponse()
        
        monkeypatch.setattr(requests, "post", mock_post)
        
        fm_api = FileMakerAPI()
        result = fm_api.authenticate("test_database")
        
        assert result is True
        assert fm_api.token == "test-token-123"
    
    def test_authenticate_failure(self, mock_streamlit, monkeypatch):
        """Test failed authentication."""
        import requests
        
        # Mock the requests.post response
        class MockResponse:
            def __init__(self):
                self.status_code = 401
                self.text = "Unauthorized"
        
        def mock_post(*args, **kwargs):
            return MockResponse()
        
        monkeypatch.setattr(requests, "post", mock_post)
        
        fm_api = FileMakerAPI()
        result = fm_api.authenticate("test_database")
        
        assert result is False
        assert fm_api.token is None
    
    def test_find_record_success(self, mock_streamlit, monkeypatch):
        """Test successful record find."""
        import requests
        
        # Mock the requests.post response
        class MockResponse:
            def __init__(self):
                self.status_code = 200
            
            def json(self):
                return {
                    "response": {
                        "data": [{
                            "fieldData": {
                                "_kp_job_id": "603142",
                                "job_date": "08/05/2022",
                                "job_status": "Completed",
                                "job_type": "Delivery"
                            },
                            "recordId": "865642",
                            "modId": "51"
                        }]
                    }
                }
        
        def mock_post(*args, **kwargs):
            return MockResponse()
        
        monkeypatch.setattr(requests, "post", mock_post)
        
        # Mock authenticate to return True
        def mock_authenticate(self, database_name):
            self.token = "test-token-123"
            return True
        
        monkeypatch.setattr(FileMakerAPI, "authenticate", mock_authenticate)
        
        fm_api = FileMakerAPI()
        result = fm_api.find_record("test_database", "jobs_api", {"_kp_job_id": "603142"})
        
        assert result is not None
        assert result.get("fieldData", {}).get("_kp_job_id") == "603142"
    
    def test_find_record_no_results(self, mock_streamlit, monkeypatch):
        """Test record find with no results."""
        import requests
        
        # Mock the requests.post response
        class MockResponse:
            def __init__(self):
                self.status_code = 200
            
            def json(self):
                return {"response": {"data": []}}
        
        def mock_post(*args, **kwargs):
            return MockResponse()
        
        monkeypatch.setattr(requests, "post", mock_post)
        
        # Mock authenticate to return True
        def mock_authenticate(self, database_name):
            self.token = "test-token-123"
            return True
        
        monkeypatch.setattr(FileMakerAPI, "authenticate", mock_authenticate)
        
        fm_api = FileMakerAPI()
        result = fm_api.find_record("test_database", "jobs_api", {"_kp_job_id": "999999"})
        
        assert result is None
    
    def test_create_record_success(self, mock_streamlit, monkeypatch):
        """Test successful record creation."""
        import requests
        
        # Mock the requests.post response
        class MockResponse:
            def __init__(self):
                self.status_code = 200
            
            def json(self):
                return {
                    "response": {
                        "recordId": "59",
                        "modId": "0"
                    }
                }
        
        def mock_post(*args, **kwargs):
            return MockResponse()
        
        monkeypatch.setattr(requests, "post", mock_post)
        
        # Mock authenticate to return True
        def mock_authenticate(self, database_name):
            self.token = "test-token-123"
            return True
        
        monkeypatch.setattr(FileMakerAPI, "authenticate", mock_authenticate)
        
        fm_api = FileMakerAPI()
        result = fm_api.create_record("pep-move-api", "table", {"field1": "value1"})
        
        assert result == "59"


class TestFileMakerFunctions:
    """Test cases for FileMaker API functions."""
    
    def test_get_filemaker_job_data(self, mock_streamlit, monkeypatch):
        """Test get_filemaker_job_data function."""
        # Mock the FileMakerAPI.find_record method
        def mock_find_record(self, database_name, layout, query):
            if query.get("_kp_job_id") == "603142":
                return {
                    "fieldData": {
                        "_kp_job_id": "603142",
                        "job_date": "08/05/2022",
                        "job_status": "Completed",
                        "job_type": "Delivery",
                        "address_C1": "123 Main St",
                        "zip_C1": "12345"
                    },
                    "recordId": "865642",
                    "modId": "51"
                }
            return None
        
        monkeypatch.setattr(FileMakerAPI, "find_record", mock_find_record)
        
        result = get_filemaker_job_data("603142")
        
        assert result is not None
        assert result["job_id"] == "603142"
        assert result["date"] == "08/05/2022"
        assert result["status"] == "Completed"
        assert result["type"] == "Delivery"
        assert result["address"] == "123 Main St"
        assert result["zip"] == "12345"
    
    def test_create_filemaker_job(self, mock_streamlit, monkeypatch):
        """Test create_filemaker_job function."""
        # Mock the FileMakerAPI.create_record method
        def mock_create_record(self, database_name, layout, field_data):
            return "59"
        
        monkeypatch.setattr(FileMakerAPI, "create_record", mock_create_record)
        
        result = create_filemaker_job({"field1": "value1"})
        
        assert result == "59"


if __name__ == "__main__":
    pytest.main([__file__])
