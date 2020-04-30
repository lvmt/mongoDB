#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pymongo
from pymongo import MongoClient

""" 登陆  """

client = MongoClient('localhost', 27017)
db = client.test 
db.authenticate('lmt1', 'lmt1')
collection = db.insert_many


""" update_one  """

condition = {'age': {'$gt': 20}}
result_one = collection.update_one(condition, {'$inc': {'age': 1}})
print(result_one.matched_count, result_one.modified_count)
# 1 1


""" update_many  """

result_many = collection.update_many(condition, {'$inc': {'age': 1}})
print(result_many.matched_count, result_many.modified_count) 
# 3 3 


""" demo """

new_srt = {'sex': 'male', 'wight': 60, 'height':'180'}
result = collection.update_many(condition,  {'$set': new_srt})


