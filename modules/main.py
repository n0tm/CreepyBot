from flask import Flask, jsonify, Response, request
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

import requests
import json
import datetime
import time


### Price-List

RECOMENDEDprice = 400

VIPprice = 600

OWNprice = 350



app = Flask('fu')
CORS(app)

token = '6242b44ff393becab5a56542cc64a50061f823d6a315fd42847f9a983a0f068c5b4dc1c742b88be69262b'

client = MongoClient()
db = client['instabot']

@app.route('/SendMessage', methods=['GET'])
def log_call():
    phone = request.args['phone']
    follow = request.args['follow']
    unfollow_all = request.args['unfollow_all']
    comment_option = request.args['comment']
    like = request.args['like']
    fname = request.args['fname']
    lname = request.args['lname']
    email = request.args['email']
    tags = request.args['tags']
    comments = request.args['comments']
    pocket_name = request.args['pocket_name']
    all_options = request.args['options']
    login = request.args['login']
    password = request.args['password']
    token_pay = request.args['token']
    promo = request.args['promo']
    price = request.args['price']
    promo = promo.lower()
    check_promo = db.coupons.find_one({"name":promo})
    if (check_promo):
        price = RECOMENDEDprice - (RECOMENDEDprice*int(check_promo['discount'])*0.01)
    else:
        price = RECOMENDEDprice
    req = 'https://api.vk.com/method/messages.send?user_id=113223865&message=Имя: %s\nФамилия: %s\nТелефон: %s\nПочта: %s\nНаименование пакета: %s\nОпции: %s\nХэштеги: %s\nКомментарии: %s\nЛогин: %s\nПароль: %s\nТокен для оплаты: %s\nПромокод: %s\nСумма заказа: %s&access_token=%s' % (fname,lname,phone,email,pocket_name,all_options,tags,comments,login,password,token_pay, promo,str(price),token)
    r = requests.get(req)
    print(json.loads(r.text))
    write_database = db.site_clients.insert({"fname":fname,"lname":lname,"phone":phone,"email":email,"tags":tags,"comments":comments,"pocket_name":pocket_name,"options":{"unfollow_all":unfollow_all, "like":like, "comment":comment_option,"follow":follow},"login":login,"password":password,"token":token_pay,"promo":promo,"time":int(time.time()),"status":"waiting"})
    return jsonify({'succes': True})


@app.route('/get_promo', methods=['GET'])
def promo():
    promocode = request.args['promo']
    promocode = promocode.lower()
    check_promo = db.coupons.find_one({"name":promocode})
    if (check_promo):
        return jsonify({'Answer': check_promo['discount']})
    else:
        return jsonify({'Answer': False})

@app.route('/get_promo_length', methods=['GET'])
def get_promo_length():
    length = []
    for user in db.coupons.find():
        length.append(1)
    return jsonify({'Answer': len(length)})

if __name__ == '__main__':
    app.run(use_reloader=True, debug=True, host='0.0.0.0')
