import csv
from datetime import datetime

# import faker

import pymysql

_default_host = "127.0.0.1"
_default_port = 3306


def generate_random():
    f = open("data/users.csv", "w")
    userwriter = csv.writer(f, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    f = open("data/accounts.csv", "w")
    accountwriter = csv.writer(f, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)

    f = open("data/roles.csv", "w")
    rolewriter = csv.writer(f, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    n = 10000

    for i in range(0, n + 1):
        id = 10000 + i
        create_time = "2022-04-16 00:00:00.000000"
        modify_time = "2022-04-16 00:00:00.000000"
        balance = 1000000
        bank_account_sn = id
        user_id = id
        accountwriter.writerow([id,
                                create_time,
                                modify_time,
                                balance,
                                bank_account_sn,
                                user_id])

    #     create table user_roles
    for i in range(0, n + 1):
        user_id = 10000 + i
        roles = "test"
        rolewriter.writerow([user_id, roles])

    for i in range(0, n + 1):
        # id          bigint auto_increment primary key, 100000 + i
        id = 10000 + i
        create_time = "2022-04-16 00:00:00.000000"
        modify_time = "2022-04-16 00:00:00.000000"
        idnumber = str(id) + "idnumber"
        age = 30
        country = "中国"
        dishonest = False
        employment = "Employed"
        gender = "Male"
        name = "test-name"
        over_dual = 0
        password = "$2a$10$A77LByAaUQrDUHjz61.eKO3baRgsCByiaH0aKAYSgYJ5RvNoIoxkm"
        username = "user" + str(id)
        year_income = 100000
        userwriter.writerow([id, create_time, modify_time, idnumber,
                             age,
                             country,
                             dishonest,
                             employment,
                             gender,
                             name,
                             over_dual,
                             password,
                             username,
                             year_income
                             ])


class MYSQL:
    def __init__(self, user, pwd, host=_default_host, port=_default_port):
        self.host = host
        self.port = port
        self.user = user
        self.__pwd = pwd
        self.db = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.__pwd,
            local_infile=1
        )
        self.__drop_table("user_roles")
        self.__drop_table("bank_account")
        self.__drop_table("user")
        self.__create_tables()

    def connect_database(self, database_name):
        self.db.db = database_name

    def load_user_data(self, filepath, table):
        # self.__drop_table(table)
        # self.__create_tables()
        start = datetime.now()
        sql = """
        LOAD DATA LOCAL INFILE '%s' INTO TABLE ms.%s FIELDS TERMINATED BY ',' (
            id, create_time, modify_time, idnumber,
                         age,
                         country,
                         dishonest,
                         employment,
                         gender,
                         name,
                         over_dual,
                         password,
                         username,
                         year_income
        );
        """
        self.execute_sql(sql % (filepath, table))
        print("load data finish after", datetime.now() - start)

    def load_roles_data(self, filepath, table):
        # self.__drop_table(table)
        # self.__create_tables()
        start = datetime.now()
        sql = """
        LOAD DATA LOCAL INFILE '%s' INTO TABLE ms.%s FIELDS TERMINATED BY ',' (
            user_id, roles
        );
        """
        self.execute_sql(sql % (filepath, table))
        print("load data finish after", datetime.now() - start)

    def load_account_data(self, filepath, table):
        # self.__create_tables()
        start = datetime.now()
        sql = """
        LOAD DATA LOCAL INFILE '%s' INTO TABLE ms.%s FIELDS TERMINATED BY ',' (
            id,
                            create_time,
                            modify_time,
                            balance,
                            bank_account_sn,
                            user_id
        );
        """
        self.execute_sql(sql % (filepath, table))
        print("load data finish after", datetime.now() - start)

    def execute_sql(self, sql):
        try:
            self.db.cursor().execute(sql)
            self.db.commit()
        except pymysql.Error as e:
            print("error in execute_sql:", e)
            # print("sql:", sql)

    def __drop_table(self, table):
        print("drop")
        sql = """
        DROP TABLE IF EXISTS ms.%s;
        """
        self.execute_sql(sql % table)
        print("drop success")

    def __create_tables(self):
        sql = """
        CREATE TABLE ms.user (
            `id` bigint(20) NOT NULL AUTO_INCREMENT,
            `create_time` datetime(6) DEFAULT NULL,
            `modify_time` datetime(6) DEFAULT NULL,
            `idnumber` varchar(255) NOT NULL,
            `age` int(11) NOT NULL,
            `city` varchar(255) DEFAULT NULL,
            `country` varchar(255) DEFAULT NULL,
            `dishonest` bit(1) DEFAULT NULL,
            `employment` varchar(255) DEFAULT NULL,
            `gender` varchar(255) NOT NULL,
            `name` varchar(64) NOT NULL,
            `over_dual` bigint(20) DEFAULT NULL,
            `password` varchar(255) NOT NULL,
            `province` varchar(255) DEFAULT NULL,
            `username` varchar(255) NOT NULL,
            `year_income` bigint(20) DEFAULT NULL,
            PRIMARY KEY (`id`),
            UNIQUE KEY `UK_tgkwrgg3qouq6087dy4schx61` (`idnumber`(10)),
            UNIQUE KEY `UK_sb8bbouer5wak8vyiiy4pf2bx` (`username`(10))
        ) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4;
        """
        self.execute_sql(sql)

        sql = '''
        CREATE TABLE ms.user_roles (
            `user_id` bigint(20) NOT NULL,
            `roles` varchar(255) DEFAULT NULL,
            KEY `FK55itppkw3i07do3h7qoclqd4k` (`user_id`),
            CONSTRAINT `FK55itppkw3i07do3h7qoclqd4k` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        '''
        self.execute_sql(sql)

        sql = '''
        CREATE TABLE ms.bank_account (
            `id` bigint(20) NOT NULL AUTO_INCREMENT,
            `create_time` datetime(6) DEFAULT NULL,
            `modify_time` datetime(6) DEFAULT NULL,
            `balance` bigint(20) NOT NULL,
            `bank_account_sn` bigint(20) NOT NULL,
            `user_id` bigint(20) NOT NULL,
            PRIMARY KEY (`id`),
            UNIQUE KEY `UK_sufktt3h6rerqjo7kxrogmr30` (`bank_account_sn`)
        ) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4;
        '''
        self.execute_sql(sql)


if __name__ == '__main__':
    # generate_random()
    db = MYSQL('root', 'ms', host='localhost')
    db.connect_database('ms')

    db.load_user_data('data/users.csv', "user")
    db.load_roles_data('data/roles.csv', "user_roles")
    db.load_account_data('data/accounts.csv', "bank_account")
