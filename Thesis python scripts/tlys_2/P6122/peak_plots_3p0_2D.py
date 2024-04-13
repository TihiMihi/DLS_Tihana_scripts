import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# Put the path to your data files here
file_paths = [
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/3p0_1_peaks.csv',
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/3p0_2_peaks.csv',
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/3p0_3_peaks.csv',
    '/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/csv_files/3p0_4_peaks.csv'
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
    cm = sns.color_palette("crest", as_cmap=True)
    ax = pd.DataFrame({'ac':list(ac['value']), 'acsh':list(acsh['value']), 'sh':list(sh['value'])}, index=list(ac['set_id']))
    # ax = ax.style.background_gradient(cmap=cm)
    #sns.catplot(data={'ac':list(ac['value']), 'acsh':list(acsh['value']), 'sh':list(sh['value'])}, x='Dataset', y='Peak heights', kind='bar')
    ax = ax.plot(kind='bar', legend=True, figsize=(12,8))
    
    for container in ax.containers:
        ax.bar_label(container)
    plt.xlabel('Dataset')
    plt.ylabel('Anomalous density peaks')
    plt.xticks(rotation=0)
    if i ==1:
        plt.title('Zinc Anomalous density peaks at 3000 keV')
        plt.savefig('/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/plots/3p0_zn_2Dbar.png')
    if i ==2:
        plt.title('Methionine-205 Anomalous density peaks at 3000 keV')
        plt.savefig('/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/plots/3p0_m205_2Dbar.png')
    if i ==3:
        plt.title('Methionine-120 Anomalous density peaks at 3000 keV')
        plt.savefig('/dls/i23/data/2024/cm37273-1/processing/tihana/tlys_2/plots/3p0_m120_2Dbar.png')
    plt.show()

print(final_averages)

'''
# Plotting
plt.figure(figsize=(15, 8))

# We will use the same marker style for methods across all data sets
# Assigning a color for each set
set_colors = sns.color_palette("Set1", n_colors=len(file_paths))

for set_id, color in zip(combined_data['set_id'].unique(), set_colors):
    set_data = filtered_combined_data[filtered_combined_data['set_id'] == set_id]
    #print(set_data)
    for method in methods:
        method_data = set_data[set_data['method'] == method]
        print(method_data)
        plt.scatter(method_data['label'], method_data['value'], 
                    label=f"{method[7:-1]} ({set_id})", 
                    #marker = 'o',
                    marker=method_to_marker[methods.index(method)],
                    color=color)

plt.title('Thermolysin P6122 at 3.0 keV: Anode peak heights')
plt.xlabel('Atoms')
plt.ylabel('Peak Height')
plt.grid(True)
plt.legend(title='Method and Set', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f'./plots/P6122_3p0_all_peaks.png')
plt.show()
'''