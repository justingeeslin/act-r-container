"""
Tests for Docker container specific functionality.
Tests the various ways the container can be started and used.
"""
import pytest
import subprocess
import os
import time
import socket


class TestContainerFunctionality:
    """Test Docker container specific functionality."""
    
    def test_start_script_exists(self):
        """Test that the start-it.sh script exists and is executable."""
        script_path = '/start-it.sh'
        assert os.path.exists(script_path)
        assert os.access(script_path, os.X_OK)
    
    def test_act_r_script_exists(self):
        """Test that the act-r.sh script exists and is executable."""
        script_path = '/act-r.sh'
        assert os.path.exists(script_path)
        assert os.access(script_path, os.X_OK)
    
    def test_jupyter_script_exists(self):
        """Test that the run-jupyter.sh script exists and is executable."""
        script_path = '/run-jupyter.sh'
        assert os.path.exists(script_path)
        assert os.access(script_path, os.X_OK)
    
    def test_environment_html_files_exist(self):
        """Test that the HTML environment files exist."""
        html_files = [
            'environment.html',
            'environment-jupyter.html',
            'expwindow.html',
            'expwindow-jupyter.html',
            'env-link.html',
            'exp-link.html'
        ]
        
        for html_file in html_files:
            assert os.path.exists(html_file), f"Missing HTML file: {html_file}"
    
    def test_tutorial_notebooks_exist(self):
        """Test that tutorial Jupyter notebooks exist."""
        notebooks = [
            'tutorial.ipynb',
            'unit1-demo.ipynb',
            'unit2-demo.ipynb',
            'unit3-demo.ipynb',
            'unit4-demo.ipynb',
            'unit5-demo.ipynb',
            'unit6-demo.ipynb',
            'unit7-demo.ipynb',
            'unit8-demo.ipynb'
        ]
        
        for notebook in notebooks:
            assert os.path.exists(notebook), f"Missing notebook: {notebook}"
    
    def test_actr_directory_structure(self):
        """Test that the ACT-R directory structure is properly set up."""
        actr_dir = os.path.expanduser('~/actr7.x')
        
        # Check main ACT-R files
        assert os.path.exists(os.path.join(actr_dir, 'load-act-r.lisp'))
        
        # Check tutorial directory
        tutorial_dir = os.path.join(actr_dir, 'tutorial')
        assert os.path.exists(tutorial_dir)
        
        # Check original tutorial backup
        original_tutorial_dir = os.path.join(actr_dir, 'original-tutorial')
        if os.path.exists(original_tutorial_dir):
            assert os.path.isdir(original_tutorial_dir)
        
        # Check Python tutorial directory
        python_dir = os.path.join(tutorial_dir, 'python')
        if os.path.exists(python_dir):
            assert os.path.exists(os.path.join(python_dir, 'actr.py'))
    
    def test_node_modules_available(self):
        """Test that required Node.js modules are available."""
        # Check if node is available
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        assert result.returncode == 0
        
        # Check if npm is available
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        assert result.returncode == 0
    
    def test_python_packages_available(self):
        """Test that required Python packages are available."""
        required_packages = ['numpy', 'matplotlib', 'scipy', 'notebook']
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                pytest.fail(f"Required Python package not available: {package}")
    
    def test_actr_loads_with_node_env(self):
        """Test that ACT-R loads successfully with Node.js environment."""
        cmd = [
            'sbcl', '--non-interactive',
            '--load', 'quicklisp/setup.lisp',
            '--load', 'actr7.x/load-act-r.lisp',
            '--eval', '''(progn 
                           (init-des) 
                           (run-node-env) 
                           (format t "ACTR-NODE-ENV-SUCCESS~%") 
                           (quit))'''
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        # ACT-R might exit with different codes but should complete successfully
        assert result.returncode in [0, 1]
        assert 'ACTR-NODE-ENV-SUCCESS' in result.stdout
    
    def test_tutorial_files_copied_correctly(self):
        """Test that tutorial files are properly copied and accessible."""
        # This simulates what start-it.sh does
        tutorial_dir = os.path.expanduser('~/actr7.x/tutorial')
        original_dir = os.path.expanduser('~/actr7.x/original-tutorial')
        
        if os.path.exists(original_dir):
            # Check that we can copy files (simulating container startup)
            assert os.path.isdir(original_dir)
            
            # Check that tutorial directory exists
            assert os.path.exists(tutorial_dir)
    
    def test_pythonpath_setup(self):
        """Test that PYTHONPATH can be set up correctly for ACT-R Python interface."""
        python_path = os.path.expanduser('~/actr7.x/tutorial/python')
        
        if os.path.exists(python_path):
            # Test that we can add this to Python path
            import sys
            original_path = sys.path.copy()
            
            try:
                sys.path.append(python_path)
                # Should be able to find actr module now
                import importlib.util
                spec = importlib.util.find_spec('actr')
                assert spec is not None, "ACT-R Python module not found in tutorial path"
            finally:
                sys.path = original_path
    
    def test_container_user_setup(self):
        """Test that the container user environment is set up correctly."""
        # Check that we're running as the actr user
        import pwd
        current_user = pwd.getpwuid(os.getuid()).pw_name
        
        # In the container, we should be the actr user
        # This test might not apply outside the container
        if os.path.exists('/home/actr'):
            assert current_user == 'actr' or os.getuid() == 1000
            
            # Check home directory setup
            home_dir = os.path.expanduser('~')
            assert os.path.exists(home_dir)
            assert os.path.exists(os.path.join(home_dir, 'actr7.x'))
            assert os.path.exists(os.path.join(home_dir, 'quicklisp'))
    
    def test_file_permissions(self):
        """Test that files have correct permissions."""
        # Check script permissions
        scripts = ['/start-it.sh', '/act-r.sh', '/run-jupyter.sh']
        for script in scripts:
            if os.path.exists(script):
                assert os.access(script, os.X_OK), f"Script not executable: {script}"
        
        # Check that user can write to home directory
        home_dir = os.path.expanduser('~')
        assert os.access(home_dir, os.W_OK), "Cannot write to home directory"