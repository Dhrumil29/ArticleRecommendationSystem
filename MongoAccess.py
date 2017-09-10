import pymongo
from bson.objectid import ObjectId

# try:
#     connection = pymongo.MongoClient(connect="false")
# except:
#     print("vchd")
# db = connection.tut
# xyz=db.xyz
# cursor=xyz.find({"name":"aslam"}).distinct("name")
#
# for document in cursor:
#     print(document)
def url_with_key_freq(url,keywords):
