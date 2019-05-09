"""
Code for adaptive k-NN classifier.
"""
import numpy as np, os, time, scipy as sp, sklearn
from sklearn import preprocessing


# Apply aknn rule, returning (predicted label, index of k)
def aknn(nbrs_arr, labels, thresholds, mode='ovr'):
    query_nbrs = labels[nbrs_arr]
    mtr = np.stack([query_nbrs == i for i in range(10)])
    rngarr = np.arange(len(nbrs_arr))+1
    fracs_labels = np.cumsum(mtr, axis=1)/rngarr
    if mode == 'ucb':
        best_labels = np.argmax(fracs_labels, axis=0)
        biases = np.max(fracs_labels, axis=0) - fracs_labels
        biases[biases == 0] = 1
        admissible_ndces = np.where(np.min(biases, axis=0) > thresholds)[0]
        first_admissible_ndx = admissible_ndces[0] if len(admissible_ndces) > 0 else (len(nbrs_arr) - 1)
        return (labels[first_admissible_ndx], first_admissible_ndx, fracs_labels)
    elif mode == 'ovr':
        biases = fracs_labels - 0.1
        numlabels = np.sum(biases > thresholds, axis=0)
        admissible_ndces = np.where(numlabels > 0)[0]
        first_admissible_ndx = admissible_ndces[0] if len(admissible_ndces) > 0 else (len(nbrs_arr) - 1)
        return (np.argmax(biases[:, first_admissible_ndx]), first_admissible_ndx, fracs_labels)      # Breaking any ties between labels at stopping radius by taking the most biased label

"""
Given matrix with ordered nearest neighbors computed for each point, returns AKNN's label predictions and k-values for all points.
"""
def predict_nn_rule(nbr_list_sorted, labels, log_complexity=1.0, mode='ovr'):
    itime = time.time()
    pred_labels = []
    adaptive_ks = []
    thresholds = log_complexity/np.sqrt(np.arange(nbr_list_sorted.shape[1])+1)
    for i in range(nbr_list_sorted.shape[0]):
        (pred_label, adaptive_k, _) = aknn(nbr_list_sorted[i,:], labels, thresholds, mode=mode)
        pred_labels.append(pred_label)
        adaptive_ks.append(adaptive_k)
    return pred_labels, adaptive_ks     # Returns a pair of the points' respective (labels, adaptive k-values)