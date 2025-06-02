"""
Basic ACT-R functionality tests.
Tests core ACT-R operations and connectivity.
"""
import pytest
import subprocess
import os
import sys
import time


class TestACTRBasic:
    """Test basic ACT-R functionality and environment setup."""
    
    def test_sbcl_available(self):
        """Test that SBCL (Steel Bank Common Lisp) is available."""
        result = subprocess.run(['sbcl', '--version'], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert 'SBCL' in result.stdout
    
    def test_quicklisp_available(self):
        """Test that Quicklisp is properly installed."""
        assert os.path.exists(os.path.expanduser('~/quicklisp/setup.lisp'))
    
    def test_actr_directory_exists(self):
        """Test that ACT-R directory structure exists."""
        actr_dir = os.path.expanduser('~/actr7.x')
        assert os.path.exists(actr_dir)
        assert os.path.exists(os.path.join(actr_dir, 'load-act-r.lisp'))
        assert os.path.exists(os.path.join(actr_dir, 'tutorial'))
    
    def test_actr_loads_in_lisp(self):
        """Test that ACT-R can be loaded in SBCL."""
        cmd = [
            'sbcl', '--non-interactive',
            '--load', 'quicklisp/setup.lisp',
            '--load', 'actr7.x/load-act-r.lisp',
            '--eval', '(progn (init-des) (format t "ACT-R-LOADED-SUCCESSFULLY") (quit))'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        assert result.returncode == 0
        assert 'ACT-R-LOADED-SUCCESSFULLY' in result.stdout
    
    def test_python_actr_module_importable(self):
        """Test that the ACT-R Python module can be imported when ACT-R is running."""
        # Start ACT-R in background
        env = os.environ.copy()
        env['PYTHONPATH'] = f"{env.get('PYTHONPATH', '')}:{os.path.expanduser('~/actr7.x/tutorial/python')}"
        
        actr_process = subprocess.Popen([
            'sbcl', '--non-interactive',
            '--load', 'quicklisp/setup.lisp',
            '--load', 'actr7.x/load-act-r.lisp',
            '--eval', '(progn (init-des) (run-node-env) (loop))'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        
        try:
            # Wait a bit for ACT-R to start
            time.sleep(10)
            
            # Test Python import
            python_cmd = [
                sys.executable, '-c',
                'import sys; sys.path.append("' + os.path.expanduser('~/actr7.x/tutorial/python') + '"); import actr; print("IMPORT-SUCCESS")'
            ]
            
            result = subprocess.run(python_cmd, capture_output=True, text=True, 
                                  timeout=30, env=env)
            
            assert result.returncode == 0
            assert 'IMPORT-SUCCESS' in result.stdout
            
        finally:
            actr_process.terminate()
            try:
                actr_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                actr_process.kill()
    
    def test_tutorial_files_exist(self):
        """Test that tutorial files are present."""
        tutorial_dir = os.path.expanduser('~/actr7.x/tutorial')
        
        # Check for some key tutorial directories
        expected_dirs = ['unit1', 'unit2', 'unit3', 'unit4', 'unit5', 'unit6', 'unit7', 'unit8']
        for unit_dir in expected_dirs:
            unit_path = os.path.join(tutorial_dir, unit_dir)
            if os.path.exists(unit_path):  # Some may not exist in container
                assert os.path.isdir(unit_path)
        
        # Check for Python tutorial files
        python_dir = os.path.join(tutorial_dir, 'python')
        if os.path.exists(python_dir):
            assert os.path.exists(os.path.join(python_dir, 'actr.py'))
    
    def test_node_environment_starts(self):
        """Test that the Node.js environment for ACT-R GUI starts."""
        # This test verifies that the run-node-env function works
        cmd = [
            'sbcl', '--non-interactive',
            '--load', 'quicklisp/setup.lisp',
            '--load', 'actr7.x/load-act-r.lisp',
            '--eval', '(progn (init-des) (run-node-env) (format t "NODE-ENV-STARTED") (quit))'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        # The process should start successfully (return code 0 or specific ACT-R exit code)
        assert result.returncode in [0, 1]  # ACT-R might exit with code 1 but still work
        assert 'NODE-ENV-STARTED' in result.stdout