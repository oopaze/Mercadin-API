import pytest
from run import app as aplicattion

@pytest.fixture(scope='module')
def app():
    """ Instance of Main Flask App """
    return aplicattion
