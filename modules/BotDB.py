from pymongo import MongoClient

client = MongoClient()
db = client['CreepyBot']


def getAllContentThemes():
    result = []
    for i in db.AllContentThemes.find():
        result.append(i['name'])
    return result


def getAllMessagesThemes():
    result = []
    for i in db.AllMessagesThemes.find():
        result.append(i['name'])
    return result


def InsertTo(database,data):
    db['%s' % database].insert_one(data)

def RemoveFrom(database,data):
    db['%s' % database].remove(data)


