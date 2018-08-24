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

uniprot_mapping_url = api_base + 'mappings/uniprot/'

"""
2) Defining request function
Let's start with defining a function that can be used to GET a single PDB entry. Please note that the APi 
call we use in this exercise accepts only GET requests, thus, only single PDB ids.

We will use this function to retrieve UniProt mapping between PDB residues and UniProt residues.
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
3) Mapping PDB residues to UniProt residues
The numbering of residues in PDB entries is unfortunately not a trivial matter. Residue indexing not 
necessarily starts from 1, as authors may choose to use any indexing they would find best suited for their needs. 
For example the first residue in the PDB structure can have an "author_residue_number" of 42 or -6.

The situation is further complicated when you try to find out how a certain residue in the PDB entry relates to the 
same residue numbered in UniProt (i.e. the main protein sequence database).

We have developed SIFTS to address this issue. SIFTS is an up-to-date resource for residue-level mapping between 
UniProt and PDB entries. The resource also provides residue-level annotation from the IntEnz, GO, Pfam, InterPro, 
SCOP, CATH and PubMed resources. The information is updated and released every week at the same time as the 
release of new PDB entries and is widely used by resources such as RCSB, PDBsum, Pfam, SCOP, InterPro.

In this example we will look at how to map PDB residues to UniProt residues.
"""

"""
3.1) Example data
Let's start by looking at the JSON served by the PDBe API (http://www.ebi.ac.uk/pdbe/api/mappings/uniprot/1cbs)
"""

example = {
    "1cbs": {
        "UniProt": {
            "P29373": {
                "identifier": "RABP2_HUMAN",
                "name": "RABP2_HUMAN",
                "mappings": [
                    {
                        "entity_id": 1,
                        "end": {
                            "author_residue_number": 137,
                            "author_insertion_code": "",
                            "residue_number": 137
                        },
                        "chain_id": "A",
                        "start": {
                            "author_residue_number": 1,
                            "author_insertion_code": "",
                            "residue_number": 1
                        },
                        "unp_end": 138,
                        "unp_start": 2,
                        "struct_asym_id": "A"
                    }
                ]
            }
        }
    }
}

"""
According to the data, PDB entry "1cbs" maps to UniProt entry "P29373". The "mappings" list contains the actual 
mappings corresponding to regions of entities and chains. In the data above, entity 1 seen in chain A is indexed 
from 1 to 137, and in terms of UniProt sequence, 2 to 138.
"""

"""
3.2) Defining the mapper function
We move on to defining functions to retrieve the mapping for a specific PDB entry, and process the mapping:
"""


def get_mappings_data(pdb_id):
    """
    This function will GET the mappings data from
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

    # GET the mappings data
    mappings_data = make_request(uniprot_mapping_url, "get", pdb_id)

    # Check if there is data
    if not mappings_data:
        print("No data found")
        return None

    return mappings_data


def list_uniprot_pdb_mappings(pdb_id):
    """
    This function retrieves PDB > UniProt
    mappings using the get_mappings_data() function

    :param pdb_id: String,
    :return: None
    """

    # Getting the mappings data
    mappings_data = get_mappings_data(pdb_id)

    # If there is no data, return None
    if not mappings_data:
        return None

    uniprot = mappings_data[pdb_id]["UniProt"]
    for uniprot_id in uniprot.keys():
        mappings = uniprot[uniprot_id]["mappings"]

        for mapping in mappings:
            entity_id = mapping["entity_id"]
            chain_id = mapping["chain_id"]
            pdb_start = mapping["start"]["residue_number"]
            pdb_end = mapping["end"]["residue_number"]
            uniprot_start = mapping["unp_start"]
            uniprot_end = mapping["unp_end"]
            print("entity %i in chain %s is indexed from %i to %i in PDB, and from %i to %i in UniProt %s" % (
                entity_id,
                chain_id,
                pdb_start,
                pdb_end,
                uniprot_start,
                uniprot_end,
                uniprot_id
            )
                  )

    return None


list_uniprot_pdb_mappings("3bow")

"""
3.3) Getting mapping for a specific residue of a certain chain
If we are only interested in a particular residue of a chain, we could write a function such as:
"""


def get_uniprot_pdb_residue_mapping(pdb_id, chain_id, residue_number):
    """
    This function uses get_mappings_data() function
    to retrieve mappings between UniProt and PDB
    for a PDB entry, and then maps one specific
    residue of one specific chain

    :param pdb_id: String,
    :param chain_id: String,
    :param residue_number: String,
    :return: Integer
    """

    mappings_data = get_mappings_data(pdb_id)

    if not mappings_data:
        return None

    uniprot = mappings_data[pdb_id]["UniProt"]
    for uniprot_id in uniprot:
        for i in range(len(uniprot[uniprot_id]["mappings"])):
            mapping = uniprot[uniprot_id]["mappings"][i]
            if not mapping["chain_id"] == chain_id:
                continue
            pdb_start = mapping["start"]["residue_number"]
            pdb_end = mapping["end"]["residue_number"]
            uniprot_start = mapping["unp_start"]
            uniprot_end = mapping["unp_end"]
            if residue_number >= pdb_start and residue_number <= pdb_end:
                offset = uniprot_start - pdb_start
                return residue_number + offset
    return None


print("Examples of residue mappings:")
print("Residue 3 of chain C in PDB entry 3bow is mapped to UniProt residue %i" %
      (get_uniprot_pdb_residue_mapping("3bow", "C", 3)))

print("Residue 184 of chain B in PDB entry 3bow is mapped to UniProt residue %i" %
      (get_uniprot_pdb_residue_mapping("3bow", "B", 184)))
