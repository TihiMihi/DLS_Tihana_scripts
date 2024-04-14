import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Put the path to your data files here
file_paths = [
    '/dls/i23/data/2024/nr29467-33/processing/tomography/results/csvs/prot_ls_6_3p5_I_and_r_merge.csv',
    '/dls/i23/data/2024/nr29467-33/processing/tomography/results/csvs/prot_ls_6_3p0_I_and_r_merge.csv',
    '/dls/i23/data/2024/nr29467-33/processing/tomography/results/csvs/prot_con_9_3p5_I_and_r_merge.csv',
    '/dls/i23/data/2024/nr29467-33/processing/tomography/results/csvs/prot_con_9_3p0_I_and_r_merge.csv'
]

# Read and concatenate all datasets, adding a 'set_id' to distinguish them
all_data = []
methods = ['method:acsh:', 'method:sh:', 'method:ac:']

for i, file_path in enumerate(file_paths, start=1):
    df = pd.read_csv(file_path, names=['set_id', 'method', 'I_value', 'r_value'], skiprows=0, sep=('  '))
    df['set_id'] = df['set_id']#.replace(to_replace='_', value=': ')
    all_data.append(df)

# Concatenating all the dataframes
combined_data = pd.concat(all_data)
print(combined_data)

ac = combined_data[combined_data['method']==':ac:']
acsh = combined_data[combined_data['method']==':acsh:']
sh = combined_data[combined_data['method']==':sh:']

sns.set_style("darkgrid")
ax = pd.DataFrame({'ac':list(ac['I_value']), 'acsh':list(acsh['I_value']), 'sh':list(sh['I_value'])}, index=list(ac['set_id']))
ax = ax.plot(kind='bar', legend=True, figsize=(12,8))
plt.title(f'Proteinase-K laser-shaped (LS) and control crystal: Intensity / sigma')
plt.xlabel('Crystal : Energy (keV)')
#plt.ylabel('Intensity')
plt.xticks(rotation=0)
for container in ax.containers:
    ax.bar_label(container)
plt.savefig('/dls/i23/data/2024/nr29467-33/processing/tomography/results/plots/prot_I_over_sigma.png')
plt.show()


sns.set_style("darkgrid")
ax2 = pd.DataFrame({'ac':list(ac['r_value']), 'acsh':list(acsh['r_value']), 'sh':list(sh['r_value'])}, index=list(ac['set_id']))
ax2 = ax2.plot(kind='bar', legend=True, figsize=(12,8))
plt.title(f'Proteinase-K laser-shaped (LS) and control crystal: R-merge factor')
plt.xlabel('Crystal : Energy (keV)')
#plt.ylabel('R-merge')
plt.xticks(rotation=0)
for container in ax2.containers:
    ax2.bar_label(container)
plt.savefig('/dls/i23/data/2024/nr29467-33/processing/tomography/results/plots/prot_rmerges.png')
plt.show()