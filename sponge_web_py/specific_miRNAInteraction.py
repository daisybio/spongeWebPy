import json
import requests
from pandas import json_normalize

# local import
import sponge_web_py.config as config

def get_specific_miRNAInteraction(disease_name = None,
                                  mimat_number = None,
                                  hs_number = None,
                                  limit = 100,
                                  offset = None):
    """
    Get all ceRNA interactions where miRNA(s) of interest (different identifiers available - e.g. hs number or mimat number) contribute to.
    :param disease_name: The name of the dataset of interest as string.
                         If default (None) is set, all available datasets with corresponding information are shown.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param mimat_number: A list of mimat_number(s). If mimat_number is set, hs_number must be None.
    :param hs_number: A list of hs_number(s). If hs_number is set, mimat_number must be None.
    :param limit: Number of results that should be shown. Default value is 100 and can be up to 1000.
                  For more results please use batches, the provided offset parameter or download the whole dataset.
    :param offset: Starting point from where results should be shown.
    :return: A pandas dataframe containing all ceRNA interactions fitting the parameters.
             If empty return value will be the reason for failure.
    :example: get_specific_miRNAInteraction(disease_name = "kidney clear cell carcinoma",
                                            mimat_number = ["MIMAT0000076", "MIMAT0000261"],
                                            limit = 15)
    """

    params = {"disease_name": disease_name, "limit":limit, "offset":offset, "information": False}

    # Add list type parameters
    if mimat_number is not None:
        params.update({"mimat_number": ",".join(mimat_number)})
    if hs_number is not None:
        params.update({"hs_number": ",".join(hs_number)})

    api_url = '{0}miRNAInteraction/findSpecific'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)