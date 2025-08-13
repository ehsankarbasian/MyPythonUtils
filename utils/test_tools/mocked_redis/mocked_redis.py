# pip install fakeredis

import fakeredis
from fakeredis import TcpFakeServer
from threading import Thread


def run_fake_server(server_address):
    server = TcpFakeServer(server_address, server_type="redis")
    t = Thread(target=server.serve_forever, daemon=True)
    t.start()
    
    return server_address


def get_fake_client():
    client = fakeredis.FakeStrictRedis(server_type="redis")
    return client


'''
Use as a pytest fixture¶

import pytest

@pytest.fixture
def redis_client(request):
    import fakeredis
    redis_client = fakeredis.FakeRedis()
    return redis_client
'''
