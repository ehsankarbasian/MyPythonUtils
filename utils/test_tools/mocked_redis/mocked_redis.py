import fakeredis
from fakeredis import TcpFakeServer
from threading import Thread


def run_fake_server():
    server_address = ("127.0.0.1", 6379)
    server = TcpFakeServer(server_address, server_type="redis")
    t = Thread(target=server.serve_forever, daemon=True)
    t.start()
    
    return server_address


def get_fake_client():
    client = fakeredis.FakeStrictRedis(server_type="redis")
    return client


# TODO Read more: https://fakeredis.readthedocs.io/en/latest/
