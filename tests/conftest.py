"""
Test configuration and fixtures for ACT-R container tests.
"""
import pytest
import subprocess
import time
import os
import signal
import socket
from contextlib import contextmanager


def is_port_open(host, port, timeout=5):
    """Check if a port is open and accepting connections."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


@contextmanager
def actr_environment():
    """
    Context manager to start and stop ACT-R environment for testing.
    This starts ACT-R in the background and ensures it's cleaned up.
    """
    # Start ACT-R in background mode
    env = os.environ.copy()
    env['PYTHONPATH'] = f"{env.get('PYTHONPATH', '')}:{os.path.expanduser('~/actr7.x/tutorial/python')}"
    
    process = subprocess.Popen([
        'sbcl', '--non-interactive',
        '--load', 'quicklisp/setup.lisp',
        '--load', 'actr7.x/load-act-r.lisp',
        '--eval', '(progn (init-des) (run-node-env) (loop))'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    
    # Wait for ACT-R to start (check if port 2650 is open)
    max_wait = 30  # seconds
    wait_time = 0
    while wait_time < max_wait:
        if is_port_open('localhost', 2650):
            break
        time.sleep(1)
        wait_time += 1
    
    if wait_time >= max_wait:
        process.terminate()
        raise RuntimeError("ACT-R failed to start within timeout period")
    
    try:
        yield process
    finally:
        # Clean up: terminate the process
        try:
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


@pytest.fixture(scope="session")
def actr_session():
    """Session-scoped fixture that provides an ACT-R environment for all tests."""
    with actr_environment() as process:
        yield process


@pytest.fixture
def actr_connection():
    """Fixture that provides a fresh ACT-R connection for each test."""
    try:
        import actr
        # Reset ACT-R state for clean test
        actr.reset()
        yield actr
    except ImportError:
        pytest.skip("ACT-R Python module not available")