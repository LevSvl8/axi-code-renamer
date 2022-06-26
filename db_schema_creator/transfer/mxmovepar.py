#from sqlalchemy.orm import make_transient
import os

import datetime

from sqlalchemy import func, Column, text
from sqlalchemy.schema import CreateSchema
from sqlalchemy.exc import DataError, ProgrammingError, DBAPIError
from sqlalchemy.orm import Session
from sqlalchemy import Text, LargeBinary

from sqlalchemy import BigInteger, Date, Integer, SmallInteger, LargeBinary, Time, Unicode, DateTime, Float, \
    LargeBinary, Numeric, String, Text
from sqlalchemy.dialects.oracle.base import RAW

from aconn import AConnector
from transfer.export_filter import apply_filter

from axi_renamer.renamer_starter import Renamer


def __make_dest_entity(source_rec, dest_class):
    result = dest_class()
    j = 0
    for col in dest_class.__table__.columns:
        dest_prop = str(col.key).upper()
        source_prop = dest_prop
        if dest_class.__table_args__['schema'] == 'axioma' and source_rec.__table_args__['schema'] == 'MAXIMO':
            source_prop = Renamer().get_max_val(dest_prop)
        value = getattr(source_rec, source_prop)
        # if col.name == 'rowstamp' or col.type not in (DateTime, Date, Time, LargeBinary, RAW):
        if value is not None:
            try:
                # if prop == 'ROWSTAMP':
                #     value = col.type.python_type(value)
                # # elif value.__class__ is str:
                # #     print('DEBUG> %s str: %s' % (col.name, value))
                # #     # if col.name == 'assetattrid':
                # #     #     print('assetattrid len', len(value))
                # #     #     value = u'Привет'
                # #     # else:
                # #     #     value = u''
                # #
                # #     # value = unicode(value, 'utf-8')
                # #     # print('DECODED: %s' % value)
                # # elif prop == 'RESOURCES':
                # #     print('DEBUG> %s ( %s ) : %s' % (prop, col.type, value))
                # #     print('%s is BLOB: %s, python %s' % (prop, col.type is RAW, col.type.python_type))
                # else:
                if dest_class.__table_args__['schema'] == 'axioma' and source_rec.__table_args__['schema'] == 'MAXIMO':
                    value = Renamer().get_axi_val(value)

                value = col.type.python_type(value)
            except:
                pass

        setattr(result, dest_prop, value)

        # j += 1
        # if j == 3:
        #     break
    return result


def get_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count

def safe_flush(dest_class, objects: list, dest: AConnector):
    key_field_U = str(list(dest_class.__table__.primary_key)[0].name).upper()
    tablename = dest_class.__tablename__

    con = dest.con # type: Session

    commited, failed = [], []

    try:

        con.bulk_save_objects(objects)
        con.commit()
        for obj in objects:
            commited.append(getattr(obj, key_field_U))

    except DBAPIError as e:

        con.rollback()
        dest.status()
        dest.log('ERROR moving packet to table %s. Trying single record copy' % (tablename))
        dest.log('ERROR: %s' % str(e))
        con.expunge_all()

        for obj in objects:
            con.add(obj)
            try:
                con.flush()
                con.commit()
                commited.append(getattr(obj, key_field_U))
            except DBAPIError as e:
                failed.append('%s\t%s' % (getattr(obj, key_field_U), str(e).replace('\n', '\t')))
                dest.log('ERROR: Table %s insert failed. %s = %s' % (tablename, key_field_U, getattr(obj, key_field_U)))
                dest.log('ERROR: %s' % str(e))
                con.rollback()
                con.expunge_all()
    return commited, failed

def create_schema(dest: AConnector, schema_name, dest_model):
    #for class_name, table_class in source_model.SCHEMA_TABLES.items():
    #    if class_name not in dest_model.SCHEMA_TABLES:
    #        raise Exception('Source and destination models composition check fail')
    try:
        dest.engine.execute(CreateSchema(schema_name))
    except ProgrammingError:
        pass
    dest.log('Creating destination schema tables')
    dest_model.Base.metadata.create_all(dest.engine)


def fix_packet_size(dest_class, packet_size):
    BLOB_PACKET_SIZE = 1
    CLOB_DIVIDER = 10

    has_clobs = False
    has_blobs = False

    for col in dest_class.__table__.columns:  # type: Column
        if isinstance(col.type, LargeBinary):
            has_blobs = True
            break
        elif isinstance(col.type, Text):
            has_clobs = True
    if has_blobs:
        return BLOB_PACKET_SIZE
    elif has_clobs:
        return packet_size // CLOB_DIVIDER
    else:
        return packet_size


def copy_records(src: AConnector, dest: AConnector,
                 source_model_tables, dest_model_tables,
                 tablename, full_load=True, cleanup=False,
                 start_id=None, limit=None,
                 full_size: int=0, packet_size: int=1000,
                 task_no=0, journal_dir=None):
    for class_name, source_class in source_model_tables.items():
        if str(source_class.__tablename__).lower() != str(tablename).lower():
            continue
        if dest.schema=='axioma':
            ax_class_name = Renamer().get_axi_val(class_name)
            tablename = Renamer().get_axi_val(tablename)
            dest_class = dest_model_tables[ax_class_name]
        else:
            dest_class = dest_model_tables[class_name]

        if cleanup:
            src.log('Cleanup table %s' % tablename)
            dest.sql('DELETE FROM %s' % tablename)

        src.status('Selecting data from table %s' % tablename)


        objects = []
        fixed_packet_size = fix_packet_size(dest_class, packet_size)
        if packet_size != fixed_packet_size:
            src.log('Table %s packet size fixed to %s' % (tablename, fixed_packet_size))


        q = src.con.query(source_class)
        q = apply_filter(q, source_model_tables, source_class)


        src_count = full_size
        if not full_load:
            pk_col = list(source_class.__table__.primary_key)[0]  # type: Column
            q = q.order_by(pk_col).filter(pk_col >= start_id)
            src_count = '???'
            if limit is not None:
                q = q.limit(limit)
                src_count = limit

        j = fixed_packet_size
        total = 0

        if journal_dir is not None:
            commited_log_name = journal_dir + os.sep + str(task_no) + '_' + tablename + '.ok'
            errors_log_name = journal_dir + os.sep + str(task_no) + '_' + tablename + '.failed'

        def __save_to_journal(_commited, _failed):
            if journal_dir is None:
                return
            if _commited is not None and len(_commited) > 0:
                with open(commited_log_name, 'a') as f:
                    f.write('\n' + '\n'.join([str(s) for s in _commited]))
            if _failed is not None and len(_failed) > 0:
                with open(errors_log_name, 'a') as f:
                    f.write('\n' + '\n'.join([str(s) for s in _failed]))


        for obj in q.yield_per(fixed_packet_size):
            j -= 1
            total += 1
            dest_obj = __make_dest_entity(obj, dest_class)
            objects.append(dest_obj)
            if j <= 0:
                j = fixed_packet_size
                commited, failed = safe_flush(dest_class, objects, dest)
                __save_to_journal(commited, failed)
                dest.status('Table %s copied: %s/%s' % (tablename, total, src_count))
                objects.clear()


        if len(objects) > 0:
            commited, failed = safe_flush(dest_class, objects, dest)
            __save_to_journal(commited, failed)

        dest.status('Table %s done: %s records' % (tablename, total))
        dest.status()
        return total
