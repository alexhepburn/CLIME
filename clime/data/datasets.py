'''
Generate toy data
'''
# author: Jonny Erskine
# email: jonathan.erskine@bristol.ac.uk

# author2: Matt Clifford
# email2: matt.clifford@bristol.ac.uk
import os
import sklearn.datasets
import sklearn.model_selection
import sklearn.utils
import random
import numpy as np
import clime


def get_moons(samples=200):
    '''
    sample from the half moons data distribution
    returns:
        - data: dict containing 'X', 'y'
    '''
    X, y = sklearn.datasets.make_moons(noise=0.2,
                                       random_state=clime.RANDOM_SEED,
                                       n_samples=[int(samples/2)]*2)
    X, y = sklearn.utils.shuffle(X, y, random_state=clime.RANDOM_SEED)
    return {'X': X, 'y':y}


def get_gaussian(samples=200,
                 var=1,
                 cov=[[1,0],[0,1]],
                 test=False):
    '''
    sample from two Gaussian dataset

    returns:
        - data: dict containing 'X', 'y'
    '''

    X = np.empty([0, 2])
    y = np.empty([0], dtype=np.int64)
    labels = [0, 1]
    class_means = [[0, 0], [1, 1]] # X1 and X2 cooridnates of mean
    for mean, label in zip(class_means, labels):
        # equal proportion of class samples
        class_samples = int(samples/len(labels))
        # set up current class' sampler
        gaussclass = GaussClass(mean[0],
                                         mean[1],
                                         variance=var,
                                         covariance=cov)
        # get random seed
        seed = clime.RANDOM_SEED+label
        if test == True:
            seed += 1
            seed *= 2
        # sample points
        gaussclass.gen_data(seed, class_samples)
        X = np.vstack([X, gaussclass.data])
        y = np.append(y, [label]*class_samples)
    X, y = sklearn.utils.shuffle(X, y, random_state=clime.RANDOM_SEED)
    return {'X': X, 'y':y}

class GaussClass():
    def __init__(self, x, y, variance = 1, covariance=None):
        self.mean = np.array([x, y])

        if covariance is None:
            self.cov = variance * np.eye(2)
        else:
            self.cov = covariance*variance

    def gen_data(self, randomseed, size):
        rng = np.random.default_rng(randomseed)
        self.data    = np.array(rng.multivariate_normal(self.mean, self.cov, size))
