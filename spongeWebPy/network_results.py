import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

import spongeWebPy.config as config


def get_network_results(
    disease_name="Pan-cancer", level="gene", sponge_db_version=config.LATEST
):
    """
    Scores and coordinates within a 2D MDS map between Cancer Type network and other Cancer Type or Subtype networks.
    :param disease_name: The name of the Cancer Type of interest as string. If default is set, only cancer types.
    :param level: Either "gene" or "transcript", which was introduced in SPONGEdb version 2. The default is "gene".
    :param sponge_db_version: Version of SPONGEdb to use. Default is set in config.
    :return: dict containing pairwise scores and 2D coordinates for all Cancer Types and, if available, the Types Subtypes.
    """
    params = {
        "disease_name": disease_name,
        "level": level,
        "sponge_db_version": sponge_db_version,
    }
    api_url = "{0}networkResults".format(config.api_url_base)
    response = requests.get(api_url, headers=config.headers, params=params)
    print(response.url)
    json_dicts = json.loads(response.content.decode("utf-8"))

    type_scores = pd.DataFrame(
        json_dicts["type"]["scores"]["values"],
        columns=json_dicts["type"]["scores"]["labels"],
    )
    type_distances = pd.DataFrame(
        {
            "x": json_dicts["type"]["euclidean_distances"]["x"],
            "y": json_dicts["type"]["euclidean_distances"]["y"],
            "labels": json_dicts["type"]["euclidean_distances"]["labels"],
        }
    )
    type_res = {"scores": type_scores, "distances": type_distances}
    if len(json_dicts["subtype"]) != 0:
        subtype_scores = pd.DataFrame(
            json_dicts["subtype"]["scores"]["values"],
            columns=json_dicts["subtype"]["scores"]["labels"],
        )
        subtype_distances = pd.DataFrame(
            {
                "x": json_dicts["subtype"]["euclidean_distances"]["x"],
                "y": json_dicts["subtype"]["euclidean_distances"]["y"],
                "labels": json_dicts["subtype"]["euclidean_distances"]["labels"],
            }
        )
        subtype = {"scores": subtype_scores, "distances": subtype_distances}
    else:
        subtype = {}
    return {"type": type_res, "subtype": subtype}


def plot_heatmap(df: pd.DataFrame, title: str = "Heatmap", tri: bool = True):
    """
    Shows a Heat map of hubness scores
    :param df: A pd.DataFrame with hubness values returned from the get_network_results function.
    :param title: Allows the user to specify a plot title.
    :param tri: Toggles triangle shape for enhanced visibility of differences. Default is True.
    :return:
    """
    df = df.iloc[::-1]
    x_labels = df.columns
    y_labels = df.columns[::-1]
    # fill bottom right triangle with None
    if tri:
        x_labels = x_labels[:-1]
        y_labels = y_labels[:-1]
        scores = df.to_numpy()
        i = np.triu_indices(scores.shape[0])
        a, b = i
        i = b, scores.shape[0] - 1 - a
        scores[i] = None
        # delete last column and row
        del df[df.columns[-1]]
        df = df[:-1]
    # color map
    colormap = cm.get_cmap("Purples", 512)
    new_colormap = LinearSegmentedColormap.from_list("custom", ["#D099F2", "#540A67"])
    # plot
    fig, ax = plt.subplots()
    plt.imshow(df, cmap=new_colormap)
    # labels
    ax.set_xticks(np.arange(len(x_labels)), labels=x_labels)
    ax.set_yticks(np.arange(len(y_labels)), labels=y_labels)
    # rotate and align labels
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    plt.setp(ax.get_xticklabels(), rotation=-45, ha="right", rotation_mode="anchor")
    # set title
    plt.title(title)
    # plt.tight_layout()
    plt.colorbar()
    plt.show()


def plot_MDS(df: pd.DataFrame, title: str = "MDS plot"):
    """
    Shows an MDS plot of euclidean distances
    :param df: A pd.DataFrame with cmdscaled values returned from the get_network_results function.
    :param title: Allows the user to specify a plot title.
    :return:
    """
    plt.scatter(df["x"], df["y"])
    # labels
    for i, txt in enumerate(df["labels"]):
        plt.annotate(txt, (df["x"][i], df["y"][i] + 0.5), ha="center", fontsize=7)
    # set title
    plt.title(title)
    plt.show()


if __name__ == "__main__":
    res = get_network_results("Breast invasive carcinoma", "gene")
    plot_heatmap(res["type"]["scores"])
    plot_MDS(res["type"]["distances"])
    plot_heatmap(res["subtype"]["scores"])
    plot_MDS(res["subtype"]["distances"])
