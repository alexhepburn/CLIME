# author: Matt Clifford <matt.clifford@bristol.ac.uk>

import warnings
from clime.data import costs
import numpy as np


def fidelity(expl, black_box_model, data, **kwargs):
    '''
    get fidelity accuracy between both models
    '''
    same_preds = _get_preds(expl, black_box_model, data)
    # get the accuracy
    fidelity_acc = sum(same_preds)/len(same_preds)
    return fidelity_acc

def local_fidelity(expl, black_box_model, data, query_point, **kwargs):
    '''
    get fidelity accuracy between both models but weight based on
    distance from query point
    '''
    same_preds = _get_preds(expl, black_box_model, data)
    # get weights dataset based on locality
    weights = costs.weights_based_on_distance(query_point, data['X'])
    # adjust score with weights
    fidelity_acc = sum(same_preds*weights)/ sum(weights)
    return fidelity_acc

def bal_fidelity(expl, black_box_model, data, **kwargs):
    '''
    get fidelity accuracy between both models but weight based on
    class imbalance - give higher weight to minority class (prop to instances)
    '''
    same_preds = _get_preds(expl, black_box_model, data)
    weights = _get_class_weights(data)
    # adjust score with weights
    fidelity_acc = sum(same_preds*weights)/ sum(weights)
    return fidelity_acc

def local_and_bal_fidelity(expl, black_box_model, data, query_point, **kwargs):
    '''
    combine the weights of both bal and local
    '''
    same_preds = _get_preds(expl, black_box_model, data)
    weights = costs.weights_based_on_distance(query_point, data['X'])
    weights *= _get_class_weights(data)
    # adjust score with weights
    fidelity_acc = sum(same_preds*weights)/ sum(weights)
    return fidelity_acc

def _get_preds(expl, black_box_model, data):
    # get prediction from both models
    bb_preds = black_box_model.predict(data['X'])
    expl_preds = expl.predict(data['X'])
    same_preds = (bb_preds==expl_preds).astype(np.int64)
    return same_preds

def _get_class_weights(data):
    # make sure we have class data (sampled data from LIME won't have this)
    if 'y' not in data.keys():
        warnings.warn("No class data 'y': not using class balanced weightings", Warning)
        return np.ones(data['X'].shape[0])
    # get weights dataset based on class imbalance
    weightings = costs.weight_based_on_class_imbalance(data)
    weights = data['y'].copy()
    masks = {}
    for i in range(len(weightings)):
        masks[i] = (weights==i)
    for i in range(len(weightings)):
        weights[masks[i]] = weightings[i]
    return weights


if __name__ == '__main__':
    import data
    import model
    import explainer
    # get dataset
    train_data = data.get_moons()
    train_data = data.unbalance(train_data,[1,0.5])

    # train model
    clf = model.SVM(train_data)

    # BLIMEY!
    q_point = 10
    expl = explainer.bLIMEy(clf, train_data['X'][q_point, :])

    fid = fidelity(expl, clf, train_data)
    print(fid)
    loc_fid = local_fidelity(expl, clf, train_data, train_data['X'][q_point, :])
    print(loc_fid)
    bal_fid = bal_fidelity(expl, clf, train_data)
    print(bal_fid)
