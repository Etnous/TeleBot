import sqlite3

conn = sqlite3.connect("bot.sqlite")
cursor = conn.cursor()

# 创建user表
sql = "create table if not exists user (uid bigint not null, city varchar, city_code int, warning int default 0 not null, daily int default 0 not null)"
cursor.execute(sql)

# 创建快递单号表
sql = "create table if not exists express_No (order_No text not null, commpany text not null, bid bigint not null)"
cursor.execute(sql)

cursor.close()
conn.commit()
conn.close()