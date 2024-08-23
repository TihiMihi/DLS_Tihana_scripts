import pdb
import numpy as np

import json
import os
import re
import csv

anacor_path = '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/P6122/anacor'
dials_path  = '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/P6122/just_dials'
csv_path    = '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files'

data_list = []
for dataset_path in os.listdir(anacor_path):
    if os.path.isdir(os.path.join(anacor_path, dataset_path)) is True:
        data_list.append(dataset_path)
dataset = dataset_path.split("/")
dataset = dataset[-1]
dataset_list = sorted(data_list)
print(dataset_list)

for dir in (dataset_list):
    
    I_and_rmerge = []

    for target in ['ac','acsh', 'sh']:
        
        i = dataset_list.index(dir)
        if target == 'ac' or target == 'acsh':
            target_path = os.path.join(anacor_path, dir, f'{dir}_save_data','ResultData','dials_output',f'{dir}_{target}_log.log')
        elif target == 'sh':
            target_path = os.path.join(dials_path, dir, 'LogFiles','AUTOMATIC_DEFAULT_SCALE.log')
        
        if os.path.exists(target_path):
            print(f'{dir} {target} log  exists')
            with open(target_path, 'r') as file:
                lines = file.readlines()
        else:
            print(f'{dir} {target} log does not exist')
            break

        # Find the start and end indices of the table
        start_index = None
        end_index = None
        for i, line in enumerate(lines):
            if '-------------Summary of merging statistics--------------' in line:
                start_index = i + 2#1
                
            elif 'Writing html report to ' in line:
                end_index = i - 1

        for line in lines[start_index:end_index]:
            # Remove leading/trailing whitespaces and split the line into columns
            columns = line.strip().split()

            # Convert the columns to floats
            row_data = [col for col in columns]
            if row_data[0] == 'I/sigma':
                #I_list.append(f'\n{dir} :{target}: {float(row_data[1])}')
                I_and_rmerge.append(f'\n{dir} :{target}: {float(row_data[1])} ')
            if row_data[0] == 'Rmerge(I)':
                #rmerge_list.append(f'\n{dir} :{target}: {float(row_data[1])}')
                I_and_rmerge.append(f'{float(row_data[1])}')

        #print(f'{dir}, {target}, {I_list}, {rmerge_list}')
        #table_data.append(I_list)

    dataset_filename = f'{csv_path}/{dir}_I_and_r_merge.csv'#.format(target)
    with open(dataset_filename, 'w') as dataset_file:
        writer = csv.writer(dataset_file, delimiter=' ', escapechar=' ', quoting=csv.QUOTE_NONE)
        writer.writerow(I_and_rmerge)
            