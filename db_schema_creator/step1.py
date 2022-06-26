from convertor import maxobject

import os
# oracle: select userenv('language') from dual;
from transfer.export_filter import *

os.environ["NLS_LANG"] = "RUSSIAN_RUSSIA.CL8MSWIN1251"

from connection_params import SRC_PARAMS, DEST_PARAMS


def generate_models(src_params, dest_params, generate_src=True, generate_dest=True):
    model1 = ('%s_%s_model' % (src_params['name'], src_params['dbtype'])).lower()
    table_csv = get_table_filter(init=True)
    if generate_src:
        src_model_filename = r'models' + os.sep + model1 + '.py'
        print('Generating %s schema to %s' % (src_params['dbtype'], src_model_filename))
        maxobject.create_schema(src_params['conn'], src_params['dbtype'], src_model_filename, table_csv)

    model2 = (r'%s_%s_model' % (src_params['name'], dest_params['dbtype'])).lower()
    if generate_dest:
        dest_model_filename = r'models' + os.sep +model2 + '.py'
        print('Generating %s schema to %s' % (dest_params['dbtype'], dest_model_filename))
        maxobject.create_schema(src_params['conn'], dest_params['dbtype'], dest_model_filename, table_csv)

    return model1, model2

# def create_step2_script(src_params, dest_params):
#     print('Creating STEP2 file')
#     step2filename = 'step2_' + src_params['name'] + '_to_' + dest_params['name'] + '.py'
#     with open('step2_pattern.py', 'r') as f:
#         pattern = ''.join(f.readlines())
#     result = pattern.format(pattern,
#                             src_model=src_params['model'],
#                             src_name=src_params['name'],
#                             src_conn=src_params['conn'],
#                             src_type=src_params['dbtype'],
#
#                             dest_model=dest_params['model'],
#                             dest_name=dest_params['name'],
#                             dest_conn=dest_params['conn'],
#                             dest_type=dest_params['dbtype']
#                             )
#     with open(step2filename, 'w') as f:
#         f.writelines(result)
#     print('Done!')


if __name__ == '__main__':
    #file = input("Input table list file name:")+'.csv'
    src_model, dest_model = generate_models(SRC_PARAMS, DEST_PARAMS)
    print('Source model: %s' % src_model)
    print('Destination model: %s' % dest_model)

    with open('models_params.py', 'w') as f:
        f.write('print("Importing source model %s")\n' % src_model)
        f.write('from models import %s as SRC_MODEL\n' % src_model)
        f.write('print("Importing destination model %s")\n' % dest_model)
        f.write('from models import %s as DEST_MODEL\n' % dest_model)
        print('models_params.py updated')


    #print("RUSHYDRO! REFPOINTID INTEGER --> BIGINT!!! ")