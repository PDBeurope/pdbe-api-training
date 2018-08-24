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

citation_url = api_base + 'pdb/entry/related_publications/'

"""
2) Defining request function
Let's start with defining a function that can be used to GET a single PDB entry, 
or POST a comma-separated list of PDB entries.

We will use this function to retrieve citations data for entries.
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
3) Investigating citations of PDB entries
In this exercise, we will try to evaluate the impact of a set of PDB entries based on the number of 
citations (publications that mention the entry, where the authors are not the same as the PDB depositors)

We will use the API call "related publications" to do this.
"""

"""
3.1) Defining a list of PDB entries¶
"""

pdb_list = ("1cbs", "2aqa", "3bow", "2klm", "5tok")

"""
3.2) Examining an example entry
Let's see what the API data would look like for a specific entry.

For example the entry "3bow" would have information such as this:
"""

example = {
    "3bow": {
        "appears_without_citation": {
            "Reviews": [],
            "Articles": []
        },
        "cited_by": {
            "Reviews": [
                {
                    "title": "Calpains and cancer: friends or enemies?",
                    "journal": "Arch. Biochem. Biophys.",
                    "citation_type": "Review",
                    "year": "2014",
                    "volume": "564",
                    "pubmed_id": "25305531",
                    "authors": "Moretti D, Del Bello B, Allavena G, Maellaro E.",
                    "cited_by_count": 12,
                    "pages": "26-36"
                }
            ],
            "Articles": []
        },
        "uniprot_publications": {
            "Reviews": [],
            "Articles": []
        }
    }
}

"""
As you can see, the API call returns a structured JSON object with information on three types of related publications. 
For our purposes, the most relevant citations will be found in the "cited_by" sub-dictionary. For the sake of 
this exercise, we will argue that the impact of a PDB entry is best quantified by how many times it was cited directly. 
We will also make a distinction between reviews and articles, as articles are on the frontline of science, and 
the most impactful developments are published in this type of publications.
"""

"""
3.3) Defining a function to calculate the number of review and article citations of PDB entries
"""


def calculate_citations(pdb_list):
    """
    This function will calculate the number of review and article
    citations for each PDB entry on an id list

    :param pdb_list: List
    :return: Dict or None
    """

    # We will save valid and unique PDB ids
    validated_unique_ids = []
    citation_counts = {}

    # First, we loop through the PDB list
    # and check if the ids match the PDB
    # id pattern
    for pdb_id in pdb_list:
        if not re.match("[0-9][A-Za-z][A-Za-z0-9]{2}", pdb_id):
            continue
        if pdb_id not in validated_unique_ids:
            validated_unique_ids.append(pdb_id)

    # Join the list of PDB ids in a string
    # format that the API requires
    joined_list = ", ".join(validated_unique_ids)

    # Get the citations data for the list of
    # PDB entries
    citations_data = make_request(citation_url, "post", joined_list)

    if not citations_data:
        print("No data")
        return None

    for entry_id in citations_data.keys():
        number_of_reviews = len(citations_data[entry_id]["cited_by"]["Reviews"])
        number_of_articles = len(citations_data[entry_id]["cited_by"]["Articles"])
        citation_counts[entry_id] = {"reviews": number_of_reviews, "articles": number_of_articles}
    return citation_counts

"""
Now that we have this function, we can call it with the list of PDB entries. We also added a simple function to 
print the results in a more user-friendly manner.
"""

print("Getting citation counts:")
counts = calculate_citations(pdb_list)
print(counts)
print()


def print_nicely(counts):
    """
    This function iterates through a count
    dictionary and prints the values in a
    user-friendly way

    :param counts: Dict,
    :return: None
    """
    print("pdb id\tarticles\treviews")
    for entry_id in counts.keys():
        print("%s\t%i\t%i" % (entry_id,
                              counts[entry_id]["articles"],
                              counts[entry_id]["reviews"]))
    return None


print_nicely(counts)