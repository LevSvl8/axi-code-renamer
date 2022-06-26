from my_connection import *
from axi_renamer.renamer_starter import Renamer
from utils import *
from ast import literal_eval as make_tuple

INSERT = 1
DELETE = 2
UPDATE = 3
SELECTLIMIT = 1000


class Attribute:
    def get_dbtype_from_maxtype(self, maxtype):
        maxtype_dict = {
            'ALN': 'VARCHAR2',
            'AMOUNT': 'NUMBER',
            'BIGINT': 'NUMBER',
            'BLOB': 'BLOB',
            'CLOB': 'CLOB',
            'CRYPTO': 'CRYPTO',
            'CRYPTOX': 'CRYPTOX',
            'DATE': 'DATE',
            'DATETIME': 'DATE',
            'DECIMAL': 'NUMBER',
            'DURATION': 'FLOAT',
            'FLOAT': 'FLOAT',
            'GL': 'VARCHAR2',
            'INTEGER': 'NUMBER',
            'LONGALN': 'VARCHAR2',
            'LOWER': 'VARCHAR2',
            'SMALLINT': 'NUMBER',
            'TIME': 'DATE',
            'UPPER': 'VARCHAR2',
            'YORN': 'NUMBER',
        }
        return maxtype_dict[maxtype]

    def get_placeholder(self):
        placeholders_dict = {
            'VARCHAR2': '%s',
            'NUMBER': '%s',
            'BLOB': '%s',
            'CLOB': '%s',
            'CRYPTO': '%s',
            'CRYPTOX': '%s',
            'DATE': '%d',
            'FLOAT': '%s',
        }
        return placeholders_dict[self.db_data_type]

    def __init__(self, conn, tbl_name, attr_name, maxtype,
                 required=False, default_val=None, force_value=False, domain=None,
                 new_attr_name=None):
        self.conn = conn
        self.tbl_name = tbl_name
        self.attr_name = attr_name
        if new_attr_name:
            self.new_attr_name = new_attr_name
        else:
            self.new_attr_name = attr_name

        # self.maxtype = maxtype
        self.db_data_type = self.get_dbtype_from_maxtype(maxtype)

        self.required = required
        self.default_val = default_val
        self.force_value = force_value
        self.domain = domain

    '''
    Преобразование значения для запросов Insert
    '''
    def f_value(self, value=None):
        if not value and value != 0:
            return None

        if self.db_data_type in ('VARCHAR2', 'CRYPTO', 'CRYPTOX'):
            if isinstance(value, bytes):
                #print(value)
                #val = value.decode('WINDOWS-1251')
                val = value#.decode('cp1252')
            else:
                val = str(value)#.replace("'", "''")
            # f"'{val}'"

        elif self.db_data_type in ('BLOB', 'CLOB'):
            try:
                val = value.read()
            except Exception:
                val = value

        #elif self.dbtype == 'DATE':
        #    return f"TO_DATE('{str(value)}', 'yyyy-mm-dd hh24:mi:ss')"
        else:
            val = value #str(value)

        #переименование
        if self.db_data_type in ('VARCHAR2'):
            if self.conn.axirename:
                val = Renamer().get_axi_val(val)
        return val

    def p_value(self, value=None):
        if not value and value != 0:
            value = self.default_val
            if not value and value != 0:
                return None

        if self.db_data_type in ('VARCHAR2'):
            val = str(value)#.replace("'", "''")
            return f"'{val}'"
            
        elif self.db_data_type == 'DATE':
            return f"TO_TIMESTAMP('{str(value)}', 'yyyy-mm-dd hh24:mi:ss')"
        else:
            return value


def calc_default_value(curr_attr_meta, select_res, attr_list_to):
    return_val = curr_attr_meta.default_val
    if curr_attr_meta.default_val == None and curr_attr_meta.force_value:
        select_statement = f"SELECT SEQUENCENAME FROM MAXSEQUENCE m WHERE TBNAME ='{curr_attr_meta.tbl_name}' " \
                           f"AND NAME ='{curr_attr_meta.attr_name}'"
        curr_attr_meta.conn.set_select_where(select_statement)
        seqname = curr_attr_meta.conn.fetch_next()[0]
        if seqname != None:
            select_nextval = f"SELECT {seqname}.NEXTVAL FROM DUAL"
            curr_attr_meta.conn.set_select_where(select_nextval)
            return_val = curr_attr_meta.conn.fetch_next()[0]
    if curr_attr_meta.default_val == '&AUTOKEY&':
        siteid = ''
        if 'SITEID' in attr_list_to:
            siteid = select_res[attr_list_to.index('SITEID')]
        orgid = ''
        if 'ORGID' in attr_list_to:
            orgid = select_res[attr_list_to.index('ORGID')]

        where_clause = f" WHERE AUTOKEYNAME='{curr_attr_meta.attr_name}' AND "\
                           f"(ORGID IS NULL OR ORGID = '{orgid}') AND (SITEID IS NULL OR SITEID = '{siteid}')"

        select_statement = f'SELECT SEED FROM AUTOKEY' + where_clause
        curr_attr_meta.conn.set_select_where(select_statement)
        return_val = curr_attr_meta.conn.fetch_next()[0]

        upd_statement = f'UPDATE AUTOKEY SET SEED={return_val+1}' + where_clause
        curr_attr_meta.conn.execute(upd_statement)
        curr_attr_meta.conn.commit()

    if curr_attr_meta.default_val == "&PERSONID&" or curr_attr_meta.default_val == "&USERNAME&":
        return_val = 'MAXADMIN'
    if curr_attr_meta.default_val == "&SYSDATE&":
        return_val = datetime.datetime.now()
    if str(curr_attr_meta.default_val).startswith('!'):
        return_val = str(curr_attr_meta.default_val).split('!')[1]
        select_statement = f"SELECT VALUE FROM SYNONYMDOMAIN WHERE " \
                           f"MAXVALUE ='{return_val}' AND DOMAINID ='{curr_attr_meta.domain}' AND DEFAULTS = 1"
        curr_attr_meta.conn.set_select_where(select_statement)
        return_val = curr_attr_meta.conn.fetch_next()[0]

    return return_val


def get_value_list(attributes_meta, select_res, attr_list_to):
    val_list = []

    for i in range(attributes_meta.__len__()):
        if attributes_meta[i].force_value:
            val_list.append(calc_default_value(attributes_meta[i], select_res, attr_list_to))
        elif select_res[i]!=None:
            val_list.append(attributes_meta[i].f_value(select_res[i]))
        else:
            if attributes_meta[i].required:
                calc_def_value = calc_default_value(attributes_meta[i], select_res, attr_list_to)
                if calc_def_value:
                    val_list.append(attributes_meta[i].f_value(calc_def_value))
            else:
                val_list.append(attributes_meta[i].f_value())
    return val_list


def get_multi_id_binding(id_meta, uid, axirename=False):
# для составных ID
    
    id_binding = []
    for i in range(uid.__len__()):
        attr_name = id_meta[i].attr_name
        value = id_meta[i].p_value(uid[i])
        id_binding.append(f'{attr_name} = {value}')
    return id_binding


def get_select_result(tbldef, attr_list, attr_list_to, attributes_meta, id_from_meta, uid_list, conn_from):
    where = ''
    if len(tbldef[1]) == 1:
        id_list = [id_from_meta[0].p_value(x[0]) for x in uid_list]
        where = f" {tbldef[1][0]} IN ({', '.join(map(str, id_list))}) "
    else:
        id_binding = []
        for uid in uid_list:
            id_binding.append(f'{" and ".join(get_multi_id_binding(id_from_meta, uid))}')
        where = f'({") or (".join(id_binding)})'
    select_statement = f" SELECT {', '.join(attr_list)} FROM MAXIMO.{tbldef[0]} WHERE {where}"

    #print(select_statement)
    conn_from.set_select_where(select_statement)
    # select_res = conn1.engine.execute(select_statement).fetchall()
    select_res = list()
    row = conn_from.fetch_next()
    while row:
        val_list1 = tuple(get_value_list(attributes_meta, row, attr_list_to))#список сформированных значений для вставки
        select_res.append(val_list1)  # словарь с ключом=uid
        row = conn_from.fetch_next()
    #print (f'select return {len(select_res)} rows')
    return tuple(select_res)


def get_attributes_from_db(tbl, conn):
    result = {}
    if conn.axirename:
        select_statement = f" select objectname, columnname, axitype, required, defaultvalue, domainid " \
                           f"from AXIOMA.AXIATTRIBUTE where persistent = 1 and objectname ='{tbl}'"
    else:
        select_statement = f" select objectname, columnname, maxtype, required, defaultvalue, domainid " \
                       f"from MAXIMO.MAXATTRIBUTE where persistent = 1 and objectname ='{tbl}'"

    #print(select_statement)

    conn.set_select_where(select_statement)
    row = conn.fetch_next()
    while row:
        if row[0]:
            result.update({
                row[1]: [row[2], row[3], row[4], row[5],],
                #[1]columnname, [2]maxtype, [3]required, [4]defaultvalue, [5]domainid
            })
        row = conn.fetch_next()

    return result


def axi_tbldef(tbldef):
    return make_tuple(Renamer().get_axi_val(str(tbldef)))


def delete_data(in_tbldef, conn, uid_list):
    if conn.axirename:
        tbldef = axi_tbldef(in_tbldef)
    else:
        tbldef = in_tbldef
    printlog(f" Delete data for table {tbldef[0]}")
    result = 0
    if len(uid_list)==0:
        count = conn.get_row_count(tbldef[0])
        if conn.dbtype=='PG':
            sql_statement = f'DELETE FROM {tbldef[0]} '
        else:
            sql_statement = f'TRUNCATE {tbldef[0]} '
        conn.execute(sql_statement)
        conn.commit()
        return count

    attrs_to = get_attributes_from_db(tbldef[0], conn)
    # Сформируем список атрибутов
    attrlist1 = list(dict(attrs_to).keys())

    id_meta = [Attribute(conn=conn, attr_name=a, tbl_name=tbldef[0], maxtype=attrs_to[a][0])
                        for a in tbldef[1]]

    if len(uid_list)>1:
        for uid in uid_list:
            id_binding = get_multi_id_binding(id_meta, uid)
            sql_statement = f'DELETE FROM {tbldef[0]} WHERE {" and ".join(id_binding)} '
            #print(sql_statement)
            conn.execute(sql_statement)
    else:
        limit = SELECTLIMIT
        while uid_list.__len__():
            uid_list_short = uid_list[:limit]
            del uid_list[:limit]

            sql_statement = f'DELETE FROM {tbldef[0]} WHERE {tbldef[1][0]} IN ({", ".join(map(str,uid_list_short[0]))})'
            conn.execute(sql_statement)
    conn.commit()
    return len(uid_list)


def copy_table(in_tbldef, connFrom, connTo, uid_list):
    if connFrom.axirename:
        tbldefFrom = axi_tbldef(in_tbldef)
    else:
        tbldefFrom = in_tbldef

    if connTo.axirename:
        tbldefTo = axi_tbldef(in_tbldef)
    else:
        tbldefTo = in_tbldef

    printlog(f"Copy data from table {tbldefFrom[0]} to table {tbldefTo[0]}")
    result = 0

    # Сформируем список атрибутов целевой базы
    attrs_to = get_attributes_from_db(tbldefTo[0], connTo)
    # attrs_to: columnname:[[0]maxtype, [1]required, [2]defaultvalue, [3]domainid]
    attrlist_to = list(dict(attrs_to).keys())
    # Перемещаем UID на 0 позицию списка. Остальные поля могут идти в произвольном порядке
    uidname = tbldefTo[1][0]
    pos_uid = attrlist_to.index(uidname)
    attrlist_to[pos_uid], attrlist_to[0] = attrlist_to[0], attrlist_to[pos_uid]

    # найдем атрибуты, которые есть только во второй базе
    attrs_from = get_attributes_from_db(tbldefFrom[0], connFrom)
    attrs_from_set = set(list(attrs_from.keys()))
    attrs_to_set = set(list(dict(attrs_to).keys()))
    new_attrs = attrs_to_set.difference(attrs_from_set)

    # для тестирования разных атрибутов
    #new_attrs.add('COMMLOGID')
    ######
    # Список атриботув источника формируется на основе списка атрибутов целевой БД
    attrlist_from = list(attrlist_to)
    #import copy
    #attrs_from = copy.deepcopy(attrs_to)
    # атрибуты, созданные в целевой БД и отсутствующие в исходной, заполняются '' as {new_attr} для обязательных полей
    # или удаляются из списка атрибутов
    for new_attr in new_attrs:
        # если атрибут переименован
        if connTo.axirename and not connFrom.axirename:
            try:
                old_attr = Renamer().get_max_val(new_attr)
            except Exception as err:
                print(f'{new_attr} get_max_val raise an exception')
                raise err
            if old_attr:
                attrlist_from[attrlist_from.index(new_attr)] = f"{old_attr} as {new_attr}"

        elif attrs_to[new_attr][1] == 1: #required
            attrlist_from[attrlist_from.index(new_attr)] = f"'' as {new_attr}"
            #attrs_from[new_attr][0] = f"'' as {new_attr}"
        else:
            attrs_to.__delitem__(new_attr)
            attrlist_to.remove(new_attr)
            attrlist_from.remove(new_attr)
            #attrs_from.__delitem__(new_attr)

    attrs_to_meta = [Attribute(conn=connTo, attr_name=a, tbl_name=tbldefTo[0], maxtype=attrs_to[a][0],
                                  required=attrs_to[a][1], default_val=attrs_to[a][2], domain=attrs_to[a][3],
                                  force_value=(a in tbldefTo[5]))
                        for a in attrlist_to]
    # Сформируем метадату для идентификаторов
    id_to_meta = []
    for i in range(len(tbldefTo[1])):
        id_name = tbldefTo[1][i]
        id_to_meta.extend([x for x in attrs_to_meta if x.attr_name == id_name])

    id_from_meta = [Attribute(conn=connFrom, attr_name=a, tbl_name=tbldefFrom[0], maxtype=attrs_from[a][0])
                        for a in tbldefFrom[1]]

    limit = SELECTLIMIT

    #for db2 prepare Stmt in DB, for PG only form sql string:
    preparedStmt = connTo.prepareStmt(tbldefTo[0], attrlist_to)

    printlog(f" Executing the prepared SQL statement ... ", replace=True)
    #print(f"prepsql: {sqlStatement}")
    while uid_list.__len__():
        try:
            uid_list_short = uid_list[:limit]

            # Выполняем запрос для получения значений из базы 1
            # Create A Tuple Of Data Values
            pmValues = get_select_result(tbldefFrom, attrlist_from, attrlist_to, attrs_to_meta, id_from_meta, uid_list_short, connFrom)
            template = None
            if connTo.dbtype=='PG':
                template = '('+ ', '.join(['%s' for attr_meta in attrs_to_meta]) +')'

            # Execute The SQL Statement Just Prepared
            returnCode = connTo.execute_many(preparedStmt, pmValues, template, page_size=limit)


        except Exception as e:
            connTo.rollback()
            if limit == 1:
                printlog(pmValues)
                raise e
            else:
                try:
                    delete_data(tbldefTo, connTo, uid_list_short)
                except Exception as e:
                    pass
                limit = 1
                continue

        connTo.commit()
        del uid_list[:limit]

        result += returnCode
        printlog(f" Executing the prepared SQL statement ... {result}", replace=True)


    printlog(f" Executing the prepared SQL statement  Done! {result}\n", replace=True)
    return result


def copy(connection_def1, connection_def2, compare_result):

    execute_report = get_report(file_name='execute_report.csv', folder_name=OUT_FOLDER2)

    with My_Connection(connection_def1) as conn1:
        with My_Connection(connection_def2) as conn2:
            for tbl_result in compare_result:

                delete_count = 0
                insert_count = 0

                tbl_name = str(tbl_result["table"]).upper()
                tbldef = get_tbldict()[tbl_name]

                if tbl_name in execute_report.keys():
                    continue
                if "same" in dict(tbl_result).keys():
                    execute_report[tbl_name] = [0, 0, 0]
                    continue

                if tbldef[4] == 'cleanup':
                    delete_data(tbldef, conn2, [])

                if "miss2" in dict(tbl_result).keys() and list(tbl_result["miss2"]).__len__():
                    delete_data(tbldef, conn2, tbl_result["miss2"])

                if "diff" in dict(tbl_result).keys() and list(tbl_result["diff"]).__len__():
                    delete_data(tbldef, conn2, tbl_result["diff"])
                    insert_count += copy_table(tbldef, conn1, conn2, tbl_result["diff"])

                if "miss1" in dict(tbl_result).keys() and list(tbl_result["miss1"]).__len__():
                    insert_count += copy_table(tbldef, conn1, conn2, tbl_result["miss1"])

                execute_report[tbl_name] = [insert_count, delete_count, 0]
                add_report({tbl_name: [insert_count, delete_count, 0]}, file_name='execute_report.csv', folder_name=OUT_FOLDER2)
