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
import os
import frame
import frame.etool
from frame.log import *
from frame.cases import *
from frame.sql import *
from frame.caseBase import *
from frame import *


class TDTestCase(TBase):
    def caseDescription(self):
        """
        [TS-3060] taosBenchmark test cases
        """



    def run(self):
        binPath = etool.benchMarkFile()
        cmd = "%s -f ./tools/benchmark/basic/json/taosc_only_create_table.json" % binPath
        tdLog.info("%s" % cmd)
        os.system("%s" % cmd)
        tdSql.execute("reset query cache")
        tdSql.query("show db.tables")
        tdSql.checkRows(8)

        #        tdSql.query("select * from db.stb")
        #        dbresult = tdSql.queryResult
        #        print(dbresult)
        #        if dbresult != []:
        #            for i in range(len(dbresult[0])):
        #                if i in (1, 2) and dbresult[0][i] == None:
        #                    tdLog.exit("result[0][%d] is NULL, which should not be" % i)
        #            else:
        #                tdLog.info("result[0][{0}] is {1}".format(i, dbresult[0][i]))

        # Shuduo: temporary disable check count() from db.stb
        #        tdSql.query("select count(*) from db.stb")
        #        tdSql.checkRows(0)
        tdSql.query("describe db.stb")
        tdSql.checkData(9, 1, "NCHAR")
        # varchar in 3.0 but binary in 2.x
        # tdSql.checkData(14, 1, "BINARY")
        tdSql.checkData(23, 1, "NCHAR")
        # tdSql.checkData(28, 1, "BINARY")
        tdSql.checkData(9, 2, 64)
        tdSql.checkData(14, 2, 64)
        tdSql.checkData(23, 2, 64)
        tdSql.checkData(28, 2, 64)

        cmd = "%s -f ./tools/benchmark/basic/json/stmt_limit_offset.json" % binPath
        tdLog.info("%s" % cmd)
        os.system("%s" % cmd)
        tdSql.execute("reset query cache")
        tdSql.query("show db.tables")
        tdSql.checkRows(8)
        tdSql.query("select count(*) from db.stb")
        tdSql.checkData(0, 0, 40)
        tdSql.query("select distinct(c3) from db.stb")
        tdSql.checkData(0, 0, None)
        tdSql.query("select distinct(c4) from db.stb")
        tdSql.checkData(0, 0, None)
        tdSql.query("select distinct(c5) from db.stb")
        tdSql.checkData(0, 0, None)
        tdSql.query("select distinct(c6) from db.stb")
        tdSql.checkData(0, 0, None)
        tdSql.query("select distinct(c7) from db.stb")
        tdSql.checkData(0, 0, None)
        tdSql.query("select distinct(c8) from db.stb")
        tdSql.checkData(0, 0, None)
        tdSql.query("select distinct(c9) from db.stb")
        tdSql.checkData(0, 0, None)
        tdSql.query("select distinct(c10) from db.stb")
        tdSql.checkData(0, 0, None)
        tdSql.query("select distinct(c11) from db.stb")
        tdSql.checkData(0, 0, None)
        tdSql.query("select distinct(c12) from db.stb")
        tdSql.checkData(0, 0, None)
        tdSql.query("select distinct(c13) from db.stb")
        tdSql.checkData(0, 0, None)

    def stop(self):
        tdSql.close()
        tdLog.success("%s successfully executed" % __file__)


tdCases.addWindows(__file__, TDTestCase())
tdCases.addLinux(__file__, TDTestCase())
