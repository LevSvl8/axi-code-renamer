from sqlalchemy import text
from sqlalchemy.orm import Query

import csv
import os

table_filter = dict()
MAPPING_FLDR = r'mapping'


def need_create_schema():
    return ("_create_schema" in get_table_filter().keys())


def get_current_table_file():
    with open(MAPPING_FLDR + os.sep + "current_table_file.txt", encoding='UTF-8') as f:
        file_name = f.read()
    return file_name

def get_table_filter(init=False):
    file_name = ''
    global table_filter

    if table_filter.__len__() == 0 or init:
        if not init:
            file_name = get_current_table_file()
        if init or file_name == '':
            file_name = input("Input table csv file name:") + '.csv'
            with open(MAPPING_FLDR + os.sep + "current_table_file.txt", encoding='UTF-8', mode='w') as f:
                f.write(file_name)
        with open(MAPPING_FLDR + os.sep + file_name, encoding='UTF-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if row[0]:
                    table_filter.setdefault((row[0]), [row[0], row[1], row[2]])
    return table_filter


def kpi(q, source_model_tables, source_class):

    kpimain = source_model_tables['T_KPIMAIN']
    kpihistory = source_model_tables['T_KPIHISTORY']
    if source_class.__name__ == 'T_KPIMAIN':
        q = q.filter(kpimain.ISPUBLIC == '1')
    elif source_class.__name__ == 'T_KPIHISTORY':
        q = q.join(kpimain, kpihistory.KPIMAINID == kpimain.KPIMAINID, isouter=True)
        q = q.filter(kpimain.ISPUBLIC == '1')

    #q = q.filter(kpihistory.KPIHISTORYID == '33')
    return q


def view(q, source_model_tables, source_class):

    maxobj = source_model_tables['T_MAXOBJECTCFG']
    maxattr = source_model_tables['T_MAXATTRIBUTECFG']
    if source_class.__name__ == 'T_MAXATTRIBUTECFG':
        q = q.join(maxobj, maxattr.OBJECTNAME == maxobj.OBJECTNAME)
    q = q.filter(maxobj.ISVIEW == '1')
    q = q.filter(maxobj.IMPORTED == '0') #убрать в конечном варианте
    return q


def tbl(q, source_model_tables, source_class):
    maxobj = source_model_tables['T_MAXOBJECTCFG']
    if source_class.__name__ == 'T_MAXATTRIBUTECFG' or source_class.__name__ == 'T_MAXATTRIBUTE':
        q = q.join(maxobj, source_class.OBJECTNAME == maxobj.OBJECTNAME)
    q = q.filter(maxobj.ISVIEW == '0')
    q = q.filter(maxobj.IMPORTED == '0')
    return q


def config(q, source_model_tables, source_class):
    if source_class.__name__ == 'T_MAXATTRIBUTECFG' or source_class.__name__ == 'T_MAXATTRIBUTE':
        q = q.filter(source_class.ATTRIBUTENAME == 'ODK_ISOLATIONFLAG')
        q = q.filter(source_class.OBJECTNAME.in_(('ALNDOMAIN','SYNONYMDOMAIN')))
    return q


def activeservice(q, source_model_tables, source_class):

    if source_class.__name__ == 'T_MAXSERVICE':
        sqltxt = "internal=1 and active=1 AND SERVICENAME!='CUSTAPP'"
    elif source_class.__name__ == 'T_MAXOBJECTCFG' or source_class.__name__ == 'T_MAXOBJECT':
        sqltxt = "internal=1 and SERVICENAME IN (SELECT SERVICENAME FROM MAXSERVICE WHERE active=1) AND SERVICENAME!='CUSTAPP'"
    elif source_class.__name__ == 'T_MAXATTRIBUTECFG' or source_class.__name__ == 'T_MAXATTRIBUTE':
        sqltxt = "USERDEFINED=0 AND OBJECTNAME IN (SELECT OBJECTNAME FROM MAXOBJECT m3 WHERE internal=1 and SERVICENAME IN " \
                 "(SELECT SERVICENAME FROM MAXSERVICE WHERE active=1) AND SERVICENAME!='CUSTAPP')"

    elif source_class.__name__ == 'T_MAXSYSINDEXES':
        sqltxt = "TBNAME IN (SELECT ENTITYNAME FROM MAXOBJECT m3 WHERE internal=1 and SERVICENAME IN " \
                 "(SELECT SERVICENAME FROM MAXSERVICE WHERE active=1) AND SERVICENAME!='CUSTAPP')"
    elif source_class.__name__ == 'T_MAXSYSKEYS':
        sqltxt = "IXNAME IN (select NAME from MAXSYSINDEXES m WHERE TBNAME IN " \
                 "(SELECT ENTITYNAME FROM MAXOBJECT m3 WHERE internal=1 and SERVICENAME IN " \
                 "(SELECT SERVICENAME FROM MAXSERVICE WHERE active=1) AND SERVICENAME!='CUSTAPP'))"
    elif source_class.__name__ == 'T_MAXTABLECFG':
        sqltxt = "TABLENAME IN (SELECT ENTITYNAME FROM MAXOBJECT m3 WHERE internal=1 and SERVICENAME IN " \
                 "(SELECT SERVICENAME FROM MAXSERVICE WHERE active=1) AND SERVICENAME!='CUSTAPP')"
    elif source_class.__name__ == 'T_MAXVIEWCFG' or source_class.__name__ == 'T_MAXVIEWCOLUMNCFG':
        sqltxt = "VIEWNAME IN (SELECT OBJECTNAME FROM MAXOBJECT m3 WHERE internal=1 and SERVICENAME IN " \
                 "(SELECT SERVICENAME FROM MAXSERVICE WHERE active=1) AND SERVICENAME!='CUSTAPP')"

    elif source_class.__name__ == 'T_MAXDOMAIN':
        sqltxt = "exists (select 1 from maximo.MAXATTRIBUTE m WHERE USERDEFINED=0 AND MAXDOMAIN.DOMAINID = m.DOMAINID and " \
                "OBJECTNAME IN (SELECT OBJECTNAME FROM MAXOBJECT m3 WHERE internal=1 AND SERVICENAME IN "\
                "(SELECT SERVICENAME FROM MAXSERVICE WHERE active=1) AND SERVICENAME!='CUSTAPP'))"
    elif source_class.__name__ == 'T_ALNDOMAIN':
        sqltxt = "SITEID IS NULL AND exists (select 1 from maximo.MAXATTRIBUTE m WHERE USERDEFINED=0 AND ALNDOMAIN.DOMAINID = m.DOMAINID and "\
                "OBJECTNAME IN (SELECT OBJECTNAME FROM MAXOBJECT m3 WHERE internal=1 AND SERVICENAME IN " \
                 "(SELECT SERVICENAME FROM MAXSERVICE WHERE active=1) AND SERVICENAME!='CUSTAPP'))"
    elif source_class.__name__ == 'T_SYNONYMDOMAIN':
        sqltxt = "SITEID IS NULL AND exists (select 1 from maximo.MAXATTRIBUTE m WHERE USERDEFINED=0 AND SYNONYMDOMAIN.DOMAINID = m.DOMAINID and " \
        "OBJECTNAME IN (SELECT OBJECTNAME FROM MAXOBJECT m3 WHERE internal=1 AND SERVICENAME IN " \
        "(SELECT SERVICENAME FROM MAXSERVICE WHERE active=1) AND SERVICENAME!='CUSTAPP'))"
    elif source_class.__name__ == 'T_MAXTABLEDOMAIN':
        sqltxt = "SITEID IS NULL AND exists (select 1 from maximo.MAXATTRIBUTE m WHERE USERDEFINED=0 AND MAXTABLEDOMAIN.DOMAINID = m.DOMAINID and " \
                 "OBJECTNAME IN (SELECT OBJECTNAME FROM MAXOBJECT m3 WHERE internal=1 AND SERVICENAME IN " \
                 "(SELECT SERVICENAME FROM MAXSERVICE WHERE active=1) AND SERVICENAME!='CUSTAPP'))"
    elif source_class.__name__ == 'T_NUMERICDOMAIN':
        sqltxt = "SITEID IS NULL AND exists (select 1 from maximo.MAXATTRIBUTE m WHERE USERDEFINED=0 AND NUMERICDOMAIN.DOMAINID = m.DOMAINID and " \
                 "OBJECTNAME IN (SELECT OBJECTNAME FROM MAXOBJECT m3 WHERE internal=1 AND SERVICENAME IN " \
                 "(SELECT SERVICENAME FROM MAXSERVICE WHERE active=1) AND SERVICENAME!='CUSTAPP'))"
    else:
        sqltxt = "1=2"
    q = q.filter(text(sqltxt))
    return q


def axiattr(q, source_model_tables, source_class):
    q = q.filter(text("OBJECTNAME IN (SELECT OBJECTNAME FROM MAXOBJECT m3 WHERE SERVICENAME IN (SELECT SERVICENAME FROM MAXSERVICE WHERE active=1) AND SERVICENAME!='CUSTAPP')"))
    return q


def empty(q, source_model_tables, source_class):
    q = q.filter(text('1=2'))
    return q


functions = {
    'kpi': kpi,
    'view': view,
    'tbl': tbl,
    'activeservice': activeservice,
    'config': config,
    '1=2': empty,
}


def apply_filter(q, source_model_tables, source_class):
    tbl_name = source_class.__tablename__
    table_dict = get_table_filter()
    where = table_dict[tbl_name][1]
    if where:
        return functions[where](q, source_model_tables, source_class)
    else:
        return q

