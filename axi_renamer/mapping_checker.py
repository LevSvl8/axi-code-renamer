from axi_renamer.renamer_starter import Renamer
from axi_renamer.mapping_reader import get_name_mapping


if __name__ == '__main__':
    mapping = get_name_mapping('rename_db_object.csv')
    for r in mapping:
        val = r[0]
        axival = Renamer().get_axi_val(val)
        maxval = Renamer().get_max_val(axival)
        if val!= maxval:
            print('ERROR '+ val + maxval)