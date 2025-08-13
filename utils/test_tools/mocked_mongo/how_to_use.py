from mocked_mongo import get_mongo_mocked_colletion, mocked_tunnel, close_mongo_mocked


collection = get_mongo_mocked_colletion('my_collection')
collection.insert_one({'name': 'a'})
collection.insert_one({'name': 'b'})
collection.insert_one({'name': 'c'})

a = collection.find_one({'name': 'b'})
print(a)
a = collection.find_one({'name': 'D'})
print(a)


close_mongo_mocked(mocked_tunnel, collection)
a = collection.find_one({'name': 'b'})
print(a)
