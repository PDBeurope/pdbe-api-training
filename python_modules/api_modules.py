import pandas as pd
import requests

# from pprint import pprint

# settings for PDBe API
base_url = "https://www.ebi.ac.uk/pdbe/"  # the beginning of the URL for PDBe's API.
search_url = base_url + 'search/pdb/select?'  # the rest of the URL used for PDBe's search API.

pdbe_kb_interacting_residues_api = base_url + "graph-api/uniprot/ligand_sites/"
pdbe_kb_api_uniprot_base_url = base_url + "graph-api/uniprot/"


def get_ligand_site_url():
    return pdbe_kb_api_uniprot_base_url + "ligand_sites/"


def get_interaction_site_url():
    return pdbe_kb_api_uniprot_base_url + "interface_residues/"


def get_url_with_accession(url, accession):
    url = url + accession
    ret = get_url(url)
    return ret.get(accession, {})


def get_url(url):
    """
    Makes a request to a URL. Returns a JSON of the results
    :param str url:
    :return dict:
    """
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("[No data retrieved - %s] %s" % (response.status_code, response.text))

    return {}


def make_request_post(search_dict, number_of_rows=10):
    """
    makes a get request to the PDBe API
    :param dict search_dict: the terms used to search
    :param number_of_rows: number or rows to return - limited to 10
    :return dict: response JSON
    """
    if 'rows' not in search_dict:
        search_dict['rows'] = number_of_rows
    search_dict['wt'] = 'json'
    # pprint(search_dict)
    response = requests.post(search_url, data=search_dict)

    if response.status_code == 200:
        return response.json()
    else:
        print("[No data retrieved - %s] %s" % (response.status_code, response.text))

    return {}


def quote_value(value):
    if ' ' in value and '[' not in value:
        if '"' not in value:
            value = '"{}"'.format(value)
        elif "'" not in value:
            value = "'{}'".format(value)
    return value


def format_search_terms_post(search_terms, filter_terms=None, **kwargs):
    ret = {'q': str(search_terms)}
    if filter_terms:
        fl = '{}'.format(','.join(filter_terms))
        ret['fl'] = fl
    for arg in kwargs:
        ret[arg] = kwargs[arg]
    return ret


def format_sequence_search_terms(sequence, filter_terms=None):
    """
    Format parameters for a sequence search
    :param str sequence: one letter sequence
    :param lst filter_terms: Terms to filter the results by
    :return str: search string
    """
    params = {
        'json.nl': 'map',
        'start': '0',
        'sort': 'fasta(e_value) asc',
        'xjoin_fasta': 'true',
        'bf': 'fasta(percentIdentity)',
        'xjoin_fasta.external.expupperlim': '0.1',
        'xjoin_fasta.external.sequence': sequence,
        'q': '*:*',
        'fq': '{!xjoin}xjoin_fasta'
    }
    if filter_terms:
        for term in ['pdb_id', 'entity_id', 'entry_entity', 'chain_id']:
            filter_terms.append(term)
        filter_terms = list(set(filter_terms))
        params['fl'] = ','.join(filter_terms)

    return params


def run_sequence_search(sequence, filter_terms=None, number_of_rows=10):
    """
    Runs a sequence search and results the results
    :param str sequence: sequence in one letter code
    :param lst filter_terms: terms to filter the results by
    :param int number_of_rows: number of results to return
    :return lst: List of results
    """
    group_field = 'entry_entity'
    search_dict = format_sequence_search_terms(sequence=sequence, filter_terms=filter_terms)
    response = make_request_post(search_dict=search_dict, number_of_rows=number_of_rows)
    # results = response.get('grouped', {}).get(group_field, {}).get('groups', [])
    results = response.get('response', {}).get('docs', [])
    print('Number of results {}'.format(len(results)))

    raw_fasta_results = response.get('xjoin_fasta').get('external')
    fasta_results = {}

    for fasta_row in raw_fasta_results:
        # join_id = fasta_row.get('joinId')
        fasta_doc = fasta_row.get('doc', {})
        percent_identity = fasta_doc.get('percent_identity')
        e_value = fasta_doc.get('e_value')
        return_sequence = fasta_row.get('return_sequence_string')
        pdb_id_chain = fasta_doc.get('pdb_id_chain').split('_')
        pdb_id = pdb_id_chain[0].lower()
        chain_id = pdb_id_chain[-1]
        join_id = '{}_{}'.format(pdb_id, chain_id)
        fasta_results[join_id] = {'e_value': e_value,
                                  'percentage_identity': percent_identity,
                                  'return_sequence': return_sequence}

    ret = []
    for row in results:
        # doc = row.get('doclist', {}).get('docs', [])[0]
        pdb_id = row.get('pdb_id').lower()
        chain_ids = row.get('chain_id')
        for chain_id in chain_ids:
            search_id = '{}_{}'.format(pdb_id, chain_id)
            entry_fasta_results = fasta_results.get(search_id, {})
            if entry_fasta_results:
                row['e_value'] = entry_fasta_results.get('e_value')
                row['percentage_identity'] = entry_fasta_results.get('percentage_identity')
                row['result_sequence'] = entry_fasta_results.get('return_sequence_string')

                ret.append(row)
    return ret


def run_search(search_terms, filter_terms=None, number_of_rows=10, **kwargs):
    """
    Run the search with set of search terms
    :param str search_terms: string of search terms
    :param list filter_terms: list of terms to filter by
    :param int number_of_rows: number of search rows to return
    :return lst: list of results
    """
    search_params = format_search_terms_post(search_terms=search_terms, filter_terms=filter_terms)
    if search_params:
        response = make_request_post(search_dict=search_params, number_of_rows=number_of_rows)
        if response:
            results = response.get('response', {}).get('docs', [])
            print('Number of results for {}: {}'.format(search_terms, len(results)))
            return results

    print('No results')
    return []


def get_ligand_site_data(uniprot_accession):
    url = get_ligand_site_url() + uniprot_accession
    print(url)
    data = get_url(url=url)
    data_to_ret = []
    for data_uniprot_accession in data:
        accession_data = data.get(data_uniprot_accession)
        for row in accession_data.get('data'):
            ligand_accession = row.get('accession')
            name = row.get('name')
            num_atoms = row.get('additionalData', {}).get('numAtoms')
            for residue in row.get('residues', []):
                residue['ligand_accession'] = ligand_accession
                residue['ligand_name'] = name
                residue['ligand_num_atoms'] = num_atoms
                residue['uniprot_accession'] = uniprot_accession
                residue['interaction_ratio'] = len(residue.get('interactingPDBEntries', [])) / len(
                    residue.get('allPDBEntries', []))
                data_to_ret.append(residue)
    return data_to_ret


def get_macromolecule_interaction_data(uniprot_accession):
    url = get_interaction_site_url() + uniprot_accession
    print(url)
    data = get_url(url=url)
    data_to_ret = []

    for data_uniprot_accession in data:
        accession_data = data.get(data_uniprot_accession)
        length = accession_data.get('length')
        for row in accession_data.get('data'):
            interaction_accession = row.get('accession')
            all_pdb_entries = row.get('allPDBEntries')
            name = row.get('name')
            accession_type = row.get('additionalData', {}).get('type')
            for residue in row.get('residues', []):
                residue['interaction_accession'] = interaction_accession
                residue['interaction_name'] = name
                residue['length'] = length
                residue['uniprot_accession'] = uniprot_accession
                residue['interaction_accession_type'] = accession_type
                interacting_entries = residue.get('interactingPDBEntries', [])
                residue['interacting_pdb_entries'] = interacting_entries
                residue['interaction_ratio'] = len(interacting_entries) / len(all_pdb_entries)
                residue['allPDBEntries'] = all_pdb_entries
                data_to_ret.append(residue)
    return data_to_ret


def change_lists_to_strings(results):
    """
    updates lists to strings for loading into Pandas
    :param dict results: dictionary of results to process
    :return dict: dictionary of results
    """
    for row in results:
        for data in row:
            if type(row[data]) == list:
                # if there are any numbers in the list change them into strings
                row[data] = [str(a) for a in row[data]]
                # unique and sort the list and then change the list into a string
                row[data] = ','.join(sorted(list(set(row[data]))))

    return results


def pandas_dataset(list_of_results):
    results = change_lists_to_strings(list_of_results)  # we have added our function to change lists to strings
    df = pd.DataFrame(results)
    return df


def explode_dataset(result):
    df = pd.DataFrame(result)
    for column in df.select_dtypes(include='object'):
        df = df.explode(column=column).reset_index(drop=True)
    return df


def pandas_count(df, column_to_group_by):
    ds = df.groupby(column_to_group_by)['pdb_id'].nunique()
    return ds


def pandas_min_max(list_of_results, column_to_group_by, get_min=True):
    df = pandas_dataset(list_of_results)
    if get_min:
        ds = df.groupby(column_to_group_by)['pdb_id'].min()
    else:
        ds = df.groupby(column_to_group_by)['pdb_id'].max()
    return ds


def pandas_plot(df, column_to_group_by, graph_type='bar'):
    ds = pandas_count(df=df, column_to_group_by=column_to_group_by)
    ds.plot(kind=graph_type)


def pandas_plot_multi_groupby(df, first_column_to_group_by, second_column_to_group_by, y_axis='pdb_id',
                              graph_type='line'):
    new_df = df.groupby([first_column_to_group_by, second_column_to_group_by])
    ds = new_df.count().unstack().reset_index(first_column_to_group_by)
    ds.plot(x=first_column_to_group_by, y=y_axis, kind=graph_type).legend(bbox_to_anchor=(1.04, 1))


def pandas_plot_multi_groupby_min(df, first_column_to_group_by, second_column_to_group_by, graph_type='line',
                                  use_min=False, use_max=False):
    new_df = df.groupby([first_column_to_group_by])[second_column_to_group_by]
    if use_min:
        ds = new_df.min()
    elif use_max:
        ds = new_df.max()
    else:
        print('specify either use_min or use_max')
        return None
    ds.plot(x=first_column_to_group_by, y=second_column_to_group_by, kind=graph_type)


def pandas_box_plot(df, first_column_to_group_by, second_column_to_group_by):
    df.boxplot(column=second_column_to_group_by, by=first_column_to_group_by)
