import json
import requests
from pandas import json_normalize

#local import
import sponge_web_py.config as config

def get_geneExprValues(disease_name, ensg_number = None, gene_symbol = None):
    """
    Get all expression values for gene(s) of interest.
    :param disease_name: The name of the dataset of interest as string.
                         If default (None) is set, all available datasets with corresponding information are shown.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param ensg_number: A list of ensg number(s). If ensg_number is set, gene_symbol must be None.
    :param gene_symbol: A list of gene symbol(s). If gene_symbol is set, ensg_number must be None.
    :return: A pandas dataframe with gene expression values. - If empty return value will be the reason for failure.
    :example: get_geneExprValues(disease_name = "kidney clear cell carcinoma",
                    ensg_number = ["ENSG00000259090","ENSG00000217289"])
    """
    params = {"disease_name": disease_name, "ensg_number" : ensg_number, "gene_symbol" : gene_symbol}
    api_url = '{0}exprValue/getceRNA'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)


def get_mirnaExprValues(disease_name, mimat_number = None, hs_number = None):
    """
    Get all expression values for miRNA(s) of interest.
    :param disease_name: The name of the dataset of interest as string.
                         If default (None) is set, all available datasets with corresponding information are shown.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param mimat_number: A list of mimat_number(s). If mimat_number is set, hs_number must be None.
    :param hs_number: A list of hs_number(s). If hs_number is set, mimat_number must be None.
    :return: A pandas dataframe with gene mirna values. - If empty return value will be the reason for failure.
    :example: get_mirnaExprValues(disease_name = "kidney clear cell carcinoma",
                     mimat_number = ["MIMAT0000076", "MIMAT0000261"])
    """
    params = {"disease_name": disease_name, "mimat_number": mimat_number, "hs_number": hs_number}
    api_url = '{0}exprValue/getmirNA'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)