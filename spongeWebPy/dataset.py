import json
import requests
from pandas import json_normalize

#local import
import spongeWebPy.config as config


def get_subtypeRunsForCancer(disease_name):
    """
        Retrieve cancer subtype runs for the provided cancer type
        :param disease_name: The name of the dataset of interest as string.
                             Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
        :return: Information about all subtypes as pandas dataframe - If empty return value will be the reason for failure.
        :example: get_subtypeRunsForCancer("kidney clear cell carcinoma")
    """
    params = {"disease_name": disease_name}
    api_url = '{0}dataset'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    cancer_abbreviation = json_dicts[0]['disease_name_abbreviation']
    if cancer_abbreviation != '':
        subtypes = get_datasetInformation(disease_name=cancer_abbreviation)
        return subtypes
    else:
        if response.status_code == 404:
            raise ValueError("Invalid request. Reason: " + response["message"])
    return None


def get_datasetInformation(disease_name=None):
    """
    Get information about all available datasets to start browsing or search for a specific cancer type/dataset.
    :param disease_name: The name of the dataset of interest as string.
                         If default (None) is set, all available datasets with corresponding information are shown.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :return: Information about all or specific dataset(s) as pandas dataframe - If empty return value will be the reason for failure.
    :example: get_datasetInformation("kidney clear cell carcinoma")
    """
    params = {"disease_name": disease_name}
    api_url = '{0}dataset'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)

def get_runInformation(disease_name):
    """
    Retrieve all used parameters of the SPONGE method to create published results for the cancer type/dataset of interest.
    :param disease_name: Name of the specific cancer type/dataset as string.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :return: Run information about dataset of interest as pandas dataframe - If empty return value will be the reason for failure.
    :example: get_runInformation("kidney clear cell carcinoma")
    """

    params = {"disease_name": disease_name}
    api_url = '{0}dataset/runInformation'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)

get_subtypeRunsForCancer('breast invasive')