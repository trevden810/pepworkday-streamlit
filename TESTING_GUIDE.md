# Testing Guide for PEP Workday Streamlit Application

This guide provides comprehensive information about the testing setup and how to run tests for the Streamlit application.

## 📁 Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Pytest configuration and shared fixtures
└── test_data_loader.py         # Tests for data loading functions
```

## 🧪 Test Categories

### Unit Tests
- **TestLoadData**: Tests for the `load_data()` function
- **TestLoadLargeDataset**: Tests for the `load_large_dataset()` function
- **TestLoadCSV**: Tests for CSV file loading functionality
- **TestMergeData**: Tests for data merging operations

### Integration Tests
- **TestIntegration**: End-to-end workflow tests combining multiple functions

## 🚀 Running Tests

### Quick Start
```bash
# Install test dependencies
python -m pip install pytest pytest-cov pytest-mock pytest-timeout

# Run all tests
python -m pytest tests/ -v

# Or use the test runner script
python run_tests.py
```

### Test Runner Options

The `run_tests.py` script provides various options:

```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py --unit           # Unit tests only
python run_tests.py --integration    # Integration tests only
python run_tests.py --csv           # CSV-related tests only
python run_tests.py --merge         # Merge-related tests only

# Run with coverage report
python run_tests.py --coverage

# Run specific test file
python run_tests.py --file tests/test_data_loader.py

# Run specific test function
python run_tests.py --function test_load_data_returns_dataframe

# Install dependencies automatically
python run_tests.py --install-deps
```

### Direct Pytest Commands

```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run specific test class
python -m pytest tests/test_data_loader.py::TestLoadData -v

# Run specific test method
python -m pytest tests/test_data_loader.py::TestLoadData::test_load_data_returns_dataframe -v

# Run tests with coverage
python -m pytest tests/ --cov=data_loader --cov-report=html

# Run tests with specific markers
python -m pytest tests/ -m "unit" -v
python -m pytest tests/ -m "csv or merge" -v
```

## 📊 Test Coverage

### Generating Coverage Reports

```bash
# HTML coverage report
python -m pytest tests/ --cov=data_loader --cov=app --cov-report=html

# Terminal coverage report
python -m pytest tests/ --cov=data_loader --cov=app --cov-report=term-missing

# XML coverage report (for CI/CD)
python -m pytest tests/ --cov=data_loader --cov=app --cov-report=xml
```

### Viewing Coverage Reports

- **HTML Report**: Open `htmlcov/index.html` in your browser
- **Terminal Report**: Shows coverage percentages and missing lines
- **XML Report**: `coverage.xml` for integration with CI/CD tools

## 🔧 Test Configuration

### pytest.ini
The `pytest.ini` file contains global pytest configuration:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers --disable-warnings --color=yes
```

### Test Markers

Tests are categorized using pytest markers:

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.csv`: CSV-related functionality
- `@pytest.mark.merge`: Data merging functionality
- `@pytest.mark.slow`: Slow-running tests

## 🛠️ Test Fixtures

### Shared Fixtures (conftest.py)

- `sample_filemaker_data`: Sample FileMaker DataFrame
- `sample_samsara_data`: Sample Samsara DataFrame
- `temp_csv_files`: Temporary CSV files for testing
- `mock_streamlit`: Mocked Streamlit functions
- `large_dataset`: Large dataset for performance testing

### Using Fixtures

```python
def test_example(sample_filemaker_data, temp_csv_files):
    """Example test using fixtures."""
    # Use sample_filemaker_data DataFrame
    assert len(sample_filemaker_data) == 5
    
    # Use temporary CSV files
    csv_path = temp_csv_files['filemaker_csv']
    df = load_csv(csv_path)
    assert not df.empty
```

## 📝 Test Examples

### Testing CSV Loading

```python
def test_load_csv_valid_file(self):
    """Test loading a valid CSV file."""
    result = load_csv(self.valid_csv_path)
    
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (3, 3)
    assert list(result.columns) == ['name', 'age', 'city']
```

### Testing Data Merging

```python
def test_merge_data_inner_join(self):
    """Test inner join merge (default behavior)."""
    result = merge_data(self.filemaker_df, self.samsara_df)
    
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (3, 5)  # 3 matching rows, 5 total columns
    assert 'driver_name' in result.columns
    assert 'miles_driven' in result.columns
```

### Testing Error Handling

```python
def test_load_csv_nonexistent_file(self):
    """Test loading a non-existent CSV file."""
    with patch('builtins.print') as mock_print:
        result = load_csv(self.nonexistent_path)
        
        assert isinstance(result, pd.DataFrame)
        assert result.empty
        mock_print.assert_called_once()
```

## 🐛 Debugging Tests

### Running Tests in Debug Mode

```bash
# Run with Python debugger
python -m pytest tests/ --pdb

# Run with verbose output and no capture
python -m pytest tests/ -v -s

# Run specific failing test
python -m pytest tests/test_data_loader.py::TestLoadCSV::test_load_csv_empty_file -v -s
```

### Common Issues and Solutions

1. **Import Errors**
   ```bash
   # Ensure the project root is in Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **Streamlit Cache Errors**
   ```python
   # Mock Streamlit cache in tests
   @patch('streamlit.cache_data', lambda func: func)
   def test_cached_function():
       # Test code here
   ```

3. **File Path Issues**
   ```python
   # Use absolute paths in tests
   test_file = os.path.join(os.path.dirname(__file__), 'test_data.csv')
   ```

## 🔄 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python run_tests.py --coverage
```

## 📈 Best Practices

1. **Test Naming**: Use descriptive test names that explain what is being tested
2. **Test Isolation**: Each test should be independent and not rely on others
3. **Fixtures**: Use fixtures for common test data and setup
4. **Mocking**: Mock external dependencies (databases, APIs, file systems)
5. **Coverage**: Aim for high test coverage but focus on critical paths
6. **Documentation**: Document complex test scenarios and edge cases

## 🔗 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Coverage Plugin](https://pytest-cov.readthedocs.io/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Streamlit Testing Guide](https://docs.streamlit.io/library/advanced-features/testing)
