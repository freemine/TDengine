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

// TAOS standard API example. The same syntax as MySQL, but only a subset
// to compile: gcc -o with_reqid_demo with_reqid_demo.c -ltaos

#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "taosws.h"

static int DemoWithReqId() {
  // ANCHOR: with_reqid
  int   code = 0;
  char *dsn = "ws://localhost:6041";

  // connect
  WS_TAOS *taos = ws_connect(dsn);
  if (taos == NULL) {
    fprintf(stderr, "Failed to connect to %s, ErrCode: 0x%x, ErrMessage: %s.\n", dsn, ws_errno(NULL), ws_errstr(NULL));
    return -1;
  }

  const char *sql = "SELECT ts, current, location FROM power.meters limit 1";
  // query data with reqid
  long    reqid = 3L;
  WS_RES *result = ws_query_with_reqid(taos, sql, reqid);
  code = ws_errno(result);
  if (code != 0) {
    fprintf(stderr, "Failed to execute sql withQID: %ld, ErrCode: 0x%x, ErrMessage: %s\n.", reqid, code,
            ws_errstr(result));
    ws_close(taos);
    return -1;
  }

  WS_ROW          row = NULL;
  int             rows = 0;
  int             num_fields = ws_field_count(result);
  const WS_FIELD *fields = ws_fetch_fields(result);

  fprintf(stdout, "query successfully, got %d fields, the sql is: %s.\n", num_fields, sql);

  // fetch the records row by row
  while ((row = ws_fetch_row(result))) {
    // Add your data processing logic here

    rows++;
  }
  fprintf(stdout, "total rows: %d\n", rows);
  ws_free_result(result);

  // close & clean
  ws_close(taos);
  return 0;
  // ANCHOR_END: with_reqid
}

int main(int argc, char *argv[]) { return DemoWithReqId(); }
