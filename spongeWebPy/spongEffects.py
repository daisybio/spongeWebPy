import json

import requests
from pandas import json_normalize

# local import
import spongeWebPy.config as config


def get_spongeEffectsRuns(disease_name):
    """
    Get all available spongEffects runs and their dataset informations
    :param disease_name: The name of the dataset of interest as string.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :return: Information about all spongEffects runs as pandas dataframe - If empty return value will be the reason for failure.
    :example: get_subtypeRunsForCancer("kidney clear cell carcinoma")
    """
    params = {"disease_name": disease_name}
    api_url = "{0}spongEffects/getSpongEffectsRuns".format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode("utf-8"))

    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)


def get_spongeEffectsRunPerformance(disease_name, level="gene"):
    """
    Get best spongEffects run performance for selected disease
    :param disease_name: The name of the dataset of interest as string.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param level: Element level to use, either gene or transcript
    :return: Information about performance of spongEffects runs as pandas dataframe - If empty return value will be the reason for failure.
    :example: get_subtypeRunsForCancer("kidney clear cell carcinoma")
    """
    params = {"disease_name": disease_name, "level": level}
    api_url = "{0}spongEffects/getRunPerformance".format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode("utf-8"))

    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)


def get_spongeEffectsRunClassPerformance(disease_name, level="gene"):
    """
    Get detailed spongEffects model performance information for given disease type
    :param disease_name: The name of the dataset of interest as string.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param level: Element level to use, either gene or transcript
    :return: Information about detailed performance of spongEffects runs as pandas dataframe - If empty return value will be the reason for failure.
    :example: get_subtypeRunsForCancer("kidney clear cell carcinoma")
    """
    params = {"disease_name": disease_name, "level": level}
    api_url = "{0}spongEffects/getRunClassPerformance".format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode("utf-8"))

    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)


def get_spongeEffectsEnrichmentScoreDistributions(disease_name, level="gene"):
    """
    Get enrichment score class distributions of a trained spongEffects model for a given disease
    :param disease_name: The name of the dataset of interest as string.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param level: Element level to use, either gene or transcript
    :return: Information about detailed performance of spongEffects runs as pandas dataframe - If empty return value will be the reason for failure.
    :example: get_subtypeRunsForCancer("kidney clear cell carcinoma")
    """
    params = {"disease_name": disease_name, "level": level}
    api_url = "{0}spongEffects/enrichmentScoreDistributions".format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode("utf-8"))

    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)


def get_spongeEffectsModules(disease_name, level="gene"):
    """
    Extract module hub elements for a given disease and level
    :param disease_name: The name of the dataset of interest as string.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param level: Element level to use, either gene or transcript
    :return: Information about detailed performance of spongEffects runs as pandas dataframe - If empty return value will be the reason for failure.
    :example: get_subtypeRunsForCancer("kidney clear cell carcinoma")
    """

    if level not in ["gene", "transcript"]:
        raise ValueError(
            "level " + level + " is not an allowed value [gene, transcript]."
        )

    params = {"disease_name": disease_name}
    endpoint = (
        "getSpongEffectsGeneModules"
        if level == "gene"
        else "getSpongEffectsTranscriptModules"
    )
    api_url = "{0}spongEffects/{1}".format(config.api_url_base, endpoint)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode("utf-8"))

    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)


def get_spongeEffectsModuleMembers(
    disease_name, level="gene", ensg_number=None, gene_symbol=None, gene_id=None
):
    """
    Get connected nodes of specified ceRNA hub(s)
    :param disease_name: The name of the dataset of interest as string.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param level: Element level to use, either gene or transcript
    :param ensg_number: A list of ensg number(s). If ensg_number is set, gene_symbol and gene_id must be None.
    :param gene_symbol: A list of gene symbol(s). If gene_symbol is set, ensg_number and gene_id must be None.
    :param gene_id: A list of internal gene id(s). If gene_symbol is set, ensg_number and gene_symbol must be None.
    :return: Information about detailed performance of spongEffects runs as pandas dataframe - If empty return value will be the reason for failure.
    :example: get_subtypeRunsForCancer("kidney clear cell carcinoma")
    """

    if level not in ["gene", "transcript"]:
        raise ValueError(
            "level " + level + " is not an allowed value [gene, transcript]."
        )

    params = {"disease_name": disease_name}

    if ensg_number is not None and gene_symbol is not None:
        raise ValueError(
            "Only one of ensg_number, gene_symbol and gene_id can to be set."
        )

    if ensg_number is not None:
        params.update({"ensg_number": ",".join(ensg_number)})
    if gene_symbol is not None:
        params.update({"gene_symbol": ",".join(gene_symbol)})
    if gene_id is not None:
        params.update({"gene_id": ",".join(gene_id)})

    endpoint = (
        "getSpongEffectsGeneModuleMembers"
        if level == "gene"
        else "getSpongEffectsTranscriptModuleMembers"
    )
    api_url = "{0}spongEffects/{1}".format(config.api_url_base, endpoint)

    response = requests.get(api_url, headers=config.headers, params=params)

    print(response.url)

    json_dicts = json.loads(response.content.decode("utf-8"))

    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)
