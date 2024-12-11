import json

import requests
from pandas import json_normalize

# local import
import spongeWebPy.config as config


def get_geneOntology(gene_symbol):
    """
    Associated GO terms for gene(s) of interest. QuickGO - a fast web-based browser of the Gene Ontology and Gene Ontology annotation data - is used as external source.
    :param gene_symbol: A list of gene symbol(s). Required parameter.
    :example: Get all GO terms associated with gene(s) of interest.
              get_geneOntology(gene_symbol=["PTEN","TIGAR"])
    """

    params = {}

    # Add list type parameters
    if gene_symbol is not None:
        params.update({"gene_symbol": ",".join(gene_symbol)})

    api_url = "{0}getGeneOntology".format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode("utf-8"))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 202:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)
