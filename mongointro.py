import pymongo
from bson.objectid import ObjectId
try:
    connection = pymongo.MongoClient(connect="false")
except:
    print("vchd")
db = connection.tut
xyz=db.xyz
post={"author":"mke"}
print(xyz.find_one(post))

