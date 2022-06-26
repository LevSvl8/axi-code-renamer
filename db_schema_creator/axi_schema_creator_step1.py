from axi_code_renamer.folder_handler import FolderHandler

from step1 import *
from aconn import AConnector
from connection_params import SRC_PARAMS, DEST_PARAMS

from transfer.mxmovepar import create_schema

if __name__ == '__main__':
    # step1

    #file = input("Input table list file name:")+'.csv'
    src_model, dest_model = generate_models(SRC_PARAMS, DEST_PARAMS)
    print('Source model: %s' % src_model)
    print('Destination model: %s' % dest_model)

    # rename
    in_folder = r'models'
    out_folder = r'models'
    valid_suffixes = ['.py',]
    process_files = [dest_model]
    r = FolderHandler(in_folder, out_folder, rename=True,
                             process_files=process_files,
                             valid_suffixes=valid_suffixes,
           target='DB_SCHEMA')
    r.simple_replace()

    dest_model = r.renamer.get_axi_val(dest_model)

    with open('models_params.py', 'w') as f:
        f.write('print("Importing source model %s")\n' % src_model)
        f.write('from models import %s as SRC_MODEL\n' % src_model)
        f.write('print("Importing destination model %s")\n' % dest_model)
        f.write('from models import %s as DEST_MODEL\n' % dest_model)
        print('models_params.py updated')

    # импортируем не вначале скрипта, а только после актуализации файла!!!
    from models_params import DEST_MODEL

    # create_schema
    dest_params = DEST_PARAMS
    dest = AConnector(dest_params['name'], dest_params['conn'], schema_name='axioma', echo=False, encoding='utf8')

    print('Creating schema.')
    create_schema(dest, schema_name='axioma', dest_model=DEST_MODEL)

    del dest  # close connection
    # return