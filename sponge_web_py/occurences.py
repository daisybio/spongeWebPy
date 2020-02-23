import json
import requests
from pandas import json_normalize

# local import
import sponge_web_py.config as config

def get_miRNAOccurences(disease_name,
                        mimat_number = None,
                        hs_number = None,
                        occurences = None,
                        sorting = None,
                        descending = None,
                        limit = 100,
                        offset = None):
    """
    Get all mirna involved in cancer type/dataset of interest occurring a certain amount of times.
    :param disease_name: The name of the dataset of interest as string.
                         If default (None) is set, all available datasets with corresponding information are shown.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param mimat_number: A list of mimat_number(s). If mimat_number is set, hs_number must be None.
    :param hs_number: A list of hs_number(s). If hs_number is set, mimat_number must be None.
    :param occurences: Threshold of amount of contributions a miRNA should be considered.
    :param sorting: Possibilities for sorting of the results. Possible values are "pValue", "mscor" or "correlation".
    :param descending: Descending (TRUE, default) or ascending (FALSE) ordering of the results.
    :param limit: Number of results that should be shown. Default value is 100 and can be up to 1000.
                  For more results please use batches, the provided offset parameter or download the whole dataset.
    :param offset: Starting point from where results should be shown.
    :return: A pandas dataframe with all miRNAs occurring at leat "occurrences" times.
             If empty return value will be the reason for failure.
    :example: get_miRNAOccurences(disease_name="kidney clear cell carcinoma", occurences = 1000, limit = 10)
    """
    # Test given parameter
    if sorting is not None:
        if sorting not in ["pValue", "mscor", "correlation"]:
            raise ValueError("Provided Ssrting parameter: ", sorting,
                             " is not an allowed value. Please check the help page for further information.")

    params = {"disease_name": disease_name, "occurences": occurences, "sorting": sorting,
              "descending": descending, "limit": limit, "offset": offset}

    # Add list type parameters
    if mimat_number is not None:
        params.update({"mimat_number": ",".join(mimat_number)})
    if hs_number is not None:
        params.update({"hs_number": ",".join(hs_number)})

    api_url = '{0}miRNAInteraction/getOccurence'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)