# coding: utf-8
from sqlalchemy import Column, MetaData, Table
from sqlalchemy import BigInteger, Date, Integer, SmallInteger, LargeBinary, Time, Unicode, DateTime, Float,     LargeBinary, Numeric, String, Text, VARBINARY
from sqlalchemy.dialects.oracle.base import RAW

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class T_ALNDOMAIN(Base):
    """Alpha numeric type of domain""" 
    __tablename__ = 'ALNDOMAIN'
    __table_args__ = {'schema': 'MAXIMO'}

    DOMAINID = Column('DOMAINID', String(22), nullable=False)  # UPPER
    VALUE = Column('VALUE', String(254), nullable=False)  # ALN
    DESCRIPTION = Column('DESCRIPTION', String(120))  # ALN
    SITEID = Column('SITEID', String(8))  # UPPER
    ORGID = Column('ORGID', String(8))  # UPPER
    ALNDOMAINID = Column('ALNDOMAINID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    VALUEID = Column('VALUEID', String(300), nullable=False)  # ALN
    ODK_ISOLATIONFLAG = Column('ODK_ISOLATIONFLAG', Integer, nullable=False)  # YORN
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_CROSSOVERDOMAIN(Base):
    """Table for user database crossover fields""" 
    __tablename__ = 'CROSSOVERDOMAIN'
    __table_args__ = {'schema': 'MAXIMO'}

    DOMAINID = Column('DOMAINID', String(22), nullable=False)  # UPPER
    SOURCEFIELD = Column('SOURCEFIELD', String(50), nullable=False)  # UPPER
    DESTFIELD = Column('DESTFIELD', String(50), nullable=False)  # UPPER
    SITEID = Column('SITEID', String(8))  # UPPER
    ORGID = Column('ORGID', String(8))  # UPPER
    CROSSOVERDOMAINID = Column('CROSSOVERDOMAINID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    COPYEVENIFSRCNULL = Column('COPYEVENIFSRCNULL', Integer, nullable=False)  # YORN
    COPYONLYIFDESTNULL = Column('COPYONLYIFDESTNULL', Integer, nullable=False)  # YORN
    DESTCONDITION = Column('DESTCONDITION', String(20))  # UPPER
    SOURCECONDITION = Column('SOURCECONDITION', String(20))  # UPPER
    SEQUENCE = Column('SEQUENCE', Integer)  # INTEGER
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_L_MAXATTRIBUTE(Base):
    """Language table of MAXATTRIBUTE""" 
    __tablename__ = 'L_MAXATTRIBUTE'
    __table_args__ = {'schema': 'MAXIMO'}

    REMARKS = Column('REMARKS', String(4000))  # ALN
    TITLE = Column('TITLE', String(118))  # ALN
    OWNERID = Column('OWNERID', BigInteger, nullable=False)  # BIGINT
    LANGCODE = Column('LANGCODE', String(4), nullable=False)  # UPPER
    L_MAXATTRIBUTEID = Column('L_MAXATTRIBUTEID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_L_MAXATTRCFG(Base):
    """Language table of MAXATTRIBUTECFG""" 
    __tablename__ = 'L_MAXATTRCFG'
    __table_args__ = {'schema': 'MAXIMO'}

    L_MAXATTRCFGID = Column('L_MAXATTRCFGID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    LANGCODE = Column('LANGCODE', String(4), nullable=False)  # UPPER
    OWNERID = Column('OWNERID', BigInteger, nullable=False)  # BIGINT
    REMARKS = Column('REMARKS', String(4000))  # ALN
    TITLE = Column('TITLE', String(118))  # ALN
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXATTRIBUTE(Base):
    """Maximo Attribute""" 
    __tablename__ = 'MAXATTRIBUTE'
    __table_args__ = {'schema': 'MAXIMO'}

    OBJECTNAME = Column('OBJECTNAME', String(30), nullable=False)  # UPPER
    ATTRIBUTENAME = Column('ATTRIBUTENAME', String(50), nullable=False)  # UPPER
    ALIAS = Column('ALIAS', String(50))  # ALN
    AUTOKEYNAME = Column('AUTOKEYNAME', String(40))  # UPPER
    ATTRIBUTENO = Column('ATTRIBUTENO', Integer, nullable=False)  # INTEGER
    CANAUTONUM = Column('CANAUTONUM', Integer, nullable=False)  # YORN
    CLASSNAME = Column('CLASSNAME', String(256))  # ALN
    COLUMNNAME = Column('COLUMNNAME', String(30))  # UPPER
    DEFAULTVALUE = Column('DEFAULTVALUE', String(50))  # ALN
    DOMAINID = Column('DOMAINID', String(22))  # UPPER
    EAUDITENABLED = Column('EAUDITENABLED', Integer, nullable=False)  # YORN
    ENTITYNAME = Column('ENTITYNAME', String(30))  # UPPER
    ESIGENABLED = Column('ESIGENABLED', Integer, nullable=False)  # YORN
    ISLDOWNER = Column('ISLDOWNER', Integer, nullable=False)  # YORN
    ISPOSITIVE = Column('ISPOSITIVE', Integer, nullable=False)  # YORN
    LENGTH = Column('LENGTH', Integer, nullable=False)  # INTEGER
    MAXTYPE = Column('MAXTYPE', String(8), nullable=False)  # UPPER
    MUSTBE = Column('MUSTBE', Integer, nullable=False)  # YORN
    REQUIRED = Column('REQUIRED', Integer, nullable=False)  # YORN
    PERSISTENT = Column('PERSISTENT', Integer, nullable=False)  # YORN
    PRIMARYKEYCOLSEQ = Column('PRIMARYKEYCOLSEQ', Integer)  # INTEGER
    REMARKS = Column('REMARKS', String(4000), nullable=False)  # ALN
    SAMEASATTRIBUTE = Column('SAMEASATTRIBUTE', String(50))  # UPPER
    SAMEASOBJECT = Column('SAMEASOBJECT', String(30))  # UPPER
    SCALE = Column('SCALE', Integer, nullable=False)  # INTEGER
    TITLE = Column('TITLE', String(118), nullable=False)  # ALN
    USERDEFINED = Column('USERDEFINED', Integer, nullable=False)  # YORN
    SEARCHTYPE = Column('SEARCHTYPE', String(20), nullable=False)  # ALN
    MLSUPPORTED = Column('MLSUPPORTED', Integer, nullable=False)  # YORN
    MLINUSE = Column('MLINUSE', Integer, nullable=False)  # YORN
    HANDLECOLUMNNAME = Column('HANDLECOLUMNNAME', String(30))  # UPPER
    MAXATTRIBUTEID = Column('MAXATTRIBUTEID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    RESTRICTED = Column('RESTRICTED', Integer, nullable=False)  # YORN
    LOCALIZABLE = Column('LOCALIZABLE', Integer, nullable=False)  # YORN
    TEXTDIRECTION = Column('TEXTDIRECTION', String(20))  # ALN
    COMPLEXEXPRESSION = Column('COMPLEXEXPRESSION', String(20))  # UPPER
    EXTENDED = Column('EXTENDED', Integer)  # INTEGER
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXATTRIBUTECFG(Base):
    """Maximo Attribute Configuration""" 
    __tablename__ = 'MAXATTRIBUTECFG'
    __table_args__ = {'schema': 'MAXIMO'}

    OBJECTNAME = Column('OBJECTNAME', String(30), nullable=False)  # UPPER
    ATTRIBUTENAME = Column('ATTRIBUTENAME', String(50), nullable=False)  # UPPER
    ALIAS = Column('ALIAS', String(50))  # ALN
    AUTOKEYNAME = Column('AUTOKEYNAME', String(40))  # UPPER
    ATTRIBUTENO = Column('ATTRIBUTENO', Integer, nullable=False)  # INTEGER
    CANAUTONUM = Column('CANAUTONUM', Integer, nullable=False)  # YORN
    CLASSNAME = Column('CLASSNAME', String(256))  # ALN
    COLUMNNAME = Column('COLUMNNAME', String(30))  # UPPER
    DEFAULTVALUE = Column('DEFAULTVALUE', String(50))  # ALN
    DOMAINID = Column('DOMAINID', String(22))  # UPPER
    EAUDITENABLED = Column('EAUDITENABLED', Integer, nullable=False)  # YORN
    ENTITYNAME = Column('ENTITYNAME', String(30))  # UPPER
    ESIGENABLED = Column('ESIGENABLED', Integer, nullable=False)  # YORN
    ISLDOWNER = Column('ISLDOWNER', Integer, nullable=False)  # YORN
    ISPOSITIVE = Column('ISPOSITIVE', Integer, nullable=False)  # YORN
    LENGTH = Column('LENGTH', Integer, nullable=False)  # INTEGER
    MAXTYPE = Column('MAXTYPE', String(8), nullable=False)  # UPPER
    MUSTBE = Column('MUSTBE', Integer, nullable=False)  # YORN
    REQUIRED = Column('REQUIRED', Integer, nullable=False)  # YORN
    PERSISTENT = Column('PERSISTENT', Integer, nullable=False)  # YORN
    PRIMARYKEYCOLSEQ = Column('PRIMARYKEYCOLSEQ', Integer)  # INTEGER
    REMARKS = Column('REMARKS', String(4000), nullable=False)  # ALN
    SAMEASATTRIBUTE = Column('SAMEASATTRIBUTE', String(50))  # UPPER
    SAMEASOBJECT = Column('SAMEASOBJECT', String(30))  # UPPER
    SCALE = Column('SCALE', Integer, nullable=False)  # INTEGER
    TITLE = Column('TITLE', String(118), nullable=False)  # ALN
    USERDEFINED = Column('USERDEFINED', Integer, nullable=False)  # YORN
    CHANGED = Column('CHANGED', String(1), nullable=False)  # ALN
    SEARCHTYPE = Column('SEARCHTYPE', String(20), nullable=False)  # ALN
    MLSUPPORTED = Column('MLSUPPORTED', Integer, nullable=False)  # YORN
    MLINUSE = Column('MLINUSE', Integer, nullable=False)  # YORN
    HANDLECOLUMNNAME = Column('HANDLECOLUMNNAME', String(30))  # UPPER
    MAXATTRIBUTEID = Column('MAXATTRIBUTEID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    RESTRICTED = Column('RESTRICTED', Integer, nullable=False)  # YORN
    LOCALIZABLE = Column('LOCALIZABLE', Integer, nullable=False)  # YORN
    TEXTDIRECTION = Column('TEXTDIRECTION', String(20))  # ALN
    COMPLEXEXPRESSION = Column('COMPLEXEXPRESSION', String(20))  # UPPER
    EXTENDED = Column('EXTENDED', Integer)  # INTEGER
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXDOMAIN(Base):
    """Definition of a domain or set of values.""" 
    __tablename__ = 'MAXDOMAIN'
    __table_args__ = {'schema': 'MAXIMO'}

    DOMAINID = Column('DOMAINID', String(22), nullable=False)  # UPPER
    DESCRIPTION = Column('DESCRIPTION', String(100))  # ALN
    DOMAINTYPE = Column('DOMAINTYPE', String(20), nullable=False)  # UPPER
    MAXTYPE = Column('MAXTYPE', String(8))  # UPPER
    LENGTH = Column('LENGTH', Integer)  # INTEGER
    SCALE = Column('SCALE', Integer)  # INTEGER
    MAXDOMAINID = Column('MAXDOMAINID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    INTERNAL = Column('INTERNAL', Integer, nullable=False)  # INTEGER
    NEVERCACHE = Column('NEVERCACHE', Integer)  # YORN
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXOBJECT(Base):
    """Maximo Object""" 
    __tablename__ = 'MAXOBJECT'
    __table_args__ = {'schema': 'MAXIMO'}

    OBJECTNAME = Column('OBJECTNAME', String(30), nullable=False)  # UPPER
    CLASSNAME = Column('CLASSNAME', String(256))  # ALN
    DESCRIPTION = Column('DESCRIPTION', String(119), nullable=False)  # ALN
    EAUDITENABLED = Column('EAUDITENABLED', Integer, nullable=False)  # YORN
    EAUDITFILTER = Column('EAUDITFILTER', String(254))  # ALN
    ENTITYNAME = Column('ENTITYNAME', String(30))  # UPPER
    ESIGFILTER = Column('ESIGFILTER', String(254))  # ALN
    EXTENDSOBJECT = Column('EXTENDSOBJECT', String(30))  # UPPER
    IMPORTED = Column('IMPORTED', Integer, nullable=False)  # YORN
    ISVIEW = Column('ISVIEW', Integer, nullable=False)  # YORN
    PERSISTENT = Column('PERSISTENT', Integer, nullable=False)  # YORN
    SERVICENAME = Column('SERVICENAME', String(18), nullable=False)  # UPPER
    SITEORGTYPE = Column('SITEORGTYPE', String(18), nullable=False)  # UPPER
    USERDEFINED = Column('USERDEFINED', Integer, nullable=False)  # YORN
    MAINOBJECT = Column('MAINOBJECT', Integer, nullable=False)  # YORN
    INTERNAL = Column('INTERNAL', Integer, nullable=False)  # YORN
    MAXOBJECTID = Column('MAXOBJECTID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    TEXTDIRECTION = Column('TEXTDIRECTION', String(20))  # ALN
    RESOURCETYPE = Column('RESOURCETYPE', String(20))  # UPPER
    HASLD = Column('HASLD', Integer, nullable=False)  # YORN
    LANGCODE = Column('LANGCODE', String(4), nullable=False)  # UPPER
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXOBJECTCFG(Base):
    """Maximo Object Configuration""" 
    __tablename__ = 'MAXOBJECTCFG'
    __table_args__ = {'schema': 'MAXIMO'}

    OBJECTNAME = Column('OBJECTNAME', String(30), nullable=False)  # UPPER
    CLASSNAME = Column('CLASSNAME', String(256))  # ALN
    DESCRIPTION = Column('DESCRIPTION', String(119), nullable=False)  # ALN
    EAUDITENABLED = Column('EAUDITENABLED', Integer, nullable=False)  # YORN
    EAUDITFILTER = Column('EAUDITFILTER', String(254))  # ALN
    ENTITYNAME = Column('ENTITYNAME', String(30))  # UPPER
    ESIGFILTER = Column('ESIGFILTER', String(254))  # ALN
    EXTENDSOBJECT = Column('EXTENDSOBJECT', String(30))  # UPPER
    IMPORTED = Column('IMPORTED', Integer, nullable=False)  # YORN
    ISVIEW = Column('ISVIEW', Integer, nullable=False)  # YORN
    PERSISTENT = Column('PERSISTENT', Integer, nullable=False)  # YORN
    SERVICENAME = Column('SERVICENAME', String(18), nullable=False)  # UPPER
    SITEORGTYPE = Column('SITEORGTYPE', String(18), nullable=False)  # UPPER
    USERDEFINED = Column('USERDEFINED', Integer, nullable=False)  # YORN
    CHANGED = Column('CHANGED', String(1), nullable=False)  # ALN
    MAINOBJECT = Column('MAINOBJECT', Integer, nullable=False)  # YORN
    INTERNAL = Column('INTERNAL', Integer, nullable=False)  # YORN
    MAXOBJECTID = Column('MAXOBJECTID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    TEXTDIRECTION = Column('TEXTDIRECTION', String(20))  # ALN
    RESOURCETYPE = Column('RESOURCETYPE', String(20))  # UPPER
    HASLD = Column('HASLD', Integer, nullable=False)  # YORN
    LANGCODE = Column('LANGCODE', String(4), nullable=False)  # UPPER
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXPROP(Base):
    """Maximo Properties""" 
    __tablename__ = 'MAXPROP'
    __table_args__ = {'schema': 'MAXIMO'}

    MAXPROPID = Column('MAXPROPID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    PROPNAME = Column('PROPNAME', String(50), nullable=False)  # ALN
    DESCRIPTION = Column('DESCRIPTION', String(192), nullable=False)  # ALN
    MAXTYPE = Column('MAXTYPE', String(8), nullable=False)  # UPPER
    GLOBALONLY = Column('GLOBALONLY', Integer, nullable=False)  # YORN
    INSTANCEONLY = Column('INSTANCEONLY', Integer, nullable=False)  # YORN
    MAXIMODEFAULT = Column('MAXIMODEFAULT', String(512))  # ALN
    LIVEREFRESH = Column('LIVEREFRESH', Integer, nullable=False)  # YORN
    ENCRYPTED = Column('ENCRYPTED', Integer, nullable=False)  # YORN
    DOMAINID = Column('DOMAINID', String(22))  # UPPER
    NULLSALLOWED = Column('NULLSALLOWED', Integer, nullable=False)  # YORN
    SECURELEVEL = Column('SECURELEVEL', String(20), nullable=False)  # ALN
    USERDEFINED = Column('USERDEFINED', Integer, nullable=False)  # YORN
    ONLINECHANGES = Column('ONLINECHANGES', Integer, nullable=False)  # YORN
    CHANGEBY = Column('CHANGEBY', String(60), nullable=False)  # ALN
    CHANGEDATE = Column('CHANGEDATE', DateTime, nullable=False)  # DATETIME
    MASKED = Column('MASKED', Integer, nullable=False)  # YORN
    ACCESSTYPE = Column('ACCESSTYPE', Integer)  # INTEGER
    VALUERULES = Column('VALUERULES', String(50))  # UPPER
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXPROPVALUE(Base):
    """Maximo Property Values""" 
    __tablename__ = 'MAXPROPVALUE'
    __table_args__ = {'schema': 'MAXIMO'}

    MAXPROPVALUEID = Column('MAXPROPVALUEID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    PROPNAME = Column('PROPNAME', String(50), nullable=False)  # ALN
    SERVERNAME = Column('SERVERNAME', String(100), nullable=False)  # ALN
    SERVERHOST = Column('SERVERHOST', String(100))  # ALN
    PROPVALUE = Column('PROPVALUE', String(512))  # ALN
    ENCRYPTEDVALUE = Column('ENCRYPTEDVALUE', VARBINARY(1840))  # CRYPTO
    CHANGEBY = Column('CHANGEBY', String(60), nullable=False)  # ALN
    CHANGEDATE = Column('CHANGEDATE', DateTime, nullable=False)  # DATETIME
    ACCESSTYPE = Column('ACCESSTYPE', Integer)  # INTEGER
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXSEQUENCE(Base):
    """Records UniqueID Sequence Reservations.""" 
    __tablename__ = 'MAXSEQUENCE'
    __table_args__ = {'schema': 'MAXIMO'}

    TBNAME = Column('TBNAME', String(30), nullable=False)  # UPPER
    NAME = Column('NAME', String(30), nullable=False)  # UPPER
    MAXRESERVED = Column('MAXRESERVED', BigInteger, nullable=False)  # BIGINT
    MAXVALUE = Column('MAXVALUE', BigInteger)  # BIGINT
    RANGE = Column('RANGE', BigInteger)  # BIGINT
    SEQUENCENAME = Column('SEQUENCENAME', String(30), nullable=False)  # UPPER
    MAXSEQUENCEID = Column('MAXSEQUENCEID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXSERVICE(Base):
    """Java Services""" 
    __tablename__ = 'MAXSERVICE'
    __table_args__ = {'schema': 'MAXIMO'}

    SERVICENAME = Column('SERVICENAME', String(18), nullable=False)  # UPPER
    DESCRIPTION = Column('DESCRIPTION', String(100))  # ALN
    CLASSNAME = Column('CLASSNAME', String(256), nullable=False)  # ALN
    MAXSERVICEID = Column('MAXSERVICEID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    INITORDER = Column('INITORDER', Integer, nullable=False)  # INTEGER
    INTERNAL = Column('INTERNAL', Integer, nullable=False)  # YORN
    ACTIVE = Column('ACTIVE', Integer, nullable=False)  # YORN
    SINGLETON = Column('SINGLETON', Integer)  # YORN
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXSYSINDEXES(Base):
    """The MAXSYSINDEXES Table""" 
    __tablename__ = 'MAXSYSINDEXES'
    __table_args__ = {'schema': 'MAXIMO'}

    NAME = Column('NAME', String(30), nullable=False)  # UPPER
    TBNAME = Column('TBNAME', String(30), nullable=False)  # UPPER
    UNIQUERULE = Column('UNIQUERULE', String(1), nullable=False)  # UPPER
    CHANGED = Column('CHANGED', String(1))  # ALN
    CLUSTERRULE = Column('CLUSTERRULE', Integer, nullable=False)  # YORN
    STORAGEPARTITION = Column('STORAGEPARTITION', String(30))  # ALN
    REQUIRED = Column('REQUIRED', Integer, nullable=False)  # YORN
    TEXTSEARCH = Column('TEXTSEARCH', Integer, nullable=False)  # YORN
    MAXSYSINDEXESID = Column('MAXSYSINDEXESID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXSYSKEYS(Base):
    """The MAXSYSKEYS Table""" 
    __tablename__ = 'MAXSYSKEYS'
    __table_args__ = {'schema': 'MAXIMO'}

    IXNAME = Column('IXNAME', String(30), nullable=False)  # UPPER
    COLNAME = Column('COLNAME', String(30), nullable=False)  # UPPER
    COLSEQ = Column('COLSEQ', Integer, nullable=False)  # SMALLINT
    ORDERING = Column('ORDERING', String(1), nullable=False)  # UPPER
    CHANGED = Column('CHANGED', String(1))  # ALN
    MAXSYSKEYSID = Column('MAXSYSKEYSID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXTABLE(Base):
    """Maximo Table""" 
    __tablename__ = 'MAXTABLE'
    __table_args__ = {'schema': 'MAXIMO'}

    TABLENAME = Column('TABLENAME', String(30), nullable=False)  # UPPER
    ADDROWSTAMP = Column('ADDROWSTAMP', Integer, nullable=False)  # YORN
    EAUDITTBNAME = Column('EAUDITTBNAME', String(30))  # UPPER
    ISAUDITTABLE = Column('ISAUDITTABLE', Integer, nullable=False)  # YORN
    RESTOREDATA = Column('RESTOREDATA', Integer, nullable=False)  # YORN
    STORAGEPARTITION = Column('STORAGEPARTITION', String(30))  # ALN
    TEXTSEARCHENABLED = Column('TEXTSEARCHENABLED', Integer, nullable=False)  # YORN
    LANGTABLENAME = Column('LANGTABLENAME', String(30))  # UPPER
    LANGCOLUMNNAME = Column('LANGCOLUMNNAME', String(30))  # UPPER
    UNIQUECOLUMNNAME = Column('UNIQUECOLUMNNAME', String(30))  # UPPER
    ISLANGTABLE = Column('ISLANGTABLE', Integer, nullable=False)  # YORN
    MAXTABLEID = Column('MAXTABLEID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ALTIXNAME = Column('ALTIXNAME', String(30))  # UPPER
    TRIGROOT = Column('TRIGROOT', String(29), nullable=False)  # UPPER
    CONTENTATTRIBUTE = Column('CONTENTATTRIBUTE', String(30))  # UPPER
    STORAGETYPE = Column('STORAGETYPE', Integer, nullable=False)  # INTEGER
    EXTTABLENAME = Column('EXTTABLENAME', String(30))  # UPPER
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXTABLECFG(Base):
    """Maximo Table Configuration""" 
    __tablename__ = 'MAXTABLECFG'
    __table_args__ = {'schema': 'MAXIMO'}

    TABLENAME = Column('TABLENAME', String(30), nullable=False)  # UPPER
    ADDROWSTAMP = Column('ADDROWSTAMP', Integer, nullable=False)  # YORN
    EAUDITTBNAME = Column('EAUDITTBNAME', String(30))  # UPPER
    ISAUDITTABLE = Column('ISAUDITTABLE', Integer, nullable=False)  # YORN
    RESTOREDATA = Column('RESTOREDATA', Integer, nullable=False)  # YORN
    STORAGEPARTITION = Column('STORAGEPARTITION', String(30))  # ALN
    TEXTSEARCHENABLED = Column('TEXTSEARCHENABLED', Integer, nullable=False)  # YORN
    LANGTABLENAME = Column('LANGTABLENAME', String(30))  # UPPER
    LANGCOLUMNNAME = Column('LANGCOLUMNNAME', String(30))  # UPPER
    UNIQUECOLUMNNAME = Column('UNIQUECOLUMNNAME', String(30))  # UPPER
    ISLANGTABLE = Column('ISLANGTABLE', Integer, nullable=False)  # YORN
    MAXTABLEID = Column('MAXTABLEID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ALTIXNAME = Column('ALTIXNAME', String(30))  # UPPER
    TRIGROOT = Column('TRIGROOT', String(29), nullable=False)  # UPPER
    CONTENTATTRIBUTE = Column('CONTENTATTRIBUTE', String(30))  # UPPER
    STORAGETYPE = Column('STORAGETYPE', Integer, nullable=False)  # INTEGER
    EXTTABLENAME = Column('EXTTABLENAME', String(30))  # UPPER
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXTABLEDOMAIN(Base):
    """Defines a MAXIMO table type of value domain""" 
    __tablename__ = 'MAXTABLEDOMAIN'
    __table_args__ = {'schema': 'MAXIMO'}

    DOMAINID = Column('DOMAINID', String(22), nullable=False)  # UPPER
    VALIDTNWHERECLAUSE = Column('VALIDTNWHERECLAUSE', String(4000))  # ALN
    LISTWHERECLAUSE = Column('LISTWHERECLAUSE', String(4000))  # ALN
    ERRORRESOURCBUNDLE = Column('ERRORRESOURCBUNDLE', String(50))  # ALN
    ERRORACCESSKEY = Column('ERRORACCESSKEY', String(50))  # ALN
    OBJECTNAME = Column('OBJECTNAME', String(30), nullable=False)  # UPPER
    SITEID = Column('SITEID', String(8))  # UPPER
    ORGID = Column('ORGID', String(8))  # UPPER
    MAXTABLEDOMAINID = Column('MAXTABLEDOMAINID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXVARS(Base):
    """The MAXVARS Table""" 
    __tablename__ = 'MAXVARS'
    __table_args__ = {'schema': 'MAXIMO'}

    VARNAME = Column('VARNAME', String(18), nullable=False)  # ALN
    VARVALUE = Column('VARVALUE', String(254))  # ALN
    ORGID = Column('ORGID', String(8))  # UPPER
    SITEID = Column('SITEID', String(8))  # UPPER
    MAXVARSID = Column('MAXVARSID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    VARTYPE = Column('VARTYPE', String(6))  # ALN
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXVARTYPE(Base):
    """Identifies the domain of a MaxVar""" 
    __tablename__ = 'MAXVARTYPE'
    __table_args__ = {'schema': 'MAXIMO'}

    VARNAME = Column('VARNAME', String(18), nullable=False)  # ALN
    VARTYPE = Column('VARTYPE', String(6), nullable=False)  # ALN
    DEFAULTVALUE = Column('DEFAULTVALUE', String(254))  # ALN
    DESCRIPTION = Column('DESCRIPTION', String(150))  # ALN
    MAXVARTYPEID = Column('MAXVARTYPEID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXVIEWCFG(Base):
    """Maximo View Configuration""" 
    __tablename__ = 'MAXVIEWCFG'
    __table_args__ = {'schema': 'MAXIMO'}

    VIEWNAME = Column('VIEWNAME', String(30), nullable=False)  # UPPER
    VIEWSELECT = Column('VIEWSELECT', String(4000))  # ALN
    VIEWWHERE = Column('VIEWWHERE', String(4000))  # ALN
    AUTOSELECT = Column('AUTOSELECT', Integer, nullable=False)  # YORN
    MAXVIEWID = Column('MAXVIEWID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    VIEWFROM = Column('VIEWFROM', String(1000))  # ALN
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_MAXVIEWCOLUMNCFG(Base):
    """Maximo View Column Configuration""" 
    __tablename__ = 'MAXVIEWCOLUMNCFG'
    __table_args__ = {'schema': 'MAXIMO'}

    VIEWNAME = Column('VIEWNAME', String(30), nullable=False)  # UPPER
    VIEWCOLUMNNAME = Column('VIEWCOLUMNNAME', String(30), nullable=False)  # UPPER
    SAMESTORAGEAS = Column('SAMESTORAGEAS', String(30))  # UPPER
    TABLENAME = Column('TABLENAME', String(30))  # UPPER
    TABLECOLUMNNAME = Column('TABLECOLUMNNAME', String(30))  # UPPER
    CHANGED = Column('CHANGED', String(1), nullable=False)  # ALN
    MAXVIEWCOLUMNID = Column('MAXVIEWCOLUMNID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_NUMERICDOMAIN(Base):
    """Numeric type domain""" 
    __tablename__ = 'NUMERICDOMAIN'
    __table_args__ = {'schema': 'MAXIMO'}

    DOMAINID = Column('DOMAINID', String(22), nullable=False)  # UPPER
    VALUE = Column('VALUE', Numeric(30, 10), nullable=False)  # DECIMAL
    DESCRIPTION = Column('DESCRIPTION', String(124))  # ALN
    SITEID = Column('SITEID', String(8))  # UPPER
    ORGID = Column('ORGID', String(8))  # UPPER
    NUMERICDOMAINID = Column('NUMERICDOMAINID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    VALUEID = Column('VALUEID', String(300), nullable=False)  # ALN
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_NUMRANGEDOMAIN(Base):
    """Domain for number range""" 
    __tablename__ = 'NUMRANGEDOMAIN'
    __table_args__ = {'schema': 'MAXIMO'}

    RANGESEGMENT = Column('RANGESEGMENT', Integer, nullable=False)  # SMALLINT
    DOMAINID = Column('DOMAINID', String(22), nullable=False)  # UPPER
    RANGEMINIMUM = Column('RANGEMINIMUM', Float)  # FLOAT
    RANGEMAXIMUM = Column('RANGEMAXIMUM', Float)  # FLOAT
    RANGEINTERVAL = Column('RANGEINTERVAL', Float)  # FLOAT
    SITEID = Column('SITEID', String(8))  # UPPER
    ORGID = Column('ORGID', String(8))  # UPPER
    NUMRANGEDOMAINID = Column('NUMRANGEDOMAINID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP

class T_SYNONYMDOMAIN(Base):
    """Definition of synonym value domain""" 
    __tablename__ = 'SYNONYMDOMAIN'
    __table_args__ = {'schema': 'MAXIMO'}

    DOMAINID = Column('DOMAINID', String(22), nullable=False)  # UPPER
    MAXVALUE = Column('MAXVALUE', String(50), nullable=False)  # ALN
    VALUE = Column('VALUE', String(50), nullable=False)  # ALN
    DESCRIPTION = Column('DESCRIPTION', String(256))  # ALN
    DEFAULTS = Column('DEFAULTS', Integer, nullable=False)  # YORN
    SITEID = Column('SITEID', String(8))  # UPPER
    ORGID = Column('ORGID', String(8))  # UPPER
    SYNONYMDOMAINID = Column('SYNONYMDOMAINID', BigInteger, primary_key=True, autoincrement=False, nullable=False)  # BIGINT
    VALUEID = Column('VALUEID', String(256), nullable=False)  # ALN
    ODK_ISOLATIONFLAG = Column('ODK_ISOLATIONFLAG', Integer, nullable=False)  # YORN
    ROWSTAMP = Column('ROWSTAMP', BigInteger, nullable=False)  # ROWSTAMP


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