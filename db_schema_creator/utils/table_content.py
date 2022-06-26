import decimal
import os
os.environ["NLS_LANG"] = "RUSSIAN_RUSSIA.CL8MSWIN1251"


from aconn import AConnector

from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from xml.etree import ElementTree as ET


#import model1, model2


def download_table_as_xml(conn: AConnector, table_class, pretty=True, encoding="utf-8"):

    data = []

    for rec in conn.query(table_class).all():
        result = {}
        for col in table_class.__table__.columns:
            prop = str(col.key).upper()
            value = getattr(rec, prop)
            result[col.name] = value
        data.append(result)

    xml = parseString(dicttoxml(data, cdata=False))
    if not pretty:
        return xml.toxml(encoding=encoding)
    else:
        return xml.toprettyxml(encoding=encoding)

def xml_to_alchemy_objects(xml_text: str, table_class):
    tag_to_prop = {str(col.name): str(col.key).upper() for col in table_class.__table__.columns}

    root = ET.fromstring(xml_text)
    objects = []
    for rec in root:
        obj = table_class()
        objects.append(obj)
        for field in rec:
            prop = tag_to_prop[field.tag]
            typ = field.attrib['type']

            val = field.text
            if typ == 'number':

                 val = int(val)
            # elif typ == 'null':
            #     val = None
            # else:
            #     val = val

            setattr(obj, prop, val)
            # if field.tag == 'viewwhere':
            #     print(field.text)
            # print(field.tag, field.attrib['type'], field.text)
        #exit()

    return objects

def export_table(conn: AConnector, table_class, filename: str, pretty=True, utf8=True):
    if utf8:
        encoding = 'utf-8'
        mode = 'wb'
    else:
        encoding = None
        mode = 'w'

    xml_text = download_table_as_xml(conn, table_class, pretty=pretty, encoding=encoding)
    with open(filename, mode) as f:
        f.write(xml_text)
    conn.log('Table %s exported to %s' % (table_class.__tablename__, filename))

def import_table(conn: AConnector, table_class, filename: str, delete_existing_data=True, binary=False):
    if binary:
        mode = 'rb'
    else:
        mode = 'r'
    with open(filename, mode) as f: # , encoding="utf-8"
        data = f.read()

    objects = xml_to_alchemy_objects(data, table_class)
    table_class.__table__.create(bind=conn.engine, checkfirst=True)
    if delete_existing_data:
        conn.sql('delete from %s' % table_class.__tablename__)
    conn.con.bulk_save_objects(objects)
    conn.con.commit()

    conn.log('Import to table %s done. %s records imported' % (table_class.__tablename__, len(objects)))


def start():
    pass
    print('Imporing models')
    import models.hydro_ora_db2_model as m1
    #
    # print('Transfering')
    #
    # tables = [m1.T_MAXPROPVALUE]
    # m1.T_MAXVIEW, m1.T_MAXVIEWCFG,  m1.T_KPIMAIN,
    #           m1.T_QUERY, m1.T_CONDITION, m1.T_MAXRELATIONSHIP, m1.T_MAXTABLEDOMAIN,
    #           m1.T_WFCONDITION, m1.T_MAXDYNAMICDOMLINK]

    conn = AConnector('42', 'oracle://maximo:maximo@192.168.10.42:1521/ctginst1')
    #conn = AConnector('47', 'db2://maximo:Passw0rd@192.168.10.47:50005/maxdb76', encoding='utf-8')

    export_table(conn, m1.T_MAXRELATIONSHIP, 'maxrelationship_42.xml')

 #   import_table(conn, tables[0], 'maxpropvalue_47.xml', delete_existing_data=True, binary=True)

    #import_table(conn1, m1.T_ESCALATION, 'maxpropvalue_42_ora.xml', delete_existing_data=False, binary=True)

    # conn2 = AConnector('47', 'db2://maximo:Passw0rd@192.168.10.47:50005/maxdb76')
    # for tab_cls in tables:
    #      tab2_cls = m2.SCHEMA_TABLES[tab_cls.__name__]
    #      import_table(conn2, tab_cls, '%s_%s.xml' % (tab2_cls.__tablename__, conn1.name), delete_existing_data=True, binary=False)
    #
    # print('Done!')

if __name__ == '__main__':
    start()
