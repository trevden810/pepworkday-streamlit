"""
Unit tests for the Samsara API integration module.
"""

import pytest
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add the parent directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from samsara_api import SamsaraAPI, get_samsara_vehicles, get_samsara_drivers, get_recent_vehicle_stats


class TestSamsaraAPI:
    """Test cases for the SamsaraAPI class."""
    
    def test_init(self, mock_streamlit):
        """Test SamsaraAPI initialization."""
        samsara_api = SamsaraAPI()
        
        assert samsara_api.base_url == "https://api.samsara.com"
        assert samsara_api.api_token == "test-samsara-token"
        assert "Authorization" in samsara_api.headers
        assert samsara_api.headers["Authorization"] == "Bearer test-samsara-token"
    
    def test_get_vehicles_success(self, mock_streamlit, monkeypatch):
        """Test successful vehicle retrieval."""
        import requests
        
        # Mock the requests.get response
        class MockResponse:
            def __init__(self):
                self.status_code = 200
            
            def json(self):
                return {
                    "vehicles": [
                        {
                            "id": "123456789012345",
                            "name": "Truck 123",
                            "vin": "1HGBH41JXMN109186",
                            "odometerMeters": 125000,
                            "engineHours": 4500
                        }
                    ]
                }
        
        def mock_get(*args, **kwargs):
            return MockResponse()
        
        monkeypatch.setattr(requests, "get", mock_get)
        
        samsara_api = SamsaraAPI()
        result = samsara_api.get_vehicles()
        
        assert result is not None
        assert len(result) == 1
        assert result[0]["id"] == "123456789012345"
        assert result[0]["name"] == "Truck 123"
    
    def test_get_vehicles_failure(self, mock_streamlit, monkeypatch):
        """Test failed vehicle retrieval."""
        import requests
        
        # Mock the requests.get response
        class MockResponse:
            def __init__(self):
                self.status_code = 401
                self.text = "Unauthorized"
        
        def mock_get(*args, **kwargs):
            return MockResponse()
        
        monkeypatch.setattr(requests, "get", mock_get)
        
        samsara_api = SamsaraAPI()
        result = samsara_api.get_vehicles()
        
        assert result is None
    
    def test_get_drivers_success(self, mock_streamlit, monkeypatch):
        """Test successful driver retrieval."""
        import requests
        
        # Mock the requests.get response
        class MockResponse:
            def __init__(self):
                self.status_code = 200
                self.text = "OK"
            
            def json(self):
                return {
                    "drivers": [
                        {
                            "id": "1234567890",
                            "name": "John Doe",
                            "email": "john.doe@example.com"
                        }
                    ]
                }
        
        def mock_get(*args, **kwargs):
            return MockResponse()
        
        monkeypatch.setattr(requests, "get", mock_get)
        
        samsara_api = SamsaraAPI()
        result = samsara_api.get_drivers()
        
        assert result is not None
        assert len(result) == 1
        assert result[0]["id"] == "1234567890"
        assert result[0]["name"] == "John Doe"
    
    def test_get_drivers_failure(self, mock_streamlit, monkeypatch):
        """Test failed driver retrieval."""
        import requests
        
        # Mock the requests.get response
        class MockResponse:
            def __init__(self):
                self.status_code = 401
                self.text = "Unauthorized"
        
        def mock_get(*args, **kwargs):
            return MockResponse()
        
        monkeypatch.setattr(requests, "get", mock_get)
        
        samsara_api = SamsaraAPI()
        result = samsara_api.get_drivers()
        
        assert result is None
    
    def test_get_vehicle_stats_success(self, mock_streamlit, monkeypatch):
        """Test successful vehicle stats retrieval."""
        import requests
        
        # Mock the requests.get response
        class MockResponse:
            def __init__(self):
                self.status_code = 200
                self.text = "OK"
            
            def json(self):
                return {
                    "vehicleId": "123456789012345",
                    "startTime": "2023-01-01T00:00:00Z",
                    "endTime": "2023-01-02T00:00:00Z"
                }
        
        def mock_get(*args, **kwargs):
            return MockResponse()
        
        monkeypatch.setattr(requests, "get", mock_get)
        
        samsara_api = SamsaraAPI()
        result = samsara_api.get_vehicle_stats(
            "123456789012345",
            "2023-01-01T00:00:00Z",
            "2023-01-02T00:00:00Z"
        )
        
        assert result is not None
        assert result["vehicleId"] == "123456789012345"
    
    def test_get_vehicle_stats_failure(self, mock_streamlit, monkeypatch):
        """Test failed vehicle stats retrieval."""
        import requests
        
        # Mock the requests.get response
        class MockResponse:
            def __init__(self):
                self.status_code = 404
                self.text = "Not Found"
        
        def mock_get(*args, **kwargs):
            return MockResponse()
        
        monkeypatch.setattr(requests, "get", mock_get)
        
        samsara_api = SamsaraAPI()
        result = samsara_api.get_vehicle_stats(
            "123456789012345",
            "2023-01-01T00:00:00Z",
            "2023-01-02T00:00:00Z"
        )
        
        assert result is None


class TestSamsaraFunctions:
    """Test cases for Samsara API functions."""
    
    def test_get_samsara_vehicles(self, mock_streamlit, monkeypatch):
        """Test get_samsara_vehicles function."""
        # Mock the SamsaraAPI.get_vehicles method
        def mock_get_vehicles(self):
            return [
                {
                    "id": "123456789012345",
                    "name": "Truck 123",
                    "vin": "1HGBH41JXMN109186",
                    "odometerMeters": 125000,
                    "engineHours": 4500
                }
            ]
        
        monkeypatch.setattr(SamsaraAPI, "get_vehicles", mock_get_vehicles)
        
        result = get_samsara_vehicles()
        
        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]["id"] == "123456789012345"
    
    def test_get_samsara_drivers(self, mock_streamlit, monkeypatch):
        """Test get_samsara_drivers function."""
        # Mock the SamsaraAPI.get_drivers method
        def mock_get_drivers(self):
            return [
                {
                    "id": "1234567890",
                    "name": "John Doe",
                    "email": "john.doe@example.com"
                }
            ]
        
        monkeypatch.setattr(SamsaraAPI, "get_drivers", mock_get_drivers)
        
        result = get_samsara_drivers()
        
        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]["id"] == "1234567890"
    
    def test_get_recent_vehicle_stats(self, mock_streamlit, monkeypatch):
        """Test get_recent_vehicle_stats function."""
        # Mock the SamsaraAPI.get_vehicles method
        def mock_get_vehicles(self):
            return [
                {
                    "id": "123456789012345",
                    "name": "Truck 123",
                    "vin": "1HGBH41JXMN109186",
                    "odometerMeters": 125000,
                    "engineHours": 4500,
                    "fuelPercent": 75
                }
            ]
        
        # Mock the SamsaraAPI.get_vehicle_stats method
        def mock_get_vehicle_stats(self, vehicle_id, start_time, end_time):
            return {
                "vehicleId": vehicle_id,
                "startTime": start_time,
                "endTime": end_time
            }
        
        monkeypatch.setattr(SamsaraAPI, "get_vehicles", mock_get_vehicles)
        monkeypatch.setattr(SamsaraAPI, "get_vehicle_stats", mock_get_vehicle_stats)
        
        result = get_recent_vehicle_stats(hours=24)
        
        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]["vehicle_id"] == "123456789012345"


if __name__ == "__main__":
    pytest.main([__file__])
