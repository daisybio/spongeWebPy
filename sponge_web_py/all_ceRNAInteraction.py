import json
import requests
from pandas import json_normalize

# local import
import sponge_web_py.config as config


def get_all_ceRNAInteractions(disease_name=None,
                              ensg_number=None,
                              gene_symbol=None,
                              gene_type=None,
                              pValue=0.05,
                              pValueDirection="<",
                              mscor=None,
                              mscorDirection="<",
                              correlation=None,
                              correlationDirection="<",
                              sorting=None,
                              descending=True,
                              limit=100,
                              offset=None):
    """
    Get all ceRNA interactions by given identifications (ensg_number, gene_symbol or gene_type),
    specific cancer type/dataset or different filter possibilities according different statistical values
    (e.g. FDR adjusted p-value).
    :param disease_name: The name of the dataset of interest as string.
                         If default (None) is set, all available datasets with corresponding information are shown.
                         Fuzzy search is available (e.g. "kidney clear cell carcinoma" or just "kidney").
    :param ensg_number: A list of ensg number(s). If ensg_number is set, gene_symbol must be None.
    :param gene_symbol: A list of gene symbol(s). If gene_symbol is set, ensg_number must be None.
    :param gene_type: String that defines the type of gene of interest. One out of
                      [3prime_overlapping_ncRNA, antisense, antisense_RNA, bidirectional_promoter_lncRNA, IG_C_gene,
                      IG_C_pseudogene, IG_V_gene, IG_V_pseudogene, lincRNA, macro_lncRNA, miRNA, misc_RNA, Mt_rRNA,
                      polymorphic_pseudogene, processed_pseudogene, processed_transcript, protein_coding, pseudogene,
                      ribozyme, rRNA, rRNA_pseudogene, scaRNA, scRNA, sense_intronic, sense_overlapping, snoRNA, snRNA,
                      TEC, TR_C_gene, TR_V_gene, TR_V_pseudogene, transcribed_processed_pseudogene,
                      transcribed_unitary_pseudogene, transcribed_unprocessed_pseudogene,
                      translated_processed_pseudogene, unitary_pseudogene, unprocessed_pseudogene, vaultRNA].
    :param pValue: Threshold of the FDR adjusted p-value. Default is 0.05.
    :param pValueDirection: Direction of the FDR adjusted p-value threshold (<, >). Must be set if pValue is set.
                            Possible values are: "<", ">".
    :param mscor: Threshold of the 'multiple sensitivity correlation' (mscor).
    :param mscorDirection: Direction of the mscor threshold (<, >). Must be set if pValue is set.
                           Possible values are: "<", ">".
    :param correlation: Threshold of the correlation.
    :param correlationDirection: Direction of the correlation threshold (<, >). Must be set if pValue is set.
                                 Possible values are: "<", ">".
    :param sorting: Possibilities for sorting of the results. Possible values are "pValue", "mscor" or "correlation".
    :param descending: Descending (TRUE, default) or ascending (FALSE) ordering of the results.
    :param limit: Number of results that should be shown. Default value is 100 and can be up to 1000.
                  For more results please use batches, the provided offset parameter or download the whole dataset.
    :param offset: Starting point from where results should be shown.
    :return: A pandas dataframe containing all ceRNA interactions fitting the paramters.
             If empty return value will be the reason for failure.
    :example: #Retrieve all possible ceRNAs for gene, identified by ensg_number and threshold for pValue and mscor.
            get_all_ceRNAInteractions(ensg_number=["ENSG00000259090","ENSG00000217289"], pValue=0.5,
                                      pValueDirection="<", mscor=0.006, mscorDirection="<", limit=15)
    """

    # Test parameter settings if provided
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
    if pValueDirection is not None:
        if pValueDirection not in [">", "<"]:
            raise ValueError("pValueDirection:", pValueDirection,
                             " is not an allowed value. Please check the help page for further information.")
    if mscorDirection is not None:
        if mscorDirection not in [">", "<"]:
            raise ValueError("mscorDirection:", mscorDirection,
                             " is not an allowed value. Please check the help page for further information.")
    if correlationDirection is not None:
        if correlationDirection not in [">", "<"]:
            raise ValueError("correlationDirection:", correlationDirection,
                             " is not an allowed value. Please check the help page for further information.")
    if sorting is not None:
        if sorting not in ["pValue", "mscor", "correlation"]:
            raise ValueError("Provided Ssrting parameter: ", sorting,
                             " is not an allowed value. Please check the help page for further information.")

    params = {"disease_name": disease_name, "gene_type": gene_type, "pValue": pValue,
              "pValueDirection": pValueDirection, "mscor": mscor, "mscorDirection": mscorDirection,
              "correlation": correlation, "correlationDirection": correlationDirection, "sorting": sorting,
              "descending": descending, "limit": limit, "offset": offset, "information": False}

    # Add list type parameters
    if ensg_number is not None:
        params.update({"ensg_number": ",".join(ensg_number)})
    if gene_symbol is not None:
        params.update({"gene_symbol": ",".join(gene_symbol)})

    api_url = '{0}ceRNAInteraction/findAll'.format(config.api_url_base)

    response = requests.get(api_url, headers=config.headers, params=params)

    json_dicts = json.loads(response.content.decode('utf-8'))
    data = json_normalize(json_dicts)

    if response.status_code == 200:
        return data
    else:
        if response.status_code == 404:
            raise ValueError("API response is empty. Reason: " + data["detail"].values)