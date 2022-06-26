import cx_Oracle
import ibm_db
import psycopg2
from psycopg2.extras import execute_values

from axi_renamer.renamer_starter import Renamer

DBTYPES = ['ORA', 'DB2', 'PG']


class My_Connection:
    def __init__(self, connection_def):
        self.dbhost = connection_def[0]
        self.dbport = connection_def[1]
        self.dbname = connection_def[2]
        self.username = connection_def[3]
        self.password = connection_def[4]
        self.dbtype = connection_def[5]
        self.axirename = False
        if self.username == 'axioma':
            self.axirename = True
        if self.dbtype not in DBTYPES:
            raise Exception(f"{self.dbtype} is not a valid dbtype, chose one of: {','.join(DBTYPES)}")

    def __enter__(self):

        if self.dbtype == 'ORA':
            self.connection = cx_Oracle.connect(self.username, self.password,
                           cx_Oracle.makedsn(self.dbhost, self.dbport, self.dbname),
                           encoding="UTF-8")
            #print(f"Connected to: {self.dbtype} {self.dbhost} {self.dbname} \n")
        elif self.dbtype == 'DB2':
            connString = "DRIVER={IBM DB2 ODBC DRIVER}"
            connString += ";DATABASE=" + self.dbname
            connString += ";HOSTNAME=" + self.dbhost
            connString += ";PORT=" + self.dbport
            connString += ";PROTOCOL=TCPIP"
            connString += ";UID=" + self.username
            connString += ";PWD=" + self.password
            self.connection = ibm_db.connect(connString, "", "")
            #ibm_db.autocommit(self.connection, ibm_db.SQL_AUTOCOMMIT_OFF)
            #print(f"Connected to: {self.dbtype} {self.dbhost} {self.dbname} AUTOCOMMIT_OFF\n")
        elif self.dbtype =='PG':
            self.connection = psycopg2.connect(
                host=self.dbhost,
                database=self.dbname,
                user=self.username,
                password=self.password)

            self.connection.set_client_encoding('UTF8')
        return self

    def __exit__(self, type, value, traceback):
        if self.dbtype == 'ORA':
            self.connection.close()
        elif self.dbtype == 'DB2':
            ibm_db.close(self.connection)
        elif self.dbtype == 'PG':
            self.connection.close()
        #print(f"Disconnect: {self.dbtype} {self.dbhost} {self.dbname} \n")

    def set_select_where(self, sql):
        if self.axirename:
            sql = Renamer().get_axi_val(sql)

        if self.dbtype == 'ORA':
            self.crs = self.connection.cursor().execute(sql)

        elif self.dbtype == 'DB2':
            self.crs = ibm_db.exec_immediate(self.connection, sql)

        elif self.dbtype == 'PG':
            self.crs = self.connection.cursor()
            self.crs.execute(sql)

    def fetch_next(self):
        res = None
        if self.dbtype == 'ORA':
            res = self.crs.fetchone()
        elif self.dbtype == 'DB2':
            res = ibm_db.fetch_tuple(self.crs)
        elif self.dbtype == 'PG':
            res = self.crs.fetchone()
        return res

    def prepareStmt(self, tablename, attrlist_to):

        if self.dbtype == 'ORA':
            pass
        elif self.dbtype == 'DB2':
            sqlStatement = f"INSERT INTO {tablename} ({', '.join(attrlist_to)}) " \
                               f"VALUES({', '.join(['?' for i in range(len(attrlist_to))])})"
            return ibm_db.prepare(self.connection, sqlStatement)
        elif self.dbtype == 'PG':
            sqlStatement = f"INSERT INTO {tablename} ({', '.join(attrlist_to)}) " \
                           f"VALUES %s"
            self.crs = self.connection.cursor()
            return sqlStatement


    def execute(self, sql):
        if self.axirename:
            sql = Renamer().get_axi_val(sql)

        if self.dbtype == 'ORA':
            self.crs = self.connection.cursor().execute(sql)
        elif self.dbtype == 'DB2':
            self.crs = ibm_db.exec_immediate(self.connection, sql)
        elif self.dbtype == 'PG':
            self.crs = self.connection.cursor()
            self.crs.execute(sql)
        return self.crs

    def execute_many(self, preparedStmt, values, template, page_size=1000):
        if self.dbtype == 'ORA':
            pass
        elif self.dbtype == 'DB2':
            return ibm_db.execute_many(preparedStmt, values)

        elif self.dbtype == 'PG':
            # page_size Должен быть не меньше, чем количество строк в values. Потому что если будет разбиение строк на
            # страницы, то rowcount покажет только количество последнего запроса (последней страницы).
            # Разбиение на страницы необходимо осуществлять через переменную limit в модуле copy_data
            execute_values(self.crs, preparedStmt, values, template=template, page_size=page_size)

            return self.crs.rowcount

    def rollback(self):
        if self.dbtype == 'ORA':
            pass
        elif self.dbtype == 'DB2':
            ibm_db.rollback(self.connection)
        elif self.dbtype == 'PG':
            self.connection.rollback()

    def commit(self):
        if self.dbtype == 'ORA':
            pass
        elif self.dbtype == 'DB2':
            ibm_db.commit(self.connection)
        elif self.dbtype == 'PG':
            self.connection.commit()

    def get_row_count(self, tableName):
        if self.axirename:
            tableName = Renamer().get_axi_val(tableName)

        dataRecord = False
        sqlStatement = f"SELECT COUNT(*) FROM {tableName}"

        self.set_select_where(sqlStatement)
        dataRecord = self.fetch_next()

        return dataRecord[0]