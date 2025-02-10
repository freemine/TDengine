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
        [TD-21806] taosBenchmark specifying vgroups test cases
        """



    def run(self):
        binPath = etool.benchMarkFile()
        cmd = (
            "%s -t 1 -n 1 -v 3 -y &"
            % binPath
        )
        tdLog.info("%s" % cmd)
        os.system("%s" % cmd)
        time.sleep(2)

        tdSql.query("select `vgroups` from information_schema.ins_databases where name='test'")
        tdSql.checkData(0, 0, 3)

    def stop(self):
        tdSql.close()
        tdLog.success("%s successfully executed" % __file__)


tdCases.addWindows(__file__, TDTestCase())
tdCases.addLinux(__file__, TDTestCase())
