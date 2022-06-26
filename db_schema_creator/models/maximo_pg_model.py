# coding: utf-8
from sqlalchemy import Column, MetaData, Table
from sqlalchemy import BigInteger, Date, Integer, SmallInteger, LargeBinary, Time, Unicode, DateTime, Float,     LargeBinary, Numeric, String, Text, VARBINARY
from sqlalchemy.dialects.oracle.base import RAW

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class T_ALNDOMAIN(Base):
    """Alpha numeric type of domain""" 
    __tablename__ = 'alndomain'
    __table_args__ = {'schema': 'maximo'}

    DOMAINID = Column('domainid', String(22), nullable=False)  # UPPER
    VALUE = Column('value', String(254), nullable=False)  # ALN
    DESCRIPTION = Column('description', String(120))  # ALN
    SITEID = Column('siteid', String(8))  # UPPER
    ORGID = Column('orgid', String(8))  # UPPER
    ALNDOMAINID = Column('alndomainid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    VALUEID = Column('valueid', String(300), nullable=False)  # ALN
    ODK_ISOLATIONFLAG = Column('odk_isolationflag', SmallInteger, nullable=False)  # YORN
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_CROSSOVERDOMAIN(Base):
    """Table for user database crossover fields""" 
    __tablename__ = 'crossoverdomain'
    __table_args__ = {'schema': 'maximo'}

    DOMAINID = Column('domainid', String(22), nullable=False)  # UPPER
    SOURCEFIELD = Column('sourcefield', String(50), nullable=False)  # UPPER
    DESTFIELD = Column('destfield', String(50), nullable=False)  # UPPER
    SITEID = Column('siteid', String(8))  # UPPER
    ORGID = Column('orgid', String(8))  # UPPER
    CROSSOVERDOMAINID = Column('crossoverdomainid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    COPYEVENIFSRCNULL = Column('copyevenifsrcnull', SmallInteger, nullable=False)  # YORN
    COPYONLYIFDESTNULL = Column('copyonlyifdestnull', SmallInteger, nullable=False)  # YORN
    DESTCONDITION = Column('destcondition', String(20))  # UPPER
    SOURCECONDITION = Column('sourcecondition', String(20))  # UPPER
    SEQUENCE = Column('sequence', Integer)  # INTEGER
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_L_MAXATTRIBUTE(Base):
    """Language table of MAXATTRIBUTE""" 
    __tablename__ = 'l_maxattribute'
    __table_args__ = {'schema': 'maximo'}

    REMARKS = Column('remarks', String(4000))  # ALN
    TITLE = Column('title', String(118))  # ALN
    OWNERID = Column('ownerid', BigInteger, nullable=False)  # BIGINT
    LANGCODE = Column('langcode', String(4), nullable=False)  # UPPER
    L_MAXATTRIBUTEID = Column('l_maxattributeid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_L_MAXATTRCFG(Base):
    """Language table of MAXATTRIBUTECFG""" 
    __tablename__ = 'l_maxattrcfg'
    __table_args__ = {'schema': 'maximo'}

    L_MAXATTRCFGID = Column('l_maxattrcfgid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    LANGCODE = Column('langcode', String(4), nullable=False)  # UPPER
    OWNERID = Column('ownerid', BigInteger, nullable=False)  # BIGINT
    REMARKS = Column('remarks', String(4000))  # ALN
    TITLE = Column('title', String(118))  # ALN
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXATTRIBUTE(Base):
    """Maximo Attribute""" 
    __tablename__ = 'maxattribute'
    __table_args__ = {'schema': 'maximo'}

    OBJECTNAME = Column('objectname', String(30), nullable=False)  # UPPER
    ATTRIBUTENAME = Column('attributename', String(50), nullable=False)  # UPPER
    ALIAS = Column('alias', String(50))  # ALN
    AUTOKEYNAME = Column('autokeyname', String(40))  # UPPER
    ATTRIBUTENO = Column('attributeno', Integer, nullable=False)  # INTEGER
    CANAUTONUM = Column('canautonum', SmallInteger, nullable=False)  # YORN
    CLASSNAME = Column('classname', String(256))  # ALN
    COLUMNNAME = Column('columnname', String(30))  # UPPER
    DEFAULTVALUE = Column('defaultvalue', String(50))  # ALN
    DOMAINID = Column('domainid', String(22))  # UPPER
    EAUDITENABLED = Column('eauditenabled', SmallInteger, nullable=False)  # YORN
    ENTITYNAME = Column('entityname', String(30))  # UPPER
    ESIGENABLED = Column('esigenabled', SmallInteger, nullable=False)  # YORN
    ISLDOWNER = Column('isldowner', SmallInteger, nullable=False)  # YORN
    ISPOSITIVE = Column('ispositive', SmallInteger, nullable=False)  # YORN
    LENGTH = Column('length', Integer, nullable=False)  # INTEGER
    MAXTYPE = Column('maxtype', String(8), nullable=False)  # UPPER
    MUSTBE = Column('mustbe', SmallInteger, nullable=False)  # YORN
    REQUIRED = Column('required', SmallInteger, nullable=False)  # YORN
    PERSISTENT = Column('persistent', SmallInteger, nullable=False)  # YORN
    PRIMARYKEYCOLSEQ = Column('primarykeycolseq', Integer)  # INTEGER
    REMARKS = Column('remarks', String(4000), nullable=False)  # ALN
    SAMEASATTRIBUTE = Column('sameasattribute', String(50))  # UPPER
    SAMEASOBJECT = Column('sameasobject', String(30))  # UPPER
    SCALE = Column('scale', Integer, nullable=False)  # INTEGER
    TITLE = Column('title', String(118), nullable=False)  # ALN
    USERDEFINED = Column('userdefined', SmallInteger, nullable=False)  # YORN
    SEARCHTYPE = Column('searchtype', String(20), nullable=False)  # ALN
    MLSUPPORTED = Column('mlsupported', SmallInteger, nullable=False)  # YORN
    MLINUSE = Column('mlinuse', SmallInteger, nullable=False)  # YORN
    HANDLECOLUMNNAME = Column('handlecolumnname', String(30))  # UPPER
    MAXATTRIBUTEID = Column('maxattributeid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    RESTRICTED = Column('restricted', SmallInteger, nullable=False)  # YORN
    LOCALIZABLE = Column('localizable', SmallInteger, nullable=False)  # YORN
    TEXTDIRECTION = Column('textdirection', String(20))  # ALN
    COMPLEXEXPRESSION = Column('complexexpression', String(20))  # UPPER
    EXTENDED = Column('extended', Integer)  # INTEGER
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXATTRIBUTECFG(Base):
    """Maximo Attribute Configuration""" 
    __tablename__ = 'maxattributecfg'
    __table_args__ = {'schema': 'maximo'}

    OBJECTNAME = Column('objectname', String(30), nullable=False)  # UPPER
    ATTRIBUTENAME = Column('attributename', String(50), nullable=False)  # UPPER
    ALIAS = Column('alias', String(50))  # ALN
    AUTOKEYNAME = Column('autokeyname', String(40))  # UPPER
    ATTRIBUTENO = Column('attributeno', Integer, nullable=False)  # INTEGER
    CANAUTONUM = Column('canautonum', SmallInteger, nullable=False)  # YORN
    CLASSNAME = Column('classname', String(256))  # ALN
    COLUMNNAME = Column('columnname', String(30))  # UPPER
    DEFAULTVALUE = Column('defaultvalue', String(50))  # ALN
    DOMAINID = Column('domainid', String(22))  # UPPER
    EAUDITENABLED = Column('eauditenabled', SmallInteger, nullable=False)  # YORN
    ENTITYNAME = Column('entityname', String(30))  # UPPER
    ESIGENABLED = Column('esigenabled', SmallInteger, nullable=False)  # YORN
    ISLDOWNER = Column('isldowner', SmallInteger, nullable=False)  # YORN
    ISPOSITIVE = Column('ispositive', SmallInteger, nullable=False)  # YORN
    LENGTH = Column('length', Integer, nullable=False)  # INTEGER
    MAXTYPE = Column('maxtype', String(8), nullable=False)  # UPPER
    MUSTBE = Column('mustbe', SmallInteger, nullable=False)  # YORN
    REQUIRED = Column('required', SmallInteger, nullable=False)  # YORN
    PERSISTENT = Column('persistent', SmallInteger, nullable=False)  # YORN
    PRIMARYKEYCOLSEQ = Column('primarykeycolseq', Integer)  # INTEGER
    REMARKS = Column('remarks', String(4000), nullable=False)  # ALN
    SAMEASATTRIBUTE = Column('sameasattribute', String(50))  # UPPER
    SAMEASOBJECT = Column('sameasobject', String(30))  # UPPER
    SCALE = Column('scale', Integer, nullable=False)  # INTEGER
    TITLE = Column('title', String(118), nullable=False)  # ALN
    USERDEFINED = Column('userdefined', SmallInteger, nullable=False)  # YORN
    CHANGED = Column('changed', String(1), nullable=False)  # ALN
    SEARCHTYPE = Column('searchtype', String(20), nullable=False)  # ALN
    MLSUPPORTED = Column('mlsupported', SmallInteger, nullable=False)  # YORN
    MLINUSE = Column('mlinuse', SmallInteger, nullable=False)  # YORN
    HANDLECOLUMNNAME = Column('handlecolumnname', String(30))  # UPPER
    MAXATTRIBUTEID = Column('maxattributeid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    RESTRICTED = Column('restricted', SmallInteger, nullable=False)  # YORN
    LOCALIZABLE = Column('localizable', SmallInteger, nullable=False)  # YORN
    TEXTDIRECTION = Column('textdirection', String(20))  # ALN
    COMPLEXEXPRESSION = Column('complexexpression', String(20))  # UPPER
    EXTENDED = Column('extended', Integer)  # INTEGER
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXDOMAIN(Base):
    """Definition of a domain or set of values.""" 
    __tablename__ = 'maxdomain'
    __table_args__ = {'schema': 'maximo'}

    DOMAINID = Column('domainid', String(22), nullable=False)  # UPPER
    DESCRIPTION = Column('description', String(100))  # ALN
    DOMAINTYPE = Column('domaintype', String(20), nullable=False)  # UPPER
    MAXTYPE = Column('maxtype', String(8))  # UPPER
    LENGTH = Column('length', Integer)  # INTEGER
    SCALE = Column('scale', Integer)  # INTEGER
    MAXDOMAINID = Column('maxdomainid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    INTERNAL = Column('internal', Integer, nullable=False)  # INTEGER
    NEVERCACHE = Column('nevercache', SmallInteger)  # YORN
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXOBJECT(Base):
    """Maximo Object""" 
    __tablename__ = 'maxobject'
    __table_args__ = {'schema': 'maximo'}

    OBJECTNAME = Column('objectname', String(30), nullable=False)  # UPPER
    CLASSNAME = Column('classname', String(256))  # ALN
    DESCRIPTION = Column('description', String(119), nullable=False)  # ALN
    EAUDITENABLED = Column('eauditenabled', SmallInteger, nullable=False)  # YORN
    EAUDITFILTER = Column('eauditfilter', String(254))  # ALN
    ENTITYNAME = Column('entityname', String(30))  # UPPER
    ESIGFILTER = Column('esigfilter', String(254))  # ALN
    EXTENDSOBJECT = Column('extendsobject', String(30))  # UPPER
    IMPORTED = Column('imported', SmallInteger, nullable=False)  # YORN
    ISVIEW = Column('isview', SmallInteger, nullable=False)  # YORN
    PERSISTENT = Column('persistent', SmallInteger, nullable=False)  # YORN
    SERVICENAME = Column('servicename', String(18), nullable=False)  # UPPER
    SITEORGTYPE = Column('siteorgtype', String(18), nullable=False)  # UPPER
    USERDEFINED = Column('userdefined', SmallInteger, nullable=False)  # YORN
    MAINOBJECT = Column('mainobject', SmallInteger, nullable=False)  # YORN
    INTERNAL = Column('internal', SmallInteger, nullable=False)  # YORN
    MAXOBJECTID = Column('maxobjectid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    TEXTDIRECTION = Column('textdirection', String(20))  # ALN
    RESOURCETYPE = Column('resourcetype', String(20))  # UPPER
    HASLD = Column('hasld', SmallInteger, nullable=False)  # YORN
    LANGCODE = Column('langcode', String(4), nullable=False)  # UPPER
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXOBJECTCFG(Base):
    """Maximo Object Configuration""" 
    __tablename__ = 'maxobjectcfg'
    __table_args__ = {'schema': 'maximo'}

    OBJECTNAME = Column('objectname', String(30), nullable=False)  # UPPER
    CLASSNAME = Column('classname', String(256))  # ALN
    DESCRIPTION = Column('description', String(119), nullable=False)  # ALN
    EAUDITENABLED = Column('eauditenabled', SmallInteger, nullable=False)  # YORN
    EAUDITFILTER = Column('eauditfilter', String(254))  # ALN
    ENTITYNAME = Column('entityname', String(30))  # UPPER
    ESIGFILTER = Column('esigfilter', String(254))  # ALN
    EXTENDSOBJECT = Column('extendsobject', String(30))  # UPPER
    IMPORTED = Column('imported', SmallInteger, nullable=False)  # YORN
    ISVIEW = Column('isview', SmallInteger, nullable=False)  # YORN
    PERSISTENT = Column('persistent', SmallInteger, nullable=False)  # YORN
    SERVICENAME = Column('servicename', String(18), nullable=False)  # UPPER
    SITEORGTYPE = Column('siteorgtype', String(18), nullable=False)  # UPPER
    USERDEFINED = Column('userdefined', SmallInteger, nullable=False)  # YORN
    CHANGED = Column('changed', String(1), nullable=False)  # ALN
    MAINOBJECT = Column('mainobject', SmallInteger, nullable=False)  # YORN
    INTERNAL = Column('internal', SmallInteger, nullable=False)  # YORN
    MAXOBJECTID = Column('maxobjectid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    TEXTDIRECTION = Column('textdirection', String(20))  # ALN
    RESOURCETYPE = Column('resourcetype', String(20))  # UPPER
    HASLD = Column('hasld', SmallInteger, nullable=False)  # YORN
    LANGCODE = Column('langcode', String(4), nullable=False)  # UPPER
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXPROP(Base):
    """Maximo Properties""" 
    __tablename__ = 'maxprop'
    __table_args__ = {'schema': 'maximo'}

    MAXPROPID = Column('maxpropid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    PROPNAME = Column('propname', String(50), nullable=False)  # ALN
    DESCRIPTION = Column('description', String(192), nullable=False)  # ALN
    MAXTYPE = Column('maxtype', String(8), nullable=False)  # UPPER
    GLOBALONLY = Column('globalonly', SmallInteger, nullable=False)  # YORN
    INSTANCEONLY = Column('instanceonly', SmallInteger, nullable=False)  # YORN
    MAXIMODEFAULT = Column('maximodefault', String(512))  # ALN
    LIVEREFRESH = Column('liverefresh', SmallInteger, nullable=False)  # YORN
    ENCRYPTED = Column('encrypted', SmallInteger, nullable=False)  # YORN
    DOMAINID = Column('domainid', String(22))  # UPPER
    NULLSALLOWED = Column('nullsallowed', SmallInteger, nullable=False)  # YORN
    SECURELEVEL = Column('securelevel', String(20), nullable=False)  # ALN
    USERDEFINED = Column('userdefined', SmallInteger, nullable=False)  # YORN
    ONLINECHANGES = Column('onlinechanges', SmallInteger, nullable=False)  # YORN
    CHANGEBY = Column('changeby', String(60), nullable=False)  # ALN
    CHANGEDATE = Column('changedate', DateTime, nullable=False)  # DATETIME
    MASKED = Column('masked', SmallInteger, nullable=False)  # YORN
    ACCESSTYPE = Column('accesstype', Integer)  # INTEGER
    VALUERULES = Column('valuerules', String(50))  # UPPER
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXPROPVALUE(Base):
    """Maximo Property Values""" 
    __tablename__ = 'maxpropvalue'
    __table_args__ = {'schema': 'maximo'}

    MAXPROPVALUEID = Column('maxpropvalueid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    PROPNAME = Column('propname', String(50), nullable=False)  # ALN
    SERVERNAME = Column('servername', String(100), nullable=False)  # ALN
    SERVERHOST = Column('serverhost', String(100))  # ALN
    PROPVALUE = Column('propvalue', String(512))  # ALN
    ENCRYPTEDVALUE = Column('encryptedvalue', LargeBinary)  # CRYPTO
    CHANGEBY = Column('changeby', String(60), nullable=False)  # ALN
    CHANGEDATE = Column('changedate', DateTime, nullable=False)  # DATETIME
    ACCESSTYPE = Column('accesstype', Integer)  # INTEGER
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXSEQUENCE(Base):
    """Records UniqueID Sequence Reservations.""" 
    __tablename__ = 'maxsequence'
    __table_args__ = {'schema': 'maximo'}

    TBNAME = Column('tbname', String(30), nullable=False)  # UPPER
    NAME = Column('name', String(30), nullable=False)  # UPPER
    MAXRESERVED = Column('maxreserved', BigInteger, nullable=False)  # BIGINT
    MAXVALUE = Column('maxvalue', BigInteger)  # BIGINT
    RANGE = Column('range', BigInteger)  # BIGINT
    SEQUENCENAME = Column('sequencename', String(30), nullable=False)  # UPPER
    MAXSEQUENCEID = Column('maxsequenceid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXSERVICE(Base):
    """Java Services""" 
    __tablename__ = 'maxservice'
    __table_args__ = {'schema': 'maximo'}

    SERVICENAME = Column('servicename', String(18), nullable=False)  # UPPER
    DESCRIPTION = Column('description', String(100))  # ALN
    CLASSNAME = Column('classname', String(256), nullable=False)  # ALN
    MAXSERVICEID = Column('maxserviceid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    INITORDER = Column('initorder', Integer, nullable=False)  # INTEGER
    INTERNAL = Column('internal', SmallInteger, nullable=False)  # YORN
    ACTIVE = Column('active', SmallInteger, nullable=False)  # YORN
    SINGLETON = Column('singleton', SmallInteger)  # YORN
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXSYSINDEXES(Base):
    """The MAXSYSINDEXES Table""" 
    __tablename__ = 'maxsysindexes'
    __table_args__ = {'schema': 'maximo'}

    NAME = Column('name', String(30), nullable=False)  # UPPER
    TBNAME = Column('tbname', String(30), nullable=False)  # UPPER
    UNIQUERULE = Column('uniquerule', String(1), nullable=False)  # UPPER
    CHANGED = Column('changed', String(1))  # ALN
    CLUSTERRULE = Column('clusterrule', SmallInteger, nullable=False)  # YORN
    STORAGEPARTITION = Column('storagepartition', String(30))  # ALN
    REQUIRED = Column('required', SmallInteger, nullable=False)  # YORN
    TEXTSEARCH = Column('textsearch', SmallInteger, nullable=False)  # YORN
    MAXSYSINDEXESID = Column('maxsysindexesid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXSYSKEYS(Base):
    """The MAXSYSKEYS Table""" 
    __tablename__ = 'maxsyskeys'
    __table_args__ = {'schema': 'maximo'}

    IXNAME = Column('ixname', String(30), nullable=False)  # UPPER
    COLNAME = Column('colname', String(30), nullable=False)  # UPPER
    COLSEQ = Column('colseq', SmallInteger, nullable=False)  # SMALLINT
    ORDERING = Column('ordering', String(1), nullable=False)  # UPPER
    CHANGED = Column('changed', String(1))  # ALN
    MAXSYSKEYSID = Column('maxsyskeysid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXTABLE(Base):
    """Maximo Table""" 
    __tablename__ = 'maxtable'
    __table_args__ = {'schema': 'maximo'}

    TABLENAME = Column('tablename', String(30), nullable=False)  # UPPER
    ADDROWSTAMP = Column('addrowstamp', SmallInteger, nullable=False)  # YORN
    EAUDITTBNAME = Column('eaudittbname', String(30))  # UPPER
    ISAUDITTABLE = Column('isaudittable', SmallInteger, nullable=False)  # YORN
    RESTOREDATA = Column('restoredata', SmallInteger, nullable=False)  # YORN
    STORAGEPARTITION = Column('storagepartition', String(30))  # ALN
    TEXTSEARCHENABLED = Column('textsearchenabled', SmallInteger, nullable=False)  # YORN
    LANGTABLENAME = Column('langtablename', String(30))  # UPPER
    LANGCOLUMNNAME = Column('langcolumnname', String(30))  # UPPER
    UNIQUECOLUMNNAME = Column('uniquecolumnname', String(30))  # UPPER
    ISLANGTABLE = Column('islangtable', SmallInteger, nullable=False)  # YORN
    MAXTABLEID = Column('maxtableid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ALTIXNAME = Column('altixname', String(30))  # UPPER
    TRIGROOT = Column('trigroot', String(29), nullable=False)  # UPPER
    CONTENTATTRIBUTE = Column('contentattribute', String(30))  # UPPER
    STORAGETYPE = Column('storagetype', Integer, nullable=False)  # INTEGER
    EXTTABLENAME = Column('exttablename', String(30))  # UPPER
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXTABLECFG(Base):
    """Maximo Table Configuration""" 
    __tablename__ = 'maxtablecfg'
    __table_args__ = {'schema': 'maximo'}

    TABLENAME = Column('tablename', String(30), nullable=False)  # UPPER
    ADDROWSTAMP = Column('addrowstamp', SmallInteger, nullable=False)  # YORN
    EAUDITTBNAME = Column('eaudittbname', String(30))  # UPPER
    ISAUDITTABLE = Column('isaudittable', SmallInteger, nullable=False)  # YORN
    RESTOREDATA = Column('restoredata', SmallInteger, nullable=False)  # YORN
    STORAGEPARTITION = Column('storagepartition', String(30))  # ALN
    TEXTSEARCHENABLED = Column('textsearchenabled', SmallInteger, nullable=False)  # YORN
    LANGTABLENAME = Column('langtablename', String(30))  # UPPER
    LANGCOLUMNNAME = Column('langcolumnname', String(30))  # UPPER
    UNIQUECOLUMNNAME = Column('uniquecolumnname', String(30))  # UPPER
    ISLANGTABLE = Column('islangtable', SmallInteger, nullable=False)  # YORN
    MAXTABLEID = Column('maxtableid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ALTIXNAME = Column('altixname', String(30))  # UPPER
    TRIGROOT = Column('trigroot', String(29), nullable=False)  # UPPER
    CONTENTATTRIBUTE = Column('contentattribute', String(30))  # UPPER
    STORAGETYPE = Column('storagetype', Integer, nullable=False)  # INTEGER
    EXTTABLENAME = Column('exttablename', String(30))  # UPPER
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXTABLEDOMAIN(Base):
    """Defines a MAXIMO table type of value domain""" 
    __tablename__ = 'maxtabledomain'
    __table_args__ = {'schema': 'maximo'}

    DOMAINID = Column('domainid', String(22), nullable=False)  # UPPER
    VALIDTNWHERECLAUSE = Column('validtnwhereclause', String(4000))  # ALN
    LISTWHERECLAUSE = Column('listwhereclause', String(4000))  # ALN
    ERRORRESOURCBUNDLE = Column('errorresourcbundle', String(50))  # ALN
    ERRORACCESSKEY = Column('erroraccesskey', String(50))  # ALN
    OBJECTNAME = Column('objectname', String(30), nullable=False)  # UPPER
    SITEID = Column('siteid', String(8))  # UPPER
    ORGID = Column('orgid', String(8))  # UPPER
    MAXTABLEDOMAINID = Column('maxtabledomainid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXVARS(Base):
    """The MAXVARS Table""" 
    __tablename__ = 'maxvars'
    __table_args__ = {'schema': 'maximo'}

    VARNAME = Column('varname', String(18), nullable=False)  # ALN
    VARVALUE = Column('varvalue', String(254))  # ALN
    ORGID = Column('orgid', String(8))  # UPPER
    SITEID = Column('siteid', String(8))  # UPPER
    MAXVARSID = Column('maxvarsid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    VARTYPE = Column('vartype', String(6))  # ALN
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXVARTYPE(Base):
    """Identifies the domain of a MaxVar""" 
    __tablename__ = 'maxvartype'
    __table_args__ = {'schema': 'maximo'}

    VARNAME = Column('varname', String(18), nullable=False)  # ALN
    VARTYPE = Column('vartype', String(6), nullable=False)  # ALN
    DEFAULTVALUE = Column('defaultvalue', String(254))  # ALN
    DESCRIPTION = Column('description', String(150))  # ALN
    MAXVARTYPEID = Column('maxvartypeid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXVIEWCFG(Base):
    """Maximo View Configuration""" 
    __tablename__ = 'maxviewcfg'
    __table_args__ = {'schema': 'maximo'}

    VIEWNAME = Column('viewname', String(30), nullable=False)  # UPPER
    VIEWSELECT = Column('viewselect', String(4000))  # ALN
    VIEWWHERE = Column('viewwhere', String(4000))  # ALN
    AUTOSELECT = Column('autoselect', SmallInteger, nullable=False)  # YORN
    MAXVIEWID = Column('maxviewid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    VIEWFROM = Column('viewfrom', String(1000))  # ALN
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_MAXVIEWCOLUMNCFG(Base):
    """Maximo View Column Configuration""" 
    __tablename__ = 'maxviewcolumncfg'
    __table_args__ = {'schema': 'maximo'}

    VIEWNAME = Column('viewname', String(30), nullable=False)  # UPPER
    VIEWCOLUMNNAME = Column('viewcolumnname', String(30), nullable=False)  # UPPER
    SAMESTORAGEAS = Column('samestorageas', String(30))  # UPPER
    TABLENAME = Column('tablename', String(30))  # UPPER
    TABLECOLUMNNAME = Column('tablecolumnname', String(30))  # UPPER
    CHANGED = Column('changed', String(1), nullable=False)  # ALN
    MAXVIEWCOLUMNID = Column('maxviewcolumnid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_NUMERICDOMAIN(Base):
    """Numeric type domain""" 
    __tablename__ = 'numericdomain'
    __table_args__ = {'schema': 'maximo'}

    DOMAINID = Column('domainid', String(22), nullable=False)  # UPPER
    VALUE = Column('value', Numeric(30, 10), nullable=False)  # DECIMAL
    DESCRIPTION = Column('description', String(124))  # ALN
    SITEID = Column('siteid', String(8))  # UPPER
    ORGID = Column('orgid', String(8))  # UPPER
    NUMERICDOMAINID = Column('numericdomainid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    VALUEID = Column('valueid', String(300), nullable=False)  # ALN
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_NUMRANGEDOMAIN(Base):
    """Domain for number range""" 
    __tablename__ = 'numrangedomain'
    __table_args__ = {'schema': 'maximo'}

    RANGESEGMENT = Column('rangesegment', SmallInteger, nullable=False)  # SMALLINT
    DOMAINID = Column('domainid', String(22), nullable=False)  # UPPER
    RANGEMINIMUM = Column('rangeminimum', Float)  # FLOAT
    RANGEMAXIMUM = Column('rangemaximum', Float)  # FLOAT
    RANGEINTERVAL = Column('rangeinterval', Float)  # FLOAT
    SITEID = Column('siteid', String(8))  # UPPER
    ORGID = Column('orgid', String(8))  # UPPER
    NUMRANGEDOMAINID = Column('numrangedomainid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP

class T_SYNONYMDOMAIN(Base):
    """Definition of synonym value domain""" 
    __tablename__ = 'synonymdomain'
    __table_args__ = {'schema': 'maximo'}

    DOMAINID = Column('domainid', String(22), nullable=False)  # UPPER
    MAXVALUE = Column('maxvalue', String(50), nullable=False)  # ALN
    VALUE = Column('value', String(50), nullable=False)  # ALN
    DESCRIPTION = Column('description', String(256))  # ALN
    DEFAULTS = Column('defaults', SmallInteger, nullable=False)  # YORN
    SITEID = Column('siteid', String(8))  # UPPER
    ORGID = Column('orgid', String(8))  # UPPER
    SYNONYMDOMAINID = Column('synonymdomainid', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    VALUEID = Column('valueid', String(256), nullable=False)  # ALN
    ODK_ISOLATIONFLAG = Column('odk_isolationflag', SmallInteger, nullable=False)  # YORN
    ROWSTAMP = Column('rowstamp', String(40), nullable=False)  # ROWSTAMP


SCHEMA_TABLES = {
    "T_ALNDOMAIN": T_ALNDOMAIN,
    "T_CROSSOVERDOMAIN": T_CROSSOVERDOMAIN,
    "T_L_MAXATTRIBUTE": T_L_MAXATTRIBUTE,
    "T_L_MAXATTRCFG": T_L_MAXATTRCFG,
    "T_MAXATTRIBUTE": T_MAXATTRIBUTE,
    "T_MAXATTRIBUTECFG": T_MAXATTRIBUTECFG,
    "T_MAXDOMAIN": T_MAXDOMAIN,
    "T_MAXOBJECT": T_MAXOBJECT,
    "T_MAXOBJECTCFG": T_MAXOBJECTCFG,
    "T_MAXPROP": T_MAXPROP,
    "T_MAXPROPVALUE": T_MAXPROPVALUE,
    "T_MAXSEQUENCE": T_MAXSEQUENCE,
    "T_MAXSERVICE": T_MAXSERVICE,
    "T_MAXSYSINDEXES": T_MAXSYSINDEXES,
    "T_MAXSYSKEYS": T_MAXSYSKEYS,
    "T_MAXTABLE": T_MAXTABLE,
    "T_MAXTABLECFG": T_MAXTABLECFG,
    "T_MAXTABLEDOMAIN": T_MAXTABLEDOMAIN,
    "T_MAXVARS": T_MAXVARS,
    "T_MAXVARTYPE": T_MAXVARTYPE,
    "T_MAXVIEWCFG": T_MAXVIEWCFG,
    "T_MAXVIEWCOLUMNCFG": T_MAXVIEWCOLUMNCFG,
    "T_NUMERICDOMAIN": T_NUMERICDOMAIN,
    "T_NUMRANGEDOMAIN": T_NUMRANGEDOMAIN,
    "T_SYNONYMDOMAIN": T_SYNONYMDOMAIN
}