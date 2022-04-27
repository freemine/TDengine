# ANCHOR: connect
from taosrest import connect, TaosRestConnection, TaosRestCursor

conn: TaosRestConnection = connect(host="localhost",
                                   user="root",
                                   password="taosdata",
                                   port=6041,
                                   timeout=30)

# ANCHOR_END: connect
# ANCHOR: basic
# create STable
cursor = conn.cursor()
cursor.execute("DROP DATABASE IF EXISTS power")
cursor.execute("CREATE DATABASE power")
cursor.execute("CREATE STABLE power.meters (ts TIMESTAMP, current FLOAT, voltage INT, phase FLOAT) TAGS (location BINARY(64), groupId INT)")

# insert data
cursor.execute("""INSERT INTO power.d1001 USING power.meters TAGS(Beijing.Chaoyang, 2) VALUES ('2018-10-03 14:38:05.000', 10.30000, 219, 0.31000) ('2018-10-03 14:38:15.000', 12.60000, 218, 0.33000) ('2018-10-03 14:38:16.800', 12.30000, 221, 0.31000)
    power.d1002 USING power.meters TAGS(Beijing.Chaoyang, 3) VALUES ('2018-10-03 14:38:16.650', 10.30000, 218, 0.25000)
    power.d1003 USING power.meters TAGS(Beijing.Haidian, 2) VALUES ('2018-10-03 14:38:05.500', 11.80000, 221, 0.28000) ('2018-10-03 14:38:16.600', 13.40000, 223, 0.29000)
    power.d1004 USING power.meters TAGS(Beijing.Haidian, 3) VALUES ('2018-10-03 14:38:05.000', 10.80000, 223, 0.29000) ('2018-10-03 14:38:06.500', 11.50000, 221, 0.35000)""")
print("affected rows", cursor.rowcount)

# query data
cursor.execute("SELECT * FROM power.meters")
# get column names from cursor
column_names = [meta[0] for meta in cursor.description]
# get rows
data: list[tuple] = cursor.fetchall()
print(column_names)
for row in data:
    print(row)

# output:
# affected rows 8
# ['ts', 'current', 'voltage', 'phase', 'location', 'groupid']
# [datetime.datetime(2018, 10, 3, 14, 38, 5, tzinfo=tzinfo(480,'+08:00')), 10.3, 219, 0.31, 'beijing.chaoyang', 2]
# [datetime.datetime(2018, 10, 3, 14, 38, 15, tzinfo=tzinfo(480,'+08:00')), 12.6, 218, 0.33, 'beijing.chaoyang', 2]
# [datetime.datetime(2018, 10, 3, 14, 38, 16, 800000, tzinfo=tzinfo(480,'+08:00')), 12.3, 221, 0.31, 'beijing.chaoyang', 2]
# [datetime.datetime(2018, 10, 3, 14, 38, 16, 650000, tzinfo=tzinfo(480,'+08:00')), 10.3, 218, 0.25, 'beijing.chaoyang', 3]
# [datetime.datetime(2018, 10, 3, 14, 38, 5, 500000, tzinfo=tzinfo(480,'+08:00')), 11.8, 221, 0.28, 'beijing.haidian', 2]
# [datetime.datetime(2018, 10, 3, 14, 38, 16, 600000, tzinfo=tzinfo(480,'+08:00')), 13.4, 223, 0.29, 'beijing.haidian', 2]
# [datetime.datetime(2018, 10, 3, 14, 38, 5, tzinfo=tzinfo(480,'+08:00')), 10.8, 223, 0.29, 'beijing.haidian', 3]
# [datetime.datetime(2018, 10, 3, 14, 38, 6, 500000, tzinfo=tzinfo(480,'+08:00')), 11.5, 221, 0.35, 'beijing.haidian', 3]

# ANCHOR_END: basic
