from aconn import AConnector
from connection_params import SRC_PARAMS, DEST_PARAMS
from transfer.export_filter import *
from models_params import SRC_MODEL, DEST_MODEL

REPORT_FLDR = 'report'

if __name__ == '__main__':
    table_dict = get_table_filter()
    report = []
    src = AConnector('counter$' + SRC_PARAMS['name'], SRC_PARAMS['conn'],
                     encoding=SRC_PARAMS['encoding'], schema_name=SRC_PARAMS['name'], echo=False)
    dest = AConnector('counter$' + DEST_PARAMS['name'], DEST_PARAMS['conn'],
                      encoding=DEST_PARAMS['encoding'], schema_name=DEST_PARAMS['name'], echo=False)  # , convert_unicode=True
    for class_name, source_class in SRC_MODEL.SCHEMA_TABLES.items():
        src_count = src.con.query(source_class).count()
        dest_count = dest.con.query(source_class).count()
        report.append([source_class.__tablename__, src_count, dest_count])
    file_name = 'count_rep_' + get_current_table_file()
    with open(REPORT_FLDR + os.sep + file_name, mode='w') as f:
        for row in report:
            f.write(';'.join(map(str, row))+"\n")