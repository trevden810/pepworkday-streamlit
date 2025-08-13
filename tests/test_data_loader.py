"""
Test suite for data_loader.py functions.

This module contains comprehensive tests for all data loading and processing
functions including CSV loading, data merging, and error handling.
"""

import pytest
import pandas as pd
import tempfile
import os
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add the parent directory to the path to import data_loader
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_loader import load_data, load_large_dataset, load_csv, merge_data


class TestLoadData:
    """Test cases for the load_data function."""
    
    def test_load_data_returns_dataframe(self):
        """Test that load_data returns a pandas DataFrame."""
        result = load_data()
        assert isinstance(result, pd.DataFrame)
    
    def test_load_data_correct_shape(self):
        """Test that load_data returns DataFrame with correct shape."""
        result = load_data()
        assert result.shape == (4, 2)
    
    def test_load_data_correct_columns(self):
        """Test that load_data returns DataFrame with correct columns."""
        result = load_data()
        expected_columns = ['column1', 'column2']
        assert list(result.columns) == expected_columns
    
    def test_load_data_correct_values(self):
        """Test that load_data returns DataFrame with correct values."""
        result = load_data()
        expected_column1 = [1, 2, 3, 4]
        expected_column2 = [10, 20, 30, 40]
        
        assert result['column1'].tolist() == expected_column1
        assert result['column2'].tolist() == expected_column2
    
    def test_load_data_data_types(self):
        """Test that load_data returns correct data types."""
        result = load_data()
        assert result['column1'].dtype == 'int64'
        assert result['column2'].dtype == 'int64'


class TestLoadLargeDataset:
    """Test cases for the load_large_dataset function."""
    
    def test_load_large_dataset_returns_dataframe(self):
        """Test that load_large_dataset returns a pandas DataFrame."""
        result = load_large_dataset()
        assert isinstance(result, pd.DataFrame)
    
    def test_load_large_dataset_correct_shape(self):
        """Test that load_large_dataset returns DataFrame with correct shape."""
        result = load_large_dataset()
        assert result.shape == (100, 2)
    
    def test_load_large_dataset_correct_columns(self):
        """Test that load_large_dataset returns DataFrame with correct columns."""
        result = load_large_dataset()
        expected_columns = ['id', 'value']
        assert list(result.columns) == expected_columns
    
    def test_load_large_dataset_id_range(self):
        """Test that load_large_dataset generates correct ID range."""
        result = load_large_dataset()
        assert result['id'].min() == 0
        assert result['id'].max() == 99
        assert len(result['id'].unique()) == 100
    
    def test_load_large_dataset_value_calculation(self):
        """Test that load_large_dataset calculates values correctly."""
        result = load_large_dataset()
        # Check that value = id * 10
        for i in range(10):  # Check first 10 rows
            assert result.iloc[i]['value'] == result.iloc[i]['id'] * 10


class TestLoadCSV:
    """Test cases for the load_csv function."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create temporary CSV files for testing
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a valid CSV file
        self.valid_csv_path = os.path.join(self.temp_dir, 'valid_data.csv')
        valid_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'city': ['New York', 'London', 'Tokyo']
        })
        valid_data.to_csv(self.valid_csv_path, index=False)
        
        # Create an empty CSV file
        self.empty_csv_path = os.path.join(self.temp_dir, 'empty_data.csv')
        empty_data = pd.DataFrame()
        empty_data.to_csv(self.empty_csv_path, index=False)
        
        # Path to non-existent file
        self.nonexistent_path = os.path.join(self.temp_dir, 'nonexistent.csv')
    
    def teardown_method(self):
        """Clean up test fixtures after each test method."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_csv_valid_file(self):
        """Test loading a valid CSV file."""
        result = load_csv(self.valid_csv_path)
        
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (3, 3)
        assert list(result.columns) == ['name', 'age', 'city']
        assert result['name'].tolist() == ['Alice', 'Bob', 'Charlie']
    
    def test_load_csv_empty_file(self):
        """Test loading an empty CSV file."""
        # Create a proper empty CSV with headers
        empty_csv_with_headers = os.path.join(self.temp_dir, 'empty_with_headers.csv')
        with open(empty_csv_with_headers, 'w') as f:
            f.write("name,age,city\n")  # Headers only

        result = load_csv(empty_csv_with_headers)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0  # No data rows
        assert len(result.columns) == 3  # But has columns
    
    def test_load_csv_nonexistent_file(self):
        """Test loading a non-existent CSV file."""
        with patch('builtins.print') as mock_print:
            result = load_csv(self.nonexistent_path)
            
            assert isinstance(result, pd.DataFrame)
            assert result.empty
            mock_print.assert_called_once()
            assert "not found" in mock_print.call_args[0][0]
    
    def test_load_csv_with_different_separators(self):
        """Test loading CSV with different separators."""
        # Create CSV with semicolon separator
        semicolon_csv_path = os.path.join(self.temp_dir, 'semicolon_data.csv')
        with open(semicolon_csv_path, 'w') as f:
            f.write("name;age;city\n")
            f.write("Alice;25;New York\n")
            f.write("Bob;30;London\n")
        
        # This should fail with default separator
        result_default = load_csv(semicolon_csv_path)
        assert result_default.shape[1] == 1  # All data in one column
    
    def test_load_csv_with_encoding_issues(self):
        """Test loading CSV with potential encoding issues."""
        # Create CSV with special characters
        special_csv_path = os.path.join(self.temp_dir, 'special_chars.csv')
        special_data = pd.DataFrame({
            'name': ['José', 'François', 'Müller'],
            'city': ['São Paulo', 'Montréal', 'München']
        })
        special_data.to_csv(special_csv_path, index=False, encoding='utf-8')
        
        result = load_csv(special_csv_path)
        assert isinstance(result, pd.DataFrame)
        assert not result.empty


class TestMergeData:
    """Test cases for the merge_data function."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create sample FileMaker data
        self.filemaker_df = pd.DataFrame({
            'id': [1, 2, 3, 4],
            'driver_name': ['Alice', 'Bob', 'Charlie', 'David'],
            'department': ['Sales', 'Marketing', 'IT', 'HR']
        })
        
        # Create sample Samsara data
        self.samsara_df = pd.DataFrame({
            'id': [1, 2, 3, 5],
            'miles_driven': [150, 200, 175, 300],
            'fuel_consumed': [12, 16, 14, 24]
        })
        
        # Create data with different column names for join
        self.different_key_df = pd.DataFrame({
            'driver_id': [1, 2, 3],
            'vehicle_type': ['Truck', 'Van', 'Car']
        })
    
    def test_merge_data_inner_join(self):
        """Test inner join merge (default behavior)."""
        result = merge_data(self.filemaker_df, self.samsara_df)
        
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (3, 5)  # 3 matching rows, 5 total columns
        assert list(result['id']) == [1, 2, 3]
        assert 'driver_name' in result.columns
        assert 'miles_driven' in result.columns
    
    def test_merge_data_left_join(self):
        """Test left join merge."""
        result = merge_data(self.filemaker_df, self.samsara_df, how='left')
        
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (4, 5)  # All 4 rows from left df
        assert list(result['id']) == [1, 2, 3, 4]
        assert pd.isna(result.iloc[3]['miles_driven'])  # David has no Samsara data
    
    def test_merge_data_right_join(self):
        """Test right join merge."""
        result = merge_data(self.filemaker_df, self.samsara_df, how='right')
        
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (4, 5)  # All 4 rows from right df
        assert 5 in result['id'].values  # ID 5 from Samsara data
        assert pd.isna(result[result['id'] == 5]['driver_name'].iloc[0])
    
    def test_merge_data_outer_join(self):
        """Test outer join merge."""
        result = merge_data(self.filemaker_df, self.samsara_df, how='outer')
        
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (5, 5)  # All unique IDs from both dfs
        assert set(result['id']) == {1, 2, 3, 4, 5}
    
    def test_merge_data_custom_key(self):
        """Test merge with custom join key."""
        # Rename id column in one dataframe
        samsara_renamed = self.samsara_df.rename(columns={'id': 'driver_id'})
        filemaker_renamed = self.filemaker_df.rename(columns={'id': 'driver_id'})
        
        result = merge_data(filemaker_renamed, samsara_renamed, on='driver_id')
        
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (3, 5)
        assert 'driver_id' in result.columns
    
    def test_merge_data_empty_dataframes(self):
        """Test merge with empty DataFrames."""
        empty_df = pd.DataFrame()

        # Test with empty left DataFrame - should handle gracefully
        try:
            result = merge_data(empty_df, self.samsara_df)
            assert isinstance(result, pd.DataFrame)
            assert result.empty
        except (KeyError, ValueError):
            # Expected behavior when merging empty DataFrame
            pass

        # Test with empty right DataFrame - should handle gracefully
        try:
            result = merge_data(self.filemaker_df, empty_df)
            assert isinstance(result, pd.DataFrame)
            assert result.empty
        except (KeyError, ValueError):
            # Expected behavior when merging empty DataFrame
            pass
    
    def test_merge_data_no_common_keys(self):
        """Test merge when no common keys exist."""
        no_common_df = pd.DataFrame({
            'different_id': [1, 2, 3],
            'some_data': ['A', 'B', 'C']
        })
        
        with pytest.raises(KeyError):
            merge_data(self.filemaker_df, no_common_df, on='id')
    
    def test_merge_data_duplicate_keys(self):
        """Test merge with duplicate keys."""
        duplicate_samsara = pd.DataFrame({
            'id': [1, 1, 2, 2],
            'miles_driven': [150, 160, 200, 210],
            'trip_number': [1, 2, 1, 2]
        })

        result = merge_data(self.filemaker_df, duplicate_samsara)

        assert isinstance(result, pd.DataFrame)
        assert result.shape[0] >= len(self.filemaker_df)  # At least as many rows, possibly more due to duplicates
        # Check that we have the expected number of rows for ID 1 (should be 2)
        id_1_rows = result[result['id'] == 1]
        assert len(id_1_rows) == 2  # Two rows for ID 1


class TestIntegration:
    """Integration tests combining multiple functions."""
    
    def setup_method(self):
        """Set up test fixtures for integration tests."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create sample FileMaker CSV
        self.filemaker_csv = os.path.join(self.temp_dir, 'filemaker_data.csv')
        filemaker_data = pd.DataFrame({
            'id': [1, 2, 3, 4],
            'driver_name': ['Alice', 'Bob', 'Charlie', 'David'],
            'department': ['Sales', 'Marketing', 'IT', 'HR']
        })
        filemaker_data.to_csv(self.filemaker_csv, index=False)
        
        # Create sample Samsara CSV
        self.samsara_csv = os.path.join(self.temp_dir, 'samsara_data.csv')
        samsara_data = pd.DataFrame({
            'id': [1, 2, 3, 5],
            'miles_driven': [150, 200, 175, 300],
            'fuel_consumed': [12, 16, 14, 24]
        })
        samsara_data.to_csv(self.samsara_csv, index=False)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_and_merge_workflow(self):
        """Test the complete workflow of loading CSVs and merging them."""
        # Load the CSV files
        filemaker_df = load_csv(self.filemaker_csv)
        samsara_df = load_csv(self.samsara_csv)
        
        # Verify loading worked
        assert not filemaker_df.empty
        assert not samsara_df.empty
        
        # Merge the data
        merged_df = merge_data(filemaker_df, samsara_df)
        
        # Verify merge worked
        assert isinstance(merged_df, pd.DataFrame)
        assert merged_df.shape == (3, 5)
        assert 'driver_name' in merged_df.columns
        assert 'miles_driven' in merged_df.columns
        
        # Verify data integrity
        assert merged_df['driver_name'].tolist() == ['Alice', 'Bob', 'Charlie']
        assert merged_df['miles_driven'].tolist() == [150, 200, 175]


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])
