"""
Code for the AKNN classification rule from:

An adaptive nearest neighbor rule for classification
Akshay Balsubramani, Sanjoy Dasgupta, Yoav Freund, Shay Moran
https://arxiv.org/abs/1905.12717

Author: Akshay Balsubramani
"""

import numpy as np, sklearn, umap
import sklearn.metrics
from sklearn import preprocessing



def aknn(nbrs_arr, labels, thresholds, distinct_labels=['A','B','C','D','E','F','G','H','I','J']):
    """
    Apply AKNN rule for a query point, given its list of nearest neighbors.
    
    Parameters
    ----------
    nbrs_arr: array of shape (n_neighbors)
        Indices of the `n_neighbors` nearest neighbors in the dataset.

    labels: array of shape (n_samples)
        Dataset labels.
    
    thresholds: array of shape (n_neighbors)
        Bias thresholds at different neighborhood sizes.

    Returns
    -------
    pred_label: string
        AKNN label prediction.

    first_admissible_ndx: int
        n-1, where AKNN chooses neighborhood size n.
    
    fracs_labels: array of shape (n_labels, n_neighbors)
        Fraction of each label in balls of different neighborhood sizes.
    """
    query_nbrs = labels[nbrs_arr]
    mtr = np.stack([query_nbrs == i for i in distinct_labels])
    rngarr = np.arange(len(nbrs_arr))+1
    fracs_labels = np.cumsum(mtr, axis=1)/rngarr
    biases = fracs_labels - 1.0/len(distinct_labels)
    numlabels_predicted = np.sum(biases > thresholds, axis=0)
    admissible_ndces = np.where(numlabels_predicted > 0)[0]
    first_admissible_ndx = admissible_ndces[0] if len(admissible_ndces) > 0 else len(nbrs_arr)
    pred_label = '?' if first_admissible_ndx == len(nbrs_arr) else distinct_labels[np.argmax(biases[:, first_admissible_ndx])]  # Break any ties between labels at stopping radius, by taking the most biased label
    return (pred_label, first_admissible_ndx, fracs_labels)


def predict_nn_rule(nbr_list_sorted, labels, log_complexity=1.0, distinct_labels=['A','B','C','D','E','F','G','H','I','J']):
    """
    Given matrix of ordered nearest neighbors for each point, returns AKNN's label predictions and adaptive neighborhood sizes.
    
    Parameters
    ----------
    nbr_list_sorted: array of shape (n_samples, n_neighbors)
        Indices of the `n_neighbors` nearest neighbors in the dataset, for each data point.

    labels: array of shape (n_samples)
        Dataset labels.
    
    log_complexity: float
        The confidence parameter "A" from the AKNN paper.

    Returns
    -------
    pred_labels: array of shape (n_samples)
        AKNN label predictions on dataset.

    adaptive_ks: array of shape (n_samples)
        AKNN neighborhood sizes on dataset.
    """
    pred_labels = []
    adaptive_ks = []
    thresholds = log_complexity/np.sqrt(np.arange(nbr_list_sorted.shape[1])+1)
    distinct_labels = np.unique(labels)
    for i in range(nbr_list_sorted.shape[0]):
        (pred_label, adaptive_k_ndx, _) = aknn(nbr_list_sorted[i,:], labels, thresholds)
        pred_labels.append(pred_label)
        adaptive_ks.append(adaptive_k_ndx + 1)
    return np.array(pred_labels), np.array(adaptive_ks)


def calc_nbrs_exact(raw_data, k=1000):
    """
    Calculate list of `k` exact Euclidean nearest neighbors for each point.
    
    Parameters
    ----------
    raw_data: array of shape (n_samples, n_features)
        Input dataset.

    Returns
    -------
    nbr_list_sorted: array of shape (n_samples, n_neighbors)
        Indices of the `n_neighbors` nearest neighbors in the dataset, for each data point.
    """
    a = sklearn.metrics.pairwise_distances(raw_data)
    nbr_list_sorted = np.argsort(a, axis=1)[:, 1:]
    return nbr_list_sorted[:, :k]


def knn_rule(nbr_list_sorted, labels, k=10):
    # For benchmarking: given matrix of ordered nearest neighbors for each point, returns kNN rule's label predictions.
    toret = []
    for i in range(nbr_list_sorted.shape[0]):
        uq = np.unique(labels[nbr_list_sorted[i,:k]], return_counts=True)
        toret.append(uq[0][np.argmax(uq[1])])
    return np.array(toret)