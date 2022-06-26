# coding: utf-8

from sqlalchemy import Column, MetaData, Table
from sqlalchemy import BigInteger, Date, Integer, SmallInteger, LargeBinary, Time, Unicode, DateTime, Float, \
    LargeBinary, Numeric, String, Text, VARBINARY

from sqlalchemy.dialects.oracle.base import RAW
from sqlalchemy.sql.type_api import TypeEngine

from sqlalchemy.ext.declarative import declarative_base

from aconn import AConnector

DB2 = 'DB2'
ORA = 'ORA'
PG = 'PG'

MXTypesList = [
    "ALN",
    "AMOUNT",
    "BIGINT",
    "BLOB",
    "CLOB",
    "CRYPTO",
    "CRYPTOX",
    "DATE",
    "DATETIME",
    "DECIMAL",
    "DURATION",
    "FLOAT",
    "GL",
    "INTEGER",
    "LONGALN",
    "LOWER",
    "SMALLINT",
    "TIME",
    "UPPER",
    "YORN"]

ExtractorBase = declarative_base()  # metadata = ExtractorBase.metadata


class T:
    def __init__(self, max_type: str, platform: str, native: str, alchemy,
                 need_length: bool, need_scale: bool, jdbc: int = None,
                 asdecimal: bool = None
    ):
        self.max_type = max_type
        self.platform = platform
        self.native = native
        self.alchemy = alchemy

        self.need_length = need_length
        self.need_scale = need_scale

        self.jdbc = jdbc

        self.asdecimal = asdecimal


class MaxTypesConvertor:
    def __init__(self):
        db2_types_list = self.__initDB2()
        ora_types_list = self.__initORA()
        pg_types_list = self.__initPG()

        self.all_types_list = db2_types_list + pg_types_list + ora_types_list
        self.pg_types = {str(t.max_type).upper(): t for t in pg_types_list}
        self.db2_types = {str(t.max_type).upper(): t for t in db2_types_list}
        self.ora_types = {str(t.max_type).upper(): t for t in ora_types_list}

    def get_type(self, db_type: str, max_type: str) -> T:
        max_type = str(max_type).upper()
        if db_type == 'PG':
            types_dict = self.pg_types
        elif db_type == 'DB2':
            types_dict = self.db2_types
        elif db_type == 'ORA':
            types_dict = self.ora_types
        else:
            raise Exception('Invalid database type: %s' % db_type)

        max_type = str(max_type).upper()
        if max_type not in types_dict:
            raise Exception('Invalid max_type: %s' % max_type)
        return types_dict[max_type]

    @staticmethod
    def __initDB2():
        return [
            T(
                max_type="ROWSTAMP",
                platform="DB2",
                native="BIGINT",
                alchemy=BigInteger,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="ALN",
                platform="DB2",
                native="VARCHAR",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="AMOUNT",
                platform="DB2",
                native="DECIMAL",
                alchemy=Numeric,
                need_length=True,
                need_scale=True,
                jdbc=None
            ),
            T(
                max_type="BIGINT",
                platform="DB2",
                native="BIGINT",
                alchemy=BigInteger,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="BLOB",
                platform="DB2",
                native="BLOB",
                alchemy=LargeBinary,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="CLOB",
                platform="DB2",
                native="CLOB",
                alchemy=Text,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="CRYPTO",
                platform="DB2",
                native="VARCHAR () FOR BIT DATA",  # think about type
                alchemy=VARBINARY,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="CRYPTOX",
                platform="DB2",
                native="VARCHAR () FOR BIT DATA",  # think about type
                alchemy=VARBINARY,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="DATE",
                platform="DB2",
                native="DATE",
                alchemy=Date,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="DATETIME",
                platform="DB2",
                native="TIMESTAMP",
                alchemy=DateTime,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="DECIMAL",
                platform="DB2",
                native="DECIMAL",
                alchemy=Numeric,
                need_length=True,
                need_scale=True,
                jdbc=None
            ),
            T(
                max_type="DURATION",
                platform="DB2",
                native="DOUBLE",
                alchemy=Float,
                need_length=False,  # 53
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="FLOAT",
                platform="DB2",
                native="DOUBLE",
                alchemy=Float,
                need_length=False,  # May set 53
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="GL",
                platform="DB2",
                native="VARGRAPHIC",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="INTEGER",
                platform="DB2",
                native="INTEGER",
                alchemy=Integer,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="LONGALN",
                platform="DB2",
                native="VARGRAPHIC",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="LOWER",
                platform="DB2",
                native="VARGRAPHIC",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="SMALLINT",
                platform="DB2",
                native="INTEGER",
                alchemy=Integer,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="TIME",
                platform="DB2",
                native="TIME",
                alchemy=Time,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="UPPER",
                platform="DB2",
                native="VARGRAPHIC",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="YORN",
                platform="DB2",
                native="INTEGER",
                alchemy=Integer,
                need_length=False,
                need_scale=False,
                jdbc=None
            )
        ]

    @staticmethod
    def __initORA():
        return [
            T(
                max_type="ROWSTAMP",
                platform="ORA",
                native="VARCHAR2",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="ALN",
                platform="ORA",
                native="VARCHAR2",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="AMOUNT",
                platform="ORA",
                native="NUMBER",
                alchemy=Numeric,
                need_length=True,
                need_scale=True,
                jdbc=None
            ),
            T(
                max_type="BIGINT",
                platform="ORA",
                native="NUMBER",
                alchemy=Numeric,
                need_length=False,
                need_scale=False,
                jdbc=None,
                asdecimal=False
            ),
            T(
                max_type="BLOB",
                platform="ORA",
                native="BLOB",
                alchemy=LargeBinary,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="CLOB",
                platform="ORA",
                native="CLOB",
                alchemy=Text,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="CRYPTO",
                platform="ORA",
                native="RAW",
                alchemy=RAW,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="CRYPTOX",
                platform="ORA",
                native="RAW",
                alchemy=RAW,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="DATE",
                platform="ORA",
                native="DATE",
                alchemy=DateTime,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="DATETIME",
                platform="ORA",
                native="DATE",
                alchemy=DateTime,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="DECIMAL",
                platform="ORA",
                native="NUMBER",
                alchemy=Numeric,
                need_length=True,
                need_scale=True,
                jdbc=None
            ),
            T(
                max_type="DURATION",
                platform="ORA",
                native="DOUBLE",
                alchemy=Float,
                need_length=False,  # 53
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="FLOAT",
                platform="ORA",
                native="DOUBLE",
                alchemy=Float,
                need_length=False,  # May set 53
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="GL",
                platform="ORA",
                native="VARCHAR2",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="INTEGER",
                platform="ORA",
                native="NUMBER",
                alchemy=Numeric,
                need_length=False,
                need_scale=False,
                jdbc=None,
                asdecimal=False
            ),
            T(
                max_type="LONGALN",
                platform="ORA",
                native="VARCHAR2",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="LOWER",
                platform="ORA",
                native="VARCHAR2",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="SMALLINT",
                platform="ORA",
                native="NUMBER",
                alchemy=Numeric,
                need_length=False,
                need_scale=False,
                jdbc=None,
                asdecimal=False
            ),
            T(
                max_type="TIME",
                platform="ORA",
                native="DATE",
                alchemy=DateTime,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="UPPER",
                platform="ORA",
                native="VARCHAR2",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="YORN",
                platform="ORA",
                native="NUMBER",
                alchemy=Numeric,
                need_length=False,
                need_scale=False,
                jdbc=None,
                asdecimal=False
            )
        ]

    @staticmethod
    def __initPG():
        return [
            T(
                max_type="ROWSTAMP",
                platform="PG",
                native="varchar",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="ALN",
                platform="PG",
                native="varchar",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="AMOUNT",
                platform="PG",
                native="numeric",
                alchemy=Numeric,
                need_length=True,
                need_scale=True,
                jdbc=None
            ),
            T(
                max_type="BIGINT",
                platform="PG",
                native="int8",
                alchemy=BigInteger,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="BLOB",
                platform="PG",
                native="bytea",
                alchemy=LargeBinary,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="CLOB",
                platform="PG",
                native="text",
                alchemy=Text,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="CRYPTO",
                platform="PG",
                native="bytea",
                alchemy=LargeBinary,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="CRYPTOX",
                platform="PG",
                native="bytea",
                alchemy=LargeBinary,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="DATE",
                platform="PG",
                native="date",
                alchemy=Date,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="DATETIME",
                platform="PG",
                native="timestamp",
                alchemy=DateTime,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="DECIMAL",
                platform="PG",
                native="numeric",
                alchemy=Numeric,
                need_length=True,
                need_scale=True,
                jdbc=None
            ),
            T(
                max_type="DURATION",
                platform="PG",
                native="float8",
                alchemy=Float,
                need_length=False,  # 17
                need_scale=False,  # 17
                jdbc=None
            ),
            T(
                max_type="FLOAT",
                platform="PG",
                native="float8",
                alchemy=Float,
                need_length=False,  # 17
                need_scale=False,  # 17
                jdbc=None
            ),
            T(
                max_type="GL",
                platform="PG",
                native="varchar",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="INTEGER",
                platform="PG",
                native="int4",
                alchemy=Integer,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="LONGALN",
                platform="PG",
                native="varchar",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="LOWER",
                platform="PG",
                native="varchar",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="SMALLINT",
                platform="PG",
                native="int2",
                alchemy=SmallInteger,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="TIME",
                platform="PG",
                native="time",
                alchemy=Time,
                need_length=False,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="UPPER",
                platform="PG",
                native="varchar",
                alchemy=String,
                need_length=True,
                need_scale=False,
                jdbc=None
            ),
            T(
                max_type="YORN",
                platform="PG",
                native="int2",
                alchemy=SmallInteger,
                need_length=False,
                need_scale=False,
                jdbc=None
            )
        ]


class MaxobjectExtractor(ExtractorBase):
    __tablename__ = 'maxobject'
    __table_args__ = {'schema': 'maximo'}

    maxobjectid = Column(BigInteger, primary_key=True)
    objectname = Column(Unicode(30), nullable=False)
    isview = Column(Integer, nullable=False)
    persistent = Column(Integer, nullable=False)
    description = Column(Unicode(100), nullable=False)
    internal = Column(Integer, nullable=False)


class MaxattributeExtractor(ExtractorBase):
    __tablename__ = 'maxattribute'
    __table_args__ = {'schema': 'maximo'}

    maxattributeid = Column(BigInteger, primary_key=True)
    objectname = Column(Unicode(30), nullable=False)
    attributename = Column(Unicode(50), nullable=False)
    attributeno = Column(Integer, nullable=False)
    columnname = Column(Unicode(30))
    length = Column(Integer, nullable=False)
    maxtype = Column(Unicode(8), nullable=False)
    persistent = Column(Integer, nullable=False)
    scale = Column(Integer, nullable=False)
    required = Column(Integer, nullable=False)  # not null


class MaxtableExtractor(ExtractorBase):
    __tablename__ = 'maxtable'
    __table_args__ = {'schema': 'maximo'}

    maxtableid = Column(BigInteger, primary_key=True)
    tablename = Column(Unicode(30), nullable=False)
    addrowstamp = Column(Integer, nullable=False)
    uniquecolumnname = Column(Unicode(30))

    trigroot = Column(Unicode(29), nullable=False)


SCHEMA_FILE_HEADER = '''# coding: utf-8
from sqlalchemy import Column, MetaData, Table
from sqlalchemy import BigInteger, Date, Integer, SmallInteger, LargeBinary, Time, Unicode, DateTime, Float, \
    LargeBinary, Numeric, String, Text, VARBINARY
from sqlalchemy.dialects.oracle.base import RAW

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

'''

MXConvertor = MaxTypesConvertor()

def get_column_string(dest_db_type: str, column_name: str, max_type: T, is_required: bool=False, is_pk: bool=False,
                      len: int=0, scale: int=0, asdecimal: bool=None):
    if dest_db_type == 'PG':
        colname = column_name.lower()
    else:
        colname = column_name.upper()
    col = "%s = Column('%s', " % (column_name.upper(), colname)
    if asdecimal is False:
        col += '{type}(asdecimal=False)'.format(type=max_type.alchemy.__name__)
    elif max_type.need_length and len > 0:
        if max_type.need_scale:
            col += '{type}({len}, {scale})'.format(type=max_type.alchemy.__name__, len=len, scale=scale)
        else:
            col += '{type}({len})'.format(type=max_type.alchemy.__name__, len=len)
    else:
        col += max_type.alchemy.__name__
    if is_pk:
        col += ', primary_key=True, autoincrement=False'
    if is_required:
        col += ', nullable=False'
    col += ')  # ' + str(max_type.max_type)
    return col

def get_column_script(dest_db_type, attribute: MaxattributeExtractor, is_pk: bool):
    max_type = MXConvertor.get_type(dest_db_type, str(attribute.maxtype))
    return get_column_string(
        dest_db_type=dest_db_type,
        column_name=str(attribute.columnname),
        max_type=max_type,
        is_required=(attribute.required == 1),
        is_pk=is_pk,
        len=int(attribute.length),
        scale=int(attribute.scale),

    )

def get_rowstamp_script(dest_db_type, is_primary_key):
    tp = MXConvertor.get_type(dest_db_type, 'ROWSTAMP')
    return get_column_string(dest_db_type, 'ROWSTAMP', tp, is_required=True, len=40, is_pk=is_primary_key)


def create_schema_script(dest_db_type, schema_data, filename, log=None):
    warns = []
    schema_classes = []
    with open(filename, 'w') as f:
        f.write(SCHEMA_FILE_HEADER)
        for object_name, object_info in schema_data.items():
            if log is not None:
                log('Generating script for object %s' % object_name)
            tab = object_info['table']  # type: MaxtableExtractor
            attrs = object_info['attributes']  # type: list

            attr_column_names = [str(attr.columnname).upper() for attr in attrs]
            pk_field = str(tab.uniquecolumnname).upper()
            if pk_field == '' or pk_field not in attr_column_names:
                pk_field = str(object_name + 'UID').upper()
                if pk_field in attr_column_names:
                    warns.append('WARNING! Set primary key of %s to *UID' % object_name)
                else:
                    pk_field = str(object_name + 'ID').upper()
                    if pk_field in attr_column_names:
                        warns.append('WARNING! Set primary key of %s to *ID' % object_name)
                    else:
                        # if str(attr_column_names[0]).upper().endswith('ID'):
                        #     pk_field = attr_column_names[0]
                        #     warns.append('WARNING! Set primary key of %s to FIRST ATTRIBUTE %s' % (object_name, pk_field))
                        # else:
                        if tab.addrowstamp == 1:
                            pk_field = 'ROWSTAMP'
                            warns.append('WARNING! Set primary key of %s to ROWSTAMP' % object_name)
                        else:
                            raise Exception("Can't determide unique ID column for object %s" % object_name)


            columns_script = ''
            for attr in attrs:  # type: MaxattributeExtractor
                if str(attr.attributename).upper() == 'ROWSTAMP' and tab.addrowstamp == 1:
                    continue  # dont duplicate rowstamp
                is_primary_key = str(attr.attributename).upper() == pk_field
                columns_script += '\n    ' + get_column_script(dest_db_type, attr, is_primary_key)
            if tab.addrowstamp == 1:
                columns_script += '\n    ' + get_rowstamp_script(dest_db_type, pk_field == 'ROWSTAMP')

            classname = 'T_' + str(tab.tablename).upper()

            if dest_db_type == 'PG':
                t_name = str(tab.tablename).lower()
                mx_schema = 'maximo'
            else:
                t_name = str(tab.tablename).upper()
                mx_schema = 'MAXIMO'
            object_script = ("\nclass {classname}(Base):" +
                            '\n    """{description}""" ' +
                            "\n    __tablename__ = '{table_low}'"
                            "\n    __table_args__ = {{'schema': '"+ mx_schema +"'}}"
                            "\n{columns}"
                            "\n"). \
                format(classname=classname,
                       table_low=t_name,
                       columns=columns_script, description=object_info['description'])
            schema_classes.append('"%s": %s' % (classname, classname))
            f.write(object_script)
        f.write('\n\nSCHEMA_TABLES = {\n    %s\n}' % (',\n    '.join(schema_classes)))
    # warns
    if len(warns) > 0:
        for w in warns:
            log(w)

def create_schema(connection_str, dest_db_type, export_filename, object_list):
    src = AConnector('src', connection_str, encoding='utf8', echo=False)

    src.log('Extracting objects')
    maxobjects = list(
        src.con.query(MaxobjectExtractor).
            filter(MaxobjectExtractor.persistent == 1).
            filter(MaxobjectExtractor.isview == 0).
            all()
    )
    maxobjects = list(filter(lambda s: s.objectname in object_list.keys(), maxobjects))

    src.log('Extracting tables')
    maxtables = list(src.con.query(MaxtableExtractor).all())

    src.log('Extracting attributes')
    maxattributes = list(
        src.con.query(MaxattributeExtractor).
            filter(MaxattributeExtractor.persistent == 1).
            order_by(MaxattributeExtractor.objectname, MaxattributeExtractor.attributeno).
            all()
    )

    schema_data = {}
    src.log('Building schema info')

    attr_dict = {}
    for attr in maxattributes:  # type: MaxattributeExtractor
        object_name = str(attr.objectname).upper()
        if object_name not in attr_dict:
            attr_dict[object_name] = []
        attr_dict[object_name].append(attr)

    tabs_dict = {}
    for tab in maxtables:  # type: MaxtableExtractor
        tabs_dict[str(tab.tablename).upper()] = tab

    errors = False
    for obj in maxobjects:  # type: MaxobjectExtractor
        object_name = str(obj.objectname).upper()
        if object_name not in tabs_dict:
            errors = True
            src.log('%s missing table' % object_name)
        if object_name not in attr_dict:
            errors = True
            src.log('%s missing attributes' % object_name)

        try:
            description = (str(obj.description).encode('ascii', 'ignore')).decode("utf-8")
        except:
            description = ''
        schema_data[object_name] = {
            'description': description,
            'table': tabs_dict[object_name],
            'attributes': attr_dict[object_name]
        }

    if errors:
        return

    src.log('Creating schema file')

    create_schema_script(dest_db_type, schema_data, export_filename, log=src.log)
    src.log('Schema file created: %s' % export_filename)

    return True

#
# if __name__ == '__main__':
# #    create_schema('postgresql://maximo:maximo@192.168.11.77/MAX1', PG, 'pg77.py')
#     create_schema('oracle://maximo:maximo@192.168.11.77:1521/max1', PG, 'ora77.py')
