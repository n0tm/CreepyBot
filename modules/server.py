from flask import Flask, jsonify, Response, request
from flask_cors import CORS, cross_origin

import requests
import json
import BotDB

app = Flask('nervoed')
CORS(app)


@app.route('/getAllMessagesThemes', methods=['GET'])
def getAllMessagesThemes():
        return jsonify({'success': BotDB.getAllMessagesThemes()})

@app.route('/getAllContentThemes', methods=['GET'])
def getAllContentThemes():
    return jsonify({'success': BotDB.getAllContentThemes()})


@app.route('/AddContentTheme', methods=['GET'])
def AddContentTheme():
    theme = request.args['name']
    BotDB.InsertTo('AllContentThemes', {"name": theme})
    return jsonify({'success': True})

@app.route('/AddMessageTheme', methods=['GET'])
def AddMessageTheme():
    theme = request.args['name']
    BotDB.InsertTo('AllMessagesThemes', {"name": theme})
    return jsonify({'success': True})

@app.route('/RemoveMessageTheme', methods=['GET'])
def RemoveMessageTheme():
    theme = request.args['name']
    BotDB.RemoveFrom('AllMessagesThemes', {"name": theme})
    return jsonify({'success': True})

@app.route('/RemoveContentTheme', methods=['GET'])
def RemoveContentTheme():
    theme = request.args['name']
    BotDB.RemoveFrom('AllContentThemes', {"name": theme})
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(use_reloader=True, debug=True, host='0.0.0.0')
