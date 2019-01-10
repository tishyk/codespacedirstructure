import pytest

@pytest.fixture(scope='module') # scope='function', autouse=True
def Server():
    class Dummy:
        host_port = 'localhost', 8081
        uri = 'http://%s:%s/' % host_port
    return Dummy