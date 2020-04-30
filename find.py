#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pymongo import MongoClient

""" 登陆  """

client = MongoClient('localhost', 27017)
db = client.test 
db.authenticate('lmt1', 'lmt1')
collection = db.col9 


""" find_one  """

result1 = collection.find_one({'title': 'python'})
print(result1)  # {'_id': ObjectId('5ea9611a13dfe369e686c8f4'), 'title': 'python', 'by_user': 'runoob', 'likes': 100.0}


""" find """
results = collection.find({'by_user': 'w3cschool'})
print(results) 
# <pymongo.cursor.Cursor object at 0x000001C44A7EF8C8>

for result in results:
    print(result) 


""" 根据objectid 进行查询 """

from bson.objectid import ObjectId

result4 = collection.find_one({'_id': ObjectId('5ea94748d2ac43f01f99ee1c')})
print(result4) 


"""  设置查询条件  """

result5 = collection.find({'likes': {'$gt': 120}}) 
print(result5) # <pymongo.cursor.Cursor object at 0x00000252EC108D48>


""" 正则匹配 """

result6 = collection.find({'title': {'$regex': '^p.*'}})
for item in result6:
    print(item)
    print(type(item))    # dict

