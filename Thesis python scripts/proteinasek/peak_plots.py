import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Put the path to your data files here
file_paths = [
    '/dls/i23/data/2024/nr29467-33/processing/tomography/results/csvs/dimple/prot_con_9_3p0_peaks.csv',
    '/dls/i23/data/2024/nr29467-33/processing/tomography/results/csvs/dimple/prot_con_9_3p5_peaks.csv',
    '/dls/i23/data/2024/nr29467-33/processing/tomography/results/csvs/dimple/prot_ls_6_3p0_peaks.csv',
    '/dls/i23/data/2024/nr29467-33/processing/tomography/results/csvs/dimple/prot_ls_6_3p5_peaks.csv'
]

# Read and concatenate all datasets, adding a 'set_id' to distinguish them
all_data = []
atoms_to_find = ['SG_A:CYS123', 'SG_A:CYS73', 'SD_A:MET225', 'SG_A:CYS178', 'SD_A:MET55', 'SG_A:CYS249', 'SD_A:MET111']

for i, file_path in enumerate(file_paths, start=0):
    df = pd.read_csv(file_path, sep=(' '))#, names=['set_id', 'method', 'value'], skiprows=0, sep=('  '))
    #df['set_id'] = f"Set {i}"  # Adding a set identifier
    all_data.append(df)

# Concatenating all the dataframes
combined_data = pd.concat(all_data)
print(combined_data)
# Melting the combined DataFrame
#melted_combined_data = combined_data.melt(id_vars=['method', 'set_id'], var_name='label', value_name='value')
combined_data = combined_data.melt(id_vars=['set_id', 'method'], var_name='label', value_name='value')
#filtered_combined_data = melted_combined_data#.dropna(subset=['value'])
combined_data = combined_data.fillna(0)

ac = combined_data[combined_data['method']==':ac:']
acsh = combined_data[combined_data['method']==':acsh:']
sh = combined_data[combined_data['method']==':sh:']

for atom in atoms_to_find:
    plot_data = combined_data[combined_data['label'].str.contains(f'{atom}')]
    
    final_averages = [[], [], []]
    
    ac = plot_data[plot_data['method']==':ac:']
    acsh = plot_data[plot_data['method']==':acsh:']
    sh = plot_data[plot_data['method']==':sh:']

    final_averages[0].append((ac['value']))
    final_averages[1].append((acsh['value']))
    final_averages[2].append((sh['value']))
    
    sns.set_style("darkgrid")
    cm = sns.color_palette("crest", as_cmap=True)
    ax = pd.DataFrame({'ac':list(ac['value']), 'acsh':list(acsh['value']), 'sh':list(sh['value'])}, index=list(ac['set_id']))
    # ax = ax.style.background_gradient(cmap=cm)
    #sns.catplot(data={'ac':list(ac['value']), 'acsh':list(acsh['value']), 'sh':list(sh['value'])}, x='Dataset', y='Peak heights', kind='bar')
    ax = ax.plot(kind='bar', legend=True, figsize=(12,8))
    
    for container in ax.containers:
        ax.bar_label(container)
    plt.xlabel('Crystal : Energy (keV)')
    plt.ylabel('Anomalous density peaks')
    plt.xticks(rotation=0)
    plt.title(f'Insulin laser-shaped (LS) and control crystal: {atom} anode peaks at 3.0 and 3.5 keV')
    plt.savefig(f"/dls/i23/data/2024/nr29467-33/processing/tomography/results/plots/dimple/proteinasek/{atom.replace(':', '_')}.png")
    plt.show()
