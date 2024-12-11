import json

import requests
from pandas import json_normalize

# local import
import spongeWebPy.config as config


def get_sponged_miRNA(
    disease_name=None, ensg_number=None, gene_symbol=None, between=False
):
    """
    Get all miRNAs that contribute to all interactions between the given identifiers (ensg_number or gene_symbol).
    :param disease_name: The name of the dataset of interest as string.
                         If default (None) is set, all available datasets with corresponding information are shown.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param ensg_number: A list of ensg number(s). If ensg_number is set, gene_symbol must be None.
    :param gene_symbol: A list of gene symbol(s). If gene_symbol is set, ensg_number must be None.
    :param between: If false (default), all interactions where one of the interaction partners fits the given genes of interest
                    will be considered. If true, just interactions between the genes of interest will be considered.
    :param sponge_db_version: Version of SPONGEdb to use. Default is set in config.
    :return: A pandas dataframe containing all found miRNAs.
             If empty return value will be the reason for failure.
    :example: get_sponged_miRNA(disease_name="kidney", gene_symbol = ["TCF7L1", "SEMA4B"])
    """
    params = {"disease_name": disease_name, "between": between}

    # Add list type parameters
    if ensg_number is not None:
        params.update({"ensg_number": ",".join(ensg_number)})
    if gene_symbol is not None:
        params.update({"gene_symbol": ",".join(gene_symbol)})

    api_url = "{0}miRNAInteraction/findceRNA".format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode("utf-8"))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)
