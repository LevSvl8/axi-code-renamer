from my_connection import My_Connection
from utils import *
from collections import namedtuple


def check_domain(connection_def1, repair):
    with My_Connection(connection_def1) as conn1:
        select_attrs = f"select objectname, attributename, a.domainid, s.maxvalue from axiattribute a, axidomain d, synonymdomain s " \
                       f"where a.domainid is not null and a.domainid =d.domainid and s.value = d.domaintype " \
                       f"and s.domainid = 'DOMTYPE' and persistent = 1"
        print(select_attrs)
        conn1.set_select_where(select_attrs)
        row = conn1.fetch_next()
        Attr = namedtuple('Attr', 'objectname attributename domainid domaintype')
        attr_def_lst = []
        while row:
            attr_def = Attr(row[0], row[1], row[2], row[3])
            attr_def_lst.append(attr_def)
            row = conn1.fetch_next()
        error_list = []
        for attr_def in attr_def_lst:
            if attr_def.domaintype == 'AXITABLE' or attr_def.domaintype == 'CROSSOVER':
                continue
            domaintbl = attr_def.domaintype + 'DOMAIN'
            select = f"select distinct({attr_def.attributename}) from {attr_def.objectname} a where {attr_def.attributename} not in " \
                     f"(select value from {domaintbl} s where domainid = '{attr_def.domainid}')"
            print(select)
            conn1.set_select_where(select)
            row = conn1.fetch_next()
            if row:
                error_list.append(attr_def)
                if repair:
                    if domaintbl == 'SYNONYMDOMAIN':
                        update = f"update {attr_def.objectname} set {attr_def.attributename} = (select value from synonymdomain s " \
                                 f"where domainid = '{attr_def.domainid}' and maxvalue = {attr_def.attributename}) " \
                                 f"where {attr_def.attributename} not in (select value from {domaintbl} s where domainid = '{attr_def.domainid}')"
                        print(update)
                        conn1.execute(update)
                        conn1.commit()

    save_tbllist(error_list, file_name='check_domain_report.csv', folder_name=OUT_FOLDER)
