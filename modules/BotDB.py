from pymongo import MongoClient

client = MongoClient()

CategoriesDB = client['CategoriesDB']
MessagesDB = client['MessagesDB']
ContentDB = client['ContentDB']

def getAllThemes(category):
    result = []
    if category == 'content':
        for i in CategoriesDB.AllContentThemes.find():
            result.append(i['name'])
    if category == 'message':
        for i in CategoriesDB.AllMessagesThemes.find():
            result.append(i['name'])
    return result

def CheckTheme(name,category):
    if category == 'content':
        for i in CategoriesDB.AllContentThemes.find():
            if i['name'] == name:
                return False
        return True
    elif category == 'message':
        for i in CategoriesDB.AllMessagesThemes.find():
            if name == i['name']:
                return False
        return True


def GetFilePath(Image):
    Image = Image.replace('http://nervoed.ru','/var/www/nervoed.ru/web')
    return Image

def GetItemData(name,category):
    result = []
    if category == 'content':
        imagePath = []
        content = []
        for i in ContentDB['%s' % name].find():
            content.append(i['content'])
            imagePath.append(i['ImagePath'])
        result = {
            "Content" : content,
            "ImagePath" : imagePath
        }
        return result
    elif category == 'message':
        stopWords = []
        answers = []
        for i in MessagesDB['%s' % name].find({}, {"StopWord": 1, "_id":0}):
            if i:
                stopWords.append(i['StopWord'])
        for i in MessagesDB['%s' % name].find({}, {"answer": 1, "_id":0}):
            if i:
                answers.append(i['answer'])
        result = {
        "stopWords": stopWords,
        "answers": answers
        }
    return result

def GetAnswersAndWords():
    result = []
    collections = MessagesDB.collection_names()
    collections.remove("init")
    for collection in collections:
        item = [{
            "Answers": [],
            "StopWords" : []
        }]
        for ItemCollection in MessagesDB['%s' % collection].find({}, {"answer": 1, "_id":0}):
            if ItemCollection:
                item[0]['Answers'].append(ItemCollection['answer'])
        for ItemCollection in MessagesDB['%s' % collection].find({}, {"StopWord": 1, "_id":0}):
            if ItemCollection:
                item[0]['StopWords'].append(ItemCollection['StopWord'])
        result.extend(item)
    return result




def DeleteMessage(name,MessageType,MessageName):
    print(MessageType)
    print(name)
    print(MessageName)
    MessagesDB["%s" % name].remove({MessageType:MessageName})
    # if not MessagesDB["%s" % name].find():
    #     RemoveThemeFrom("AllMessagesTheme",{"name":name})
    return True

def DeleteContent(name,ContentName):
    ContentDB["%s" % name].remove({"content":ContentName})
    # if not ContentDB["%s" % name].find():
    #     RemoveThemeFrom("AllContentTheme",{"name":name})
    return True

def InsertThemeTo(database,data):
    CategoriesDB['%s' % database].insert_one(data)

def CreateThemeCollection(database,item, data,ImagePath="Null"):
    if item == 'content':
        ContentDB['%s' % database].insert_one({"content": data, "ImagePath":ImagePath})
    elif item == 'message':
        for i in data["stopWords"]:
            MessagesDB['%s' % database].insert_one({"StopWord":i})
        for i in data["answers"]:
            MessagesDB['%s' % database].insert_one({"answer":i})

def RemoveThemeFrom(database,data):
    CategoriesDB['%s' % database].remove(data)

def RemoveCollection(database,category):
    if category == 'message':
        MessagesDB.drop_collection('%s' % database)
    elif category == 'content':
        ContentDB.drop_collection('%s' % database)


