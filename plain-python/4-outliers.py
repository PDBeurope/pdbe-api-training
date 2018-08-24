#!/usr/bin/env python3

# Copyright 2018 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the
# License.

"""
PDBe API Training
This interactive Python notebook will guide you through various ways of programmatically accessing Protein Data Bank in Europe (PDBe) data using REST API

The REST API is a programmatic way to obtain information from the PDB and EMDB. You can access details about:

sample
experiment
models
compounds
cross-references
publications
quality
assemblies
and more...
For more information, visit http://www.ebi.ac.uk/pdbe/pdbe-rest-api
"""

# DEPENDENCIES:
# requests

"""
1) Making imports and setting variables

First, we import some packages that we will use, and set some variables.

Note: Full list of valid URLs is available from http://www.ebi.ac.uk/pdbe/api/doc/
"""

import requests
import re

base_url = "https://www.ebi.ac.uk/pdbe/"

api_base = base_url + "api/"

outlier_data_url = api_base + 'validation/protein-ramachandran-sidechain-outliers/entry/'

"""
2) Defining request function¶
Let's start with defining a function that can be used to GET a single PDB entry, or POST a comma-separated list of PDB entries.

We will use this function to retrieve secondary structure mapping for entries.
"""


def make_request(url, mode, pdb_id):
    """
    This function can make GET and POST requests to
    the PDBe API

    :param url: String,
    :param mode: String,
    :param pdb_id: String
    :return: JSON or None
    """
    if mode == "get":
        response = requests.get(url=url + pdb_id)
    elif mode == "post":
        response = requests.post(url, data=pdb_id)

    if response.status_code == 200:
        return response.json()
    else:
        print("[No data retrieved - %s] %s" % (response.status_code, response.text))

    return None

"""
3) Investigating ourlier residues¶
We will use one of the validation data calls of the PDBe API to get information on the Ramachandran 
and side-chain outliers of various models in a PDB entry.

For this exercise, we will look at the NMR entry "2aqa". Generally, the JSON data will have the 
following basic structure:
"""

example = {
    "2aqa": {
        "ramachandran_outliers": [],
        "sidechain_outliers": []
    }
}

"""
The lists will contain dictionaries which give residue-level information. For example:
"""

example_2 = {
    "model_id": 2,
    "entity_id": 1,
    "residue_number": 47,
    "author_residue_number": 48,
    "chain_id": "A",
    "author_insertion_code": "",
    "alt_code": "",
    "struct_asym_id": "A"
}

"""
3.1) Listing the number of outliers per model
The entry "2aqa" has multiple models, and it may be of interest to see if any of the models has 
relatively more outliers than the rest.

First, we will list the number of outlier residues per models using the functions below:
"""


def get_outlier_data(pdb_id):
    """
    This function will GET the outlier data from
    the PDBe API using the make_request() function

    :param pdb_id: String
    :return: JSON
    """
    # Check if the provided PDB id is valid
    # There is no point in making an API call
    # with bad PDB ids
    if not re.match("[0-9][A-Za-z][A-Za-z0-9]{2}", pdb_id):
        print("Invalid PDB id")
        return None

    # GET the outlier data
    outlier_data = make_request(outlier_data_url, "get", pdb_id)

    # Check if there is data
    if not outlier_data:
        print("No data found")
        return None

    return outlier_data


def list_number_of_outliers_per_model(pdb_id):
    """
    This function calls get_outlier_data() and
    then list the number of Ramachandran and
    side-chain outliers per model in the PDB entry

    :param pdb_id: String,
    :return: None
    """
    # We will collect the number of outlier
    # residues per model
    outliers = {"ramachandran_outliers": {}, "sidechain_outliers": {}}

    # Getting outlier data
    outlier_data = get_outlier_data(pdb_id)

    # If there is no data, return None
    if not outlier_data:
        return None

    # Iterate through both Ramachandran and
    # side-chain outliers
    for key in outliers.keys():
        for i in range(len(outlier_data[pdb_id][key])):
            # Grab the model id
            model_id = outlier_data[pdb_id][key][i]["model_id"]
            # If the model id was not observed before, add to
            # the outliers dictionary with the corresponding
            # outlier type, otherwise increase the count by one
            if model_id not in outliers[key].keys():
                outliers[key][model_id] = 1
            else:
                outliers[key][model_id] += 1

    print("Ramachandran outliers:")
    for model in outliers["ramachandran_outliers"].keys():
        print("Model %i has %i Ramachandran outliers" % (model,
                                                         outliers["ramachandran_outliers"][model]))
    print()
    print("Side-chain outliers:")
    for model in outliers["sidechain_outliers"].keys():
        print("Model %i has %i Side-chain outliers" % (model,
                                                       outliers["sidechain_outliers"][model]))


list_number_of_outliers_per_model("2aqa")

"""
3.2) Listing all outlier residues of a model
Next, we will write a function that lists out which are the outlier residues within a specific model.
"""


def list_outlier_residues_of_model(pdb_id, model_id):
    """
    This function calls get_outlier_data()
    and lists all outlier residues of a
    specific model

    :param pdb_id: String,
    :param model_id: Integer,
    :return: None
    """

    outlier_data = get_outlier_data(pdb_id)

    # If there is no data, return None
    if not outlier_data:
        return None

    # Iterate thourgh the outlier types
    for outlier_type in outlier_data[pdb_id].keys():
        # Loop through all the residue-level outlier information
        for i in range(len(outlier_data[pdb_id][outlier_type])):
            outlier_information = outlier_data[pdb_id][outlier_type][i]
            # Only process outlier information that corresponds to
            # the model id of interest
            if outlier_information["model_id"] != model_id:
                continue

            # Set outlier type labels
            if outlier_type == "ramachandran_outliers":
                label = "Ramachandran"
            else:
                label = "side-chain"

            residue = outlier_information["residue_number"]
            chain = outlier_information["chain_id"]
            entity = outlier_information["entity_id"]
            print("Residue %i in chain %s of entity %i is a %s outlier" % (residue,
                                                                           chain,
                                                                           entity,
                                                                           label))


print("Listing outlier residues for Model #7 of PDB entry 2aqa:")
list_outlier_residues_of_model("2aqa", 7)