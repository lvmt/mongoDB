#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pymongo import MongoClient


""" 默认登陆 """ 
client1 = MongoClient(host="127.0.0.1", port=27017)
client2 = MongoClient("mongodb://127.0.0.1:27017")

db = client2.test 
collection = db.runoob
for item in  collection.find():
    print(item)

"""  账号密码登陆 """

client = MongoClient('localhost', 27017)
db = client.test 
db.authenticate('lmt1', 'lmt1')
collection = db.abc
cursort = collection.find()

# for item in cursort:
#     print(item)

def connectDB(host="127.0.0.1", port=27017, db="test", username="lmt1", password="lmt1"):

    client = MongoClient(host=host, port=port)
    db = client.db 
    db.authenticate(username, password)

    return db



