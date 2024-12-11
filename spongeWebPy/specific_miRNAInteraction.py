import json

import requests
from pandas import json_normalize

# local import
import spongeWebPy.config as config


def get_specific_miRNAInteraction(
    disease_name=None,
    mimat_number=None,
    hs_number=None,
    pValue=0.05,
    pValueDirection="<",
    mscor=None,
    mscorDirection="<",
    correlation=None,
    correlationDirection="<",
    limit=100,
    offset=None,
    sponge_db_version=config.LATEST,
):
    """
    Get all ceRNA interactions where miRNA(s) of interest (different identifiers available - e.g. hs number or mimat number) contribute to.
    :param disease_name: The name of the dataset of interest as string.
                         If default (None) is set, all available datasets with corresponding information are shown.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param mimat_number: Mimat_number of interest. If mimat_number is set, hs_number must be None.
    :param hs_number: hs_number of interest. If hs_number is set, mimat_number must be None.
    :param limit: Number of results that should be shown. Default value is 100 and can be up to 1000.
                  For more results please use batches, the provided offset parameter or download the whole dataset.
    :param pValue: Threshold of the FDR adjusted p-value. Default is 0.05.
    :param pValueDirection: Direction of the FDR adjusted p-value threshold (<, >). Must be set if pValue is set.
                            Possible values are: "<", ">".
    :param mscor: Threshold of the 'multiple sensitivity correlation' (mscor).
    :param mscorDirection: Direction of the mscor threshold (<, >). Must be set if pValue is set.
                           Possible values are: "<", ">".
    :param correlation: Threshold of the correlation.
    :param correlationDirection: Direction of the correlation threshold (<, >). Must be set if pValue is set.
                                 Possible values are: "<", ">".
    :param offset: Starting point from where results should be shown.
    :param sponge_db_version: Version of SPONGEdb to use. Default is set in config.
    :return: A pandas dataframe containing all ceRNA interactions fitting the parameters.
             If empty return value will be the reason for failure.
    :example: get_specific_miRNAInteraction(disease_name = "kidney clear cell carcinoma",
                                            mimat_number = "MIMAT0000076", pValue=0.02,
                                            limit = 15)
    """

    params = {
        "disease_name": disease_name,
        "mimat_number": mimat_number,
        "hs_number": hs_number,
        "pValue": pValue,
        "pValueDirection": pValueDirection,
        "mscor": mscor,
        "mscorDirection": mscorDirection,
        "correlation": correlation,
        "correlationDirection": correlationDirection,
        "limit": limit,
        "offset": offset,
        "sponge_db_version": sponge_db_version,
    }

    api_url = "{0}miRNAInteraction/findSpecific".format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode("utf-8"))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)
