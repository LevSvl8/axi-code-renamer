import os
os.environ["NLS_LANG"] = "RUSSIAN_RUSSIA.CL8MSWIN1251"
from aconn import AConnector

if __name__ == '__main__':

    src_params = {
        'name': 'ora127',
        'conn': 'oracle://maximo:maximo@192.168.10.127:1521/max75',
        'dbtype': 'ORA'
    }
    dest_param = {
        'name': 'pg127',
        'conn': 'postgresql://maximo:maximo@192.168.10.127/max1',
        'dbtype': 'PG'
    }

    conn_src = AConnector(src_params['name'], src_params['conn'], encoding='utf8')
    conn_dest = AConnector(dest_param['name'], dest_param['conn'], encoding='utf8')

    for row in conn_src.sql('SELECT description from l_asset').fetchmany(10):
        print(row[0])