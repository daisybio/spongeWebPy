import json
import requests
from pandas import json_normalize

# local import
import sponge_web_py.config as config

def get_geneCount(disease_name=None,
                  ensg_number=None,
                  gene_symbol=None,
                  minCountAll = None,
                  minCountSign = None):
    """
    Number of Times Gene Involved in Complete Network and Significant Interactions.
    :param disease_name: The name of the dataset of interest as string.
                         If default (None) is set, all available datasets with corresponding information are shown.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param ensg_number: A list of ensg number(s). If ensg_number is set, gene_symbol must be None.
    :param gene_symbol: A list of gene symbol(s). If gene_symbol is set, ensg_number must be None.
    :param minCountAll: Defines the minimal number of times a gene has to be involved in the complete network
                        (e.g. the degree of the corresponding node must be greater than minCountAll).
    :param minCountSign: Defines the minimal number of times a gene has to be involved in significant
                        (p.adj < 0.05) interactions in the network.
    :return: A pandas dataframe cotaining the amount of times a gene is involved in the complete network (equals to degree),
             column count_all, and in significant (FDR adjusted pValue < 0.05) interactions of the network,
             column count_sign. If empty return value will be the reason for failure.
    :example: # Get all genes from specific cancer with a minimum number of 150 at significant ceRNA interactions
              get_geneCount(disease_name = "kidney clear cell carcinoma", minCountSign = 150)
    """

    params = {"disease_name": disease_name, "minCountAll": minCountAll, "minCountSign": minCountSign}

    # Add list type parameters
    if ensg_number is not None:
        params.update({"ensg_number": ",".join(ensg_number)})
    if gene_symbol is not None:
        params.update({"gene_symbol": ",".join(gene_symbol)})

    api_url = '{0}getGeneCount'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)