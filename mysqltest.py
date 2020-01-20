import MySQLdb
from datetime import datetime

now = datetime.now()
print(now)

# 接続する
con = MySQLdb.connect(
user='root',
passwd='fallout14',
host='localhost',
db='db_cast_crawler'
,charset="utf8mb4"
)

# カーソルを取得する
cur = con.cursor()

# SQL（データベースを操作するコマンド）を実行する
# userテーブルから、HostとUser列を取り出す

# sql = "INSERT INTO posts (post_id, data_name2, caption, user_id, posted_date) VALUES (%s, %s, %s, %s, %s)"
# val = ('1','1','1','1',now)
# cur.execute(sql,val)

sql = "select * from posts"
cur.execute(sql)
result = cur.fetchall()


# con.commit()
# print(result)

# 実行結果を取得する
# rows = cur.fetchall()

# # 一行ずつ表示する
for i in result:
    caption = i[2]
    print(caption)

cur.close

# 接続を閉じる
con.close
