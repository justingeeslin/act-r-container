# ACT-R Container Test Suite

This test suite verifies that the ACT-R Docker container environment is functional and can successfully run ACT-R models from the tutorials.

## Overview

The test suite is organized into three main categories:

1. **Basic ACT-R Tests** (`test_actr_basic.py`) - Tests core ACT-R functionality and environment setup
2. **Tutorial Model Tests** (`test_tutorial_models.py`) - Tests specific ACT-R models and Python interface
3. **Container Functionality Tests** (`test_container_functionality.py`) - Tests Docker container specific features

## Test Categories

### Basic ACT-R Tests
- SBCL (Steel Bank Common Lisp) availability
- Quicklisp package manager setup
- ACT-R directory structure
- ACT-R loading in Lisp
- Python ACT-R module import
- Node.js environment startup

### Tutorial Model Tests
- ACT-R Python module import and basic functions
- Simple counting model (Unit 1 style)
- Production rule models
- Declarative memory retrieval models
- Sequential model execution

### Container Functionality Tests
- Container scripts and permissions
- HTML environment files
- Jupyter notebooks
- Directory structure
- Node.js and Python package availability
- User environment setup

## Running the Tests

### Prerequisites
The tests are designed to run inside the ACT-R Docker container or in an environment with:
- SBCL with ACT-R installed
- Python 3.7+
- Required Python packages (numpy, matplotlib, scipy, notebook)
- Node.js

### Quick Start
```bash
# Run all tests
python run_tests.py

# Run with verbose output
python run_tests.py -v

# Run only basic tests
python run_tests.py --basic-only

# Run only model tests
python run_tests.py --models-only

# Run only container tests
python run_tests.py --container-only

# Run specific test pattern
python run_tests.py -k "test_actr_import"
```

### Using pytest directly
```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_actr_basic.py

# Run with verbose output
pytest tests/ -v

# Run with timeout (useful for long-running tests)
pytest tests/ --timeout=300
```

## Test Design

### Isolation
Each test is designed to be independent and can run in isolation. Tests that require ACT-R to be running use helper functions to start and stop ACT-R processes.

### Timeouts
Long-running tests have timeouts to prevent hanging. The default timeout is 300 seconds (5 minutes) but can be adjusted.

### Error Handling
Tests include comprehensive error handling and will provide detailed output when failures occur.

### Container Compatibility
Tests are designed to work both inside the Docker container and in compatible environments outside the container.

## Expected Behavior

### Successful Test Run
When all tests pass, you should see output indicating:
- ACT-R environment loads successfully
- Python interface works correctly
- Models can be defined and executed
- Container environment is properly configured

### Common Issues

1. **ACT-R Not Starting**: If ACT-R fails to start, check that SBCL and Quicklisp are properly installed
2. **Python Import Errors**: Ensure the PYTHONPATH includes the ACT-R tutorial Python directory
3. **Timeout Errors**: Some tests may take longer on slower systems; increase timeout if needed
4. **Permission Errors**: Ensure proper file permissions in the container environment

## Extending the Tests

To add new tests:

1. **Basic functionality**: Add to `test_actr_basic.py`
2. **Model-specific tests**: Add to `test_tutorial_models.py`
3. **Container features**: Add to `test_container_functionality.py`

### Test Naming Convention
- Test methods should start with `test_`
- Use descriptive names that indicate what is being tested
- Group related tests in the same class

### Helper Functions
Use the helper functions in `conftest.py` for common operations like starting ACT-R environments.

## Continuous Integration

These tests can be integrated into CI/CD pipelines to automatically verify:
- Container builds correctly
- ACT-R environment is functional
- Tutorial models work as expected
- No regressions in functionality

## Troubleshooting

### Debug Mode
Run tests with maximum verbosity to see detailed output:
```bash
python run_tests.py -v
pytest tests/ -v -s
```

### Individual Test Debugging
Run a single test to isolate issues:
```bash
pytest tests/test_actr_basic.py::TestACTRBasic::test_sbcl_available -v
```

### Log Output
Check ACT-R and system logs for additional debugging information when tests fail.