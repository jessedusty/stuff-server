from pymongo import MongoClient
print("started mongo client")
client = MongoClient("mongodb://db")

db = client.stuff

def infoForItem(identifer):
    index =  db.items.find({"key":identifer})
    return index[0]


def insertItem(info):
    db.items.insert_one(info)
