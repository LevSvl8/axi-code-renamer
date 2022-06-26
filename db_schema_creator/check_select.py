from connection_params import SRC_PARAMS
#from models_params import SRC_MODEL
from models.test import ora42_test as SRC_MODEL
from aconn import AConnector


def start():

    start_id = 60000012241 #35000
    limit = 1
    table = 'labtrans'

    source_class = SRC_MODEL.SCHEMA_TABLES.get(('t_' + table).upper(), None)
    if source_class is None:
        raise Exception('Table %s not found in source model' % table)

    src = AConnector(SRC_PARAMS['name'], SRC_PARAMS['conn'], schema_name=SRC_PARAMS['name'], echo=False)  # , encoding='utf8'
    q = src.con.query(source_class)


    pk_col = list(source_class.__table__.primary_key)[0] # type: Column
    pk_prop = pk_col.key.upper()
    q = q.order_by(pk_col).filter(pk_col > start_id)
    if limit is not None:
        q = q.limit(limit)

    last_id = None
    try:
        for obj in q.yield_per(1):
            last_id = getattr(obj, pk_prop)
            print(last_id)
    except Exception as e:
        print('Select failed with exception %s' % str(e))
        print('Last selected id %s' % last_id)
        exit(6)




if __name__ == '__main__':
    start()
