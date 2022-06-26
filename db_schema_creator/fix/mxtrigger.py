# coding: utf-8
from aconn import AConnector

from axi_renamer.renamer_starter import Renamer


def check_trigger_posible(src: AConnector, dest: AConnector):
    trigger_statements = []

    src.log('Extracting triggers')

    trigroot_sql = 'select tablename, trigroot ' \
                   'from maxtable t join maxobject o on t.tablename = o.objectname ' \
                   'where o.persistent = 1 and o.isview = 0 order by tablename'

    trig_list = list(src.sql(trigroot_sql).fetchall())
    for tablename, trigroot_fld in trig_list:
        try:
            tablename = Renamer().get_axi_val(str(tablename))
            sql = 'select rowstamp from %s' % tablename
            r = dest.sql(sql).fetchone()
            print('Table %s ok' % tablename)
        except:
            print('ERROR:>>>>>>  Table %s rowstamp not exist' % tablename)


def copy_maximo_triggers(src: AConnector, dest: AConnector, db_type):
    trigger_statements = []

    src.log('Extracting triggers')

    trigroot_sql = 'select tablename, trigroot ' \
                   'from maxtable t join maxobject o on t.tablename = o.objectname ' \
                   'where o.persistent = 1 and o.isview = 0 order by tablename'

    trig_list = list(src.sql(trigroot_sql).fetchall())

    for tablename, trigroot_fld in trig_list:
        tab_name = Renamer().get_axi_val(str(tablename).upper())

        if trigroot_fld is None or trigroot_fld == '':
            trigroot = tab_name.lower()
        else:
            trigroot = trigroot_fld.lower()

        trigroot = Renamer().get_axi_val(trigroot)

        if db_type not in ('PG', 'DB2'):
            raise Exception('TODO!!!')

        if db_type == 'PG':
            MAX_NAME_LENGTH = 30
            noUnderscore = len(trigroot) >= MAX_NAME_LENGTH - 1
            if noUnderscore:
                trig_name = trigroot + "t "
            else:
                trig_name = trigroot + "_t "
            sql = "CREATE TRIGGER " + trig_name + \
                  " BEFORE INSERT OR UPDATE " + \
                  " ON " + tab_name.lower() + \
                  " FOR EACH ROW EXECUTE PROCEDURE tf_rowstamp()"
            trigger_statements.append(sql)
        elif db_type == 'DB2':
            noUnderscore = len(trigroot) >= 17
            if not noUnderscore:
                trigroot = trigroot + "_"

            sql = "CREATE TRIGGER {trigname}T NO CASCADE BEFORE INSERT ON {tabname} " \
                  "REFERENCING NEW AS N FOR EACH ROW MODE DB2SQL " \
                  "SET N.ROWSTAMP = NEXTVAL FOR MAXSEQ".format(trigname=trigroot.upper(), tabname=tab_name.upper())
            trigger_statements.append(sql)
            sql = sql.replace("T NO CASCADE BEFORE INSERT", "U NO CASCADE BEFORE UPDATE")
            trigger_statements.append(sql)

    dest.log('Creating triggers')
    # sql = ';'.join(trigger_statements)
    # for s in trigger_statements:
    #     print(s)
    for sql in trigger_statements:
        try:
            dest.engine.execute(sql)
        except Exception as e:
            print(str(e))
    dest.log('Done!')


def repair_index_names(dest: AConnector):

    broken = [str(row[0]) for row in dest.sql('select name from maxsysindexes where tbname = name').fetchall()]
    for ix in broken:
        ixnew = ix+'_ZQ'
        dest.sql("update maxsyskeys set ixname = '{ixnew}' where ixname = '{ixold}'".format(ixnew=ixnew, ixold=ix))
        dest.sql("update maxsysindexes set name = '{ixnew}' where name = '{ixold}'".format(ixnew=ixnew, ixold=ix))
    dest.log('Index repair done: ' + str(broken))

#
#
# def start():
#     db_src = AConnector('src', 'postgresql://maximo:maximo@192.168.11.77/MAX1')
#     db_dest = AConnector('dest', 'postgresql://maximo:maximo@192.168.11.77/MAX2')
#
#     copy_maximo_triggers(db_src, db_dest, 'PG')
#     repair_index_names(db_dest)
#
