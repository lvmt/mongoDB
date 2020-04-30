#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pymongo import MongoClient

""" 插入数据  """

client = MongoClient('localhost', 27017)
db = client.test 
db.authenticate('lmt1', 'lmt1')
collection = db.insert_many 


"""  insert data one  """ 

student = {
    'id': 20170101,
    'name': 'Jordan',
    'age': 28,
    'gender': 'male'
}

result = collection.insert_one(student)

# get _id
print(result.inserted_id)  # 5ea95cb35c2663e5f97e5eeb


""" insert  data  many  """
# 对于insert_many()方法， 我们可以将数据按照 列表  进行传递


student1 = {
    'id': '20200429',
    'name': '瑞文',
    'age': 28,
    'gender': 'female'
}

student2 = {
    'id': '20200430',
    'name': '梦婷',
    'age': 28,
    'gender': 'female'
}

insert_list = [student1, student2]

# result2 = collection.insert_many([student1, student2])
# print(result2.inserted_ids)

return3 = collection.insert_many(insert_list)

