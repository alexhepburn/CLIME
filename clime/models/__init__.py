from .base import base_model
from .linear import logistic, logistic_balanced_training
from .random_forest import random_forest, random_forest_balanced_training
# from .QDA import QDA
from .bayes_optimal import Guassian_class_conditional
from .svm import SVM, SVM_balanced_training
from .balance import adjust_boundary, adjust_proba, base_balance

AVAILABLE_MODELS = {
    'Random Forest': random_forest,
    'Random Forest balanced training': random_forest_balanced_training,
    'Logistic': logistic,
    'Logistic balanced training': logistic_balanced_training,
    'SVM': SVM,
    'SVM balanced training': SVM_balanced_training,
    # 'QDA': QDA,
    'Bayes Optimal': Guassian_class_conditional,
}

AVAILABLE_MODEL_BALANCING = {
    'none': base_balance,
    'boundary adjust': adjust_boundary,
    'probability adjust': adjust_proba,
}
