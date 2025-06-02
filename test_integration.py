#!/usr/bin/env python3
"""
Integration test script for ACT-R container.
This script performs a quick integration test to verify basic functionality.
"""
import subprocess
import sys
import os
import time


def run_command(cmd, timeout=30, check=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, 
                              text=True, timeout=timeout, check=check)
        return result
    except subprocess.TimeoutExpired:
        print(f"Command timed out: {cmd}")
        return None
    except subprocess.CalledProcessError as e:
        if check:
            print(f"Command failed: {cmd}")
            print(f"Return code: {e.returncode}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
        return e


def test_basic_environment():
    """Test basic environment setup."""
    print("🔍 Testing basic environment...")
    
    # Test Python
    result = run_command("python3 --version")
    if result and result.returncode == 0:
        print("✅ Python available")
    else:
        print("❌ Python not available")
        return False
    
    # Test file structure
    required_files = [
        'Dockerfile',
        'README.md',
        'start-it.sh',
        'act-r.sh',
        'run-jupyter.sh'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            return False
    
    return True


def test_container_scripts():
    """Test that container scripts exist and are executable."""
    print("\n🔍 Testing container scripts...")
    
    scripts = ['/start-it.sh', '/act-r.sh', '/run-jupyter.sh']
    for script in scripts:
        if os.path.exists(script) and os.access(script, os.X_OK):
            print(f"✅ {script} exists and is executable")
        else:
            print(f"❌ {script} missing or not executable")
            return False
    
    return True


def test_actr_environment():
    """Test ACT-R environment basics."""
    print("\n🔍 Testing ACT-R environment...")
    
    # Check if SBCL is available
    result = run_command("sbcl --version", check=False)
    if result and result.returncode == 0:
        print("✅ SBCL available")
    else:
        print("❌ SBCL not available")
        return False
    
    # Check ACT-R directory
    actr_dir = os.path.expanduser('~/actr7.x')
    if os.path.exists(actr_dir):
        print("✅ ACT-R directory exists")
    else:
        print("❌ ACT-R directory missing")
        return False
    
    # Check Quicklisp
    quicklisp_setup = os.path.expanduser('~/quicklisp/setup.lisp')
    if os.path.exists(quicklisp_setup):
        print("✅ Quicklisp setup exists")
    else:
        print("❌ Quicklisp setup missing")
        return False
    
    return True


def test_actr_loading():
    """Test that ACT-R can be loaded."""
    print("\n🔍 Testing ACT-R loading...")
    
    cmd = '''sbcl --non-interactive \
        --load quicklisp/setup.lisp \
        --load actr7.x/load-act-r.lisp \
        --eval '(progn (init-des) (format t "ACT-R-LOAD-SUCCESS~%") (quit))'
    '''
    
    result = run_command(cmd, timeout=60, check=False)
    if result and 'ACT-R-LOAD-SUCCESS' in result.stdout:
        print("✅ ACT-R loads successfully")
        return True
    else:
        print("❌ ACT-R failed to load")
        if result:
            print(f"Return code: {result.returncode}")
            print(f"Stdout: {result.stdout}")
            print(f"Stderr: {result.stderr}")
        return False


def test_python_tests():
    """Test that our test suite can run."""
    print("\n🔍 Testing Python test suite...")
    
    # Run a simple test
    result = run_command("python3 -m pytest tests/test_container_functionality.py::TestContainerFunctionality::test_tutorial_notebooks_exist -v", 
                        timeout=30, check=False)
    
    if result and result.returncode == 0:
        print("✅ Python tests can run")
        return True
    else:
        print("❌ Python tests failed")
        if result:
            print(f"Return code: {result.returncode}")
            print(f"Stdout: {result.stdout}")
            print(f"Stderr: {result.stderr}")
        return False


def main():
    """Run all integration tests."""
    print("🚀 Starting ACT-R Container Integration Tests")
    print("=" * 50)
    
    tests = [
        test_basic_environment,
        test_container_scripts,
        test_actr_environment,
        test_actr_loading,
        test_python_tests
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ Test failed: {test.__name__}")
        except Exception as e:
            print(f"❌ Test error in {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        return 0
    else:
        print("💥 Some integration tests failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())