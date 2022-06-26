import os
# oracle: select userenv('language') from dual;
from transfer.export_filter import *

os.environ["NLS_LANG"] = "RUSSIAN_RUSSIA.CL8MSWIN1251"

from connection_params import SRC_PARAMS, DEST_PARAMS
from models_params import SRC_MODEL

from sqlalchemy import func, Column, LargeBinary
from aconn import AConnector

import json

def get_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count


def analyze_tables_sizes(src_connector: AConnector, source_tables_classes: list):
    """

    :param conn:
    :param source_tables_classes:
    :return: dict {table_name: size}
    """
    result = {}
    for source_class in source_tables_classes:
        tablename = source_class.__tablename__
        src_connector.status('Calculating table %s' % tablename)
        result[tablename] = get_count(src_connector.con.query(source_class))
    return result


def split_to_tasks(connector: AConnector, tab_class, total_size, chunk_size):
    has_blobs = False
    # table_name = tab_class.__tablename__
    pk_col = list(tab_class.__table__.primary_key)[0]  # type: Column
    for col in tab_class.__table__.columns:  # type: Column
        if isinstance(col.type, LargeBinary):
            has_blobs = True
    if has_blobs:
        return None

    chunk_start_ids = []
    chunks_count = total_size // chunk_size + 1
    for j in range(chunks_count):
        offset = j * chunk_size
        res = connector.con.query(pk_col).order_by(pk_col).offset(offset).limit(1).all()
        if len(res) > 0:
            chunk_start_ids.append(res[0][0])

    return chunk_start_ids


def make_transfer_tasks(connector: AConnector, model, output_filename, max_size, chunk_size, skip_audit=True, cleanup=False):
    print('Making tasks')
    task_pattern = '{{"task":"{task}", "table": "{table}", "pk": "{pk}", "size": "{size}", ' \
                   '"full_load": "{full_load}", "start_id": "{start_id}", "limit": "{limit}", "cleanup": "{cleanup}" }}'

    tasks = []
    def _add_task(_table_class, _size, _full_load, _start_id, _limit, _cleanup):
        task_no = len(tasks) + 1
        _table = _table_class.__tablename__
        pk = list(_table_class.__table__.primary_key)[0]
        task = task_pattern.format(task=task_no, table=_table, pk=pk, size=_size,
                                   full_load=_full_load, start_id=_start_id, limit=_limit, cleanup=_cleanup)
        tasks.append(task)

    table_filter = get_table_filter()
    for class_name, tab_class in model.SCHEMA_TABLES.items():
        tablename = tab_class.__tablename__
        if table_filter[tablename][2] and table_filter[tablename][2]=='no_cleanup':
            cleanup = False
        if skip_audit and str(tablename).upper().startswith('A_'):
            print('Table %s skip - audit' % tablename)
            continue
        #try:
        q = connector.con.query(tab_class)
        size = get_count(apply_filter(q, model.SCHEMA_TABLES, tab_class))
        #except:
        #    pass
        #    print('!!! ERROR: Table %s skip - DATABASE ERRROR' % tablename)
        #    continue
        if size == 0:
            print('Table %s skip - empty' % tablename)
            continue
        full_load = size <= max_size
        offset = None
        limit = None
        if not full_load:
            print('Table %s size %s splitting to chunks' % (tablename, size))
            chunks = split_to_tasks(connector, tab_class, size, chunk_size)
            print('      chunks count: %s' % len(chunks))
            for start_id in chunks[:-1]:
                if start_id == chunks[0]:
                    _add_task(tab_class, size, False, start_id, chunk_size, cleanup)
                else:
                    _add_task(tab_class, size, False, start_id, chunk_size, False)
            _add_task(tab_class, size, False, chunks[-1], None, False)  # rest records
        else:
            print('Table %s size %s full load' % (tablename, size))
            _add_task(tab_class, size, True, None, None, cleanup)


    file_text = '[\n' + ',\n'.join([task for task in tasks]) + '\n]'
    with open(output_filename, 'w') as f:
        f.write(file_text)


if __name__ == '__main__':
    src = AConnector(SRC_PARAMS['name'], SRC_PARAMS['conn'], encoding='utf8', schema_name=SRC_PARAMS['name'], echo=False)
    make_transfer_tasks(src, SRC_MODEL, 'tasks\%s_to_%s_all.json' % (SRC_PARAMS['name'], DEST_PARAMS['name']),
                        300000, 100000, skip_audit=True, cleanup=True)




