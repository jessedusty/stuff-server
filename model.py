from pymongo import MongoClient
import gridfs
from bson.objectid import ObjectId

print("started mongo client")
client = MongoClient("mongodb://db")

db = client.stuff
fs = gridfs.GridFS(db)

def infoForItem(identifer):
    index = db.items.find({"key":identifer})
    if index.count() <= 0:
        return None
    return index[0]


def itemExists(identifer):
    index = db.items.find({"key":identifer})
    if index.count() > 0: return True
    return False


def insertItem(info):
    db.items.insert_one(info)


def handlePOST(request_form):
    d =  dict(request_form)
    nd = {}
    for key in d:
        nd[key] = d[key][0]
    return nd


def getKeys():
    return str(db.items.distinct("key")).replace("\'", "\"")
