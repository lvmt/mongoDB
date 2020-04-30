#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pymongo
from pymongo import MongoClient

""" 登陆  """

client = MongoClient('localhost', 27017)
db = client.test 
db.authenticate('lmt1', 'lmt1')
collection = db.col9 


"""  update  """

condition = {'title': 'mongodb'}
item = collection.find_one(condition)
print(item)
# {'_id': ObjectId('5ea94748d2ac43f01f99ee1c'), 'title': 'mongodb', 'by_user': 'w3cschool', 'likes': 100.0}


"""  更新 新字段 """
item['age'] = 25
result = collection.update(condition, item)
print(result) 
# {'n': 1, 'nModified': 1, 'ok': 1.0, 'updatedExisting': True}

print(item)
# {'_id': ObjectId('5ea94748d2ac43f01f99ee1c'), 'title': 'mongodb', 'by_user': 'w3cschool', 'likes': 100.0, 'age': 25}


""" 修改字段 """
item['likes'] = 200
result1 = collection.update(condition, item)

print(item)
# {'_id': ObjectId('5ea94748d2ac43f01f99ee1c'), 'title': 'mongodb', 'by_user': 'w3cschool', 'likes': 200, 'age': 25}