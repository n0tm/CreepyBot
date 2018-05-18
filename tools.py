from datetime import datetime
import json

pathToData = 'data.json'
with open(pathToData, 'r') as f:
    data = json.loads(f.read())

def logsDate():
    return datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
