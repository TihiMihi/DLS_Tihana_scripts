import os
import sys
import json

# Define dataset path
dataset_path = f"{input('Path to dataset in anacor where preprocess was run: ')}"
dataset = dataset_path.split("/")[-1]

# Define dataset name, reflection/experiment files, model store path
with open(f'{dataset_path}/default_preprocess_input.yaml', 'r') as file:
    lines = file.readlines()
    for i, line in enumerate(lines):
        if 'dataset:' in line:
            dataset = line.split(':')[-1].strip() # Store dataset name
        if 'refl-path:' in line:
            refl_expt = line.split(':')[-1].strip() # Store reflection/experiment filepath
            refl_expt = refl_expt.split('.')[0] # Remove .refl/.expt
        if 'model_storepath:' in line:
            model_storepath = line.split(':')[-1].strip() # Store model storepath

print('Dataset:', dataset)

# Store median results from preprocess as lists
with open(os.path.join(dataset_path, f'{dataset}_save_data','ResultData','absorption_coefficient','median_coefficients_with_percentage.json'), 'r') as file:
    lines = file.readlines()
    data = (" ".join(line.strip() for line in lines))

data_list = (json.loads(data))
acceptance_percentages = data_list[0]
materials = data_list[1]

li_list = data_list[(materials.index('li')+2)]
lo_list = data_list[(materials.index('lo')+2)]
cr_list = data_list[(materials.index('cr')+2)]

# Prompt for autofilling results from preprocess
auto_ac = input('Auto-fill absorption coeffients with 50 % acceptance from preprocess? (For manual, enter "n" or "no". For autofill, press any key.)')

if auto_ac == 'n' or auto_ac == 'no':
    # Manually input absorption coefficients
    li_ac = float(input('liquor absorption coefficient reference: '))
    lo_ac = float(input('loop absorption coefficient fixed: '))
    cr_ac = float(input('crystal absorption coefficient reference: '))
    bu_ac = float(input('bubble absorption coefficient fixed: '))
else:
    # Select absorption coefficients from list for 50 % acceptance
    li_ac = li_list[(acceptance_percentages.index(0.5))]
    lo_ac = lo_list[(acceptance_percentages.index(0.5))]
    cr_ac = cr_list[(acceptance_percentages.index(0.5))]
    bu_ac = 0
    
    print('liquor absorption coefficient: ', li_ac)
    print('loop absorption coefficient: ', lo_ac)
    print('crystal absorption coefficient: ', cr_ac)
    print('bubble absorption coefficient: ', bu_ac)
    

# Prompt for autofilling file pathways from preprocess
auto_path = input('Auto-fill reflection and experiment files from preprocess? ("n" or "no". Any other key for "yes")')
if auto_path == 'n' or auto_path == 'no':
    refl_expt = f"{input('Pathway to refl/expt files (excluding .refl or .expt): ')}"
else:
    print('refl/expt: ', refl_expt)


auto_model = input('Auto-fill model store path from preprocess? ("n" or "no". Any other key for "yes")')
if auto_model == 'n' or auto_path == 'no':
    model_storepath = f"{input('Model storepath (including .npy): ')}"
else:
    print('model store path: ', model_storepath)


# Prompt for anomalous signal
anom = str(input('Anomalous: "true" / "false" (default = true): '))

if anom != "false":
    anom = "true"
print('Anomalous = ', anom)


# Prompt for run all mp-process paths
run_all = str(input('Run anacor.mp_lite for all pathways? ("n" or "no". Any other key for "yes")'))

# Calculate AC variations
cr_list = [
    0.9 * cr_ac,
    cr_ac,
    1.1 * cr_ac,
    ]

li_list = [
    0.9 * li_ac,
    li_ac,
    1.1 * li_ac,
]

ac_values = []
for c in cr_list:
    for l in li_list:
        ac_values += [(c, l)]

# Label AC variations
ac_labels = ["crm10_lim10","crm10_li0","crm10_lip10", "cr0_lim10",  "cr0_li0",  "cr0_lip10", "crp10_lim10","crp10_li0","crp10_lip10"]

# Create store directory
for dir in ac_labels:
    parent_path = os.path.join(sys.path[0], 'ac_var')
    if not os.path.exists(parent_path):
        os.mkdir(parent_path)
        print(f"Parent Directory created.")
    else:
        pass
    
    dir_path = os.path.join(sys.path[0], 'ac_var', dir)

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        print(f"Directory {dir} successfully created.")
    else:
        print(f"Directory {dir} already exists.")
        pass

    # Write files
    mp_file = open(f"{dir_path}/default_mpprocess_input.yaml", "w+")
    mp_file.writelines(
        [
            f"store_dir: {dir_path}\n",
            f"dataset: {dataset}_{dir}\n",
            f"liac: {ac_values[ac_labels.index(dir)][1]}\n",
            f"loac: {lo_ac}\n",
            f"crac: {ac_values[ac_labels.index(dir)][0]}\n",
            f"buac: {bu_ac}\n",
            "num_cores: 20\n",
            "hour: 6\n",
            "minute: 10\n",
            "second: 10\n",
            "sampling_ratio: 0.5\n",
            "dials_dependancy: module load dials/latest\n",
            "hpc_dependancies: module load global/cluster\n",
            "offset: 0\n",
            f"refl_path: {refl_expt}.refl\n",
            f"expt_path: {refl_expt}.expt\n",
            f"model_storepath: {model_storepath}\n",
            "post_process: true\n",
            "full_iteration: 1\n",
            "with_scaling: true\n",
            f"anomalous: {anom}\n",
            "gpu: true\n"
            "mtz2sca_dependancy: module load ccp4\n",
        ]
    )
    mp_file.close()

    # Try to run all anacor jobs
    # Currently not compatible with anacor

    #run it through AnACor api
    #pth =f"{dir_path}/default_mpprocess_input.yaml"
    #from AnACor.mp_lite import main
    #main(pth)
    
    if run_all == 'n' or run_all == 'no':
        pass
    else:
        #os.system("source /dls/science/groups/i23/yishun/AnACor2.0/anacor2/bin/activate")
        #os.system("anacor.mp_lite")
        #os.system(f"source /dls/science/groups/i23/yishun/AnACor2.0/anacor2/bin/activate &cd {dir_path} &pwd & anacor.mp_lite")
	import subprocess

	subprocess.run(f"source /dls/science/groups/i23/yishun/AnACor2.0/anacor2/bin/activate && cd {dir_path} && pwd && anacor.mp_lite", shell=True)

