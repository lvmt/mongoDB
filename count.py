#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pymongo import MongoClient

""" 登陆  """

client = MongoClient('localhost', 27017)
db = client.test 
db.authenticate('lmt1', 'lmt1')
collection = db.col9 



""" count 全部item  """

count = collection.find().count()
print(count)  # 6


""" count 符合某个条件的 """
count2 = collection.find({'likes': {'$gt': 120}}).count()
print(count2) # 3

