import os
os.environ["NLS_LANG"] = "RUSSIAN_RUSSIA.CL8MSWIN1251"

from connection_params import SRC_PARAMS, DEST_PARAMS
# from models_params import SRC_MODEL, DEST_MODEL
from aconn import AConnector
from fix.mxseq import copy_max_sequences
from fix.mxtrigger import copy_maximo_triggers, check_trigger_posible


if __name__ == '__main__':
    src = AConnector(SRC_PARAMS['name'], SRC_PARAMS['conn'], echo=False, schema_name=SRC_PARAMS['name'])
    dest = AConnector(DEST_PARAMS['name'], DEST_PARAMS['conn'], echo=False, schema_name=SRC_PARAMS['name']) # , convert_unicode=True     encoding='cp1251',

    first_run = False
    if first_run:

        sql_axiseq = "CREATE SEQUENCE axioma.axiseq INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE;"
        dest.sql(sql_axiseq)

    copy_max_sequences(src, dest, True, DEST_PARAMS['dbtype'])

    #print("Executing SHAMX_SCRIPTS")
    #dest.sql(SHMAX_SCRIPTS)
    #dest.sql(FIX_MAX_PROPS)

    print("Copying triggers")
    check_trigger_posible(src, dest)
    copy_maximo_triggers(src, dest, DEST_PARAMS['dbtype'])

    del dest