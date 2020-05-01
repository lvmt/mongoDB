#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pymongo import MongoClient
import re


class RawMongodb(object):

    def __init__(self, args):
        self.args = args
        
    def __str__(self):
        return ("{}".format([x for x in self.args.items()]))

    def get_collection(self):
        client = MongoClient('localhost', 27017)
        db = client.rawdata 
        # db.authenticate('lmt1', 'lmt1')
        collection = db.collection_name
        return collection

    def rawpath2mongodb(self):

        self.pn = self.args['pn']       # 子项目编号
        self.projpath = self.args['projpath']      # 合同编号
        self.jobname = self.projpath.rstrip('/').split('/')[-1] 
        self.contractid = self.jobname.split('.')[1]
        self.sample_list = self.args['sample_list'] or input("请输入sample_list： ")
        self.fenqi = re.search(r'.*B(\d*)\D*', self.sample_list).group(1) or None  # 分期

        collection = self.get_collection()
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
                    'jobname': self.jobname, 'contractid': self.contractid}
                
                # 增加判断，防止相同的数据重复插入
                if collection.find_one(insert_item):
                    # print(collection.find_one(insert_item))
                    # print('data exist')
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

    def add_upload_tag(self, upload_file):
        collection = self.get_collection()
        with open(upload_file, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                linelist = line.strip().split('\t')

                ori_path =  "/" + "/".join(linelist[0].split(' ')[3].rstrip('*').strip('/').split('/')[0:-1])
                mv_path = linelist[0].split(' ')[4]
                sam = linelist[2]
                libid = linelist[3]
                novoid = linelist[4]
                condition = {'sam':sam, 'libid':libid, 'novoid':novoid, 'path':ori_path}

                upload_tag = {'upload': 'done', 'mv_path':mv_path}
                collection.update_many(condition, {'$set': upload_tag})
                
    def query(self):
        
        collection = self.get_collection()
        query_item = eval(input("请输入查询字符串[按照字典的形式传入]: "))
        results = collection.find(query_item)
        
        if not self.args['out']:
            n = 1
            if results:
                for result in results:
                    print(n, result)
                    n += 1
        return results
    
    def out_result(self):
        result_dict = self.query()
        with open(self.args['out'], 'w') as o:
            for item_dict in result_dict:
                values = [v for v in item_dict.values()]
                o.write("{}\n".format("\t".join(values[1:])))
                

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description="demo")
    parser.add_argument('--pn', help="pn.txt")
    parser.add_argument('--sample_list', help="sample_list")
    parser.add_argument('--projpath', help="项目路劲")
    parser.add_argument('--add_tag', action="store_true")
    parser.add_argument('--upload_file', help="如果上云无误，给数据库中的记录加上tag")
    parser.add_argument('--query', action="store_true" ,help="在数据库里面查询，按照字典的形式进行查询")
    parser.add_argument('--out', help="输出查询内容")
    args = vars(parser.parse_args())

    t = RawMongodb(args)
    # print(t)
    if args['add_tag']:
        t.add_upload_tag(args['upload_file'])
    elif args['query']:
        t.query()
    elif args['out']:
        t.out_result()
    else:
        t.rawpath2mongodb()


