import os
import pytest
import shutil
import entrypoint

build = entrypoint.get_constant(*entrypoint.constants.build_directory)
workspace = entrypoint.get_constant(*entrypoint.constants.workspace)
BUILD_DIR = f'{workspace}/{build}'

@pytest.fixture
def remove_build_dir():
    def remove():
        if os.path.exists(BUILD_DIR):
            shutil.rmtree(BUILD_DIR)
        assert os.path.exists(BUILD_DIR) is False
    return remove

def test_get_constant(monkeypatch):
    assert entrypoint.get_constant('LAMBDA_CODE_DIR', 'src')== 'src'
    assert entrypoint.get_constant(*entrypoint.constants.workspace) == '/'
    assert entrypoint.get_constant(*entrypoint.constants.build_directory) == 'package'

    monkeypatch.setenv('LAMBDA_CODE_DIR', '/tests/src')
    assert entrypoint.get_constant(*entrypoint.constants.code_dir) == '/tests/src'
    # value = entrypoint.get_constant('LAMBDA_CODE_DIR', '../../src')
    # assert value == 'src'

def test_copy_source_to_build(monkeypatch, remove_build_dir):
    remove_build_dir()
    monkeypatch.setenv('LAMBDA_CODE_DIR', '/tests/src')
    entrypoint.copy_source_to_build()
    assert os.path.exists(f'{BUILD_DIR}/lambda_function.py')
    assert os.path.exists(f'{BUILD_DIR}/requirements.txt')
    remove_build_dir()
    monkeypatch.setenv('PRESERVE_ROOT', 'True')
    entrypoint.copy_source_to_build()
    assert os.path.exists(f'{BUILD_DIR}/src/lambda_function.py')
    assert os.path.exists(f'{BUILD_DIR}/src/requirements.txt')
    remove_build_dir()

def test_install_dependencies(monkeypatch, remove_build_dir):
    remove_build_dir()
    monkeypatch.setenv('LAMBDA_CODE_DIR', '/tests/src')
    monkeypatch.setenv('REQUIREMENTS_FILE', 'requirements.txt')
    entrypoint.copy_source_to_build()
    assert entrypoint.install_dependencies() is 0
    remove_build_dir()

def test_package_contents(monkeypatch, remove_build_dir):
    remove_build_dir()
    monkeypatch.setenv('LAMBDA_CODE_DIR', '/tests/src')
    monkeypatch.setenv('REQUIREMENTS_FILE', 'requirements.txt')
    entrypoint.copy_source_to_build()
    assert entrypoint.package_contents()
    assert os.path.exists('/package.zip')
    remove_build_dir()