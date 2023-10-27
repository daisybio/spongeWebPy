import json
import requests
from pandas import json_normalize

#local import
import spongeWebPy.config as config

def get_differentialExpressionGene(disease_name_1, disease_name_2, condition_1, condition_2, ensg_number=None, gene_symbol=None, disease_subtype_1 = None, disease_subtype_2 = None):
    """
    Get differential expression information for the given comparison and gene.
    :param disease_name_1: Name of the disease type/dataset for the first part of the comparison. Fuzzy search available.
    :param disease_name_2: Name of the disease type/dataset for the second part of the comparison. Fuzzy search available.
    :param condition_1: Condition for the first part of the comparison (e.g. disease or normal).
    :param condition_2: Condition for the second part of the comparison (e.g. disease or normal).
    :param ensg_number: A list of ensg number(s). If ensg number is set, gene symbol must be NULL.
    :param gene_symbol: A list of gene symbol(s). If gene symbol is set, ensg bumber must be NULL.
    :param disease_subtype_1: Name of the disease subtype for the first part of the comparison. Overtype is selected if it is not given.
    :param disease_subtype_2: Name of the disease subtype for the second part of the comparison. Overtype is selected if it is not given.
    :return: A data_frame differential expression information for the given comparison and gene.
    :example: get_differentialExpressionGene(disease_name_1 = "liver",
                                            disease_name_2 = "thymoma",
                                            condition_1 = "disease",
                                            condition_2 = "disease",
                                            gene_symbol = "CYP2E1")
    """
    params = {
        "disease_name_1": disease_name_1,
        "disease_name_2": disease_name_2,
        "condition_1": condition_1,
        "condition_2": condition_2 
    }

    # Add list type parameters
    if ensg_number is not None and gene_symbol is not None:
        raise ValueError("Only one of ensg_number, gene_symbol is allowed")
    if ensg_number is not None:
        params.update({"ensg_number": ",".join(ensg_number)})
    if gene_symbol is not None:
        params.update({"gene_symbol": ",".join(gene_symbol)})
    if disease_subtype_1 is not None:
        params.update({"disease_subtype_1": disease_subtype_1})
    if disease_subtype_2 is not None:
        params.update({"disease_subtype_2": disease_subtype_2})

    api_url = '{0}differentialExpression'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)

def get_differentialExpressionTranscript(disease_name_1, disease_name_2, condition_1, condition_2, enst_number=None, disease_subtype_1 = None, disease_subtype_2 = None):
    """
    Get differential expression information for the given comparison and transcript.
    :param disease_name_1: Name of the disease type/dataset for the first part of the comparison. Fuzzy search available.
    :param disease_name_2: Name of the disease type/dataset for the second part of the comparison. Fuzzy search available.
    :param condition_1: Condition for the first part of the comparison (e.g. disease or normal).
    :param condition_2: Condition for the second part of the comparison (e.g. disease or normal).
    :param enst_number: A list of enst number(s). If enst number is not set, information for all transcripts is provided.
    :param disease_subtype_1: Name of the disease subtype for the first part of the comparison. Overtype is selected if it is not given.
    :param disease_subtype_2: Name of the disease subtype for the second part of the comparison. Overtype is selected if it is not given.
    :return: A data_frame differential expression information for the given comparison and transcript.
    :example: get_differentialExpressionTranscript(disease_name_1 = "liver",
                                            disease_name_2 = "thymoma",
                                            condition_1 = "disease",
                                            condition_2 = "disease")
    """
    params = {
        "disease_name_1": disease_name_1,
        "disease_name_2": disease_name_2,
        "condition_1": condition_1,
        "condition_2": condition_2 
    }

    # Add list type parameters
    if enst_number is not None:
        params.update({"enst_number": ",".join(enst_number)})
    if disease_subtype_1 is not None:
        params.update({"disease_subtype_1": disease_subtype_1})
    if disease_subtype_2 is not None:
        params.update({"disease_subtype_2": disease_subtype_2})


    api_url = '{0}differentialExpressionTranscript'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)

