import pandas as pd
import numpy as np

def correlation(dataset, threshold, correlated_mtx=None, absoluted=True):
    # Creates a dictionary with feature names and a counter initialized at zero
    counter_of_corrs = {f: 0 for f in dataset.columns}
    col_corr = set() # Set of all the names of deleted columns
    
    if correlated_mtx is None:
        corr_matrix = dataset.corr(method='spearman')
    else:
        corr_matrix = correlated_mtx
    if absoluted:
        corr_matrix = abs(corr_matrix)
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if (corr_matrix.iloc[i, j] >= threshold):
                colname_i = corr_matrix.columns[i] # getting the name of column i
                colname_j = corr_matrix.columns[j] # getting the name of column j
                counter_of_corrs[colname_i] += 1
                counter_of_corrs[colname_j] += 1
    # Trasnform the result to a series
    counter_of_corrs = pd.Series(counter_of_corrs)
    return(counter_of_corrs)

def drop_features(dataset, thr, min_thr, step, list_of_droped_features, 
                  verbose = False, correlated_mtx=None, **kwargs):
    counter_of_corrs = correlation(dataset, thr, **kwargs)
    max_n_correlations = counter_of_corrs.max()
    if max_n_correlations > 0:
        # Get the features with the max value
        features = counter_of_corrs[counter_of_corrs == max_n_correlations]
        features_names = [i for i in features.index]
        if verbose: print(features_names)
        # Drop one feature ramdomly
        feature_to_drop = np.random.choice(features_names)
        list_of_droped_features.append(feature_to_drop)
        if verbose: print('Droped conf:', feature_to_drop, '-> rho =', round(thr, 3))
        new_dataset = dataset.drop([feature_to_drop], axis = 1)
        # Recursively
        drop_features(new_dataset, thr, min_thr, step, list_of_droped_features, verbose, correlated_mtx)
    elif thr >= min_thr:
        #print(thr, min_thr)
        drop_features(dataset, thr - step, min_thr, step, list_of_droped_features, verbose, correlated_mtx)

def features_to_drop(dataset, min_thr, max_thr, step, correlated_mtx=None, **kwargs):
    dataset = dataset.copy()
    if correlated_mtx is not None:
        correlated_mtx = correlated_mtx.copy()
    list_of_droped_features = []
    # User recursion to find
    drop_features(dataset, max_thr, min_thr, step, list_of_droped_features, correlated_mtx=correlated_mtx, **kwargs)
    return(list_of_droped_features)