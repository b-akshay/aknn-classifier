"""
Code for the AKNN classification rule from:

An adaptive nearest neighbor rule for classification
Akshay Balsubramani, Sanjoy Dasgupta, Yoav Freund, Shay Moran
https://arxiv.org/abs/1905.12717

Author: Akshay Balsubramani
"""

import numpy as np, sklearn, umap
import sklearn.metrics
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing



def aknn_predict(
    ref_data, 
    labels, 
    log_complexity=1.0, 
    query_data=None, 
    max_k=100
):
    # itime = time.time()
    if query_data is None:
        query_data = ref_data
    nbrs = sklearn.neighbors.NearestNeighbors(n_neighbors=max_k).fit(ref_data)
    distances, indices = nbrs.kneighbors(query_data)
    distinct_labels = np.unique(labels)
    rngarr = np.arange(indices.shape[1])+1
    query_nbrs = labels[indices]
    fracs_labels = [np.cumsum(query_nbrs == i, axis=1)/rngarr for i in distinct_labels]
    # print("Clustering computed. Time: {}".format(time.time() - itime))
    thresholds = log_complexity/np.sqrt(np.arange(indices.shape[1]) + 1)
    numlabels_predicted = np.add.reduce([f > (thresholds + 1.0/len(distinct_labels)) for f in fracs_labels])
    adaptive_k = np.argmax(numlabels_predicted > 0, axis=1)
    
    pred_labels = np.zeros(fracs_labels[0].shape[0]).astype(str)
    for i in range(fracs_labels[0].shape[0]):
        if adaptive_k[i] == 0:
            pred_labels[i] = '?'
        else:
            lst = [f[i, adaptive_k[i]] for f in fracs_labels]
            pred_labels[i] = distinct_labels[np.argmax(lst)]
    # print("Clustering computed. Time: {}".format(time.time() - itime))
    return np.array(pred_labels), np.array(adaptive_k)


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


def predict_nn_rule(nbr_list_sorted, labels, log_complexity=1.0):
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


def calc_nbrs_exact(raw_data, k=1000, brute_force=False):
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
    if brute_force:
        a = sklearn.metrics.pairwise_distances(raw_data)
        nbr_list_sorted = np.argsort(a, axis=1)[:, 1:]
        return nbr_list_sorted[:, :k]
    else:
        distances, indices = NearestNeighbors(n_neighbors=k+1).fit(raw_data).kneighbors(raw_data)
        return indices[:, 1:]


def knn_rule(nbr_list_sorted, labels, k=10):
    # For benchmarking: given matrix of ordered nearest neighbors for each point, returns kNN rule's label predictions.
    toret = []
    for i in range(nbr_list_sorted.shape[0]):
        uq = np.unique(labels[nbr_list_sorted[i,:k]], return_counts=True)
        toret.append(uq[0][np.argmax(uq[1])])
    return np.array(toret)