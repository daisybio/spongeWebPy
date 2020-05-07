import json
import requests
from pandas import json_normalize

# local import
import spongeWebPy.config as config

def get_hallmark(gene_symbol):
    """
    Associated cancer hallmark for gene(s) of interest. Cancer Hallmark Genes (http://bio-bigdata.hrbmu.edu.cn/CHG/) is used as external source.
    :param gene_symbol: A list of gene symbol(s). Required parameter.
    :example: Get all GO terms associated with gene(s) of interest.
              get_hallmark(gene_symbol=["TUBBP2","CSNK1A1L"])
    """

    params = {}

    # Add list type parameters
    if gene_symbol is not None:
        params.update({"gene_symbol": ",".join(gene_symbol)})

    api_url = '{0}getHallmark'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)