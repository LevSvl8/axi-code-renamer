import re
from axi_renamer.constant_maps import prefix_map

def smart_rename(data, rows, case_saver=False, with_parts=True):
    for row in rows:
        if not case_saver and with_parts:
            data = re.sub(row[0], row[1], data) #Простая замена найденных значений из csv
        else:
            if with_parts:
                regFind = row[0]
            else:
                regFind = r'(\W|^)(' + row[0] + ')(\W|$)'
            while(True):
                #re.findall(r'((\W)MAXVALUE(\W|$))', data, flags=re.IGNORECASE)
                occurences = re.findall(regFind, data, flags=re.IGNORECASE)
                if not bool(occurences):
                    break
                occurences = list(set(occurences))
                for occurence in occurences:
                    if with_parts:
                        old_val = occurence
                    else:
                        old_val = occurence[1]
                    if not case_saver:
                        newVal = row[1]
                    if case_saver:
                        if row.__len__() > 2 and row[2] == 'NORMAL':
                            newVal = old_val
                            prefix_size = row[3].__len__()
                            new_prefix = prefix_map.get(row[3])

                            index = 0
                            while index < prefix_size:
                                if newVal[index].isupper():
                                    newVal = newVal[:index] + new_prefix[index].upper() + newVal[index + 1:]
                                else:
                                    newVal = newVal[:index] + new_prefix[index].lower() + newVal[index + 1:]
                                index += 1
                        else:
                            #если замена кастомная, и при этом стоит case_saver, то заменяем слово целиком, регистр по первой букве
                            if old_val[0].isupper():
                                newVal = row[1].upper()
                            else:
                                newVal = row[1].lower()
                    if with_parts:
                        data = re.sub(old_val, newVal, data)
                    else:
                        start = '' if occurence[0] == '\\' else occurence[0]
                        end = '' if occurence[2] == '\\' else occurence[2]
                        data = re.sub(re.escape(start+occurence[1]+end), start+newVal+end, data)
    return data


if __name__ == '__main__':


    # case_saver - сохранение регистра, для стандартных мапировок 'MAXVALUE', 'AXIVALUE', 'NORMAL', 'MAX'
    # сохраняется регистр полностью, например, maxPropValue заменять на axiPropValue
    # для кастомных мапировок, то есть тех, для которых в третем столбце не задан 'NORMAL': 'BMXAA', 'AXIAA', ''
    # наследуется регистр первой буквы, например, BmxAA меняется на AXIAA
    case_saver = True

    with_parts = False # искать в части слова, а не только слово целиком

    data = '$MAXVALUE) bmxAa=$maxValue yMAXVALUE'
    rows = [['MAXVALUE', 'AXIVALUE', 'NORMAL', 'MAX'],
            ['BMXAA', 'AXIERR']]

    print(data)
    data = smart_rename(data, rows, case_saver, with_parts)
    print(data)