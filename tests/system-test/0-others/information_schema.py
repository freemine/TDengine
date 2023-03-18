###################################################################
#           Copyright (c) 2016 by TAOS Technologies, Inc.
#                     All rights reserved.
#
#  This file is proprietary and confidential to TAOS Technologies.
#  No part of this file may be reproduced, stored, transmitted,
#  disclosed or used in any form or by any means other than as
#  expressly provided by the written permission from Jianhui Tao
#
###################################################################

# -*- coding: utf-8 -*-


from util.log import *
from util.cases import *
from util.sql import *
from util.common import *
from util.sqlset import *

class TDTestCase:
    def init(self, conn, logSql, replicaVar=1):
        self.replicaVar = int(replicaVar)
        tdLog.debug("start to execute %s" % __file__)
        tdSql.init(conn.cursor())
        self.setsql = TDSetSql()
        self.dbname = 'db'
        self.stbname = 'stb'
        self.binary_length = 20 # the length of binary for column_dict
        self.nchar_length = 20  # the length of nchar for column_dict
        self.ts = 1537146000000
        self.column_dict = {
            'ts'  : 'timestamp',
            'col1': 'tinyint',
            'col2': 'smallint',
            'col3': 'int',
            'col4': 'bigint',
            'col5': 'tinyint unsigned',
            'col6': 'smallint unsigned',
            'col7': 'int unsigned',
            'col8': 'bigint unsigned',
            'col9': 'float',
            'col10': 'double',
            'col11': 'bool',
            'col12': f'binary({self.binary_length})',
            'col13': f'nchar({self.nchar_length})'
        }
        self.tbnum = 20
        self.rowNum = 10
        self.tag_dict = {
            't0':'int'
        }
        self.tag_values = [
            f'1'
            ]
        self.binary_str = 'taosdata'
        self.nchar_str = '涛思数据'
        self.ins_list = ['ins_dnodes','ins_mnodes','ins_modules','ins_qnodes','ins_snodes','ins_cluster','ins_databases','ins_functions',\
            'ins_indexes','ins_stables','ins_tables','ins_tags','ins_columns','ins_users','ins_grants','ins_vgroups','ins_configs','ins_dnode_variables',\
                'ins_topics','ins_subscriptions','ins_streams','ins_stream_tasks','ins_vnodes','ins_user_privileges']
        self.perf_list = ['perf_connections','perf_queries','perf_consumers','perf_trans','perf_apps']
    def insert_data(self,column_dict,tbname,row_num):
        insert_sql = self.setsql.set_insertsql(column_dict,tbname,self.binary_str,self.nchar_str)
        for i in range(row_num):
            insert_list = []
            self.setsql.insert_values(column_dict,i,insert_sql,insert_list,self.ts)
    def prepare_data(self):
        tdSql.execute(f"create database if not exists {self.dbname} vgroups 2")
        tdSql.execute(f'use {self.dbname}')
        tdSql.execute(self.setsql.set_create_stable_sql(self.stbname,self.column_dict,self.tag_dict))
        for i in range(self.tbnum):
            tdSql.execute(f"create table {self.stbname}_{i} using {self.stbname} tags({self.tag_values[0]})")
            self.insert_data(self.column_dict,f'{self.stbname}_{i}',self.rowNum)
    def count_check(self):
        tdSql.query('select count(*) from information_schema.ins_tables')
        tdSql.checkEqual(tdSql.queryResult[0][0],self.tbnum+len(self.ins_list)+len(self.perf_list))
        tdSql.query(f'select count(*) from information_schema.ins_tables where db_name = "{self.dbname}"')
        tdSql.checkEqual(tdSql.queryResult[0][0],self.tbnum)
        tdSql.query(f'select count(*) from information_schema.ins_tables where db_name = "{self.dbname}" and stable_name = "{self.stbname}"')
        tdSql.checkEqual(tdSql.queryResult[0][0],self.tbnum)
        tdSql.execute('create database db1')
        tdSql.execute('create table stb1 (ts timestamp,c0 int) tags(t0 int)')
        tdSql.execute('create table tb1 using stb1 tags(1)')
        tdSql.query(f'select db_name, stable_name, count(*) from information_schema.ins_tables group by db_name, stable_name')
        for i in tdSql.queryResult:
            if i[0].lower() == 'information_schema':
                tdSql.checkEqual(i[2],len(self.ins_list))
            elif i[0].lower() == self.dbname and i[1] == self.stbname:
                tdSql.checkEqual(i[2],self.tbnum)
            elif i[0].lower() == self.dbname and i[1] == 'stb1':
                tdSql.checkEqual(i[2],1)
            elif i[0].lower() == 'performance_schema':
                tdSql.checkEqual(i[2],len(self.perf_list))
        tdSql.execute('create table db1.ntb (ts timestamp,c0 int)')
        tdSql.query(f'select db_name, count(*) from information_schema.ins_tables group by db_name')
        for i in tdSql.queryResult:
            if i[0].lower() == 'information_schema':
                tdSql.checkEqual(i[1],len(self.ins_list))
            elif i[0].lower() == 'performance_schema':
                tdSql.checkEqual(i[1],len(self.perf_list))
            elif i[0].lower() == self.dbname:
                tdSql.checkEqual(i[1],self.tbnum+1)
    def ins_columns_check(self):
        tdSql.execute('create database db2 vgroups 2 replica 1')
        tdSql.execute('create table db2.stb2 (ts timestamp,c0 int,c1 int, c2 double, c3 float, c4 binary(1000), c5 nchar(100),c7 bigint, c8 bool, c9 smallint) tags(t0 int)')
        for i in range(2000):
            tdSql.execute("create table db2.ctb%d using db2.stb2 tags(%d)" %(i,i))
        tdSql.query(f'select * from information_schema.ins_columns where db_name="db2" and table_type="CHILD_TABLE"')
        tdSql.checkEqual(20000,len(tdSql.queryResult))
        print("number of ins_columns of child table in db2 is %s" % len(tdSql.queryResult))
    
    def ins_col_check_4096(self):
        tdSql.execute('create database db3 vgroups 2 replica 1')
        col_str = tdCom.gen_tag_col_str("col", "int",4094)
        tdSql.execute(f'create stable if not exists db3.stb (col_ts timestamp, {col_str}) tags (t1 int)')
        for i in range(100):
            tdLog.info(f"create table db3.ctb{i} using db3.stb tags({i})")
            tdSql.execute(f"create table db3.ctb{i} using db3.stb tags({i})")
            col_value_str = '1, ' * 4093 + '1'
            tdSql.execute(f"insert into db3.ctb{i} values(now,{col_value_str})")
        tdSql.query("select * from information_schema.ins_columns")
        
        tdSql.execute('drop database db3')
    def ins_stable_check(self):
        tdSql.execute('create database db3 vgroups 2 replica 1')
        tbnum = 10
        ctbnum = 10
        for i in range(tbnum):
            tdSql.execute(f'create stable db3.stb_{i} (ts timestamp,c0 int) tags(t0 int)')
            tdSql.execute(f'create table db3.ntb_{i} (ts timestamp,c0 int)')
            for j in range(ctbnum):
                tdSql.execute(f"create table db3.ctb_{i}_{j} using db3.stb_{i} tags({j})")
        tdSql.query("select stable_name,count(table_name) from information_schema.ins_tables where db_name = 'db3' group by stable_name order by stable_name")
        result = tdSql.queryResult
        for i in range(len(result)):
            if result[i][0] == None:
                tdSql.checkEqual(result[0][1],tbnum)
            else:
                tdSql.checkEqual(result[i][0],f'stb_{i-1}')
                tdSql.checkEqual(result[i][1],ctbnum)
        


    def run(self):
        # self.prepare_data()
        # self.count_check()
        # self.ins_columns_check()
        # self.ins_col_check_4096()
        self.ins_stable_check()

    def stop(self):
        tdSql.close()
        tdLog.success("%s successfully executed" % __file__)

tdCases.addWindows(__file__, TDTestCase())
tdCases.addLinux(__file__, TDTestCase())