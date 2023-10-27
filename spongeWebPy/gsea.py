import json
import requests
from pandas import json_normalize
import base64
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

#local import
import spongeWebPy.config as config

def get_gseaSets(disease_name_1, disease_name_2, condition_1, condition_2, disease_subtype_1 = None, disease_subtype_2 = None):
    """
    Get all gene sets with results for the given diseases and conditions.
    :param disease_name_1: Name of the disease type/dataset for the first part of the comparison. Fuzzy search available.
    :param disease_name_2: Name of the disease type/dataset for the second part of the comparison. Fuzzy search available.
    :param condition_1: Condition for the first part of the comparison (e.g. disease or normal).
    :param condition_2: Condition for the second part of the comparison (e.g. disease or normal).
    :param disease_subtype_1: Name of the disease subtype for the first part of the comparison. Overtype is selected if it is not given.
    :param disease_subtype_2: Name of the disease subtype for the second part of the comparison. Overtype is selected if it is not given.
    :return: A data_frame containing all gene sets with results for the given disease and conditions.
    :example: get_gseaSets(disease_name_1 = "liver", disease_name_2 = "thymoma",
                        condition_1 = "disease", condition_2 = "disease")
    """
    params = {
        "disease_name_1": disease_name_1,
        "disease_name_2": disease_name_2,
        "condition_1": condition_1,
        "condition_2": condition_2 
    }

    if disease_subtype_1 is not None:
        params.update({"disease_subtype_1": disease_subtype_1})
    if disease_subtype_2 is not None:
        params.update({"disease_subtype_2": disease_subtype_2})


    api_url = '{0}gseaSets'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)

def get_gseaTerms(disease_name_1, disease_name_2, condition_1, condition_2, gene_set, disease_subtype_1 = None, disease_subtype_2 = None):
    """
    Get all terms with results for the given diseases, conditions and gene set.
    :param disease_name_1: Name of the disease type/dataset for the first part of the comparison. Fuzzy search available.
    :param disease_name_2: Name of the disease type/dataset for the second part of the comparison. Fuzzy search available.
    :param condition_1: Condition for the first part of the comparison (e.g. disease or normal).
    :param condition_2: Condition for the second part of the comparison (e.g. disease or normal).
    :param gene_set: Name of gene set that contains the terms which are retrieved.
    :param disease_subtype_1: Name of the disease subtype for the first part of the comparison. Overtype is selected if it is not given.
    :param disease_subtype_2: Name of the disease subtype for the second part of the comparison. Overtype is selected if it is not given.
    :return: A data_frame containing all terms with results for the given diseases, conditions and gene set.
    :example: get_gseaTerms(disease_name_1 = "liver", disease_name_2 = "thymoma",
                            condition_1 = "disease", condition_2 = "disease",
                            gene_set = "GO_Biological_Process_2023")
    """
    params = {
        "disease_name_1": disease_name_1,
        "disease_name_2": disease_name_2,
        "condition_1": condition_1,
        "condition_2": condition_2,
        "gene_set": gene_set
    }

    if disease_subtype_1 is not None:
        params.update({"disease_subtype_1": disease_subtype_1})
    if disease_subtype_2 is not None:
        params.update({"disease_subtype_2": disease_subtype_2})

    api_url = '{0}gseaTerms'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)

def get_gseaResults(disease_name_1, disease_name_2, condition_1, condition_2, gene_set, disease_subtype_1 = None, disease_subtype_2 = None, term = None):
    """
    Get gsea results for the given diseases, conditions, gene set and terms.
    Get all terms with results for the given diseases, conditions and gene set.
    :param disease_name_1: Name of the disease type/dataset for the first part of the comparison. Fuzzy search available.
    :param disease_name_2: Name of the disease type/dataset for the second part of the comparison. Fuzzy search available.
    :param condition_1: Condition for the first part of the comparison (e.g. disease or normal).
    :param condition_2: Condition for the second part of the comparison (e.g. disease or normal).
    :param gene_set: Name of gene set that contains the terms for which to get the results.
    :param disease_subtype_1: Name of the disease subtype for the first part of the comparison. Overtype is selected if it is not given.
    :param disease_subtype_2: Name of the disease subtype for the second part of the comparison. Overtype is selected if it is not given.
    :param term: List of the terms for which to get the results. Gets results for all terms if it is not given.
    :return: A data_frame containing all results for the given diseases, conditions, gene set and terms.
    :example: get_gseaResults(disease_name_1 = "liver", disease_name_2 = "thymoma",
                              condition_1 = "disease", condition_2 = "disease",
                              gene_set = "GO_Biological_Process_2023", term="GO:0001676")
    """
    params = {
        "disease_name_1": disease_name_1,
        "disease_name_2": disease_name_2,
        "condition_1": condition_1,
        "condition_2": condition_2,
        "gene_set": gene_set
    }

    if disease_subtype_1 is not None:
        params.update({"disease_subtype_1": disease_subtype_1})
    if disease_subtype_2 is not None:
        params.update({"disease_subtype_2": disease_subtype_2})
    if term is not None:
        params.update({"term": ",".join(term)})

    api_url = '{0}gseaResults'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)

def get_gseaPlot(disease_name_1, disease_name_2, condition_1, condition_2, gene_set, term, disease_subtype_1 = None, disease_subtype_2 = None):
    """
    Get gsea enrichment plot for the given diseases, conditions, gene set and term.
    Get all terms with results for the given diseases, conditions and gene set.
    :param disease_name_1: Name of the disease type/dataset for the first part of the comparison. Fuzzy search available.
    :param disease_name_2: Name of the disease type/dataset for the second part of the comparison. Fuzzy search available.
    :param condition_1: Condition for the first part of the comparison (e.g. disease or normal).
    :param condition_2: Condition for the second part of the comparison (e.g. disease or normal).
    :param gene_set: Name of gene set that contains the terms for which to get the enrichment plot.
    :param term: Name of the term for which to get the enrichment plot.
    :param disease_subtype_1: Name of the disease subtype for the first part of the comparison. Overtype is selected if it is not given.
    :param disease_subtype_2: Name of the disease subtype for the second part of the comparison. Overtype is selected if it is not given.
    :return: A matplotlib plot object containing the gsea enrichment plot
    :example: get_gseaPlot(disease_name_1 = "liver", disease_name_2 = "thymoma",
                              condition_1 = "disease", condition_2 = "disease",
                              gene_set = "GO_Biological_Process_2023", term="GO:0001676")
    """
    params = {
        "disease_name_1": disease_name_1,
        "disease_name_2": disease_name_2,
        "condition_1": condition_1,
        "condition_2": condition_2,
        "gene_set": gene_set,
        "term": term
    }

    if disease_subtype_1 is not None:
        params.update({"disease_subtype_1": disease_subtype_1})
    if disease_subtype_2 is not None:
        params.update({"disease_subtype_2": disease_subtype_2})

    api_url = '{0}gseaPlot'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    result = json.loads(response.content.decode('utf-8'))
    img = base64.b64decode(result)
    img = io.BytesIO(img)
    img = mpimg.imread(img, format='PNG')
    figure, axes = plt.subplots()
    axes.imshow(img, interpolation='nearest')

    if response.status_code == 200:
        return figure
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + result["detail"].values)