from step1 import *
import psycopg2

from connection_params import SRC_PARAMS, DEST_PARAMS


if __name__ == '__main__':
    #file = input("Input table list file name:")+'.csv'
    src_model, dest_model = generate_models(SRC_PARAMS, DEST_PARAMS)
    print('Source model: %s' % src_model)
    print('Destination model: %s' % dest_model)
#step1
    with open('models_params.py', 'w') as f:
        f.write('print("Importing source model %s")\n' % src_model)
        f.write('from models import %s as SRC_MODEL\n' % src_model)
        f.write('print("Importing destination model %s")\n' % dest_model)
        f.write('from models import %s as DEST_MODEL\n' % dest_model)
        print('models_params.py updated')
#step2
    from step2 import *
    src = AConnector(SRC_PARAMS['name'], SRC_PARAMS['conn'], encoding='utf8', schema_name=SRC_PARAMS['name'], echo=False)
    make_transfer_tasks(src, SRC_MODEL, 'tasks\%s_to_%s_all.json' % (SRC_PARAMS['name'], DEST_PARAMS['name']),
                        300000, 100000, skip_audit=False, cleanup=True)
#step3
    from step3 import *
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