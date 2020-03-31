import json
import requests
from pandas import json_normalize

# local import
import spongeWebPy.config as config

def get_ceRNA(disease_name,
              gene_type=None,
              minBetweenness=None,
              minNodeDegree=None,
              minEigenvector=None,
              sorting=None,
              descending=True,
              limit=100,
              offset=None):
    """
    Get all ceRNAs in a disease of interest (search not for a specific ceRNA, but search for all ceRNAs satisfying filter functions).
    :param disease_name: The name of the dataset of interest as string.
                         If default (None) is set, all available datasets with corresponding information are shown.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param gene_type: String that defines the type of gene of interest. One out of
                      [3prime_overlapping_ncRNA, antisense, antisense_RNA, bidirectional_promoter_lncRNA, IG_C_gene,
                      IG_C_pseudogene, IG_V_gene, IG_V_pseudogene, lincRNA, macro_lncRNA, miRNA, misc_RNA, Mt_rRNA,
                      polymorphic_pseudogene, processed_pseudogene, processed_transcript, protein_coding, pseudogene,
                      ribozyme, rRNA, rRNA_pseudogene, scaRNA, scRNA, sense_intronic, sense_overlapping, snoRNA, snRNA,
                      TEC, TR_C_gene, TR_V_gene, TR_V_pseudogene, transcribed_processed_pseudogene,
                      transcribed_unitary_pseudogene, transcribed_unprocessed_pseudogene,
                      translated_processed_pseudogene, unitary_pseudogene, unprocessed_pseudogene, vaultRNA].
    :param minBetweenness: Threshold of the betweenness.
    :param minNodeDegree: Threshold of the degree.
    :param minEigenvector: Threshold of the eigenvektor.
    :param sorting: Possibilities for sorting of the results. Possible values are "degree", "betweenness" or "eigenvector".
    :param descending: Descending (TRUE, default) or ascending (FALSE) ordering of the results.
    :param limit: Number of results that should be shown. Default value is 100 and can be up to 1000.
                  For more results please use batches, the provided offset parameter or download the whole dataset.
    :param offset: Starting point from where results should be shown.
    :return: A pandas dataframe containing all ceRNAs (genes) satisfying the given filters.
             If empty return value will be the reason for failure.
    :example: get_ceRNA(disease_name = "kidney clear cell carcinoma",
                        gene_type = "lincRNA", minBetweenness = 0.8)
    """

    # Test given parameter
    if gene_type is not None:
        types = ["3prime_overlapping_ncRNA", "antisense", "antisense_RNA", "bidirectional_promoter_lncRNA",
                 "IG_C_gene", "IG_C_pseudogene",
                 "IG_V_gene", "IG_V_pseudogene", "lincRNA", "macro_lncRNA", "miRNA", "misc_RNA", "Mt_rRNA",
                 "polymorphic_pseudogene",
                 "processed_pseudogene", "processed_transcript", "protein_coding", "pseudogene", "ribozyme", "rRNA",
                 "rRNA_pseudogene",
                 "scaRNA", "scRNA", "sense_intronic", "sense_overlapping", "snoRNA", "snRNA", "TEC", "TR_C_gene",
                 "TR_V_gene", "TR_V_pseudogene",
                 "transcribed_processed_pseudogene", "transcribed_unitary_pseudogene",
                 "transcribed_unprocessed_pseudogene",
                 "translated_processed_pseudogene", "unitary_pseudogene", "unprocessed_pseudogene", "vaultRNA"]
        if gene_type not in types:
            raise ValueError(
                "Gene_type " + gene_type + " is not an allowed value. Please check the help page for further information.")
    if sorting is not None:
        if sorting not in ["degree", "betweenness", "eigenvector"]:
            raise ValueError("Provided Ssrting parameter: ", sorting,
                             " is not an allowed value. Please check the help page for further information.")

    params = {"disease_name": disease_name, "gene_type": gene_type, "minBetweenness": minBetweenness,
              "minNodeDegree": minNodeDegree, "minEigenvector": minEigenvector, "sorting": sorting,
              "descending": descending, "limit": limit, "offset": offset, "information": False}

    api_url = '{0}/findceRNA'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)