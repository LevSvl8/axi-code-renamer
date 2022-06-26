from pathlib import Path
import re
from axi_renamer.renamer_starter import Renamer, code_rename_map
from axi_renamer.constant_maps import pkg_map_for_folders
import os


class FolderHandler:
    def __init__(self, in_folder, out_folder, rename=False, valid_suffixes:list=None, process_files:list=None,
                       delete_sourcefile=False, target='CODE'):
        self.renamer = Renamer(target=target)
        self.root_folder = in_folder
        self.root_out_folder = out_folder
        self.valid_suffixes = valid_suffixes
        self.process_files = process_files
        self.delete_sourcefile = delete_sourcefile
        if rename:
            if delete_sourcefile:
                print('Rename & remove mode')
            else:
                print('Rename & copy mode')

        elif delete_sourcefile:
            print('Move mode')
        else:
            print('Copy mode')

    def simple_replace(self):
        self.replace_in_file_tree(self.root_folder)

    def make_renamed_dir(self, current_folder):
        relative_path = Path(current_folder).relative_to(self.root_folder)
        relative_path_str = str(relative_path)
        for row in code_rename_map:
            relative_path_str = re.sub(row[0], row[1], relative_path_str)
        relative_path_str = relative_path_str.replace('\\', '/')
        for row in pkg_map_for_folders:
            relative_path_str = re.sub(row[0], row[1], relative_path_str)
        os.path.normpath(relative_path_str)
        out_path = os.path.join(self.root_out_folder, relative_path_str)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        return out_path

    def need_to_process_file(self, file_fullname):
        if self.valid_suffixes and os.path.splitext(file_fullname)[1] not in self.valid_suffixes:
            return False

        if not self.process_files:
            return True
        b = False
        for process_file in self.process_files:
            try:
                file_fullname.index(process_file)
                b = True
                break
            except:
                continue
        return b

    def replace_in_file_tree(self, current_folder):
        files = os.listdir(current_folder)

        for file in files:
            full_name = os.path.join(current_folder, file)
            if os.path.isfile(full_name):

                if self.need_to_process_file(full_name):
                    print('Process File: ' + full_name)
                    infile = open(full_name, 'rt', encoding='UTF-8')
                    data = infile.read()
                    new_filename = str(file)

                    #Переименование файла
                    new_filename = self.renamer.get_axi_val(new_filename)

                    # Переименование других вхождений в тексте кода
                    data = self.renamer.get_axi_val(data, content_type='code')

                    # Создание переименованной директории
                    out_folder = self.make_renamed_dir(current_folder)

                    # Запись переименованнного файла
                    outfile = open(os.path.join(out_folder, new_filename), 'wt', encoding='UTF-8')
                    outfile.write(data)
                    infile.close()
                    outfile.close()

                    # Удаление исходного файла при включенной опции удаления (в т.ч. для удаления неиспользуемых файлов)
                    if self.delete_sourcefile:
                        os.remove(full_name)
            else:
                self.replace_in_file_tree(full_name)

    def free_find(self, reg_list):
        self.free_find_in_file_tree(reg_list, self.root_folder)

    def free_find_in_file_tree(self, reg_list, current_folder):
        files = os.listdir(current_folder)

        for file in files:
            full_name = os.path.join(current_folder, file)
            if os.path.isfile(full_name):

                if self.need_to_process_file(full_name):

                    infile = open(full_name, 'rt', encoding='UTF-8')
                    data = infile.read()
                    for reg in reg_list:
                        occurences = re.findall(reg, data, flags=re.IGNORECASE)
                        if bool(occurences):
                            occurences = list(set(occurences))
                            print('File: ' + full_name)
                            print(occurences)
            else:
                self.free_find_in_file_tree(reg_list, full_name)

