from compare import *
from copy_data import *

def compare_and_copy(con_def_compare, con_def_from, con_def_to,
                     optimal_scan=False,
                     save_json=False,
                     verbose=False,
                     collect_all=False,
                     no_diff=False,
                     no_del=False,
                     axirename=False):
    '''
    Сравнение и перенос таблиц.
    По каждой таблице из файла со списком таблиц делает сначала сравнение, затем перенос данных.
    :param con_def_from: параметры подключения к БД откуда переносить
    :param con_def_to: параметры подключения к БД куда переносить
    :param optimal_scan: поставить False, чтобы выключить оптимизацию и сравнивать базы данных, которые могли меняться
    параллельно, поставить True, если изменения могли вноситься только во вторую базу
    :param save_json: True, если нужно сохранить json файл с айдишниками, используется для проверки правильности
     сравнения, save_json работает медленнее.
    :param verbose: True - создает файл с подробными результатами сравнение.
    :param collect_all: выбрать все идентификаторы второй базы без запуска сравнения.
    :param no_diff: не учитывать измененные записи, в результат сравнения попадают только новые и удаленные записи.
    :param no_del: не учитывать удаленные записи, в результат сравнения попадают только новые и измененные записи.
    при комбинации no_diff=True, no_del=True, в результат сравнения попадают только новые записи.
    :param set_nextval: при переносе записей выполняется вызов следующего значения сиквенса на целевой среде вместо
    переноса идентификаторов.
    :param axirename ***

    '''

    tbldict = get_tbldict()
    report = []
    execute_report = get_report(file_name='execute_report.csv', folder_name=OUT_FOLDER2)
    short_report = get_report('compare_report.csv', folder_name=OUT_FOLDER1)
    completed_tables = list(short_report.keys())
    executed_tables = list(execute_report.keys())

    report = get_compare_result_from_file()
    json_tables = [str(row["table"]).upper() for row in report]

    temp_tbldict = dict(tbldict)

    for tbl_in_file in executed_tables:
        temp_tbldict.pop(tbl_in_file, None)
    with My_Connection(con_def_compare) as conn_compare:
        with My_Connection(con_def_from) as conn_from:
            for tbl_def in temp_tbldict.values():
                table, uidField = tbl_def[0], tbl_def[1]

                if table in execute_report.keys():
                    continue

                tbl_result = dict()
                if table in json_tables:
                    for row in report:
                        if table == row["table"]:
                            tbl_result = row

                if "table" not in tbl_result:

                    if collect_all or tbl_def[4] == 'cleanup':
                        tbl_result = collect_all_id(conn_from, table, uidField, whereclause=tbl_def[3])
                    elif optimal_scan:
                        tbl_result = compareTable(conn_compare, conn_from, table, uidField)

                    else:
                        fieldname = str(tbl_def[2][0])
                        tbl_result = full_compare_table(conn_compare, conn_from, table, uidField,
                                                        fieldname if fieldname != '' else 'ROWSTAMP',
                                                        verbose=verbose, no_diff=no_diff, where=tbl_def[3],
                                                        axirename=axirename
                                                        )
                    if save_json:
                        report.append(tbl_result)
                        save_compare_result(report)
                    if "same" in dict(tbl_result).keys():
                        short_report[table] = [0, 0, 0, 0]
                    else:
                        short_report[table] = [len(tbl_result['miss1']), len(tbl_result['miss2']),
                                               len(tbl_result['diff']), tbl_result['rowstamp'], ]
                    save_report(short_report, file_name='compare_report.csv', folder_name=OUT_FOLDER1)
                    completed_tables.append(table)

                if "same" in dict(tbl_result).keys():
                    execute_report[table] = [0, 0, 0]
                else:

                    with My_Connection(con_def_to) as conn_to:
                        delete_count = 0
                        insert_count = 0

                        if tbl_def[4] == 'cleanup':
                            delete_count += delete_data(tbl_def, conn_to, [])

                        if not no_diff and "diff" in dict(tbl_result).keys() and list(tbl_result["diff"]).__len__():
                            delete_count += delete_data(tbl_def, conn_to, list(tbl_result["diff"]))
                            insert_count += copy_table(tbl_def, conn_from, conn_to, list(tbl_result["diff"]))

                        if not no_del and "miss2" in dict(tbl_result).keys() and list(tbl_result["miss2"]).__len__():
                            delete_count += delete_data(tbl_def, conn_to, tbl_result["miss2"])

                        if "miss1" in dict(tbl_result).keys() and list(tbl_result["miss1"]).__len__():
                            insert_count += copy_table(tbl_def, conn_from, conn_to, tbl_result["miss1"])

                        execute_report[table] = [insert_count, delete_count, 0]
                        add_report({table: [insert_count, delete_count, 0]}, file_name='execute_report.csv',
                                   folder_name=OUT_FOLDER2)

