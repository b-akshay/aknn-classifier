"""
Code for adaptive k-NN classifier. Author: Akshay Balsubramani
"""
import numpy as np, os, time, scipy as sp, sklearn
from sklearn import preprocessing


"""
Apply aknn rule, given list of neighbors for a given point.
Returns (predicted label, index of k)
"""
def aknn(nbrs_arr, labels, thresholds, mode='ovr', distinct_labels=['A','B','C','D','E','F','G','H','I','J']):
    query_nbrs = labels[nbrs_arr]
    mtr = np.stack([query_nbrs == i for i in distinct_labels])
    rngarr = np.arange(len(nbrs_arr))+1
    fracs_labels = np.cumsum(mtr, axis=1)/rngarr
    if mode == 'ucb':
        best_labels = np.argmax(fracs_labels, axis=0)
        biases = np.max(fracs_labels, axis=0) - fracs_labels
        biases[biases == 0] = 1
        admissible_ndces = np.where(np.min(biases, axis=0) > thresholds)[0]
        first_admissible_ndx = admissible_ndces[0] if len(admissible_ndces) > 0 else len(nbrs_arr)
        pred_label = '?' if first_admissible_ndx == len(nbrs_arr) else labels[first_admissible_ndx]
    elif mode == 'ovr':
        biases = fracs_labels - 1.0/len(distinct_labels)
        numlabels = np.sum(biases > thresholds, axis=0)
        admissible_ndces = np.where(numlabels > 0)[0]
        first_admissible_ndx = admissible_ndces[0] if len(admissible_ndces) > 0 else len(nbrs_arr)
        pred_label = '?' if first_admissible_ndx == len(nbrs_arr) else distinct_labels[np.argmax(biases[:, first_admissible_ndx])]
    return (pred_label, first_admissible_ndx, fracs_labels)      # Breaking any ties between labels at stopping radius by taking the most biased label


"""
Given matrix with ordered nearest neighbors computed for each point, returns AKNN's label predictions and k-values for all points.
"""
def predict_nn_rule(nbr_list_sorted, labels, log_complexity=1.0, mode='ovr', distinct_labels=['A','B','C','D','E','F','G','H','I','J']):
    itime = time.time()
    pred_labels = []
    adaptive_ks = []
    thresholds = log_complexity/np.sqrt(np.arange(nbr_list_sorted.shape[1])+1)
    for i in range(nbr_list_sorted.shape[0]):
        (pred_label, adaptive_k_ndx, _) = aknn(nbr_list_sorted[i,:], labels, thresholds, mode=mode, distinct_labels=distinct_labels)
        pred_labels.append(pred_label)
        adaptive_ks.append(adaptive_k_ndx + 1)
    return np.array(pred_labels), np.array(adaptive_ks)     # Returns a pair of the points' respective (labels, adaptive k-values)


"""
For benchmarking: 
Given matrix with ordered nearest neighbors computed for each point, returns kNN rule's label predictions.
"""
def knn_rule(nbr_list_sorted, labels, k=10):
    toret = []
    for i in range(nbr_list_sorted.shape[0]):
        uq = np.unique(labels[nbr_list_sorted[i,:k]], return_counts=True)
        toret.append(uq[0][np.argmax(uq[1])])
    return np.array(toret)


"""
Compute approximate AKNN rule from small-NN graph using: 
(1) Diffusion maps to compute pairwise distances.
(2) Construction of neighbor list
(3) Standard AKNN as above
"""
def aknn_approx(nbr_list_sorted, labels, distinct_labels=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']):
    pass