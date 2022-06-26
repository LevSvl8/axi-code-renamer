print('Importing model')
import ora41_PG_model
print('Model imported')

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


def make_transfer_tasks(connector: AConnector, model, output_filename, max_size, chunk_size):
    print('Making tasks')
    task_pattern = '{{"task":"{task}", "table": "{table}", "pk": "{pk}", "size": "{size}", ' \
                   '"full_load": "{full_load}", "start_id": "{start_id}", "limit": "{limit}" }}'

    tasks = []
    def _add_task(_table_class, _size, _full_load, _start_id, _limit):
        task_no = len(tasks) + 1
        _table = _table_class.__tablename__
        pk = list(_table_class.__table__.primary_key)[0]
        task = task_pattern.format(task=task_no, table=_table, pk=pk, size=_size,
                                   full_load=_full_load, start_id=_start_id, limit=_limit)
        tasks.append(task)

    for class_name, tab_class in model.SCHEMA_TABLES.items():
        tablename = tab_class.__tablename__
        size = get_count(connector.con.query(tab_class))
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
                _add_task(tab_class, size, False, start_id, chunk_size)
            _add_task(tab_class, size, False, chunks[-1], None)  # rest records
        else:
            print('Table %s size %s full load' % (tablename, size))
            _add_task(tab_class, size, True, None, None)


    file_text = '[\n' + ',\n'.join([task for task in tasks]) + '\n]'
    with open(output_filename, 'w') as f:
        f.write(file_text)


if __name__ == '__main__':
    src_params = {
        'name': 'ora41',
        'conn': 'oracle://maximo:maximo@192.168.10.41:1521/max75',
        'dbtype': 'ORA'
    }

    src = AConnector(src_params['name'], src_params['conn'], encoding='utf8', echo=False)
    make_transfer_tasks(src, ora41_PG_model, 'ora41_task.json', 300000, 100000)
    # sizes = analyze_tables_sizes(src, SCHEMA_TABLES.values())
    #split_to_tasks(src, T_WORKORDER, 734509, 734508)




