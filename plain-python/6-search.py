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

search_url = "https://www.ebi.ac.uk/pdbe/search/pdb/select?q="

search_variables = "&wt=json&rows=10"

"""
## 2) Defining request function

Let's start with defining a function that can be used to get a URL response. We will use this function to 
retrieving the search results in JSON format.
"""


def url_response(url):
    response = requests.get(url=url)
    if response.status_code == 200:
        json_result = response.json()
        return json_result
    else:
        print(response.status_code, response.reason)
        return None


"""
3) Defining search function
We need a function that will construct the search string in the adequate query format, and which will then get the 
data in JSON format using the url_response() function implemented earlier.
"""


def run_search(pdbe_search_term):
    full_query = search_url + pdbe_search_term + search_variables

    response = url_response(full_query)

    if "response" in response:
        if "docs" in response["response"]:
            return response["response"]["docs"]
    return None


"""
4) Trying out the search
Finally, we can try out our function using a custom search term. Note that the space between words has to be 
types as "%20", for example "Homo%20sapiens".

The result will be a JSON with all PDB entries the search could find.

We print out the PDB ids using a simple for loop at the bottom.
"""

search_terms = 'molecule_name:"Dihydrofolate%20reductase" AND organism_scientific_name:"Homo%20sapiens"'
results = run_search(search_terms)

pdb_list = []
for result in results:
    pdb = result["pdb_id"]
    if pdb not in pdb_list:
        pdb_list.append(pdb)

print(pdb_list)
