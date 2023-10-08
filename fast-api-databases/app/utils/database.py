def test_database_connection():
    import os
    from pymongo.mongo_client import MongoClient

    mongo_user = os.getenv('MONGODB_USER')
    mongo_pass = os.getenv('MONGODB_PASSWORD')
    mongo_host = os.getenv('MONGODB_HOST')
    mongo_port = os.getenv('MONGODB_PORT')

    uri = f'mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/?retryWrites=true&w=majority'
    client = MongoClient(uri)

    try:
        # send a ping to the admin database to confirm a connection
        client.admin.command()
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
