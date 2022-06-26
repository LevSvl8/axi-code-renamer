#from sqlalchemy.orm import make_transient
from sqlalchemy import func
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

from aconn import AConnector

def __make_dest_entity(source_rec, dest_class):
    result = dest_class()
    for col in dest_class.__table__.columns:
        prop = str(col.key).upper()
        value = getattr(source_rec, prop)
        if col.name == 'rowstamp':
            value = col.type.python_type(value)
        setattr(result, prop, value)
    return result

def __get_value(dest_obj, fieldname):
    colname = str(fieldname).upper()
    for col in dest_obj.__table__.columns:
        prop = str(col.key).upper()
        if prop == colname:
            return getattr(dest_obj, prop)


def get_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count

import time

def safe_flush(dest_class, objects: list, dest: AConnector):
    # prop = str(col.key).upper()
    # value = getattr(source_rec, prop)
    # setattr(result, prop, value)
    key_field = list(dest_class.__table__.primary_key)[0].name
    tablename = dest_class.__tablename__

    con = dest.con # type: Session

    try:

        start_time = time.time()
        con.bulk_save_objects(objects)
        con.commit()
        print("--- %s seconds ---" % (time.time() - start_time))
    except DataError:
        con.rollback()
        dest.status()
        dest.log('ERROR moving packet to table %s. Trying single record copy' % tablename)

        con.expunge_all()

        for obj in objects:
            con.add(obj)
            try:
                con.flush()
                con.commit()
            except DataError:
                dest.log('ERROR: Table %s insert failed. %s = %s' % (tablename, key_field, __get_value(obj, key_field)))
                con.rollback()
                con.expunge_all()

def create_schema(dest: AConnector, source_model, dest_model):
    for class_name, table_class in source_model.SCHEMA_TABLES.items():
        if class_name not in dest_model.SCHEMA_TABLES:
            raise Exception('Source and destination models composition check fail')

    dest.log('Creating destination schema')
    dest_model.Base.metadata.create_all(dest.engine)


def copy_records(src: AConnector, dest: AConnector,
                 source_model, dest_model,
                 packet_size: int=100,
                 only_tables=None):
    # for class_name, table_class in source_model.SCHEMA_TABLES.items():
    #     if class_name not in dest_model.SCHEMA_TABLES:
    #         raise Exception('Source and destination models composition check fail')
    #
    # dest.log('Creating destination schema')
    #
    # dest_model.Base.metadata.create_all(dest.engine)

    tabs_count, tabs_processed = len(source_model.SCHEMA_TABLES), 0
    for class_name, source_class in source_model.SCHEMA_TABLES.items():
        tablename = source_class.__tablename__
        tabs_processed += 1

        if only_tables is not None:
            if (isinstance(only_tables, list) and tablename not in only_tables) \
                    or (isinstance(only_tables, str) and tablename != only_tables):
                continue

        dest_class = dest_model.SCHEMA_TABLES[class_name]

        total = 0
        j = packet_size

        # check counts

        dest.status('Calculating table %s' % tablename)
        src_count = get_count(src.con.query(source_class))
        dest_count = get_count(dest.con.query(dest_class))

        if src_count == dest_count:
            dest.status('[%s/%s] Table %s skip - same count (%s records)' %
                        (tabs_processed, tabs_count, tablename, src_count))
            src.status()
            continue

        dest.status('Cleaning table %s' % tablename)
        removed = dest.con.query(dest_class).delete()
        if removed is not None and removed > 0:
            dest.status()
            dest.log('Removed %s records from table %s' % (removed, tablename))
            dest.con.commit()

        src.status('Selecting data from table %s' % tablename)

        objects = []

        start_time = time.time()
        fetch_time = 0
        make_time = 0
        flush_time = 0

        fetch_start = time.time()
        for obj in src.con.query(source_class).yield_per(packet_size):

            fetch_time += time.time() - fetch_start
            j -= 1
            total += 1

            make_start = time.time()
            dest_obj = __make_dest_entity(obj, dest_class)
            make_time += time.time() - make_start
            objects.append(dest_obj)
            if j <= 0:
                j = packet_size
                flush_start = time.time()
                safe_flush(dest_class, objects, dest)
                flush_time += time.time() - flush_start
                dest.status('[%s/%s] Table %s copied: %s/%s' % (tabs_processed, tabs_count, tablename, total, src_count))

                print("\n--- fetch/make/flush/total %s / %s / %s / %s seconds ---\n" %
                      (fetch_time, make_time, flush_time, time.time() - start_time))
                start_time = time.time()

                fetch_time = 0
                make_time = 0
                flush_time = 0

                objects.clear()
            fetch_start = time.time()

        if len(objects) > 0:
            safe_flush(dest_class, objects, dest)
        dest.status('[%s/%s] Table %s done (%s records)' % (tabs_processed, tabs_count, tablename, total))
        dest.status()
