# Test Infrastructure Setup Guide

## ✅ Completed Test Infrastructure

The backend now has a comprehensive test infrastructure with:

- **pytest.ini** - Test configuration with coverage settings
- **tests/conftest.py** - Shared fixtures and test setup
- **8 test files** with 673 total lines covering:
  - Main application endpoints (`test_main.py`)
  - Configuration management (`test_config.py`)
  - Cache implementation (`test_cache.py`)
  - HTTP client (`test_client.py`)
  - Player API endpoints (`test_api_players.py`)
  - Hero API endpoints (`test_api_heroes.py`)
  - Cache API endpoints (`test_api_cache.py`)

## Setup Instructions

### 1. Install Test Dependencies

First, ensure your virtual environment is activated and dependencies are installed:

```bash
cd /Users/lalo/Documents/Dev/Dota-2-Project

# Activate virtual environment
source .venv/bin/activate

# Install backend dependencies (includes pytest, pytest-asyncio, pytest-cov)
pip install -r backend/requirements.txt
```

### 2. Verify Installation

Check that pytest is installed:

```bash
pytest --version
```

Should output something like: `pytest 7.4.3`

### 3. Run Tests

From the project root or backend directory:

```bash
# From project root
pytest backend/tests

# Or from backend directory
cd backend
pytest
```

### 4. Run Tests with Coverage

```bash
cd backend
pytest --cov=app --cov-report=term-missing --cov-report=html
```

This will:
- Run all tests
- Show coverage statistics
- Generate an HTML coverage report in `htmlcov/`

### 5. View Coverage Report

```bash
open htmlcov/index.html  # Opens in your default browser
```

## Quick Test Commands

```bash
# Run all tests
pytest

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_cache.py

# Run specific test
pytest tests/test_cache.py::test_cache_set_and_get

# Stop at first failure
pytest -x

# Show local variables in tracebacks
pytest -l
```

## Test Structure Overview

```
backend/
├── pytest.ini                  # Pytest configuration
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Fixtures: client, async_client, mock_opendota_response
│   ├── test_main.py           # 5 tests - Main endpoints (/health, /, /docs)
│   ├── test_config.py         # 5 tests - Settings and configuration
│   ├── test_cache.py          # 9 tests - Cache operations and TTL
│   ├── test_client.py         # 5 tests - HTTP client and OpenDota API
│   ├── test_api_players.py    # 12 tests - Player endpoints with caching
│   ├── test_api_heroes.py     # 4 tests - Hero and items endpoints
│   └── test_api_cache.py      # 2 tests - Cache management endpoints
```

## Expected Test Results

When properly configured, you should see output similar to:

```
============ test session starts ============
collected 42 items

tests/test_main.py .....                [ 11%]
tests/test_config.py .....               [ 23%]
tests/test_cache.py .........            [ 45%]
tests/test_client.py .....               [ 57%]
tests/test_api_players.py ............ [ 85%]
tests/test_api_heroes.py ....            [ 95%]
tests/test_api_cache.py ..               [100%]

============ 42 passed in 2.34s ============
```

## Troubleshooting

### Issue: Module not found errors

**Solution:**
```bash
# Ensure you're in the backend directory
cd backend

# Run pytest as a module
python -m pytest
```

### Issue: ImportError for app modules

**Solution:**
```bash
# Make sure PYTHONPATH includes the backend directory
export PYTHONPATH=/Users/lalo/Documents/Dev/Dota-2-Project/backend:$PYTHONPATH
pytest
```

### Issue: Tests fail due to missing main.py

**Note:** The tests reference `app.main_new` because that's the current restructured version. If tests fail:

1. Check that `backend/app/main_new.py` exists
2. Or rename it to `main.py` if you've finalized the structure

## Next Steps

1. ✅ Install dependencies: `pip install -r backend/requirements.txt`
2. ✅ Run tests: `pytest backend/tests`
3. ✅ Check coverage: `pytest --cov=app --cov-report=html`
4. Continue with remaining tasks:
   - Update frontend package manager consistency
   - Fix docker-compose port alignment
   - Update README.md

## Integration with CI/CD

These tests are ready for CI/CD integration. Example GitHub Actions workflow:

```yaml
- name: Run tests
  run: |
    cd backend
    pytest --cov=app --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./backend/coverage.xml
```
