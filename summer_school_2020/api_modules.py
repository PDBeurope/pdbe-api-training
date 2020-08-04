import pandas as pd
import requests

# settings for PDBe API
base_url = "https://www.ebi.ac.uk/pdbe/"  # the beginning of the URL for PDBe's API.
search_url = base_url + 'search/pdb/select?'  # the rest of the URL used for PDBe's search API.


def make_request(search_term, number_of_rows=10):
    """
    makes a get request to the PDBe API
    :param search_term: the terms used to search
    :param number_of_rows: number or rows to return - limited to 10
    :return dict: response JSON
    """
    search_variables = '&wt=json&rows={}'.format(number_of_rows)
    url = search_url + search_term + search_variables
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("[No data retrieved - %s] %s" % (response.status_code, response.text))

    return {}


def format_search_terms(search_terms, filter_terms=None):
    """
    Change search terms from a dictionary to a string for the URL
    :param dict search_terms: dictionary of search terms
    :param lst filter_terms: list of terms to filter with
    :return str: search string
    """
    filter_string = ''
    search_list = []
    if isinstance(search_terms, dict):
        for key in search_terms:
            term = search_terms.get(key)
            if ' ' in term and not '[' in term:
                if '"' not in term:
                    term = '"{}"'.format(term)
                elif "'" not in term:
                    term = "'{}'".format(term)
            search_list.append('{}:{}'.format(key, term))
        search_string = ' AND '.join(search_list)
        if filter_terms:
            filter_string = '&fl={}'.format(','.join(filter_terms))
        final_search_string = 'q={}{}'.format(search_string, filter_string)
        return final_search_string
    else:
        print('search terms is not defined as a dictionary')
        return ''


def run_search(search_terms, filter_terms=None, number_of_rows=10):
    """
    Run the search with set of search terms
    :param dict search_terms: dictionary of search terms
    :param list filter_terms: list of terms to filter by
    :param int number_of_rows: number of search rows to return
    :return lst: list of results
    """
    search_term = format_search_terms(search_terms, filter_terms)
    if search_term:
        response = make_request(search_term, number_of_rows)
        if response:
            results = response.get('response', {}).get('docs', [])
            print('Number of results for {}: {}'.format(','.join(search_terms.values()), len(results)))
            return results
    print('No results')
    return []


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


def pandas_count(list_of_results, column_to_group_by):
    df = pandas_dataset(list_of_results)
    ds = df.groupby(column_to_group_by)['pdb_id'].nunique()
    return ds


def pandas_min_max(list_of_results, column_to_group_by, get_min=True):
    df = pandas_dataset(list_of_results)
    if get_min:
        ds = df.groupby(column_to_group_by)['pdb_id'].min()
    else:
        ds = df.groupby(column_to_group_by)['pdb_id'].max()
    return ds


def pandas_plot(list_of_results, column_to_group_by, graph_type='bar'):
    ds = pandas_count(list_of_results=list_of_results, column_to_group_by=column_to_group_by)
    ds.plot(kind=graph_type)


def pandas_plot_multi_groupby(results, first_column_to_group_by, second_column_to_group_by, y_axis='pdb_id',
                              graph_type='line'):
    df = pandas_dataset(results)
    new_df = df.groupby([first_column_to_group_by, second_column_to_group_by])
    ds = new_df.count().unstack().reset_index(first_column_to_group_by)
    ds.plot(x=first_column_to_group_by, y=y_axis, kind=graph_type).legend(bbox_to_anchor=(1.04,1))


def pandas_plot_multi_groupby_min(results, first_column_to_group_by, second_column_to_group_by, graph_type='line',
                                  use_min=False, use_max=False):
    df = pandas_dataset(results)
    new_df = df.groupby([first_column_to_group_by])[second_column_to_group_by]
    if use_min:
        ds = new_df.min()
    elif use_max:
        ds = new_df.max()
    else:
        print('specify either use_min or use_max')
        return None
    ds.plot(x=first_column_to_group_by, y=second_column_to_group_by, kind=graph_type)


def pandas_box_plot(results, first_column_to_group_by, second_column_to_group_by):
    df = pandas_dataset(results)
    df.boxplot(column=second_column_to_group_by, by=first_column_to_group_by)
