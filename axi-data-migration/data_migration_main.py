from create_tbllist import create_tbllist
from check_data import *
from compare_and_copy import *
from utils import *


if __name__ == '__main__':
    '''
    Описание возможный функций, задаваемых в файле property.txt
    "COMPARE" - функция сравнения значений таблиц в двух БД
        
        Дополнительные параметры "COMPARE":
        "FAST_COUNT_ONLY" - создает отчет со сравнением количества записей междя двумя БД
        "OPTIMAL" - для определения дельты межды разными временными слепками одной БД, оптимизирован сравнивать по 
        растущему ROWSTAMP
        "SAVE_JSON" - сохраняет json файл с результатами сравнения (идентификаторами), используется для проверки 
        правильности сравнения, save_json работает медленнее.
        "VERBOSE
        " - сохраняет подробный отчет по различию значений заданного для сравнения поля
        "NO_DIFF" - не учитывает измененные записи, в результат сравнения попадают только новые и удаленные записи.
        "NO_DEL" - не учитывает удаленные записи, в результат сравнения попадают только новые и измененные записи.
        при комбинации "NO_DIFF,NO_DEL" в результат сравнения попадают только новые записи.
        "AXIRENAME" - переименование при миграции из maximo в axioma
        
    "EXE" - исполнение переноса данных по результатам сравнения. Применяется только вместе с функцией "COMPARE"
         
    "COPYALL" - функция загрузки всех данный из одной БД в другую.
        Дополнительные параметры:
        "SAVE_JSON" - сохраняет json файл с выборкой всех идентификаторов.
    
     
    "FIX" - функция сравнения файлов результатов сравнения. Используется при анализе ошибок загрузки данных.
    
    "TABLELIST" - функция создания csv файла со списком таблиц с указанным префиксом
    
    "CHECK_DOMAIN" - функция проверки вхождения значений в полях таблиц в привязанные к ним домены
        "REPAIR" - исправление найденных ошибок
    '''
    os.environ["PATH"] = ORACLEPATH + os.environ["PATH"]
    if "COMPARE" in FUNCS:
        if "FAST_COUNT_ONLY" in FUNCS:
            compare_fast_count_only(CONN_COMPARE, CONN_FROM)

        elif "EXE" in FUNCS:
            compare_and_copy(CONN_COMPARE, CONN_FROM, CONN_TO,
                             optimal_scan=("OPTIMAL" in FUNCS),
                             save_json=("SAVE_JSON" in FUNCS),
                             verbose=("VERBOSE" in FUNCS),
                             no_diff=("NO_DIFF" in FUNCS),
                             no_del=("NO_DEL" in FUNCS),
                             axirename=("AXIRENAME" in FUNCS),
                             )
        else:
            compare_result = compare(CONN_COMPARE, CONN_FROM,
                             optimal_scan=("OPTIMAL" in FUNCS),
                             save_json=("SAVE_JSON" in FUNCS),
                             verbose=("VERBOSE" in FUNCS),
                             no_diff=("NO_DIFF" in FUNCS),
                             axirename=("AXIRENAME" in FUNCS),
                             no_del=("NO_DEL" in FUNCS)

                                     )

    if "COPYALL" in FUNCS:
        compare_and_copy(CONN_FROM, CONN_FROM, CONN_TO, save_json=("SAVE_JSON" in FUNCS), collect_all=True)

    if "FIX" in FUNCS:
        compare_files('compare_result1.json', 'compare_result2.json')

    if "TABLELIST" in FUNCS:
        create_tbllist(CONN_FROM)

    if "CHECK_DOMAIN" in FUNCS:
        check_domain(CONN_TO, "REPAIR" in FUNCS)

    exit()
