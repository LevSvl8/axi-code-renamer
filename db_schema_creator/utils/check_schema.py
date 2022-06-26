from aconn import AConnector
from sqlalchemy import Column, MetaData, Table

from model1 import T_PRLINE

def check_table():

    pass

def check_schema():
    pass



def test_check(conn: AConnector, table_model=T_PRLINE):

    model_types = {c.name: c.type for c in table_model.__table__.columns}

    table_db = Table(table_model.__tablename__, conn.meta, autoload=True, autoload_with=conn.engine)
    db_types = {c.name: c.type for c in table_db.columns}


    errors = []

    for c in table_model.__table__.columns:  # type: Column
        if c.name not in db_types:
            errors.append((c.name, str(c.type), 'Not in db'))

    for c in table_db.columns:  # type: Column
        if c.name not in model_types:
            errors.append((c.name, 'Not in model', str(c.type)))
            continue
        model_t = model_types[c.name]
        if str(c.type) != str(model_t):
            errors.append((c.name, str(model_t), str(c.type)))

    for err in errors:
        print(err)


if __name__ == '__main__':
    _src = {
        'name': 'ora127',
        'conn': 'oracle://maximo:maximo@192.168.10.127:1521/max75',
        'dbtype': 'ORA'
    }
    conn = AConnector(_src['name'], _src['conn'])
    test_check(conn, T_PRLINE)