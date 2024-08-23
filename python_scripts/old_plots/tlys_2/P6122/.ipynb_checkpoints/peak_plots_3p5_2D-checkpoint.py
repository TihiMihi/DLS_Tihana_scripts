import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


# Put the path to your data files here
file_paths = [
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/3p5_1_peaks.csv',
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/3p5_2_peaks.csv',
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/3p5_3_peaks.csv',
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/3p5_4_peaks.csv',
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/3p5_5_peaks.csv'
    #'/dls/i23/data/2023/cm33851-5/processing/anacor/tlys_2/ac_variation_P6122/csv_files/3p_1_peaks/3p5_1_cr0_li0.csv'
    #'/dls/i23/data/2023/cm33851-5/processing/anacor/tlys_9/P6122/3p5_1.csv',
    #'/dls/i23/data/2023/cm33851-5/processing/anacor/tlys_9/P6122/3p5_2.csv',
    #'/dls/i23/data/2023/cm33851-5/processing/anacor/tlys_9/P6122/3p5_3.csv',
    #'/dls/i23/data/2023/cm33851-5/processing/anacor/tlys_9/P6122/3p5_4.csv',
    #'/dls/i23/data/2023/cm33851-5/processing/anacor/tlys_9/P6122/3p5_5.csv',
    #'/dls/i23/data/2023/cm33851-5/processing/anacor/tlys_9/P6122/3p8_1.csv',
    #'/dls/i23/data/2023/cm33851-5/processing/anacor/tlys_9/P6122/3p8_2.csv',
    #'/dls/i23/data/2023/cm33851-5/processing/anacor/tlys_9/P6122/3p8_3.csv',
    #'/dls/i23/data/2023/cm33851-5/processing/anacor/tlys_9/P6122/3p8_4.csv',
    #'/dls/i23/data/2023/cm33851-5/processing/anacor/tlys_9/P6122/3p8_5.csv'
]

# Read and concatenate all datasets, adding a 'set_id' to distinguish them
all_data = []
methods = ['method:acsh:', 'method:sh:', 'method:ac:']
method_to_marker = ['o', 's', '^']

for i, file_path in enumerate(file_paths, start=1):
    df = pd.read_csv(file_path)
    df['set_id'] = f"Set {i}"  # Adding a set identifier
    all_data.append(df)

# Concatenating all the dataframes
combined_data = pd.concat(all_data)

# Melting the combined DataFrame
melted_combined_data = combined_data.melt(id_vars=['method', 'set_id'], var_name='label', value_name='value')
filtered_combined_data = melted_combined_data.dropna(subset=['value'])
print(filtered_combined_data)

#Zn_plot = filtered_combined_data[filtered_combined_data['label']=='ZN_A:ZN405']
Zn_plot = filtered_combined_data[filtered_combined_data['label'].str.contains('ZN405')]
M205_plot = filtered_combined_data[filtered_combined_data['label'].str.contains('MET205')]
M120_plot = filtered_combined_data[filtered_combined_data['label'].str.contains('MET120')]

final_averages = [[], [], []]
i = 0
for atom in [Zn_plot, M205_plot, M120_plot]:
    i +=1
    print(i)
    ac = atom[atom['method']=='method:ac:']
    acsh = atom[atom['method']=='method:acsh:']
    sh = atom[atom['method']=='method:sh:']

    final_averages[0].append(np.average(ac['value']))
    final_averages[1].append(np.average(acsh['value']))
    final_averages[2].append(np.average(sh['value']))

    sns.set_style("darkgrid")
    ax = pd.DataFrame({'ac':list(ac['value']), 'acsh':list(acsh['value']), 'sh':list(sh['value'])}, index=list(ac['set_id']))
    ax = ax.plot(kind='bar', legend=True, figsize=(12,8))
    for container in ax.containers:
        ax.bar_label(container)
    #plt.title('Anomalous density peaks at 3000 keV ')
    plt.xlabel('Dataset')
    plt.ylabel('Anomalous density peaks')
    plt.xticks(rotation=0)
    if i ==1:
        plt.title('Zinc Anomalous density peaks at 3500 keV')
        plt.savefig('/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/plots/3p5_zn_2Dbar.png')
    if i ==2:
        plt.title('Methionine-205 Anomalous density peaks at 3500 keV')
        plt.savefig('/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/plots/3p5_m205_2Dbar.png')
    if i ==3:
        plt.title('Methionine-120 Anomalous density peaks at 3500 keV')
        plt.savefig('/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/plots/3p5_m120_2Dbar.png')
    plt.show()

print(final_averages)