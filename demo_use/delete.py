#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pymongo
from pymongo import MongoClient

""" 登陆  """

client = MongoClient('localhost', 27017)
db = client.test 
db.authenticate('lmt1', 'lmt1')
collection = db.col9 


""" remove """

result = collection.remove({'title': 'python'})
print(result)
# {'n': 2, 'ok': 1.0} 



""" delete_one """
result_one = collection.delete_one({'likes': 140})
print(result_one.deleted_count)
# 1


""" delete_many """
result_many = collection.delete_many({'score': 90})
print(result_many.deleted_count)
# 2

