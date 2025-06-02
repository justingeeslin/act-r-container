#!/usr/bin/env python3
"""
Test runner for ACT-R container tests.
This script runs the test suite and provides a summary of results.
"""
import subprocess
import sys
import os
import argparse


def install_test_dependencies():
    """Install test dependencies if needed."""
    try:
        import pytest
    except ImportError:
        print("Installing test dependencies...")
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'tests/requirements.txt'
        ])


def run_tests(test_pattern=None, verbose=False, timeout=300):
    """Run the test suite."""
    install_test_dependencies()
    
    # Prepare pytest command
    cmd = [sys.executable, '-m', 'pytest', 'tests/']
    
    if verbose:
        cmd.append('-v')
    else:
        cmd.append('-q')
    
    # Add timeout for long-running tests
    cmd.extend(['--timeout', str(timeout)])
    
    # Add specific test pattern if provided
    if test_pattern:
        cmd.extend(['-k', test_pattern])
    
    # Add output formatting
    cmd.extend(['--tb=short'])
    
    print(f"Running command: {' '.join(cmd)}")
    print("=" * 60)
    
    # Run tests
    result = subprocess.run(cmd)
    
    print("=" * 60)
    if result.returncode == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description='Run ACT-R container tests')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    parser.add_argument('-k', '--pattern', type=str,
                       help='Run only tests matching this pattern')
    parser.add_argument('-t', '--timeout', type=int, default=300,
                       help='Timeout for individual tests (seconds)')
    parser.add_argument('--basic-only', action='store_true',
                       help='Run only basic functionality tests')
    parser.add_argument('--models-only', action='store_true',
                       help='Run only model tests')
    parser.add_argument('--container-only', action='store_true',
                       help='Run only container functionality tests')
    
    args = parser.parse_args()
    
    # Set test pattern based on flags
    pattern = args.pattern
    if args.basic_only:
        pattern = 'test_actr_basic'
    elif args.models_only:
        pattern = 'test_tutorial_models'
    elif args.container_only:
        pattern = 'test_container_functionality'
    
    # Change to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    return run_tests(pattern, args.verbose, args.timeout)


if __name__ == '__main__':
    sys.exit(main())