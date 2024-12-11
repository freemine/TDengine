---
title: Icinga2
slug: /third-party-tools/data-collection/icinga2
---

import Icinga2 from "./_icinga2.mdx"

icinga2 is an open-source host and network monitoring software, originally developed from the Nagios network monitoring application. Currently, icinga2 is released under the GNU GPL v2 license.

To store data collected by icinga2 into TDengine, simply modify the icinga2 configuration to point to the corresponding server and port of taosAdapter. This allows full utilization of TDengine's efficient storage and query performance for time-series data and cluster processing capabilities.

## Prerequisites

The following preparations are needed to write icinga2 data into TDengine:

- TDengine cluster is deployed and running normally
- taosAdapter is installed and running normally. For details, please refer to [taosAdapter user manual](../../../tdengine-reference/components/taosadapter/)
- icinga2 is installed. For icinga2 installation, please refer to [official documentation](https://icinga.com/docs/icinga-2/latest/doc/02-installation/)

## Configuration Steps

<Icinga2 />

## Verification Method

Restart taosAdapter:

```shell
sudo systemctl restart taosadapter
```

Restart icinga2:

```shell
sudo systemctl restart icinga2
```

After waiting about 10 seconds, use the TDengine CLI to query TDengine to verify if the corresponding database has been created and data has been written:

```text
taos> show databases;
              name              |
=================================
 information_schema             |
 performance_schema             |
 icinga2                        |
Query OK, 3 row(s) in set (0.001867s)

taos> use icinga2;
Database changed.

taos> show stables;
              name              |
=================================
 icinga.service.users.state_... |
 icinga.service.users.acknow... |
 icinga.service.procs.downti... |
 icinga.service.users.users     |
 icinga.service.procs.procs_min |
 icinga.service.users.users_min |
 icinga.check.max_check_atte... |
 icinga.service.procs.state_... |
 icinga.service.procs.procs_... |
 icinga.service.users.users_... |
 icinga.check.latency           |
 icinga.service.procs.procs_... |
 icinga.service.users.downti... |
 icinga.service.users.users_... |
 icinga.service.users.reachable |
 icinga.service.procs.procs     |
 icinga.service.procs.acknow... |
 icinga.service.procs.state     |
 icinga.service.procs.reachable |
 icinga.check.current_attempt   |
 icinga.check.execution_time    |
 icinga.service.users.state     |
Query OK, 22 row(s) in set (0.002317s)
```

:::note

- The default subtable names generated by TDengine are unique ID values generated according to rules.

:::