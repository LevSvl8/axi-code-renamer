import ibm_db
import ibm_db_sa
import ibm_db_dbi

SRC_PARAMS = {
    'name': 'maximo',
    'conn': 'db2://maximo:maximo@192.168.10.164:50002/maxdb76',
    'dbtype': 'DB2',
    'encoding': 'cp1251'
}

DEST_PARAMS = {
    'name': 'axioma',
    'conn': 'postgres://axioma:axioma@localhost:5432/postgres',
    'dbtype': 'PG',
    'encoding': 'cp1251'
}
