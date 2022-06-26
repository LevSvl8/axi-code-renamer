from my_connection import My_Connection
from utils import *


def create_tbllist(connection_def1):
    prefix = input("Input prefix of collecting tables:")
    spam = ''
    while spam != 'Y':
        file_name = input("Input name of creating file:") + '.csv'
        if os.path.isfile(MAPPING_FOLDER + file_name):
            spam = input(
                f"File {file_name} is already exists in folder {MAPPING_FOLDER}. Do you want to overwhrite it? (Y/N)")
        else:
            spam = 'Y'

    cleanup = input("Do you want to add cleanup function (for full data migration)? (Y/N)")

    if os.path.isfile(MAPPING_FOLDER + file_name):
        os.remove(MAPPING_FOLDER + file_name)
    tables = []
    with My_Connection(connection_def1) as conn1:
        select_objects = f"select tbname, name from maxsequence where tbname in " \
                         f"(SELECT objectname from maxobject where isview=0 and persistent = 1 and objectname like '{prefix}%')"
        conn1.set_select_where(select_objects)
        row = conn1.fetch_next()
        while row:
            l = list(row)
            if cleanup == 'Y':
                l.extend(['', '', 'cleanup', ''])
            else:
                l.extend(['', '', '', ''])
            tables.append(l)
            row = conn1.fetch_next()

    save_tbllist(tables, file_name)

    print(f"File {file_name} successfully created in folder {MAPPING_FOLDER}.")
