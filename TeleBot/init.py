import sqlite3

conn = sqlite3.connect("user.sqlite")
cursor = conn.cursor()

sql = "create table if not exists user (uid bigint not null , city_code int , company text, kd text)"
cursor.execute(sql)
cursor.close()
conn.commit()
conn.close()