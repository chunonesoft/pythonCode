#coding=utf-8
import pymysql.cursors
import sys
reload(sys)

sys.setdefaultencoding('utf-8')

# 连接数据库
connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='taotao',
    charset='utf8'
)

# 获取游标
cursor = connect.cursor()

# 查询数据
sql = "SELECT * FROM tb_content "
cursor.execute(sql)
for row in cursor.fetchall():
    print(row[0])
print('共查找出', cursor.rowcount, '条数据')