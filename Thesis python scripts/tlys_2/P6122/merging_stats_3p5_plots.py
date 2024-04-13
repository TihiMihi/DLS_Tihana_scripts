import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Put the path to your data files here
file_paths = [
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/3p5_1_I_and_r_merge.csv',
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/3p5_2_I_and_r_merge.csv',
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/3p5_3_I_and_r_merge.csv',
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/3p5_4_I_and_r_merge.csv',
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/3p5_5_I_and_r_merge.csv',
]

# Read and concatenate all datasets, adding a 'set_id' to distinguish them
all_data = []
methods = ['method:acsh:', 'method:sh:', 'method:ac:']

for i, file_path in enumerate(file_paths, start=1):
    df = pd.read_csv(file_path, names=['set_id', 'method', 'I_value', 'r_value'], skiprows=0, sep=('  '))
    df['set_id'] = f"Set {i}"  # Adding a set identifier
    all_data.append(df)

# Concatenating all the dataframes
combined_data = pd.concat(all_data)
# Melting the combined DataFrame
#melted_combined_data = combined_data#.melt(id_vars=['set_id', 'method'], value_name='value')#var_name='method', value_name='value')
#filtered_combined_data = melted_combined_data#.dropna(subset=['value'])

print(combined_data)

ac = combined_data[combined_data['method']==':ac:']
acsh = combined_data[combined_data['method']==':acsh:']
sh = combined_data[combined_data['method']==':sh:']

# ac = filtered_combined_data[filtered_combined_data['method'].str.contains(':ac:')]
# acsh = filtered_combined_data[filtered_combined_data['method'].str.contains('acsh')]
# sh = filtered_combined_data[filtered_combined_data['method'].str.contains(':sh:')]

sns.set_style("darkgrid")
ax = pd.DataFrame({'ac':list(ac['I_value']), 'acsh':list(acsh['I_value']), 'sh':list(sh['I_value'])}, index=list(ac['set_id']))
ax = ax.plot(kind='bar', legend=True, figsize=(12,8))
plt.title(f'Thermolysin Intensity / sigma values in P6122 symmetry: 3.542 Å (3.5 keV)')
plt.xlabel('Dataset')
plt.ylabel('Anomalous density peaks')
plt.xticks(rotation=0)
for container in ax.containers:
    ax.bar_label(container)
plt.savefig('/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/plots/3p5_I_over_sigma.png')
plt.show()


sns.set_style("darkgrid")
ax2 = pd.DataFrame({'ac':list(ac['r_value']), 'acsh':list(acsh['r_value']), 'sh':list(sh['r_value'])}, index=list(ac['set_id']))
ax2 = ax2.plot(kind='bar', legend=True, figsize=(12,8))
plt.title(f'Thermolysin Overall R-merge values in P6122 symmetry: 3.542 Å (3.5 keV)')
plt.xlabel('Dataset')
plt.ylabel('Anomalous density peaks')
plt.xticks(rotation=0)
for container in ax2.containers:
    ax2.bar_label(container)
plt.savefig('/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/plots/3p5_rmerges.png')
plt.show()