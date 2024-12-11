import json

import requests
from pandas import json_normalize

# local import
import spongeWebPy.config as config


def get_survAna_pValues(
    disease_name, ensg_number=None, gene_symbol=None, sponge_db_version=config.LATEST
):
    """
    Retrieve pValues from log rank test based on raw survival analysis data
    :param disease_name: The name of the dataset of interest as string.
                         If default (None) is set, all available datasets with corresponding information are shown.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param ensg_number: A list of ensg number(s). If ensg_number is set, gene_symbol must be None.
    :param gene_symbol: A list of gene symbol(s). If gene_symbol is set, ensg_number must be None.
    :param sponge_db_version: Version of SPONGEdb to use. Default is set in config.
    :return: A data_frame with gene information and corresponding log rank test pValue.
             For raw data use function spongeWeb@get_survAna_rates.
             If empty return value will be the reason for failure.
    :example: get_survAna_pValues(disease_name = "kidney clear cell carcinoma",
                                  ensg_number = ["ENSG00000259090","ENSG00000217289"])
    """

    params = {"disease_name": disease_name, "sponge_db_version": sponge_db_version}

    # Add list type parameters
    if ensg_number is not None:
        params.update({"ensg_number": ",".join(ensg_number)})
    if gene_symbol is not None:
        params.update({"gene_symbol": ",".join(gene_symbol)})

    api_url = "{0}survivalAnalysis/getPValues".format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)
    json_dicts = json.loads(response.content.decode("utf-8"))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)


def get_survAna_rates(
    disease_name,
    ensg_number=None,
    gene_symbol=None,
    sample_ID=None,
    sponge_db_version=config.LATEST,
):
    """
    Get all raw survival analysis data for kaplan meier plots.
    :param disease_name: The name of the dataset of interest as string.
                         If default (None) is set, all available datasets with corresponding information are shown.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param ensg_number: A list of ensg number(s). If ensg_number is set, gene_symbol must be None.
    :param gene_symbol: A list of gene symbol(s). If gene_symbol is set, ensg_number must be None.
    :param sample_ID: A list of sample_ID of the patient/sample of interest.
    :param sponge_db_version: Version of SPONGEdb to use. Default is set in config.
    :return: A pandas dataframe with gene and patient/sample information and the "group information" encoded
             by column "overexpressed". Information about expression value of the gene
             (FALSE = underexpression, gene expression <= mean gene expression over all samples,
             TRUE = overexpression, gene expression >= mean gene expression over all samples)
             If empty return value will be the reason for failure.
    :example: get_survAna_rates(disease_name="kidney clear cell carcinoma",
                                ensg_number=["ENSG00000259090", "ENSG00000217289"],
                                sample_ID = ["TCGA-BP-4968","TCGA-B8-A54F"])
    """

    params = {"disease_name": disease_name, "sponge_db_version": sponge_db_version}

    # Add list type parameters
    if ensg_number is not None:
        params.update({"ensg_number": ",".join(ensg_number)})
    if gene_symbol is not None:
        params.update({"gene_symbol": ",".join(gene_symbol)})
    if sample_ID is not None:
        params.update({"sample_ID": ",".join(sample_ID)})

    api_url = "{0}survivalAnalysis/getRates".format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode("utf-8"))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)


def get_survAna_sampleInformation(
    disease_name, sample_ID=None, sponge_db_version=config.LATEST
):
    """
    Clinical Data For Samples/Patients
    :param disease_name: The name of the dataset of interest as string.
                         If default (None) is set, all available datasets with corresponding information are shown.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").

    :param sample_ID: A list of sample_ID of the patient/sample of interest.
    :param sponge_db_version: Version of SPONGEdb to use. Default is set in config.

    :return: A pandas dataframe with clinical date of all available or specific sample/patient.
    :example: get_survAna_sampleInformation(disease_name = "kidney clear cell carcinoma",
                                            sample_ID = ["TCGA-BP-4968","TCGA-B8-A54F"])
    """

    params = {"disease_name": disease_name, "sponge_db_version": sponge_db_version}

    # Add list type parameters
    if sample_ID is not None:
        params.update({"sample_ID": ",".join(sample_ID)})

    api_url = "{0}survivalAnalysis/sampleInformation".format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode("utf-8"))
    data = json_normalize(json_dicts)
    print(data)
    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)
