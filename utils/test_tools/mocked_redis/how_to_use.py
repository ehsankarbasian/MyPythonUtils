import redis
from mocked_redis import run_fake_server, get_fake_client


server_address = run_fake_server()
client = redis.Redis(host=server_address[0], port=server_address[1])
client.set("foo", "bar")
print(client.get("foo") == b"bar")


client = get_fake_client()
client.set("goo", "gar")
print(client.exists("foo"))
print(client.exists("goo"))
print(client.get("goo") == b"gar")
