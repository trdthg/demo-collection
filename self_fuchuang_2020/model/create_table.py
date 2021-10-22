import pymysql

class DB():
    
    def __init__(self, library="library_flow"):
        super().__init__()
        self.connect(library)

    def connect(self,DB):
        DB_USER = 'maker0'
        DB_PASS = 'Maker0000'
        DB_HOST = 'rm-bp11labi01950io698o.mysql.rds.aliyuncs.com'
        DB_PORT = 3306
        DATABASE = DB
        try:
            self.connect_info = pymysql.connect(user=DB_USER, passwd=DB_PASS, host=DB_HOST, port=DB_PORT, db=DATABASE)  #1
            self.cursor = self.connect_info.cursor()
        except:
            print("连接失败")
        
    def close(self):
        self.connect_info.close()

def createTable(db):
    for table_name in [f'input_records']:
        sql1 = f"""CREATE TABLE IF NOT EXISTS {table_name} (
            id INT NOT NULL AUTO_INCREMENT ,
            time_start CHAR(20),
            weather1 CHAR(100),
            weather2 CHAR(100),
            dayprop INT,
            temperatures1 INT,
            temperatures2 INT,
            station CHAR(100),
            flow INT,
            flow_type INT,
            station_type INT,
            station_classify INT,
            primary key(id))"""
        db.cursor.execute(sql1)
    table_name_1 = f'list1_predict'
    # table_name_2 = f'list2_predict'
    table_name_3 = f'list3_predict'
    table_name_4 = f'list4_predict'
    sql1 = f"""CREATE TABLE IF NOT EXISTS {table_name_1} (
            station  CHAR(20),
            in_flow INT,
            out_flow INT,
            in_flow_plus INT,
            out_flow_plus INT,
            turn INT,
            foreign_key INT)"""
    sql3 = f"""CREATE TABLE IF NOT EXISTS {table_name_3} (
            station_1  CHAR(20) NOT NULL,
            station_2  CHAR(20) NOT NULL,
            flow INT,
            turn INT,
            foreign_key INT)"""
    sql4 = f'''CREATE TABLE IF NOT EXISTS {table_name_4}  (
            linename CHAR(20) NOT NULL,
            flow INT,
            turn INT,
            foreign_key INT)'''
    db.cursor.execute(sql1)
    db.cursor.execute(sql3)
    db.cursor.execute(sql4)

def main():
    db = DB('library_pre')
    createTable(db)


if __name__ == '__main__':
    main()