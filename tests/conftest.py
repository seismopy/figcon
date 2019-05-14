"""
pytest configuration for figcon
"""
from pathlib import Path

import pytest


from figcon import Figcon

# --------- Add key paths to pytest namespace
TEST_PATH = Path(__file__).parent
PKG_PATH = TEST_PATH.parent
TEST_DATA_PATH = TEST_PATH / 'data'


@pytest.fixture
def default_config_1():
    """ return a path to the first config file. """
    return TEST_DATA_PATH / 'config1.py'


@pytest.fixture
def home_cwd(tmpdir):
    """ create two temporary directories simulated cwd and home.
    Return dict with contents. """
    cwd = Path(tmpdir)
    home = cwd / "home"
    home.mkdir()
    return dict(secondary_path=home, primary_path=cwd)


@pytest.fixture
def figcon(home_cwd, default_config_1):
    """ Init an options object. """
    return Figcon(default_path=default_config_1, **home_cwd)


@pytest.fixture
def config_paths():
    """ return a dict of configs in test data path. """
    path = Path(TEST_DATA_PATH) / 'config'
    return {x.name: x for x in path.rglob("*.py")}



