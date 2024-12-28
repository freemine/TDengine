import taos
import sys
import time
import socket
import os
import threading
import psutil
import platform
from util.log import *
from util.sql import *
from util.cases import *
from util.dnodes import *


class TDTestCase:
    def init(self, conn, logSql, replicaVar=1):
        self.replicaVar = int(replicaVar)
        tdLog.debug("start to execute %s" % __file__)
        tdSql.init(conn.cursor(), logSql)
        self.default_compact_options = [ "0d", "0d,0d", "0h"]
        self.compact_options = [["db00", "0m", "-0d,0", "0", "0d", "0d,0d", "0h"],
                                ["db01", "2880m", "-61d,-60", "0", "2d", "-61d,-60d", "0h"],
                                ["db02", "48h", "-87840m,-60", "1h", "2d", "-61d,-60d", "1h"],
                                ["db03", "2d", "-87840m,-1440h", "12", "2d", "-61d,-60d", "12h"],
                                ["db04", "2", "-61,-1440h", "23h", "2d", "-61d,-60d", "23h"],
                                ]

    def create_db_compact(self):
        for item in self.compact_options:
            tdSql.execute(f'create database {item[0]} compact_interval {item[1]} compact_time_range {item[2]} compact_time_offset {item[3]}')
            tdSql.query(f'select * from information_schema.ins_databases where name = "{item[0]}"')
            tdSql.checkEqual(tdSql.queryResult[0][34], item[4])
            tdSql.checkEqual(tdSql.queryResult[0][35], item[5])
            tdSql.checkEqual(tdSql.queryResult[0][36], item[6])
            tdSql.query(f'show create database {item[0]}')
            tdSql.checkEqual(tdSql.queryResult[0][0], item[0])
            tdSql.checkEqual(True, f'COMPACT_INTERVAL {item[4]} COMPACT_TIME_RANGE {item[5]} COMPACT_TIME_OFFSET {item[6]}' in tdSql.queryResult[0][1])
            tdSql.execute(f'drop database {item[0]}')

    def checkShowCreateWithTimeout(self, db, expectResult, timeout=30):
        result = False
        for i in range(timeout):
            tdSql.query(f'show create database `%s`' %(db))
            tdSql.checkEqual(tdSql.queryResult[0][0], db)
            if expectResult in tdSql.queryResult[0][1]:
                result = True
                break
            time.sleep(1)
        if result == False:
            raise Exception(f"Unexpected result of 'show create database `{db}`':{tdSql.queryResult[0][1]}")

    def alter_db_compact(self):
        for item in self.compact_options:
            tdSql.execute(f'create database {item[0]}')
            tdSql.query(f'select * from information_schema.ins_databases where name = "{item[0]}"')
            tdSql.checkEqual(tdSql.queryResult[0][34], self.default_compact_options[0])
            tdSql.checkEqual(tdSql.queryResult[0][35], self.default_compact_options[1])
            tdSql.checkEqual(tdSql.queryResult[0][36], self.default_compact_options[2])
            tdSql.query(f'show create database {item[0]}')
            tdSql.checkEqual(tdSql.queryResult[0][0], item[0])
            tdSql.checkEqual(True, f'COMPACT_INTERVAL {self.default_compact_options[0]} COMPACT_TIME_RANGE {self.default_compact_options[1]} COMPACT_TIME_OFFSET {self.default_compact_options[2]}' in tdSql.queryResult[0][1])
            tdSql.execute(f'alter database {item[0]} compact_interval {item[1]} compact_time_range {item[2]} compact_time_offset {item[3]}')
            tdSql.query(f'select * from information_schema.ins_databases where name = "{item[0]}"')
            tdSql.checkEqual(tdSql.queryResult[0][34], item[4])
            tdSql.checkEqual(tdSql.queryResult[0][35], item[5])
            tdSql.checkEqual(tdSql.queryResult[0][36], item[6])
        for item in self.compact_options:
            self.checkShowCreateWithTimeout(item[0], f'COMPACT_INTERVAL {item[4]} COMPACT_TIME_RANGE {item[5]} COMPACT_TIME_OFFSET {item[6]}')
            tdSql.execute(f'drop database {item[0]}')

    def compact_error(self):
        compact_err_list = [["compact_time_range 86400m,61d", "Invalid option compact_time_range: 86400m, start time should be in range: [-5256000m, -14400m]"],
                            ["compact_time_range 60,61", "Invalid option compact_time_range: 86400m, start time should be in range: [-5256000m, -14400m]"],
                            ["compact_time_range 60d,61d", "Invalid option compact_time_range: 86400m, start time should be in range: [-5256000m, -14400m]"],
                            ["compact_time_range -60,-60", "Invalid option compact_time_range: -86400m,-86400m, start time should be less than end time"],
                            ["compact_time_range -60,-1440h", "Invalid option compact_time_range: -86400m,-86400m, start time should be less than end time"],
                            ["compact_time_range -60d,-61d", "Invalid option compact_time_range: -86400m,-87840m, start time should be less than end time"],
                            ["compact_time_range -5256001m,-1", "Invalid option compact_time_range: -5256001m, start time should be in range: [-5256000m, -14400m]"],
                            ["compact_time_range -60d,-1", "Invalid option compact_time_range: -1440m, end time should be in range: [-5256000m, -14400m]"],
                            ["compact_interval 24h compact_time_range -60,61", "Invalid option compact_time_range: 87840m, end time should be in range: [-5256000m, -14400m]"],
                            ["compact_interval 100 compact_time_range -60d,61d", "Invalid option compact_time_range: 87840m, end time should be in range: [-5256000m, -14400m]"],
                            ["compact_time_range -60d,87840m", "Invalid option compact_time_range: 87840m, end time should be in range: [-5256000m, -14400m]"],
                            ["compact_interval 10m compact_time_range -120d,-14400m compact_time_offset -1", "syntax error near"],
                            ["compact_time_range -100,-99d compact_interval -1", "syntax error near"],
                            ["compact_time_range 0", "Invalid option compact_time_range, should have 2 value"],
                            ["compact_time_range -100", "Invalid option compact_time_range, should have 2 value"],
                            ["compact_time_range -100,-90,-80", "Invalid option compact_time_range, should have 2 value"],
                            ["compact_time_range -100;-90", "Invalid option compact_time_range, should have 2 value"],
                            ["compact_time_range -100:-90", "syntax error near"],
                            ["compact_time_range -100 -90", "syntax error near"],
                            ["compact_interval 1m", "Invalid option compact_interval: 1m, valid range: [10m, 5256000m]"],
                            ["compact_interval 5256001m", "Invalid option compact_interval: 5256001m, valid range: [10m, 5256000m]"],
                            ["compact_interval 3651", "Invalid option compact_interval: 5257440m, valid range: [10m, 5256000m]"],
                            ["compact_interval -1", "syntax error near"],
                            ["compact_time_offset -1", "syntax error near"],
                            ["compact_time_offset 1d", "Invalid option compact_time_offset unit: d, only h allowed"],
                            ["compact_time_offset 24", "Invalid option compact_time_offset: 24h, valid range: [0h, 23h]"],
                            ["compact_time_offset 24h", "Invalid option compact_time_offset: 24h, valid range: [0h, 23h]"],
                            ["compact_time_offset 1d", "Invalid option compact_time_offset unit: d, only h allowed"],
                            ["compact_interval 10m compact_time_range -120d,-60 compact_time_offset 1d", "Invalid option compact_time_offset unit: d, only h allowed"],
                            ]
        tdSql.execute('create database if not exists db')
        for item in compact_err_list:
            tdSql.error(f"create database db {item[0]}", expectErrInfo=item[1], fullMatched=False)
            tdSql.error(f"alter database db {item[0]}", expectErrInfo=item[1], fullMatched=False)
        
    def run(self):
        self.create_db_compact()
        self.alter_db_compact()
        self.compact_error()

    def stop(self):
        tdSql.close()
        tdLog.success(f"{__file__} successfully executed")


tdCases.addLinux(__file__, TDTestCase())
tdCases.addWindows(__file__, TDTestCase())
