#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pymongo
from pymongo import MongoClient

""" 登陆  """

client = MongoClient('localhost', 27017)
db = client.test 
db.authenticate('lmt1', 'lmt1')
collection = db.col9 


""" skip """

result = collection.find().sort('title', pymongo.ASCENDING)
print([item['title'] for item in result]) 
# ['Neo4j', 'mongodb', 'noSQL', 'perl', 'python', 'python']

result = collection.find().sort('title', pymongo.ASCENDING).skip(1).limit(1)
print([item['title'] for item in result]) 
# ['mongodb']