from utils import *
from my_connection import *
from filter_for_data import filter

def fetct_all_as_dict(conn, tableName, uid_field_list, value_field, where, rename=False):
    '''
    Достает таблицу значений для сравнения
    SELECT COMPARING_FIELD, ID FROM TABLE WHERE ...

    Для аудитных таблиц, чтобы оптимизированно сравнивать только по количеству записей для айдишника основной таблицы и
    не учитывать даты, в файле TABLEFILE в столбец comparing_field должно быть прописано COUNT(*), а запрос будет выглядить
    так:
    SELECT COUNT(*), ID FROM TABLE GROUP BY ID
    '''
    if tableName in filter:
        if where:
            where += ' AND (' + filter[tableName] +')'
        else:
            where += filter[tableName]

    select_uid_only = f" SELECT {value_field}, {', '.join(uid_field_list)} from {tableName}"
    if where:
        select_uid_only += f" where {where}"
    elif value_field == 'COUNT(*)':
        select_uid_only += f" group by {', '.join(uid_field_list)}"
    conn.set_select_where(select_uid_only)
    recs = dict()
    rename_map = dict()
    row = conn.fetch_next()
    while row:
        if rename:
            origrow = tuple(row)
            renamed_row = []
            for i in range(len(row)):
                renamed_val = row[i] if not isinstance(row[i], str) else Renamer().get_axi_val(row[i])
                renamed_row.append(renamed_val)
            row = tuple(renamed_row)
            rs = row[0]
            uid = row[1:]
            recs[uid] = rs
            if origrow[1:]!=row[1:]:
                rename_map[uid] = origrow[1:]
        else:
            rs = row[0]
            uid = row[1:]
            recs[uid] = rs

        row = conn.fetch_next()
    return recs, rename_map


def full_compare_table(conn1, conn2, tableName, uid_field_list, comparing_field='ROWSTAMP', verbose=False,
                       no_diff=False, no_del=False, where=None, axirename=False):
    '''
    Полное сравнение двух баз, без оптимизации.
    Сравнивает значения полей сравнения.
    '''
    printlog(f" Full comparing table {tableName}")
    rename = (axirename and conn1.axirename and not conn2.axirename)
    recs1, spam = fetct_all_as_dict(conn1, tableName, uid_field_list, comparing_field, where)
    recs2, renamemap = fetct_all_as_dict(conn2, tableName, uid_field_list, comparing_field, where, rename=rename)
    miss1 = []
    miss2 = []
    diff = []
    verbose_result = []

    for uid, rs in recs1.items():
        if uid not in recs2.keys():
            miss2.append(uid)
            if verbose:
                verbose_rr = list(uid)
                verbose_rr.extend([rs, '', 'miss2'])
                verbose_result.append(verbose_rr)

        elif not no_diff and recs2.get(uid) != rs:
            diff.append(uid)
            if verbose:
                verbose_rr = list(uid)
                verbose_rr.extend([rs, recs2.get(uid), 'diff'])
                verbose_result.append(verbose_rr)

    if not no_del:
        for uid, rs in recs2.items():
            if uid not in recs1.keys():
                if axirename and uid in renamemap:
                    miss1.append(renamemap[uid])
                else:
                    miss1.append(uid)

                if verbose:
                    verbose_rr = list(uid)
                    verbose_rr.extend(['', rs, 'miss1'])
                    verbose_result.append(verbose_rr)

    if verbose:
        save_verbose_report(tableName, uid_field_list, verbose_result)
    if len(miss1) == 0 and len(miss2) == 0 and len(diff) == 0:
        return {
            "table": tableName,
            "same": True
        }
    else:
        return {
            "table": tableName,
            'diff': diff,
            'miss1': miss1,
            'miss2': miss2,
            'rowstamp': 'N',
        }


def compareTable(conn1, conn2, tableName, uidField):
    '''
    Формирование словаря результатов сравнения.
    {
            "table": tableName,
            'diff': list(diff_set),
            'miss1': list(miss_set1),
            'miss2': list(miss_set2),
            'rowstamp': max_rs1,
        }
    Сравнение таблиц двух баз данных с оптимизации по ROWSTAMP:
    Сравнение продолжается только если ROWSTAMP во второй базе больше, чем ROWSTAMP в первой: эта дельта ROWSTAMP и
    определяет новые или измененные записи.
    Затем сравнивается только состав идентификаторов и ищутся удаленные записи.
    '''
    printlog(f" Comparing table {tableName}")

    
    select_max_rs = f" SELECT max(TO_NUMBER(rowstamp)) from {tableName}"
    conn1.set_select_where(select_max_rs)
    max_rs1 = conn1.fetch_next()[0]
    if not max_rs1:
        max_rs1 = 0

    # print(f"{str(datetime.datetime.now())} {select_max_rs} completed")
    select_new_rs = f"SELECT {', '.join(uidField)} from {tableName} where rowstamp>{max_rs1}"
    last_uids = set()

    conn2.set_select_where(select_new_rs)
    row = conn2.fetch_next()
    while row:
        last_uids.add(row)
        row = conn2.fetch_next()

    # print(f"{str(datetime.datetime.now())} {select_new_rs} completed")
    uid_set1 = set()
    uid_set2 = set()

    skip = False
    if max_rs1 == 0:  # нет данных в БД 1
        uid_set2 = last_uids
        skip = True
    elif len(last_uids) == 0:  # нет новых и измененных
        count1 = conn1.get_row_count(tableName)
        count2 = conn2.get_row_count(tableName)     

        if count1 == count2:
            skip=True

    if not skip:
        select_uid_only = f" SELECT {', '.join(uidField)} from {tableName}"

        conn1.set_select_where(select_uid_only)
        row = conn1.fetch_next()
        while row:
            uid_set1.add(row)
            row = conn1.fetch_next()


        conn2.set_select_where(select_uid_only)
        row = conn2.fetch_next()
        while row:
            uid_set2.add(row)
            row = conn2.fetch_next()

        print(f"{str(datetime.datetime.now())} {select_uid_only} completed")


    miss_set1 = uid_set2.difference(uid_set1)
    miss_set2 = uid_set1.difference(uid_set2)
    diff_set = last_uids.difference(miss_set1)

    if len(miss_set1) == 0 and len(miss_set2) == 0 and len(diff_set) == 0:
        return {
            "table": tableName,
            "same": True,
        }
    else:
        return {
            "table": tableName,
            'diff': list(diff_set),
            'miss1': list(miss_set1),
            'miss2': list(miss_set2),
            'rowstamp': max_rs1,
        }


def collect_all_id(connFrom, tableName, uid_field_list, whereclause):
    '''
    Формирование словаря результатов сравнения только исходя их полной загрузи данных.
    Все записи второй базы попадают в список новых записей
    '''
    printlog(f" Collect all id from table {tableName}")
    select_allid = f"SELECT {', '.join(uid_field_list)} from {tableName}"
    if whereclause:
        select_allid += f" where {whereclause}"
    select_allid += f" GROUP BY {', '.join(uid_field_list)}"
    id_list = list()
    connFrom.set_select_where(select_allid)
    row = connFrom.fetch_next()
    while row:
        id_list.append(row)
        row = connFrom.fetch_next()

    return {
        "table": tableName,
        'diff': [],
        'miss1': id_list,
        'miss2': [],
        'rowstamp': 'N',
    }


def compare_fast_count_only(connection_def1, connection_def2):
    '''
    Создание отчета со сравнением количества записей в таблицах одной и второй БД
    '''
    with My_Connection(connection_def1) as conn1:
        with My_Connection(connection_def2) as conn2:

            tbldict = get_tbldict()
            for tbl in tbldict.keys():

                c1 = conn1.get_row_count(tbl)
                c2 = conn2.get_row_count(tbl)
                result = {tbl: [c1, c2, c2-c1]}
                add_report(result, file_name='countreport.csv', folder_name=OUT_FOLDER1)


def compare(connection_def1, connection_def2, optimal_scan=False, save_json=False,
            verbose=False, collect_all=False, no_diff=False, no_del=False, axirename=False):
    '''
    Сравнение таблиц в двух БД по заданным параметрам
    :param connection_def1: первая база, опорный слепок для сравнения
    :param connection_def2: вторая база, актуальная
    :param optimal_scan: поставить False, чтобы выключить оптимизацию и сравнивать базы данных, которые могли меняться
    параллельно, поставить True, если изменения могли вноситься только во вторую базу
    :param save_json: True, если нужно сохранить json файл с айдишниками, используется для проверки правильности
     сравнения, save_json работает медленнее.
    :param verbose: True - создает файл с подробными результатами сравнение.
    :param collect_all: выбрать все идентификаторы второй базы без запуска сравнения.
    :param no_diff: не учитывать измененные записи, в результат сравнения попадают только новые и удаленные записи.
    :param no_del: не учитывать удаленные записи, в результат сравнения попадают только новые и измененные записи.
    при комбинации no_diff=True, no_del=True, в результат сравнения попадают только новые записи.
    :return: словарь сравнения
    {
            "table": tableName,
            'diff': list(diff_set),
            'miss1': list(miss_set1),
            'miss2': list(miss_set2),
            'rowstamp': max_rs1,
        }
    '''

    with My_Connection(connection_def1) as conn1:
        with My_Connection(connection_def2) as conn2:

            tbldict = get_tbldict()
            report = []

            short_report = get_report('compare_report.csv', folder_name=OUT_FOLDER1)
            completed_tables = list(short_report.keys())
            if save_json:
                report = get_compare_result_from_file()
                completed_tables = [str(row["table"]).upper() for row in report]            

            temp_tbldict = dict(tbldict)
            
            for tbl_in_file in completed_tables:
                temp_tbldict.pop(tbl_in_file, None)

            for tbl in temp_tbldict.values():
                table, uidField = tbl[0], tbl[1]

                if table not in completed_tables:
                    if collect_all or tbl[4] == 'cleanup':
                        tbl_result = collect_all_id(conn2, table, uidField, whereclause=tbl[3])
                    elif optimal_scan:
                        tbl_result = compareTable(conn1, conn2, table, uidField)

                    else:
                        fieldname = str(tbl[2][0])
                        tbl_result = full_compare_table(conn1, conn2, table, uidField,
                                                        fieldname if fieldname != '' else 'ROWSTAMP',
                                                        verbose=verbose, no_diff=no_diff, no_del=no_del, where=tbl[3],
                                                        axirename=axirename
                                                        )
                    if save_json:
                        report.append(tbl_result)
                        save_compare_result(report)
                    short_report = dict()
                    if "same" in dict(tbl_result).keys():
                        short_report[table] = [0,0,0,0]
                    else:
                        short_report[table] = [len(tbl_result['miss1']), len(tbl_result['miss2']), len(tbl_result['diff']), tbl_result['rowstamp'],]              
                    add_report(short_report, file_name='compare_report.csv', folder_name=OUT_FOLDER1)
                    completed_tables.append(table)
            
            return report


def compare_files(file_name1, file_name2):
    '''
    Сравнение двух json файлов.
    '''
    c1 = get_compare_result_from_file(file_name=file_name1)
    c2 = get_compare_result_from_file(file_name=file_name2)
    result = []
    for i in range(len(c1)):
        tbl_name = str(c1[i]["table"]).upper()
        if str(c2[i]["table"]).upper()!=tbl_name:
            print('different tables in reports')

        if "same" in dict(c2[i]).keys():
            result.append(c2[i])
            continue
        if "same" in dict(c1[i]).keys():
            result.append(c2[i])
            continue

        diff_set1 = set(tuple(item) for item in c1[i]["diff"])
        miss1_set1 = set(tuple(item) for item in c1[i]["miss1"])
        miss2_set1 = set(tuple(item) for item in c1[i]["miss2"])
        diff_set2 = set(tuple(item) for item in c2[i]["diff"])
        miss1_set2 = set(tuple(item) for item in c2[i]["miss1"])
        miss2_set2 = set(tuple(item) for item in c2[i]["miss2"])

        res_diff = diff_set2.difference(diff_set1)
        res_miss1 = miss1_set2.difference(miss1_set1)
        res_miss2 = miss2_set2.difference(miss2_set1)
        result.append({
            'table': tbl_name,
            'diff': list(res_diff),
            'miss1': list(res_miss1),
            'miss2': list(res_miss2),
            'rowstamp': 0,
        })
        save_compare_result(result)