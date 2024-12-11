import json

import requests
from pandas import json_normalize

# local import
import spongeWebPy.config as config


def get_overallCounts(sponge_db_version=config.LATEST):
    """
    Function return current statistic about database - amount of shared miRNA, significant and insignificant interactions per dataset
    :param sponge_db_version: Version of SPONGEdb to use. Default is set in config.
    :return: Overview of interaction counts about all or specific dataset as pandas dataframe.
    :example: get_overallCounts()
    """

    params = {"sponge_db_version": sponge_db_version}
    api_url = "{0}getOverallCounts".format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode("utf-8"))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)
