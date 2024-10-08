import pandas
from sqlalchemy import create_engine

engine = create_engine("taos://root:taosdata@localhost:6030/power")
df = pandas.read_sql("SELECT * FROM meters", engine)

# print index
print(df.index)
# print data type  of element in ts column
print(type(df.ts[0]))
print(df.head(3))

# output:
# RangeIndex(start=0, stop=8, step=1)
# <class 'pandas._libs.tslibs.timestamps.Timestamp'>
#                        ts  current  voltage  phase          location  groupid
# 0 2018-10-03 14:38:05.000     10.3      219   0.31  beijing.chaoyang        2
# 1 2018-10-03 14:38:15.000     12.6      218   0.33  beijing.chaoyang        2
# 2 2018-10-03 14:38:16.800     12.3      221   0.31  beijing.chaoyang        2
