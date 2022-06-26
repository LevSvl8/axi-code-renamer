import os
os.environ["NLS_LANG"] = "RUSSIAN_RUSSIA.CL8MSWIN1251"

from connection_params import SRC_PARAMS, DEST_PARAMS
from aconn import AConnector

if __name__ == '__main__':
    src = AConnector(SRC_PARAMS['name'], SRC_PARAMS['conn'], echo=False, schema_name=SRC_PARAMS['name'],)
    dest = AConnector(DEST_PARAMS['name'], DEST_PARAMS['conn'], echo=False, schema_name=DEST_PARAMS['name'],) # , convert_unicode=True     encoding='cp1251',

    DBCONFIG_UPDATE_INDEXES = '''update axisysindexes set changed = 'Y' '''
    print('Executing update indexes script')
    dest.sql(DBCONFIG_UPDATE_INDEXES)

    print('Executing create views script')
    DBCONFIG_CREATE_VIEWS = '''update axiobjectcfg set changed = 'I' where objectname in (select viewname from axiview)'''

    dest.sql(DBCONFIG_CREATE_VIEWS)
    print('Done')

    del dest