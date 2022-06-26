from utils import get_never_copy_list

axi_never_copy_object = ', '.join(["'" + o + "'" for o in get_never_copy_list('axi_never_copy_object.csv')])
axi_never_copy_service = ', '.join(["'" + o + "'" for o in get_never_copy_list('axi_never_copy_service.csv')])
axi_never_copy_messages = ', '.join(["'" + o + "'" for o in get_never_copy_list('axi_never_copy_messages.csv')])

filter = {
'MAXSERVICE': f"servicename not in ({axi_never_copy_service})",
'MAXOBJECT': f"objectname not in ({axi_never_copy_object})",
'MAXOBJECTCFG': f"objectname not in ({axi_never_copy_object})",
'MAXATTRIBUTECFG': f"OBJECTNAME NOT IN ({axi_never_copy_object})",
'MAXATTRIBUTE': f"OBJECTNAME NOT IN ({axi_never_copy_object})",
'MAXSYSINDEXES': f"TBNAME IN (SELECT ENTITYNAME FROM MAXOBJECT m3 WHERE OBJECTNAME NOT IN ({axi_never_copy_object}))",
'MAXSYSKEYS': f"IXNAME IN (select NAME from MAXSYSINDEXES m WHERE TBNAME IN (SELECT ENTITYNAME FROM MAXOBJECT m3 WHERE OBJECTNAME NOT IN ({axi_never_copy_object})))",
'MAXTABLECFG': f"TABLENAME IN (SELECT ENTITYNAME FROM MAXOBJECT m3 WHERE OBJECTNAME NOT IN ({axi_never_copy_object}))",
#'MAXVIEWCFG': f"",
#'MAXVIEWCOLUMNCFG': f"",
#'MAXVARS': f"",
#'MAXVARTYPE': f"",
#'MAXPROP': f"",
#'MAXPROPVALUE': f"",
'L_MAXATTRCFG': f"OWNERID IN (SELECT MAXATTRIBUTEID FROM MAXATTRIBUTE m2 WHERE OBJECTNAME NOT IN ({axi_never_copy_object}))",
'L_MAXATTRIBUTE': f"OWNERID IN (SELECT MAXATTRIBUTEID FROM MAXATTRIBUTE m2 WHERE OBJECTNAME NOT IN ({axi_never_copy_object}))",
'MAXINTOBJECT': f"intobjectname not like '%APIWEATHER%'",
'MAXMESSAGES': f"msgid not in ({axi_never_copy_messages})",
'L_MAXMESSAGES': f"OWNERID IN (SELECT MAXMESSAGEID FROM MAXMESSAGES m2 WHERE msgid not in ({axi_never_copy_messages}))"
}