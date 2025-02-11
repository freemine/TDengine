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
        case1<sdsang>: [TS-3072] taosdump dump escaped db name test
        """

    def checkVersion(self):
        # run
        outputs = etool.runBinFile("taosdump", "-V")
        print(outputs)
        if len(outputs) != 3:
            tdLog.exit(f"checkVersion return lines count {len(outputs) != 3}")
        # version string len
        assert len(outputs[0]) > 22
        assert len(outputs[1]) > 43
        assert len(outputs[2]) > 36

        tdLog.info("check taosdump version successfully.")


    def run(self):
        # check version
        self.checkVersion()

        tdSql.prepare()

        tdSql.execute("drop database if exists db")
        tdSql.execute("create database `Db`")

        tdSql.execute("use `Db`")
        tdSql.execute(
            "create table st(ts timestamp, c1 INT) tags(n1 INT)"
        )
        tdSql.execute(
            "create table t1 using st tags(1)"
        )
        tdSql.execute(
            "insert into t1 values(1640000000000, 1)"
        )
        #        sys.exit(1)

        binPath = etool.taosDumpFile()
        if binPath == "":
            tdLog.exit("taosdump not found!")
        else:
            tdLog.info("taosdump found in %s" % binPath)

        if not os.path.exists(self.tmpdir):
            os.makedirs(self.tmpdir)
        else:
            print("directory exists")
            os.system("rm -rf %s" % self.tmpdir)
            os.makedirs(self.tmpdir)

        print("%s Db st -R -e -o %s -T 1" % (binPath, self.tmpdir))
        os.system("%s Db st -R -e -o %s -T 1" % (binPath, self.tmpdir))
        # sys.exit(1)

        tdSql.execute("drop database `Db`")
        #        sys.exit(1)

        os.system("%s -R -e -i %s -T 1" % (binPath, self.tmpdir))

        tdSql.query("show databases")
        dbresult = tdSql.res

        found = False
        for i in range(len(dbresult)):
            print("Found db: %s" % dbresult[i][0])
            if dbresult[i][0] == "Db":
                found = True
                break

        assert found == True

        tdSql.execute("use `Db`")
        tdSql.query("show stables")
        tdSql.checkRows(1)
        tdSql.checkData(0, 0, "st")

        tdSql.query("select count(*) from `Db`.st")
        tdSql.checkData(0, 0, 1)

    def stop(self):
        tdSql.close()
        tdLog.success("%s successfully executed" % __file__)


tdCases.addWindows(__file__, TDTestCase())
tdCases.addLinux(__file__, TDTestCase())
