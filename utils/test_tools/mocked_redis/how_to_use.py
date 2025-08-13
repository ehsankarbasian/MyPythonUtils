import redis
from mocked_redis import run_fake_server, get_fake_client


server_address = ("127.0.0.1", 6379)
run_fake_server(server_address)
client = redis.Redis(host=server_address[0], port=server_address[1])
client.set("foo", "bar")
assert client.get("foo") == b'bar'


client = get_fake_client()
client.set("goo", "gar")
assert client.exists("foo") == 0
assert client.exists("goo") == 1
assert client.get("goo") == b'gar'
