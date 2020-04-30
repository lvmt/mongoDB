#!/usr/bin/env python
#-*- coding:utf-8 -*-


"""

1、存储数据
    先判断数据是否存在database中
    存在： pass
    不存在：出入

2、数据查询

    查询

3、存储数据
    包含的item


显示配置文件时，保存信息到数据库；
上云完成后，记录上云成功的标签

"""



from pymongo import MongoClient
import re


class RawMongodb(object):

    def __init__(self, args):

        self.args = args
        self.pn = args['pn']  # 子项目编号
        self.projpath = args['projpath']  # 合同编号
        self.jobname = self.projpath.rstrip('/').split('/')[-1] 
        self.contractid = self.jobname.split('.')[1] 
        self.sample_list = args['sample_list'] or input("请输入sample_list： ")
        self.fenqi = re.search(r'.*B(\d.*)S.*', self.sample_list).group(1) or None # 分期

    def opendb(self):
        client = MongoClient('localhost', 27017)
        db = client.rawdata 
        # db.authenticate('lmt1', 'lmt1')
        collection = db.rawpath
        return collection

    def menu(self):
        print("欢迎使用原始数据查询系统：\n1：添加样本信息到数据库记录\n2: 样本信息查询\n3: 功能待完善\n4: 剔除系统")
        tag = eval(input("请做出你的选择： "))
        if tag == 1:
            self.add_rawpath2mongodb()
        elif tag == 2:
            self.query_rawpath()
        elif tag == 3:
            print("时间太匆匆，待我思考中。。。")
        elif tag == 4:
            print("有缘千里来相见，我们下次见")
            exit()

    def add_rawpath2mongodb(self):
        self.sample_list = args['sample_list'] or input("请输入sample_list： ")
        fenqi = re.search(r'.*B(\d.*)S.*', self.sample_list)
        if fenqi:
            self.fenqi = fenqi.group(1)
        else:
            self.fenqi = "None"
        print(fenqi)
        collection = self.opendb()
        projid, projname = open(self.pn, 'r', encoding="utf-8").read().strip().split('\t')
        
        
        with open(self.sample_list, 'r') as f:
            insert_list = []
            for line in f:
                if line.startswith('#'):
                    continue
                linelist = line.strip().split('\t')
                laneid = linelist[0]
                sam = linelist[1]
                libid = linelist[3]
                novoid = linelist[4]
                index = linelist[5]
                path = linelist[6]
                
                insert_item = {'laneid':laneid, 'sam':sam, 'libid':libid, 'novoid':novoid, 'index':index, \
                    'path':path, 'projid':projid, 'projname':projname, 'fenqi': self.fenqi, \
                    'jobname': jobname, 'contractid': contractid}
                
                # 增加判断，防止相同的数据重复插入
                if collection.find_one(insert_item):
                    # print(collection.find_one(insert_item))
                    #print('data exist')
                    pass
                else:
                    insert_list.append(insert_item)

        # 根据插入条目数目，选择不同的插入函数
        if len(insert_list) > 1:
            print('begin insert many data')
            collection.insert_many(insert_list)
        elif len(insert_list) == 1:
            print("begin insert one data")
            collection.insert_one(insert_list[0])
        else:
            print('no data need insert')


    def query_rawpath(self):

        """查询指定条目在数据库中的详细信息 
        """
        collections = self.opendb()
        condition = eval(input("请输入查询条件： "))
       
        results = collections.find(condition)

        for item in results:
            print(item)  

    


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="demo")
    parser.add_argument('--pn')
    parser.add_argument('--sample_list')
    parser.add_argument('--projpath')
    parser.add_argument('--query', action="store_true")
    args = vars(parser.parse_args())

    t = RawMongodb(args)
    # t.add_rawpath2mongodb()

    t.menu()
        



