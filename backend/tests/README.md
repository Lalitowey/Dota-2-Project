# Backend Test Suite

This directory contains the comprehensive test suite for the Dota 2 Analytics API backend.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and test configuration
├── test_main.py             # Tests for main application endpoints
├── test_config.py           # Tests for configuration management
├── test_cache.py            # Unit tests for cache implementation
├── test_client.py           # Unit tests for HTTP client
├── test_api_players.py      # Integration tests for player endpoints
├── test_api_heroes.py       # Integration tests for hero endpoints
└── test_api_cache.py        # Integration tests for cache endpoints
```

## Running Tests

### Run All Tests
```bash
cd backend
pytest
```

### Run with Coverage Report
```bash
pytest --cov=app --cov-report=term-missing
```

### Run Specific Test Types
```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Exclude slow tests
pytest -m "not slow"
```

### Run Specific Test Files
```bash
pytest tests/test_cache.py
pytest tests/test_api_players.py
```

### Run Specific Test Functions
```bash
pytest tests/test_cache.py::test_cache_set_and_get
pytest tests/test_api_players.py::test_get_player_profile_success
```

### Verbose Output
```bash
pytest -v
```

### See Print Statements
```bash
pytest -s
```

## Test Markers

The test suite uses pytest markers to categorize tests:

- `@pytest.mark.unit` - Fast unit tests for individual components
- `@pytest.mark.integration` - Integration tests for API endpoints
- `@pytest.mark.slow` - Slow-running tests (can be excluded during development)

## Coverage Reports

After running tests with coverage, view the HTML report:

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Test Fixtures

Common fixtures are defined in `conftest.py`:

- `client` - Synchronous TestClient for FastAPI
- `async_client` - Asynchronous client for testing async endpoints
- `test_settings` - Test-specific configuration
- `mock_opendota_response` - Mock OpenDota API responses
- `sample_account_id` - Sample player account ID for testing

## Writing New Tests

### Unit Test Example
```python
@pytest.mark.unit
def test_my_function():
    result = my_function()
    assert result == expected_value
```

### Integration Test Example
```python
@pytest.mark.integration
def test_my_endpoint(client: TestClient):
    response = client.get("/api/v1/my-endpoint")
    assert response.status_code == 200
```

### Async Test Example
```python
@pytest.mark.asyncio
@pytest.mark.unit
async def test_my_async_function():
    result = await my_async_function()
    assert result is not None
```

## Best Practices

1. **Isolation** - Each test should be independent and not rely on other tests
2. **Mocking** - Use mocks for external dependencies (OpenDota API, database)
3. **Clear Names** - Test function names should describe what is being tested
4. **Arrange-Act-Assert** - Follow the AAA pattern in test structure
5. **Coverage** - Aim for high code coverage but focus on meaningful tests
6. **Fast Tests** - Keep unit tests fast; use markers for slow integration tests

## Continuous Integration

Tests are designed to run in CI environments. Make sure all tests pass before pushing:

```bash
pytest --cov=app --cov-report=term-missing --tb=short
```

## Troubleshooting

### Import Errors
Ensure you're running pytest from the `backend` directory and have installed all dependencies:
```bash
cd backend
pip install -r requirements.txt
pytest
```

### Fixture Not Found
Make sure `conftest.py` is in the `tests` directory and fixtures are properly defined.

### Coverage Not Working
Install pytest-cov:
```bash
pip install pytest-cov
```

## Future Enhancements

- [ ] Add database integration tests
- [ ] Add performance/load tests
- [ ] Add end-to-end tests with real OpenDota API
- [ ] Add test data factories for complex objects
- [ ] Add mutation testing for test quality verification
