import os

from transfer.export_filter import need_create_schema

#os.environ["NLS_LANG"] = "RUSSIAN_RUSSIA.CL8MSWIN1251"
os.environ["NLS_LANG"] = ".UTF8"

# print('Step 3 importing models')
# from models import ora42_test as src_model, db242_test as dest_model
from connection_params import SRC_PARAMS, DEST_PARAMS
from models_params import SRC_MODEL, DEST_MODEL

import ibm_db_sa

from transfer import parmove

if __name__ == '__main__':

    # parmove.batch_move(src_params=SRC_PARAMS, dest_params=DEST_PARAMS,
    #                    src_model=SRC_MODEL, dest_model=DEST_MODEL,
    #                    tasks_list=r'tasks\%s_to_%s_all.json' % (SRC_PARAMS['name'], DEST_PARAMS['name']),
    #                    processes_count=1,
    #                    report_filename=r'logs\%s_to_%s_test.log' % (SRC_PARAMS['name'], DEST_PARAMS['name']),
    #                    journal_dir=r'logs\%s_to_%s.journal' % (SRC_PARAMS['name'], DEST_PARAMS['name']),
    #                    packet_size=1,
    #                    do_create_schema=False
    #                    )

    parmove.batch_move(src_params=SRC_PARAMS, dest_params=DEST_PARAMS,
                       src_model=SRC_MODEL, dest_model=DEST_MODEL,
                       tasks_list=r'tasks\%s_to_%s_all.json' % (SRC_PARAMS['name'], DEST_PARAMS['name']),
                       processes_count=1,
                       report_filename=r'logs\%s_to_%s.log' % (SRC_PARAMS['name'], DEST_PARAMS['name']),
                       journal_dir=r'logs\%s_to_%s.journal' % (SRC_PARAMS['name'], DEST_PARAMS['name']),
                       packet_size=1000,
                       do_create_schema=need_create_schema(),
                       start_from=0,
                       echo=False
                       )