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
from util.dnodes import *
from util.sql import *
from util.common import tdCom
import threading


class TDTestCase:
    def init(self, conn, logSql, replicaVar=1):
        tdLog.debug(f"start to init {__file__}")
        self.replicaVar = int(replicaVar)
        tdSql.init(conn.cursor(), logSql)  # output sql.txt file

    def run(self):
        tdLog.debug(f"start to excute {__file__}")

        tdSql.execute('CREATE DATABASE db vgroups 4 replica 1;')

        tdSql.execute('use db;')

        tdLog.debug("start test1")
        event = threading.Event()
        newTdSql=tdCom.newTdSql()
        t0 = threading.Thread(target=self.compactDBThread, args=('', event, newTdSql))
        t0.start()
        tdLog.info("t0 threading started,wait compact db tran finish")
        event.wait()
        tdSql.error('ALTER DATABASE db REPLICA 3;', expectErrInfo="Transaction not completed due to conflict with compact")
        tdLog.info("wait compact db finish")
        t0.join()
        
        tdLog.debug("start test2")
        event1 = threading.Event()
        newTdSql1=tdCom.newTdSql()
        t1 = threading.Thread(target=self.compactDBThread, args=('', event1, newTdSql1))
        t1.start()
        tdLog.info("t1 threading started,wait compact db tran finish")
        event1.wait()
        tdSql.error('REDISTRIBUTE VGROUP 5 DNODE 1;', expectErrInfo="Transaction not completed due to conflict with compact")
        tdLog.info("wait compact db finish")
        t1.join()

        tdLog.debug("start test3")
        event2 = threading.Event()
        newTdSql2=tdCom.newTdSql()
        t2 = threading.Thread(target=self.compactDBThread, args=('', event2, newTdSql2))
        t2.start()
        tdLog.info("t2 threading started,wait compact db tran finish")
        event2.wait()
        tdSql.error('REDISTRIBUTE VGROUP 5 DNODE 1;', expectErrInfo="Transaction not completed due to conflict with compact")
        tdLog.info("wait compact db finish")
        t2.join()

        tdLog.debug("start test4")
        event3 = threading.Event()
        newTdSql3=tdCom.newTdSql()
        t3 = threading.Thread(target=self.compactDBThread, args=('', event3, newTdSql3))
        t3.start()
        tdLog.info("t3 threading started!!!!!")
        event3.wait()
        tdSql.error('BALANCE VGROUP;', expectErrInfo="Transaction not completed due to conflict with compact")
        t3.join()

        tdLog.debug("start test5")
        newTdSql4=tdCom.newTdSql()
        t4 = threading.Thread(target=self.splitVgroupThread, args=('', newTdSql4))
        t4.start()
        tdLog.info("t4 threading started!!!!!")
        time.sleep(1)
        tdSql.error('compact database db;', expectErrInfo="Conflict transaction not completed")
        t4.join()
        
        tdLog.debug("start test6")
        newTdSql5=tdCom.newTdSql()
        t5 = threading.Thread(target=self.RedistributeVGroups, args=('', newTdSql5))
        t5.start()
        tdLog.info("t5 threading started!!!!!")
        time.sleep(1)
        tdSql.error('compact database db;', expectErrInfo="Conflict transaction not completed")
        t5.join()

        tdLog.debug("start test7")
        newTdSql6=tdCom.newTdSql()
        t6 = threading.Thread(target=self.balanceVGROUPThread, args=('', newTdSql6))
        t6.start()
        tdLog.info("t6 threading started!!!!!")
        time.sleep(1)
        tdSql.error('compact database db;', expectErrInfo="Conflict transaction not completed")
        t6.join()

        tdLog.debug("start test8")
        newTdSql7=tdCom.newTdSql()
        t7 = threading.Thread(target=self.alterDBThread, args=('', newTdSql7))
        t7.start()
        tdLog.info("t7 threading started!!!!!")
        time.sleep(1)
        tdSql.error('compact database db;', expectErrInfo="Conflict transaction not completed")
        t7.join()


    def compactDBThread(self, p, event, newtdSql):
        tdLog.info("compact db start")
        newtdSql.execute('compact DATABASE db')
        event.set()
        if self.waitCompactsZero() is False:
                tdLog.info(f"compact not finished")

    def alterDBThread(self, p, newtdSql):
        tdLog.info("alter db start")
        newtdSql.execute('ALTER DATABASE db REPLICA 3')
        if self.waitTransactionZero() is False:
                tdLog.info(f"transaction not finished")

    def balanceVGROUPThread(self, p, newtdSql):
        tdLog.info("balance VGROUP start")
        newtdSql.execute('BALANCE VGROUP')
        if self.waitTransactionZero() is False:
                tdLog.info(f"transaction not finished")

    def RedistributeVGroups(self, p, newtdSql):
        tdLog.info("REDISTRIBUTE VGROUP start")
        sql = f"REDISTRIBUTE VGROUP 5 DNODE 1"
        newtdSql.execute(sql, show=True)
        if self.waitTransactionZero() is False:
            tdLog.exit(f"{sql} transaction not finished")
            return False

        sql = f"REDISTRIBUTE VGROUP 4 DNODE 1"
        newtdSql.execute(sql, show=True)
        if self.waitTransactionZero() is False:
            tdLog.exit(f"{sql} transaction not finished")
            return False
        
        sql = f"REDISTRIBUTE VGROUP 3 DNODE 1"
        newtdSql.execute(sql, show=True)
        if self.waitTransactionZero() is False:
            tdLog.exit(f"{sql} transaction not finished")
            return False
        
        return True

    def splitVgroupThread(self, p, newtdSql):
        rowLen = tdSql.query('show vgroups')
        if rowLen > 0:
            vgroupId = tdSql.getData(0, 0)
            tdLog.info(f"splitVgroupThread vgroupId:{vgroupId} start")
            newtdSql.execute(f"split vgroup {vgroupId}")
        else:
            tdLog.exit("get vgroupId fail!")
        if self.waitTransactionZero() is False:
            tdLog.info(f"transaction not finished")
    
    def waitTransactionZero(self, seconds = 300, interval = 1):
        # wait end
        for i in range(seconds):
            sql ="show transactions;"
            rows = tdSql.query(sql)
            if rows == 0:
                tdLog.info("transaction count became zero.")
                return True
            #tdLog.info(f"i={i} wait ...")
            time.sleep(interval)
        
        return False 
    def waitCompactsZero(self, seconds = 300, interval = 1):
        # wait end
        for i in range(seconds):
            sql ="show compacts;"
            rows = tdSql.query(sql)
            if rows == 0:
                tdLog.info("compacts count became zero.")
                return True
            #tdLog.info(f"i={i} wait ...")
            time.sleep(interval)
        
        return False  
     
    def stop(self):
        tdSql.close()
        tdLog.success(f"{__file__} successfully executed")


tdCases.addLinux(__file__, TDTestCase())
tdCases.addWindows(__file__, TDTestCase())