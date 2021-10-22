from sqlalchemy import create_engine
import pandas as pd
import pymysql
DB_USER = 'maker0'
DB_PASS = 'Maker0000'
DB_HOST = 'rm-bp11labi01950io698o.mysql.rds.aliyuncs.com'
DB_PORT = 3306
DATABASE = 'library_flow'
connect_info = pymysql.connect(user=DB_USER, passwd=DB_PASS, host=DB_HOST, port=DB_PORT, db=DATABASE)  #1
cursor = connect_info.cursor()
# 查询语句，选出testexcel表中的所有数据
sql = f"""CREATE TABLE IF NOT EXISTS student (
    id int primary key auto_increment,
    name varchar(20),
    score float,
    birthday date )"""
cursor.execute(sql)
connect_info.commit()
connect_info.close()
