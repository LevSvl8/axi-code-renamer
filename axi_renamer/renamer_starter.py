import re
from axi_renamer.mapping_reader import get_name_mapping
from axi_renamer.constant_maps import pkg_map_for_folders
from axi_renamer.smart_rename import smart_rename

vars_map = get_name_mapping('rename_vars_and_prop.csv') # название различных переменных и свойств, которые храняться в БД и используются в коде
pkg_map_for_content = get_name_mapping('rename_pkg.csv') # маппинг имен пакетов
db_object_rename_map = get_name_mapping('rename_db_object.csv') # названия имен объектов и атрибутов, таблиц и столбцов БД
#mx_object_rename_map = get_name_mapping('rename_mx.csv') # значения с префиксом mx
class_name_map = get_name_mapping('rename_class_name.csv') # локальные переменные в коде
code_rename_map = get_name_mapping('rename_in_code.csv') # локальные переменные в коде
other_place_rename_map = get_name_mapping('rename_other.csv') # другие файлы и значения
excluded_classes_map = get_name_mapping('rename_exceptions.csv') # замена исключенных классов на стандартные в ссылках в базе данных
exception_map = get_name_mapping('rename_exceptions.csv') # обратное переименование исключений

CASE_SENCETIVE = True
CASE_INSENCETIVE = False
class Renamer:
    def __new__(cls, target='CODE'):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Renamer, cls).__new__(cls)
            cls.instance.reversible_maps = [db_object_rename_map]

            if target=='CODE':
                cls.instance.all_maps = [
                    [other_place_rename_map, CASE_SENCETIVE],
                    [pkg_map_for_content, CASE_SENCETIVE],
                    [class_name_map, CASE_SENCETIVE],
                    [code_rename_map, CASE_SENCETIVE],
                    [vars_map, CASE_INSENCETIVE],
                    [db_object_rename_map, CASE_INSENCETIVE],
                    [excluded_classes_map, CASE_SENCETIVE],
                    [exception_map, CASE_SENCETIVE],
                ]
            if target=='DB_SCHEMA':
                cls.instance.all_maps = [
                    [vars_map, CASE_INSENCETIVE],
                    [db_object_rename_map, CASE_INSENCETIVE],
                ]
            #cls.instance.check_reversible_maps()

        return cls.instance

    def add_mapping(self, mapping:list):
        self.all_maps.append(mapping)


    def get_max_val(self, data):
        for map in self.reversible_maps:
            if map.__len__():
                for row in map:
                    data = re.sub(row[1], row[0], data)
        return data

    def get_axi_val(self, data, content_type='code'):
        for row in pkg_map_for_folders:
            data = re.sub(row[0], row[1], data)
        for map_row in self.all_maps:
            map, casesence = map_row[0], map_row[1]
            if map.__len__():
                if casesence:
                    data = smart_rename(data, map, case_saver=False, with_parts=True)
                else:
                    if content_type == 'code':
                        data = smart_rename(data, map, case_saver=True, with_parts=True)
                    else:
                        data = smart_rename(data, map, case_saver=True, with_parts=False)
        return data

    def check_reversible_maps(self):
        for map in self.reversible_maps:
            for r in map:
                val = r[0]
                axival = Renamer().get_axi_val(val)
                maxval = Renamer().get_max_val(axival)
                if val != maxval:
                    raise Exception(f'Mapping error in reversible mapping file. Renaming is not reversible for value {val}: {maxval}')
