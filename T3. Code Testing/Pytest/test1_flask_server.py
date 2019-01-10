import datetime
import pytest
import socket as s


@pytest.fixture
def socket(request):
    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    def socket_teardown():
        _socket.close()
    request.addfinalizer(socket_teardown)
    return _socket

# or this one context manager
@pytest.yield_fixture
def socket():
    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    yield _socket
    _socket.close()

@pytest.fixture(scope='module') # scope='function', autouse=True
def Server():
    class Dummy:
        host_port = 'localhost', 8081
        uri = 'http://%s:%s/' % host_port
    return Dummy

# Get fixture name example only
@pytest.yield_fixture(scope='function', autouse=True)
def collect_logs(request):
    if 'Server' in request.fixturenames:
        # with some_logfile_collector(SERVER_LOCATION):
        yield
    else:
        yield


@pytest.yield_fixture
def reset_shifted_time(Service):
    yield
    Service.set_time(datetime.datetime.now())

# Test to check server exist on localhost 8081 port
def test_server_connect(socket):
    socket.connect(('localhost', 8081))
    assert socket

def test2_server_connect(socket, Server):
    socket.connect(Server.host_port)
    assert socket

# @pytest.mark.usefixtures("reset_shifted_time")
# Need Service class with set_time method for this example
# class TestWithShiftedTime():
#     def test_shift_milesecond(self, Service):
#         Service.set_time()
#         assert True
#     def test_shift_time_far_far_away(self, Service):
#         Service.set_time()
#         assert True

def test_dict():
    assert dict(foo='bar', baz=None).items() == list({'foo': 'bar'}.items())