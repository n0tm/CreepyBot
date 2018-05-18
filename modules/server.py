from flask import Flask, jsonify, Response, request
from flask_cors import CORS, cross_origin

import requests
import json
import BotDB

app = Flask('nervoed')
CORS(app)

@app.route('/getAllThemes', methods=['GET'])
def getAllThemes():
    category = request.args['category']
    return jsonify({'success': BotDB.getAllThemes(category)})

@app.route('/CheckTheme', methods=['GET'])
def CheckTheme():
    category = request.args['category']
    name = request.args['name']
    name = name.lower()
    return jsonify({'success': BotDB.CheckTheme(name,category)})

@app.route('/GetItemData', methods=['GET'])
def GetItemData():
    name = request.args['name']
    name = name.lower()
    category = request.args['category']
    result = BotDB.GetItemData(name,category)
    return jsonify({'success': result})

@app.route('/AddMessageTheme', methods=['GET'])
def AddMessageTheme():
    theme = request.args['name']
    theme = theme.lower()
    data = request.args['data']
    data = json.loads(data)
    BotDB.InsertThemeTo('AllMessagesThemes', {"name": theme})
    BotDB.CreateThemeCollection(theme,'message', data)
    return jsonify({'success': True})

@app.route('/AddContentTheme', methods=['GET'])
def AddContentTheme():
    theme = request.args['name']
    ImagePath = request.args['imagePath']
    theme = theme.lower()
    content = request.args['content']
    if (BotDB.CheckTheme(theme, 'content')):
        BotDB.InsertThemeTo('AllContentThemes', {"name": theme})
    BotDB.CreateThemeCollection(theme,'content', content, ImagePath)
    return jsonify({'success': True})

@app.route('/RemoveTheme', methods=['GET'])
def RemoveTheme():
    theme = request.args['name']
    theme = theme.lower()
    category = request.args['category']
    if category == 'message':
        BotDB.RemoveThemeFrom('AllMessagesThemes', {"name": theme})
        BotDB.RemoveCollection(theme,'message')
    if category == 'content':
        BotDB.RemoveThemeFrom('AllContentThemes', {"name": theme})
        BotDB.RemoveCollection(theme,'content')
    return jsonify({'success': True})

@app.route('/DeleteMessage', methods=['GET'])
def DeleteMessage():
    MessageName = request.args['MessageName']
    name = request.args['name']
    MessageType = request.args['MessageType']
    return jsonify({'success': BotDB.DeleteMessage(name,MessageType,MessageName)})

@app.route('/DeleteContent', methods=['GET'])
def DeleteContent():
    ContentName = request.args['ContentName']
    name = request.args['name']
    return jsonify({'success': BotDB.DeleteContent(name,ContentName)})

if __name__ == '__main__':
    app.run(use_reloader=True, debug=True, host='0.0.0.0')
