import csv
import os
import json
import datetime
import sys

CONFIG_FOLDER = '../axi-data-migration/config/'
MAPPING_FOLDER = '../axi-data-migration/mapping/'
NEVERCOPY_FOLDER = '../axi-data-migration/filter/'
OUT_FOLDER = './out/'
OUT_FOLDER1 = './out1/'
OUT_FOLDER2 = './out2/'

with open(CONFIG_FOLDER + 'oracle_path.txt', encoding='UTF-8') as f:
    ORACLEPATH = str(f.read())

with open(CONFIG_FOLDER + 'properties.txt', encoding='UTF-8') as f:
    reader = csv.reader(f, delimiter=';')
    p={}
    for row in reader:
        if row[1]:
            p.setdefault(row[0], (row[1].split(',')))
    CONN_COMPARE = p["CONN1"]
    CONN_FROM = p["CONN2"]
    CONN_TO = p["CONN3"]
    FUNCS = p["FUNCS"]
    if "TABLEFILE" not in p.keys():
        TFILENAME = 'tables'
    else:
        TFILENAME = p["TABLEFILE"][0]

def get_tbldict(file_name = TFILENAME + '.csv'):
    """
    Получить структуру, определяющую соотношения объекта к его ключевым полям и сиквенсам.
    select tbname, name from maxsequence where tbname in (
    SELECT OBJECTNAME FROM MAXOBJECTCFG m WHERE persistent = 1 and internal = 0)

    имя таблицы; список ее идентификаторов; поле для сравнения; условие where; очищать при загрузке;force_value
    """
    tbldict = dict()
    with open(MAPPING_FOLDER + file_name, encoding='UTF-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row[0] and str.lower(row[0]) != 'objectname':
                tbldict.setdefault(row[0], (row[0],
                                            row[1].split(','),
                                            row[2].split(','),
                                            row[3] if len(row) > 3 else 0,
                                            row[4] if len(row) > 4 else 0,
                                            row[5].split(',') if len(row) > 5 else [None,],
                                            ))
    return tbldict

def save_tbllist(tables, file_name, folder_name=MAPPING_FOLDER):
    path = f"{folder_name}{file_name}"
    with open(path, 'w', encoding='UTF-8') as file:
        file.write(f"objectname;uid_list;comparing_field;where_clause;cleanup;force_value\n")
        for info in tables:
            file.write(f"{';'.join(map(str,info))}\n")

'''
def get_attributes1(file_name='attributes1.csv'):
    """
    Формирует структуру для поиска метаданных атрибутов с группировкой по объектам
    """
    result = dict()
    with open(MAPPING_FOLDER + file_name, encoding='UTF-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row[0]:
                result.setdefault(row[0], dict()).update({
                    row[1]: row[3],
                })
    return result
'''

def get_report(file_name='report.csv', folder_name=OUT_FOLDER, tables_file=TFILENAME):
    """
    Формирует структуру общего отчета объект:[количество insert, delete, update]
    """

    f_path = f"{folder_name}{tables_file}_{file_name}"
    result = dict()
    if not os.path.isfile(f_path):
        with open(f_path, 'w', encoding='UTF-8') as file:
            file.write(f"objectname;insert;delete;update;max(rowstamp)\n")
        return result
    
    with open(f_path, encoding='UTF-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row[0] and str.lower(row[0]) != 'objectname':
                result.setdefault(row.pop(0), row)
                
    return result


def save_report(result={}, file_name='report.csv', folder_name=OUT_FOLDER, tables_file=TFILENAME):
    """
    Сохраняет общее количество сформированных запросов в формате: объект;кол-во insert;кол-во delete;кол-во update
    """
    path = f"{folder_name}{tables_file}_{file_name}"
    with open(path, 'w', encoding='UTF-8') as file:
        file.write(f"objectname;insert;delete;update;max(rowstamp)\n")
        for tbl, info in result.items():
            file.write(f"{tbl};{';'.join(map(str,info))}\n")


def add_report(result={}, file_name='report.csv', folder_name=OUT_FOLDER, tables_file=TFILENAME):
    """
    Сохраняет общее количество сформированных запросов в формате: объект;кол-во insert;кол-во delete;кол-во update
    """
    path = f"{folder_name}{tables_file}_{file_name}"
    with open(path, 'a', encoding='UTF-8') as file:
        for tbl, info in result.items():
            file.write(f"{tbl};{';'.join(map(str,info))}\n")


def save_verbose_report(tableName, uidFields, result, file_name='vcompare.csv', folder_name=OUT_FOLDER):
    """
    Сохраняет подробный отчет о расхождениях в формате: объект;кол-во insert;кол-во delete;кол-во update
    """
    path = f'{folder_name}{tableName}_{file_name}'

    with open(path, 'w', encoding='UTF-8') as file:
        file.write(f"{';'.join(map(str, uidFields))};SOURCE;TARGET;DIFF_TYPE\n")
        for info in result:
            file.write(f"{';'.join(map(str,info))}\n")

def get_attributes2(file_name='attributes2.csv'):
    """
    Формирует структуру для поиска метаданных атрибутов с группировкой по объектам
    Только обязательные для заполнения атрибуты, которых нет в первой базе.
    Результат запроса select objectname, attributename, maxtype, required, defaultvalue from MAXATTRIBUTE
    where persistent = 1 and required = 1 and objectname in (список таблиц)
    
    0               1           2           3       4
    objectname:[{attributename:[maxtype, required, defaultvalue]},]
    """
    result = dict()
    with open(MAPPING_FOLDER + file_name, encoding='UTF-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row[0]:
                result.setdefault(row[0], dict()).update({
                    row[1]: [row[2], row[3], row[4]]
                })
    return result

'''
def get_selectresult_from_file(file_name='selectresult.csv'):
    """
    для тестирования результат селекта для переноса данных
    """
    res = []
    with open(MAPPING_FOLDER + file_name, encoding='UTF-8') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            if row[0]:
                res.append([row[i] for i in range (row.__len__())])
    return res
'''

def get_compare_result_from_file(file_name='compare_result.json', folder_name=OUT_FOLDER1, tables_file=TFILENAME):
    report = []
    path = f"{folder_name}{tables_file}_{file_name}"
    if not os.path.isfile(path):
        return report
    with open(path, "r") as f:
        try:
            report = json.load(f)
            
        except Exception:
            print(Exception)
    return report


def save_compare_result(compare_result, file_name='compare_result.json', folder_name=OUT_FOLDER1, tables_file=TFILENAME):
    fpath = f"{folder_name}{tables_file}_{file_name}"
    with open(fpath, "w") as f:
        f.write(json.dumps(compare_result, indent=2))


def printlog(text, replace=False):
    if replace:
        sys.stdout.write("\r{0}> {1}                                                                                 ".format(
            datetime.datetime.now().strftime("%H:%M:%S"), text, end=''))
    else:
        print("{0}> {1}                                                                                 ".format(
            datetime.datetime.now().strftime("%H:%M:%S"), text, end=''))


def get_never_copy_list(filename):
    rows = []
    with open(os.path.join(NEVERCOPY_FOLDER, filename)) as csv_file:
        csv_reader = csv_file.read()
        rows = csv_reader.split('\n')
    return rows