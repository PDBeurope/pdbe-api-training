

# Define the commands for running superposition applications
ssm = "superpose"
gesamt = "gesamt"

import os
import subprocess

# Allow CCP4 tools to be used through Jupyter Notebooks
# subprocess.run(["source", "/Applications/ccp4-8.0/bin/ccp4.setup-sh"], shell=True)

# Strings that will not change in script
path_structures = "./examples_mmcif/"
static_struct = "6mka.cif"
path_static = f"{path_structures}{static_struct}"

# Loop over the structures for superposition
for mobile_struct in ["6mkf.cif", "6mkg.cif", "6mkj.cif"]:

    # Path to mobile structure in superposition
    path_mobile = f"{path_structures}{mobile_struct}"

    # Out file names
    save_file_ssm = f"ssm_{mobile_struct[:4]}_to_{static_struct[:4]}.pdb"
    save_file_gesamt = f"gesamt_{mobile_struct[:4]}_to_{static_struct[:4]}.pdb"

    # SSM command ready
    command_ssm = [ssm, path_static, path_mobile, "-o", save_file_ssm]
    command_ssm = f"{ssm} {path_static} {path_mobile} -o {save_file_ssm}"
    # GESAMT command ready
    command_gesamt = f"{gesamt} {path_static} {path_mobile} -o {save_file_gesamt}"
    print(command_ssm)

    # Execute SSM command
    os.system(command_ssm)
    # Execute GESAMT command
    os.system(command_gesamt)