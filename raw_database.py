#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
\033[32m
#########################################################################
设计初衷：找原始数据真的太麻烦啦....... 

1、 记录分析过的数据的信息 
2、如果原始数据转移成功，在第一步的基础上添加标签：是否转移成功，转移路径
3、增加查询：键值对查找方式，
4、是否对查询到的结果进行写出，主要是用于数据查找方面 

喔， 需要python3
##########################################################################
\033[0m"""

import re
import logging
from collections import defaultdict
from pymongo import MongoClient
import textwrap

class RawMongodb(object):

    def __init__(self, args):
        self.args = args
        
    def __str__(self):
        return ("{}".format([x for x in self.args.items()]))

    def logger(self):
        logging.basicConfig(
            format='[%(asctime)s %(funcName)s %(levelname)s %(message)s]',
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.INFO)
        log = logging.getLogger(__name__)
        return log

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
                
                insert_item = defaultdict()  # 防止插入乱序，导致后面写出文件出错
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
            self.logger().info("开始插入许多数据......")
            collection.insert_many(insert_list)
        elif len(insert_list) == 1:
            self.logger().info("开始插入一条数据......")
            collection.insert_one(insert_list[0])
        else:
            self.logger().info("全都是重复数据，无需再次插入......")
            
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
                self.logger().info("给上云成功的文件插入标签")
                upload_tag = {'upload': 'done', 'mv_path':mv_path}
                collection.update_many(condition, {'$set': upload_tag})
                
    def query(self):
        collection = self.get_collection()
        query_item = eval(input("请输入查询字符串[按照字典的形式传入, 支持多个键值对]: \n"))
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
                del item_dict["_id"]  # 字典不晓得为毛乱序啦
                values = [v for v in item_dict.values()]
                self.logger().info("输出查询结果到文件:{out}".format(out=self.args["out"]))
                o.write("{}\n".format("\t".join(values[1:])))
                

def main():
    
    t = RawMongodb(args)
    # print(t)
    if args['add_tag']:
        t.add_upload_tag(args['upload_file'])
    elif args["query"] and args["out"]:
        t.out_result()
    elif args['query']:
        t.query()
    else:
        t.rawpath2mongodb()
 

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--pn', help="pn.txt")
    parser.add_argument('--sample_list', help="sample_list")
    parser.add_argument('--projpath', help="项目路劲")
    parser.add_argument('--add_tag', action="store_true", help="store_true")
    parser.add_argument('--upload_file', help="如果上云无误，给数据库中的记录加上tag")
    parser.add_argument('--query', action="store_true" ,help="在数据库里面查询，按照字典的形式进行查询, store_true")
    parser.add_argument('--out', help="输出查询内容到文件")
    args = vars(parser.parse_args())

    main()


