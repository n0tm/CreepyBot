import sys
sys.path.append('modules')
import vkModule
import BotDB
import random
import time
import requests

def CheckNewMessages():
    return vkModule.method('messages.getDialogs', {
           "count" : 200,
            "unread" : 1
    })['response']['items']

def CheckMenu(messages):
    for i in messages:
        if i['message']['body'].lower() == 'скинь кошмары':
            #Показываем истории
            AnswerString = 'Выбери тему:\n'
            themesArray = BotDB.getAllThemes('content')
            for theme in themesArray:
                AnswerString += '\n' + theme
            AnswerString += '\n Если хочешь увидеть самые страшные кошмары, то НАПИШИ\n\n"Скинь мне немного <НАЗВАНИЕ ТЕМЫ ИЗ СПИСКА>"'
            vkModule.method('messages.send', {
                "user_id": i['message']['user_id'],
                "message": AnswerString
            })
            return True
        elif i['message']['body'].lower() == 'поговори со мной':
            vkModule.method('messages.send', {
                "user_id" : i['message']['user_id'],
                "message" : "Если ты не боишься смерти, я готов с тобой поговорить"
            })
            return True
def SendCategoryContent(messages):
    for i in messages:
        if 'скинь мне немного' in i['message']['body'].lower():
            textFrom = i['message']['body'].lower()
            textFrom = textFrom.replace('скинь мне немного','')
            textFrom = textFrom.replace('.','')
            textFrom = textFrom.replace(',','')
            textFrom = textFrom[1:]
            themesArray = BotDB.getAllThemes('content')
            for theme in themesArray:
                if textFrom in theme:
                    data = BotDB.GetItemData(theme, 'content')
                    RandomInt = random.randint(0, len(data['Content']) - 1)
                    ImagePath = data['ImagePath'][RandomInt]
                    AnswerString = data['Content'][RandomInt]
                    if ImagePath == 'Null':
                        vkModule.method('messages.send', {
                            "user_id": i['message']['user_id'],
                            "message": AnswerString
                        })
                    else:
                        uploadServer = vkModule.method('photos.getMessagesUploadServer')['response']['upload_url']
                        file = {'file1' : open(BotDB.GetFilePath(ImagePath), 'rb')}
                        uploadPhoto = requests.post(uploadServer, files=file).json()
                        time.sleep(1/3)
                        attachment = vkModule.method('photos.saveMessagesPhoto', {
                            "server" : uploadPhoto['server'],
                            "photo" : uploadPhoto['photo'],
                            "hash" : uploadPhoto['hash'],
                        })
                        time.sleep(1/3)
                        vkModule.method('messages.send', {
                            "user_id": i['message']['user_id'],
                            "message": AnswerString,
                            "attachment" : "photo" + str(attachment['response'][0]['owner_id']) + '_' + str(attachment['response'][0]['id'])
                        })
                    return True

def LazyTalk(messages):
    for i in messages:
        for data in BotDB.GetAnswersAndWords():
            for StopWord in data['StopWords']:
                if StopWord.lower() in i['message']['body'].lower():
                    AnswerString = data['Answers'][random.randint(0,len(data['Answers']) - 1)]
                    vkModule.method('messages.send', {
                        "user_id": i['message']['user_id'],
                        "message": AnswerString
                    })


def main():
    CheckMenu(CheckNewMessages())
    time.sleep(1)
    SendCategoryContent(CheckNewMessages())
    time.sleep(1)
    LazyTalk(CheckNewMessages())
    time.sleep(1)

while True:
    main()






