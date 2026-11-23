import os

import pymongo

client = pymongo.MongoClient(os.environ.get("MONGODB_URI", "mongodb://localhost:27017"), connect=False)
db = client["FakeNews"]
