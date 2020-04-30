#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pymongo
from pymongo import MongoClient

""" 登陆  """

client = MongoClient('localhost', 27017)
db = client.test 
db.authenticate('lmt1', 'lmt1')
collection = db.col9 


""" $set: 这样可以只更新 new_srt 字典内存在的字段。如果原先还有其他字段，则不会更新，也不会删除。
而如果不用$set的话，则会把之前的数据全部用student字典替换；如果原本存在其他字段，则会被删除

参考 demo1 和 demo2

"""



""" demo1 """
condition = {'title': 'perl'}
new_str = {'title': 'new_perl', 'score': 90, 'name': 'lmt'}

collection.update(condition, new_str)
# ori: {'title':'perl', 'by_user':'runoob', 'likes':100}
# update: {'title':'new_perl', 'score':90, 'name':'lmt'}




""" demo2 """
condition1 = {'title': 'noSQL'}
new_str1 = {'score': 90, 'sex': 'male'}
collection.update(condition1, {'$set': new_str1})

# ori:  {'title': 'noSQL', 'by_user':'w3cschool', 'likes':120}
# update: {'title': 'noSQL', 'by_user':'w3cschool', 'likes':120, 'score':90, 'sex':'male'}