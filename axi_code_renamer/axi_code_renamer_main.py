from axi_code_renamer.folder_handler import FolderHandler
import os

mapping_folder = './filter/'


def getlist(filename):
    rows = []
    with open(os.path.join(mapping_folder, filename)) as csv_file:
        csv_reader = csv_file.read()
        rows = csv_reader.split('\n')
    return rows


if __name__ == '__main__':

    mode = 'REMOVE'
    in_folder = r'C:\Users\EAbashina\IdeaProjects\axicorede'
    renamed_folder = r'C:\Users\EAbashina\IdeaProjects\axicorede_maxrename'
    trash_folder = r'C:\Users\EAbashina\IdeaProjects\axicorede_removed'

    # файлы, попадающие под фильтр по имени process_files и расширению valid_suffixes копируются в папку out по
    # аналогичному относительному пути с заменой техкстовых включений по маппировке из файла max-rename.csv
    #TODO добавить список исключений отдельным файлом. Например pom.xml не должен перезаписываться
    if mode == 'RENAME':
        out_folder = renamed_folder
        #mapping = get_name_mapping('max-rename.csv')
        valid_suffixes = ['.java',]# '.xml']#['.properties']['.sh', '.bat', '.sql']
        process_files = ['Service']# ['AbstractShiftBucketDataSet']
        fh = FolderHandler(in_folder, out_folder, rename=True,
                                 process_files=process_files,
                                 valid_suffixes=valid_suffixes)

        fh.simple_replace()

    # файлы, попадающие под фильтр по имени remove_files.csv и расширению valid_suffixes удаляются из исходной папки и
    # переносятся в папку out по аналогичному относительному пути
    if mode == 'REMOVE':
        out_folder = trash_folder
        process_files = getlist('remove_files.csv')
        valid_suffixes = ['.java']
        fh = FolderHandler(in_folder, out_folder, process_files=process_files, valid_suffixes=valid_suffixes,
                                 delete_sourcefile=True)

        fh.simple_replace()

    # Все файлы, попадающие в папку "Корзина" с расширением valid_suffixes
    # переносятся в исходную папку по аналогичному относительному пути
    if mode == 'RESTORE':
        pass

    #Поиск в файлах текстовых вхождений по регулярному выражению
    if mode == 'FIND':
        in_folder = r'C:\Users\EAbashina\IdeaProjects\axicorede_maxrename'
        process_files = []
        valid_suffixes = ['.java']
        fh = FolderHandler(in_folder, in_folder, process_files=process_files, valid_suffixes=valid_suffixes)
        regFind = regFind = [r'(axi\w*length)', r'(axi\w*count)', r'(axi\w*value)']
        fh.free_find(regFind)
