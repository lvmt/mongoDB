#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pymongo
from pymongo import MongoClient

""" 登陆  """

client = MongoClient('localhost', 27017)
db = client.test 
db.authenticate('lmt1', 'lmt1')
collection = db.col9 


""" 排序  

sort 
pymongo.ASCENDING：升序
pymongo.DESCENDING：降序

"""

result = collection.find().sort('likes', pymongo.ASCENDING)
print([item['likes'] for item in result])
# [100.0, 100.0, 120.0, 130.0, 140.0, 150.0]



