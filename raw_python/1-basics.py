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

import re
import requests

base_url = "https://www.ebi.ac.uk/pdbe/"
api_base = base_url + "api/"
summary_url = api_base + 'pdb/entry/summary/'

"""
2) Basic examples
We will start with some very basic examples and operations.
"""

"""
2.1) Iterating through lists
"""

# This is a simple list with 2 PDB entry IDs
basic_pdb_list = ["1cbs", "3bow"]


# Iterating through this list (or any other lists)
# can be done with a simple function, such as:
def iterate_list(my_list):
    """
    This function will iterate through a list,
    and print each item

    :param my_list: List
    :return: None
    """
    for item in my_list:
        print(item)


# Calling the function:
print("Iterating through PDB id list")
print()
iterate_list(basic_pdb_list)

"""
2.2) Getting a specific item from a list
Getting a specific element of a list can be done using a function such as this below. 
Please note that indices start from 0 in Python, so the first element of a list has an index of 0
"""


def get_item(index, my_list):
    """
    This function will get an item from a list
    using the index of the item

    :param index: Integer
    :param my_list: List
    :return: String
    """
    return my_list[index]


# Calling the function for the first element
first = get_item(0, basic_pdb_list)
print("First PDB id: %s" % first)

# Calling the function for the second element
second = get_item(1, basic_pdb_list)
print("Second PDB id: %s" % second)

"""
2.3) Getting a value for a key from a dictionary
Dictionaries are data structures with unique keys and corresponding values.

PDBe API calls generally return data in the form of dictionaries, i.e. collections of key and value pairs

Getting values from a dictionary can be done either by directly accessing the value using the key, 
or by using a simple function, such as below.
"""

simple_dictionary = {"key": "value"}

# Getting value directly from a dictionary using its key
simple_dictionary["key"]

# Basic example of a dictionary with two keys and two
# corresponding values
basic_pdb_dictionary = {
    "pdb_id": "1cbs",
    "experimental_method": "X-ray diffraction",
}

# Getting value directly using key
print("Getting value directly: %s" % basic_pdb_dictionary["pdb_id"])


# Getting value using simple function
def get_value(key, my_dictionary):
    """
    Gets the value that corresponds to a key in a
    dictionary

    :param key: String,
    :param my_dictionary: Dict
    :return: String
    """
    return (my_dictionary[key])


print("Getting value using function: %s" % get_value("pdb_id", basic_pdb_dictionary))

"""
3) Creating a mock PDBe entry¶
The dictionary below will serve as an offline example of what an actual API call 
would return for the entry "1CBS" when querying for the entry summary

You can try to make this call from your browser by copy/pasting the URL below:

https://www.ebi.ac.uk/pdbe/api/pdb/entry/summary/1cbs
"""

mock_entry_summary = {
    "1cbs": [
        {
            "related_structures": [],
            "split_entry": [],
            "title": "CRYSTAL STRUCTURE OF CELLULAR RETINOIC-ACID-BINDING PROTEINS I AND II IN COMPLEX WITH ALL-TRANS-RETINOIC ACID AND A SYNTHETIC RETINOID",
            "release_date": "19950126",
            "experimental_method": [
                "X-ray diffraction"
            ],
            "experimental_method_class": [
                "x-ray"
            ],
            "revision_date": "20110713",
            "entry_authors": [
                "Kleywegt, G.J.",
                "Bergfors, T.",
                "Jones, T.A."
            ],
            "deposition_site": "null",
            "number_of_entities": {
                "polypeptide": 1,
                "dna": 0,
                "ligand": 1,
                "dna/rna": 0,
                "rna": 0,
                "sugar": 0,
                "water": 1,
                "other": 0
            },
            "processing_site": "null",
            "deposition_date": "19940928",
            "assemblies": [
                {
                    "assembly_id": "1",
                    "form": "homo",
                    "preferred": "true",
                    "name": "monomer"
                }
            ]
        }
    ]
}

"""
As you can see, the data is structured as a JSON dictionary, with key and value pairs, for example: "revision_data": "20110713"

We will use this mock data for our first few operations.
"""

"""
4) Getting entry from the mock PDB data
Now let's try to get entries using a simple function! We will first use the mock PDB data 
to perform our GET function (and call our get_value function)
"""


def get_entry(pdb_id):
    """
    This function tries to get the data that corresponds to
    a PDB id

    If the entry id is not found, it print an error message
    and returns None

    :param pdb_id: String
    :return: Dict or None
    """
    try:
        # This next line will use our previously written
        # get_value() function
        return {pdb_id: get_value(pdb_id, mock_entry_summary)}
    except KeyError as error:
        print("Key error: %s" % error)
        return None


# Try to get PDB entry "3bow"
print("Trying with PDB id which is not in the dictionary:")
print(get_entry("3bow"))
print()

# Try to get PDB entry "1cbs"
print("Trying with PDB id which is in the dictionary:")
print(get_entry("1cbs"))

"""
5) Getting summary information for an entry (still using mock data)
Let's write a function that can be used to write a brief summary of a PDB entry

Please note, that certain calls could return multiple PDB entries (i.e. POST calls), 
but the GET summary call we use in this exercise will always return only one PDB entry
"""


def make_summary(data):
    """
    This function creates a summary for a PDB entry
    by getting data for an entry, and extracting
    pieces of information

    :param data: Dict
    :return: String
    """

    pdb_id = ""
    # Certain calls could return multiple PDB entries,
    # but the GET summary call we use in this exercise
    # will always return only one PDB entry
    for key in data.keys():
        pdb_id = key

    # The data is a list of dictionaries, and for the summary information,
    # it is always the first element of the list
    entry = get_item(0, data[pdb_id])

    # Getting the title of the entry
    title = get_value("title", entry)

    # Getting the release date of the entry
    release_date = get_value("release_date", entry)
    # Formatting the entry to make it more user-friendly
    formatted_release_date = "%s/%s/%s" % (
        release_date[:4],
        release_date[4:6],
        release_date[6:])

    # Getting the experimental methods
    # Note that there can be multiple methods, so this is a list that
    # needs to be iterated
    experimental_methods = ""
    for experimental_method in get_value("experimental_method", entry):
        if experimental_methods:
            experimental_methods += " and "
        experimental_methods += experimental_method

    # Creating the summary text using all the extracted
    # information
    summary = "Entry is titled \"%s\" and was released on %s." % (
        title,
        formatted_release_date)
    summary += " This entry was determined using %s." % experimental_methods
    return summary


print(make_summary(get_entry("1cbs")))

"""
6) Switching to real API data
Finally, we will start using the PDBe API to make real calls to get data for any PDB entry of interest

First, we need a function to communicate with the API

Making calls over the network is more expensive than getting data from a mock dictionary, so we will include 
an additional check before making the call: we will check if the PDB id in the pdb_id argument is a valid id 
that matches the PDB id pattern
"""


def get_entry_from_api(pdb_id, api_url):
    """
    This function will make a call to the PDBe API using
    the PDB id and API url provided as arguments

    :param pdb_id: String,
    :param api_url: String
    :return: Dict or None
    """
    if not re.match("[0-9][A-Za-z][A-Za-z0-9]{2}", pdb_id):
        print("Invalid PDB id")
        return None

    # Make a GET call to the API URL
    get_request = requests.get(url=api_url + pdb_id)

    if get_request.status_code == 200:
        # If there is data returned (with HTML status code 200)
        # then return the data in JSON format
        return get_request.json()
    else:
        # If there is no data, print status code and response
        print(get_request.status_code, get_request.text)
        return None


# Try our GET function with an invalid PDB id
print("Trying to GET data with invalid PDB id:")
print(get_entry_from_api("whatever", summary_url))
print()

print("Trying to GET data with valid PDB id:")
print(get_entry_from_api("1cbs", summary_url))

"""
As you can hopefully see, the data displayed is very similar to what we had in the mock data 
in previous sections - however, this is actual data coming from the PDBe API

7) Trying the make_summary() function with real API data
To wrap up this first interactive notebook, we will try to use our make_summary() function on real API data - All we need to do is to change the argument (data) we are passing into it
"""

print("Example #1")
print(make_summary(get_entry_from_api("3bow", summary_url)))
print()
print("Example #2")
print(make_summary(get_entry_from_api("2klm", summary_url)))
