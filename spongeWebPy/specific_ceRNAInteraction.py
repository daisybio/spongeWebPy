import json

import requests
from pandas import json_normalize

# local import
import spongeWebPy.config as config


def get_specific_ceRNAInteractions(
    disease_name=None,
    ensg_number=None,
    gene_symbol=None,
    pValue=0.05,
    pValueDirection="<",
    limit=100,
    offset=None,
    sponge_db_version=config.LATEST,
):
    """
    Get all interactions between the given identifiers (ensg_number or gene_symbol).
    :param disease_name: The name of the dataset of interest as string.
                         If default (None) is set, all available datasets with corresponding information are shown.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param ensg_number: A list of ensg number(s). If ensg_number is set, gene_symbol must be None.
    :param gene_symbol: A list of gene symbol(s). If gene_symbol is set, ensg_number must be None.
    :param pValue: Threshold of the FDR adjusted p-value. Default is 0.05.
    :param pValueDirection: Direction of the FDR adjusted p-value threshold (<, >). Must be set if pValue is set.
                            Possible values are: "<", ">".
    :param limit: Number of results that should be shown. Default value is 100 and can be up to 1000.
                  For more results please use batches, the provided offset parameter or download the whole dataset.
    :param offset: Starting point from where results should be shown.
    :param sponge_db_version: Version of SPONGEdb to use. Default is set in config.
    :return: A pandas dataframe containing all interactions between genes of interest.
             If empty return value will be the reason for failure.
    :example: get_specific_ceRNAInteractions(disease_name = "pancancer",
                                             gene_symbol = ["PTENP1","VCAN","FN1"])
    """
    # Test parameter settings
    if pValueDirection is not None:
        if pValueDirection not in [">", "<"]:
            raise ValueError(
                "pValueDirection:",
                pValueDirection,
                " is not an allowed value. Please check the help page for further information.",
            )

    params = {
        "disease_name": disease_name,
        "pValue": pValue,
        "pValueDirection": pValueDirection,
        "limit": limit,
        "offset": offset,
        "sponge_db_version": sponge_db_version,
    }

    # Add list type parameters
    if ensg_number is not None:
        params.update({"ensg_number": ",".join(ensg_number)})
    if gene_symbol is not None:
        params.update({"gene_symbol": ",".join(gene_symbol)})

    api_url = "{0}ceRNAInteraction/findSpecific".format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode("utf-8"))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)
