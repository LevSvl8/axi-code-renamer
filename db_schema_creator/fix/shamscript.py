
SHMAX_SCRIPTS = """CREATE EXTENSION intarray
    SCHEMA maximo
    VERSION "1.2";

CREATE FUNCTION maximo.tf_rowstamp()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF 
AS $BODY$

DECLARE NEXTVAL numeric; BEGIN SELECT nextval('maxseq') INTO NEXTVAL; NEW.ROWSTAMP := NEXTVAL; RETURN NEW;
END

$BODY$;

ALTER FUNCTION maximo.tf_rowstamp()
    OWNER TO maximo;

CREATE OR REPLACE VIEW maximo.fs_index1 AS
 SELECT n.nspname AS namespace,
    t.relname AS tablename,
    i.relname AS indexname,
    icount(ix.indkey::integer[]) AS colcount,
    a.attname AS colname,
    idx(ix.indkey::integer[], a.attnum::integer) AS colseq,
    ix.indisunique AS isunique,
    ix.indisclustered AS isclustered,
    (ix.indoption[idx(ix.indkey::integer[], a.attnum::integer) - 1]::integer & 1) = 1 AS coldesc,
    a.attnum AS indexcolkey,
    ix.indkey AS indexkeys,
    ix.indoption AS indexoptions
   FROM pg_class t
     JOIN pg_index ix ON t.oid = ix.indrelid
     JOIN pg_class i ON i.oid = ix.indexrelid
     LEFT JOIN pg_namespace n ON i.relnamespace = n.oid
     JOIN pg_attribute a ON a.attrelid = t.oid
  WHERE (a.attnum = ANY (ix.indkey::smallint[])) AND t.relkind = 'r'::"char";

ALTER TABLE maximo.fs_index1
    OWNER TO maximo;
"""

DROP_ALL_INDEXES = '''CREATE OR REPLACE FUNCTION drop_all_indexes() RETURNS INTEGER AS $$
DECLARE
  i RECORD;
BEGIN
  FOR i IN 
    (SELECT relname FROM pg_class
       -- exclude all pkey, exclude system catalog which starts with 'pg_'
      WHERE relkind = 'i' AND relname NOT LIKE '%_pkey%' AND relname NOT LIKE 'pg_%')
  LOOP
    -- RAISE INFO 'DROPING INDEX: %', i.relname;
    EXECUTE 'DROP INDEX ' || i.relname;
  END LOOP;
RETURN 1;
END;
$$ LANGUAGE plpgsql;'''


PREPAIR_FOR_DBCONFIG = '''update maxobjectcfg set changed = 'M' 
  where objectname not in (select viewname from maxview) 
  and objectname not in ('MAXATTRIBUTE', 'MAXATTRIBUTECFG', 'MAXOBJECT', 'MAXOBJECTCFG', 
  'MAXTABLE', 'MAXTABLECFG', 'MAXPROP', 'MAXPROPVALUE')
'''

DBCONFIG_UPDATE_INDEXES = '''update maxsysindexes set changed = 'Y' '''

DBCONFIG_CREATE_VIEWS = '''update maxobjectcfg set changed = 'M' where objectname in (select viewname from maxview)'''


FIX_MAX_PROPS = \
'''update maxpropvalue set propvalue = 'UPPER' where propname = 'mxe.db.format.upper';
update maxpropvalue set propvalue = 'TYPE_FORWARD_ONLY' where propname = 'mxe.db.format.resultsettype';
update maxpropvalue set propvalue = 'coalesce' where propname = 'mxe.db.format.nullvalue';
update maxpropvalue set propvalue = 'LOCALTIMESTAMP' where propname = 'mxe.db.systemdateformat';
update maxpropvalue set propvalue = 'to_timestamp' where propname = 'mxe.db.format.date';
update maxpropvalue set propvalue = 'to_timestamp' where propname = 'mxe.db.format.time';
update maxpropvalue set propvalue = 'to_timestamp' where propname = 'mxe.db.format.timestamp';
'''




'''
select * from maxview where 
	lower(viewwhere) like '%dual%' 
	or lower(viewwhere) like '%nvl%' 
	or lower(viewwhere) like '%connect by%' 
	or lower(viewwhere) like '%decode%'
	or lower(viewwhere) like '%minus%'


'''