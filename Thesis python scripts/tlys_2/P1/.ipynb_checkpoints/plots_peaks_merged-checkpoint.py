import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


# Put the path to your data files here
file_paths = [
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/P1/peaks_csvs/3p0_peaks.csv',
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/P1/peaks_csvs/3p5_peaks.csv'
]

# Read and concatenate all datasets, adding a 'set_id' to distinguish them
all_data = []
methods = ['method:acsh:', 'method:sh:', 'method:ac:']
method_to_marker = ['o', 's', '^']
energy_list = ['3000', '3500']

for i, file_path in enumerate(file_paths, start=1):
    df = pd.read_csv(file_path)
    #print(df)
    df['energy'] = f"{energy_list[i-1]}"  # Adding a set identifier
    atoms = df.columns[2:].to_list()
    all_data.append(df)

# Concatenating all the dataframes
combined_data = pd.concat(all_data)

# Melting the combined DataFrame
melted_combined_data = combined_data.melt(id_vars=['energy', 'method'], var_name='label', value_name='value')
filtered_combined_data = melted_combined_data.fillna(0) #melted_combined_data.dropna(subset=['value'])
print(filtered_combined_data)

final_averages = [[], [], []]

for atom in atoms:
    print(atom)
    data = filtered_combined_data[filtered_combined_data['label'].str.contains(atom)]

    ac = data[data['method']=='method:ac:']
    acsh = data[data['method']=='method:acsh:']
    sh = data[data['method']=='method:sh:']

    final_averages[0].append(np.average(ac['value']))
    final_averages[1].append(np.average(acsh['value']))
    final_averages[2].append(np.average(sh['value']))

    sns.set_style("darkgrid")
    cm = sns.color_palette("crest", as_cmap=True)
    ax = pd.DataFrame({'ac':list(ac['value']), 'acsh':list(acsh['value']), 'sh':list(sh['value'])}, index=list(ac['energy']))
    # ax = ax.style.background_gradient(cmap=cm)
    #sns.catplot(data={'ac':list(ac['value']), 'acsh':list(acsh['value']), 'sh':list(sh['value'])}, x='Dataset', y='Peak heights', kind='bar')
    ax = ax.plot(kind='bar', legend=True, figsize=(12,8))
    
    for container in ax.containers:
        ax.bar_label(container)
    plt.xlabel('Energy (eV)')
    plt.ylabel('Anomalous density peaks')
    plt.title(f'Thermolysin processed in P1: {atom} Anomalous density peaks')
    plt.savefig(f"/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/P1/merged_data/plots/{atom.replace(':','_')}_2Dbar.png")
    #plt.show()

print(final_averages)