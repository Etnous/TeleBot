import sqlite3

conn = sqlite3.connect("bot.sqlite")
cursor = conn.cursor()

# 创建user表
sql = "create table if not exists user " \
      "(uid bigint not null, " \
      "city varchar, " \
      "city_code int, " \
      "weather varchar default '0', " \
      "warning int default 0 not null, " \
      "daily int default 0 not null, " \
      "tweet int default 0 not null)" \

cursor.execute(sql)

# 创建推特表
sql = "create table if not exists twitter" \
      "(uid bigint," \
      "screen_name text," \
      "last_id bigint)"
cursor.execute(sql)

# 创建测试IP表
sql = "create table if not exists ping " \
      "(name text not null, " \
      "ip varchar not null, " \
      "status int default 0 not null, " \
      "link text)"
cursor.execute(sql)

cursor.close()
conn.commit()
conn.close()