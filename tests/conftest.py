"""
Pytest configuration and shared fixtures for the test suite.

This file contains pytest fixtures and configuration that are shared
across multiple test modules.
"""

import pytest
import pandas as pd
import tempfile
import os
import sys
from pathlib import Path

# Add the parent directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_filemaker_data():
    """Fixture providing sample FileMaker data for testing."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'driver_name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'David Wilson', 'Eva Davis'],
        'department': ['Sales', 'Marketing', 'IT', 'HR', 'Operations'],
        'hire_date': ['2020-01-15', '2019-03-22', '2021-07-10', '2018-11-05', '2022-02-28'],
        'salary': [55000, 62000, 75000, 58000, 51000]
    })


@pytest.fixture
def sample_samsara_data():
    """Fixture providing sample Samsara data for testing."""
    return pd.DataFrame({
        'id': [1, 2, 3, 6, 7],
        'miles_driven': [1250, 1800, 950, 2100, 1600],
        'fuel_consumed': [85, 120, 65, 140, 110],
        'hours_driven': [45, 62, 38, 75, 58],
        'vehicle_id': ['V001', 'V002', 'V003', 'V004', 'V005']
    })


@pytest.fixture
def temp_csv_files(sample_filemaker_data, sample_samsara_data):
    """Fixture providing temporary CSV files for testing."""
    temp_dir = tempfile.mkdtemp()
    
    # Create FileMaker CSV
    filemaker_path = os.path.join(temp_dir, 'filemaker_test.csv')
    sample_filemaker_data.to_csv(filemaker_path, index=False)
    
    # Create Samsara CSV
    samsara_path = os.path.join(temp_dir, 'samsara_test.csv')
    sample_samsara_data.to_csv(samsara_path, index=False)
    
    # Create empty CSV
    empty_path = os.path.join(temp_dir, 'empty_test.csv')
    pd.DataFrame().to_csv(empty_path, index=False)
    
    # Create malformed CSV
    malformed_path = os.path.join(temp_dir, 'malformed_test.csv')
    with open(malformed_path, 'w') as f:
        f.write("name,age,city\n")
        f.write("Alice,25\n")  # Missing city column
        f.write("Bob,30,London,Extra\n")  # Extra column
    
    yield {
        'temp_dir': temp_dir,
        'filemaker_csv': filemaker_path,
        'samsara_csv': samsara_path,
        'empty_csv': empty_path,
        'malformed_csv': malformed_path,
        'nonexistent_csv': os.path.join(temp_dir, 'does_not_exist.csv')
    }
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_streamlit():
    """Fixture to mock Streamlit functions for testing."""
    import unittest.mock as mock
    
    with mock.patch('streamlit.cache_data') as mock_cache:
        # Make cache_data decorator a pass-through
        mock_cache.side_effect = lambda func: func
        yield mock_cache


@pytest.fixture(scope="session")
def test_data_dir():
    """Fixture providing path to test data directory."""
    test_dir = Path(__file__).parent
    data_dir = test_dir / "test_data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


@pytest.fixture
def large_dataset():
    """Fixture providing a larger dataset for performance testing."""
    return pd.DataFrame({
        'id': range(1000),
        'value': [i * 2.5 for i in range(1000)],
        'category': [f'Cat_{i % 10}' for i in range(1000)],
        'timestamp': pd.date_range('2024-01-01', periods=1000, freq='H')
    })


@pytest.fixture
def dataframes_with_different_schemas():
    """Fixture providing DataFrames with different schemas for testing edge cases."""
    df1 = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['A', 'B', 'C'],
        'value': [10, 20, 30]
    })
    
    df2 = pd.DataFrame({
        'id': [1, 2, 4],
        'description': ['Desc A', 'Desc B', 'Desc D'],
        'amount': [100, 200, 400]
    })
    
    df3 = pd.DataFrame({
        'driver_id': [1, 2, 3],  # Different key column name
        'miles': [150, 250, 350]
    })
    
    return {
        'df1': df1,
        'df2': df2,
        'df3': df3
    }


# Pytest configuration hooks
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "csv: mark test as CSV-related"
    )
    config.addinivalue_line(
        "markers", "merge: mark test as merge-related"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add markers based on test names
        if "csv" in item.name.lower():
            item.add_marker(pytest.mark.csv)
        if "merge" in item.name.lower():
            item.add_marker(pytest.mark.merge)
        if "integration" in item.name.lower():
            item.add_marker(pytest.mark.integration)
        if "large" in item.name.lower():
            item.add_marker(pytest.mark.slow)
        
        # Default to unit test if no other marker
        if not any(marker.name in ['integration', 'slow'] for marker in item.iter_markers()):
            item.add_marker(pytest.mark.unit)
