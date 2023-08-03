import pymysql

db = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',    #在这里输入用户名
    password='123456',     #在这里输入密码
    charset='utf8mb4'
    )

cursor = db.cursor() #创建游标对象
try:

    sql = 'show databases'
    cursor.execute(sql)
    print('未创建数据库前：', cursor.fetchall()) #获取创建数据库前全部数据库

    dbname = 'justtest'
    sql = 'create database if not exists %s'%(dbname) #创建数据库
    cursor.execute(sql)
    sql = 'show databases'
    cursor.execute(sql)
    print('创建新的数据库后：', cursor.fetchall()) #获取创建数据库后全部数据库

    sql = 'drop database if exists %s'%(dbname) #删除数据库
    cursor.execute(sql)
    sql = 'show databases'
    cursor.execute(sql)
    print('删除新的数据库后：', cursor.fetchall()) #获取删除数据库后全部数据库

except Exception as e:
    print(e)
    db.rollback()  #回滚事务

finally:
    cursor.close()
    db.close()  #关闭数据库连接
