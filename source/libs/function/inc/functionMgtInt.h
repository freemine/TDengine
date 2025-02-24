/*
 * Copyright (c) 2019 TAOS Data, Inc. <jhtao@taosdata.com>
 *
 * This program is free software: you can use, redistribute, and/or modify
 * it under the terms of the GNU Affero General Public License, version 3
 * or later ("AGPL"), as published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef _TD_FUNCTION_MGT_INT_H_
#define _TD_FUNCTION_MGT_INT_H_

#ifdef __cplusplus
extern "C" {
#endif

#include "functionMgt.h"

#define FUNCTION_NAME_MAX_LENGTH 32

#define FUNC_MGT_FUNC_CLASSIFICATION_MASK(n) ((uint64_t)1 << n)

#define FUNC_MGT_AGG_FUNC               FUNC_MGT_FUNC_CLASSIFICATION_MASK(0)
#define FUNC_MGT_SCALAR_FUNC            FUNC_MGT_FUNC_CLASSIFICATION_MASK(1)
#define FUNC_MGT_INDEFINITE_ROWS_FUNC   FUNC_MGT_FUNC_CLASSIFICATION_MASK(2)
#define FUNC_MGT_STRING_FUNC            FUNC_MGT_FUNC_CLASSIFICATION_MASK(3)
#define FUNC_MGT_DATETIME_FUNC          FUNC_MGT_FUNC_CLASSIFICATION_MASK(4)
#define FUNC_MGT_TIMELINE_FUNC          FUNC_MGT_FUNC_CLASSIFICATION_MASK(5)
#define FUNC_MGT_IMPLICIT_TS_FUNC       FUNC_MGT_FUNC_CLASSIFICATION_MASK(6)
#define FUNC_MGT_PSEUDO_COLUMN_FUNC     FUNC_MGT_FUNC_CLASSIFICATION_MASK(7)
#define FUNC_MGT_WINDOW_PC_FUNC         FUNC_MGT_FUNC_CLASSIFICATION_MASK(8)
#define FUNC_MGT_SPECIAL_DATA_REQUIRED  FUNC_MGT_FUNC_CLASSIFICATION_MASK(9)
#define FUNC_MGT_DYNAMIC_SCAN_OPTIMIZED FUNC_MGT_FUNC_CLASSIFICATION_MASK(10)
#define FUNC_MGT_MULTI_RES_FUNC         FUNC_MGT_FUNC_CLASSIFICATION_MASK(11)
#define FUNC_MGT_SCAN_PC_FUNC           FUNC_MGT_FUNC_CLASSIFICATION_MASK(12)
#define FUNC_MGT_SELECT_FUNC            FUNC_MGT_FUNC_CLASSIFICATION_MASK(13)
#define FUNC_MGT_REPEAT_SCAN_FUNC       FUNC_MGT_FUNC_CLASSIFICATION_MASK(14)
#define FUNC_MGT_FORBID_FILL_FUNC       FUNC_MGT_FUNC_CLASSIFICATION_MASK(15)
#define FUNC_MGT_INTERVAL_INTERPO_FUNC  FUNC_MGT_FUNC_CLASSIFICATION_MASK(16)
#define FUNC_MGT_FORBID_STREAM_FUNC     FUNC_MGT_FUNC_CLASSIFICATION_MASK(17)
#define FUNC_MGT_SYSTEM_INFO_FUNC       FUNC_MGT_FUNC_CLASSIFICATION_MASK(18)
#define FUNC_MGT_CLIENT_PC_FUNC         FUNC_MGT_FUNC_CLASSIFICATION_MASK(19)
#define FUNC_MGT_MULTI_ROWS_FUNC        FUNC_MGT_FUNC_CLASSIFICATION_MASK(20)
#define FUNC_MGT_KEEP_ORDER_FUNC        FUNC_MGT_FUNC_CLASSIFICATION_MASK(21)
#define FUNC_MGT_CUMULATIVE_FUNC        FUNC_MGT_FUNC_CLASSIFICATION_MASK(22)
#define FUNC_MGT_INTERP_PC_FUNC         FUNC_MGT_FUNC_CLASSIFICATION_MASK(23)
#define FUNC_MGT_GEOMETRY_FUNC          FUNC_MGT_FUNC_CLASSIFICATION_MASK(24)
#define FUNC_MGT_FORBID_SYSTABLE_FUNC   FUNC_MGT_FUNC_CLASSIFICATION_MASK(25)
#define FUNC_MGT_SKIP_SCAN_CHECK_FUNC   FUNC_MGT_FUNC_CLASSIFICATION_MASK(26)
#define FUNC_MGT_IGNORE_NULL_FUNC       FUNC_MGT_FUNC_CLASSIFICATION_MASK(27)
#define FUNC_MGT_PRIMARY_KEY_FUNC       FUNC_MGT_FUNC_CLASSIFICATION_MASK(28)
#define FUNC_MGT_TSMA_FUNC              FUNC_MGT_FUNC_CLASSIFICATION_MASK(29)
#define FUNC_MGT_COUNT_LIKE_FUNC        FUNC_MGT_FUNC_CLASSIFICATION_MASK(30) // funcs that should also return 0 when no rows found
#define FUNC_MGT_PROCESS_BY_ROW         FUNC_MGT_FUNC_CLASSIFICATION_MASK(31)
#define FUNC_MGT_FORECAST_PC_FUNC       FUNC_MGT_FUNC_CLASSIFICATION_MASK(32)
#define FUNC_MGT_SELECT_COLS_FUNC       FUNC_MGT_FUNC_CLASSIFICATION_MASK(33)

#define FUNC_MGT_TEST_MASK(val, mask) (((val) & (mask)) != 0)

#define FUNC_UDF_ID_START 5000

#define FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(n) ((uint64_t)1 << n)
#define FUNC_PARAM_SUPPORT_ALL_TYPE         FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(0)
#define FUNC_PARAM_SUPPORT_NUMERIC_TYPE     FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(1)
#define FUNC_PARAM_SUPPORT_VAR_TYPE         FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(2)
#define FUNC_PARAM_SUPPORT_STRING_TYPE      FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(3)
#define FUNC_PARAM_SUPPORT_BOOL_TYPE        FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(4)
#define FUNC_PARAM_SUPPORT_TINYINT_TYPE     FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(5)
#define FUNC_PARAM_SUPPORT_SMALLINT_TYPE    FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(6)
#define FUNC_PARAM_SUPPORT_INT_TYPE         FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(7)
#define FUNC_PARAM_SUPPORT_BIGINT_TYPE      FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(8)
#define FUNC_PARAM_SUPPORT_FLOAT_TYPE       FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(9)
#define FUNC_PARAM_SUPPORT_DOUBLE_TYPE      FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(10)
#define FUNC_PARAM_SUPPORT_VARCHAR_TYPE     FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(11)
#define FUNC_PARAM_SUPPORT_TIMESTAMP_TYPE   FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(12)
#define FUNC_PARAM_SUPPORT_NCHAR_TYPE       FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(13)
#define FUNC_PARAM_SUPPORT_UTINYINT_TYPE    FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(14)
#define FUNC_PARAM_SUPPORT_USMALLINT_TYPE   FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(15)
#define FUNC_PARAM_SUPPORT_UINT_TYPE        FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(16)
#define FUNC_PARAM_SUPPORT_UBIGINT_TYPE     FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(17)
#define FUNC_PARAM_SUPPORT_JSON_TYPE        FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(18)
#define FUNC_PARAM_SUPPORT_VARB_TYPE        FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(19)
#define FUNC_PARAM_SUPPORT_GEOMETRY_TYPE    FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(20)
#define FUNC_PARAM_SUPPORT_INTEGER_TYPE     FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(21)
#define FUNC_PARAM_SUPPORT_NULL_TYPE        FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(22)
#define FUNC_PARAM_SUPPORT_UNIX_TS_TYPE     FUNC_MGT_FUNC_PARAM_SUPPORT_TYPE(23)



#define FUNC_MGT_FUNC_PARAM_SUPPORT_NODE(n) ((uint64_t)1 << n)
#define FUNC_PARAM_SUPPORT_EXPR_NODE                    FUNC_MGT_FUNC_PARAM_SUPPORT_NODE(0)
#define FUNC_PARAM_SUPPORT_VALUE_NODE                   FUNC_MGT_FUNC_PARAM_SUPPORT_NODE(1)
#define FUNC_PARAM_SUPPORT_OPERATOR_NODE                FUNC_MGT_FUNC_PARAM_SUPPORT_NODE(2)
#define FUNC_PARAM_SUPPORT_FUNCTION_NODE                FUNC_MGT_FUNC_PARAM_SUPPORT_NODE(3)
#define FUNC_PARAM_SUPPORT_LOGIC_CONDITION_NODE         FUNC_MGT_FUNC_PARAM_SUPPORT_NODE(4)
#define FUNC_PARAM_SUPPORT_CASE_WHEN_NODE               FUNC_MGT_FUNC_PARAM_SUPPORT_NODE(5)
#define FUNC_PARAM_SUPPORT_COLUMN_NODE                  FUNC_MGT_FUNC_PARAM_SUPPORT_NODE(6)
#define FUNC_PARAM_SUPPORT_NOT_VALUE_NODE               FUNC_MGT_FUNC_PARAM_SUPPORT_NODE(7)

#define FUNC_PARAM_NO_SPECIFIC_ATTRIBUTE               0
#define FUNC_PARAM_MUST_BE_PRIMTS                      1
#define FUNC_PARAM_MUST_BE_PK                          2
#define FUNC_PARAM_MUST_HAVE_COLUMN                    3
#define FUNC_PARAM_MUST_BE_TIME_UNIT                   4
#define FUNC_PARAM_VALUE_NODE_NOT_NULL                 5

#define FUNC_PARAM_NO_SPECIFIC_VALUE                  0
#define FUNC_PARAM_HAS_RANGE                          1
#define FUNC_PARAM_HAS_FIXED_VALUE                    2

#define FUNC_ERR_RET(c)                \
  do {                                 \
    int32_t _code = c;                 \
    if (_code != TSDB_CODE_SUCCESS) {  \
      terrno = _code;                  \
      return _code;                    \
    }                                  \
  } while (0)
#define FUNC_RET(c)                    \
  do {                                 \
    int32_t _code = c;                 \
    if (_code != TSDB_CODE_SUCCESS) {  \
      terrno = _code;                  \
    }                                  \
    return _code;                      \
  } while (0)
#define FUNC_ERR_JRET(c)              \
  do {                                \
    code = c;                         \
    if (code != TSDB_CODE_SUCCESS) {  \
      terrno = code;                  \
      goto _return;                   \
    }                                 \
  } while (0)

#ifdef __cplusplus
}
#endif

#endif  // _TD_FUNCTION_MGT_INT_H_
