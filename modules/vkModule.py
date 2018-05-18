# VK MODULE, which keep all vk api requests
import sys
sys.path.append('../')

import requests
import tools
import json


BOT_TOKEN = tools.data['BOT_TOKEN']

BASE_URL = 'https://api.vk.com/method/'


# Главная фукция method позволяет сделать запрос посредству передачи в неё словаря с параметрами

def method(method, params=False):
    requestStr = BASE_URL + method + "?access_token=%s&v=5.74" % (BOT_TOKEN)
    if params:
        for i in params:
            requestStr += "&" + str(i) + "=" + str(params[str(i)])
        query = requests.get(requestStr)
        return json.loads(query.text)
    # Написать логирование
    query = requests.get(requestStr)
    return json.loads(query.text)


