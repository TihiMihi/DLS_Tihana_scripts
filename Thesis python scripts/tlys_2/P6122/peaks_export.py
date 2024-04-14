
import pdb
import numpy as np

import json
import os
import re
import csv

def extract_numeric_part(s):
    match = re.search(r'\d+', s)
    if match:
        return int(match.group())
    return float('inf')

def find_indices(list_to_check, item_to_find):
    array = np.array(list_to_check)
    indices = np.where(array == item_to_find)[0]
    return list(indices)
    
single_pth='/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/P6122/anacor'
prefix='auto'
data_list=[]
for dir_pth in os.listdir(single_pth):
    if os.path.isdir(os.path.join(single_pth, dir_pth)) is False:
        continue
    
    data_list.append(dir_pth)

sorted_data_list = sorted(data_list)

dataset_list= sorted_data_list
#single_num=len(sorted_data_list)
single_num=len(data_list)
print(dataset_list)


for dir_pth in (dataset_list):
    final_result=[['method','ZN_A:ZN405','ZN_B:ZN405','ZN_C:ZN405','ZN_D:ZN405','ZN_E:ZN405','ZN_F:ZN405','ZN_G:ZN405','ZN_H:ZN405','ZN_I:ZN405','ZN_J:ZN405','ZN_K:ZN405','ZN_L:ZN405','SD_A:MET205', 'SD_B:MET205', 'SD_C:MET205', 'SD_D:MET205', 'SD_E:MET205', 'SD_F:MET205', 'SD_G:MET205', 'SD_H:MET205', 'SD_I:MET205', 'SD_J:MET205', 'SD_K:MET205', 'SD_L:MET205', 'SD_A:MET120', 'SD_B:MET120', 'SD_C:MET120', 'SD_D:MET120', 'SD_E:MET120', 'SD_F:MET120', 'SD_G:MET120', 'SD_H:MET120','SD_I:MET120', 'SD_J:MET120', 'SD_K:MET120', 'SD_L:MET120']]
    counter=0
    atoms_to_find = final_result[0][1:]

    for target in ['acsh','sh', 'ac']:
        
        i = dataset_list.index(dir_pth)
        try:
            if i < single_num:
                with open(os.path.join( single_pth ,dir_pth ,'dimple',target,'anode.lsa'), 'r') as file:
                    lines = file.readlines()

        except:
            continue
            
        # Find the start and end indices of the table
        start_index = None
        end_index = None
        for i, line in enumerate(lines):
            if '          X        Y        Z   Height(sig)  SOF     Nearest atom' in line:
                start_index = i + 2#1
                
            elif 'Peaks output to file' in line:
                end_index = i - 1
                
        print(f'{dir_pth}, {target}')
        
        table_data = []
        atom_list = []
        peak_list = []
        for line in lines[start_index:end_index]:
            #print(line)
            
            # Remove leading/trailing whitespaces and split the line into columns
            columns = line.strip().split()
            atom_list.append(columns[-1])
            peak_list.append(columns[4])

            # Convert the columns to floats
            row_data = [col for col in columns]
            table_data.append(row_data)
        
        # Convert the table data to a NumPy array
        #table_array = np.array(table_data)
        row=[f'method:{target}:']

        for label in atoms_to_find:

            if atom_list.count(label) > 1:
                indexes = (np.where(np.array(atom_list) == label))[0]#.tolist()
                #duplicate_peaks = peak_list[atom_list.index('ZN_C:ZN405')]
                duplicate_peaks = np.array(peak_list)[indexes]
                duplicate_peaks = np.asarray(duplicate_peaks, dtype=float)
                max_peak = np.max((duplicate_peaks))
                row.append(str(max_peak))

            elif atom_list.count(label) == 1:
                row.append(peak_list[atom_list.index(label)])
            
            elif any(atom == label for atom in atom_list) == False:
                row.append('nan')

        final_result.append(row)

        dataset_filename = f'/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/{dir_pth}_peaks.csv'.format(target)
        with open(dataset_filename, 'w') as dataset_file:
            writer = csv.writer(dataset_file)
            for r in final_result:
                writer.writerow(r)
        dataset_file.close()

