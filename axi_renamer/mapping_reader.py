import os
import csv

mapping_folder = '../axi_renamer/mapping/'


def get_name_mapping(filename):
    rows = []
    with open(os.path.join(mapping_folder, filename)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            rows.append(row)
    return rows


def getlist(filename):
    rows = []
    with open(os.path.join(mapping_folder, filename)) as csv_file:
        csv_reader = csv_file.read()
        rows = csv_reader.split('\n')
    return rows