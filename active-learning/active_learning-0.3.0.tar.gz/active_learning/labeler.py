import numpy as np
import pandas as pd
from sklearn import metrics

class Labeler():
    """
    args:
        rule_function: function to label given data
    """

    def __init__(self, rule_function):
        self.rule_function = rule_function

    def predict(self, X):
        """
        args:
            X: dataset without labels

        returns:
            preds: predictions for X
        """

        if isinstance(X, pd.DataFrame):
            X=X.values
        preds = self.rule_function(X)
        return preds

    def score(self, X, y):
        """
        args:
            X: features
            y: ground truths

        returns:
            prec: average precision
            auc: auc score
            prec: precision at .8 recall
        """
        pred = self.predict(X)
        # would be probabilities if we had
        precision, recall, thresholds = metrics.precision_recall_curve(y, pred)
        auc = metrics.auc(recall,precision)
        idx = (np.abs(recall - .8)).argmin()
        prec = precision[idx]

        return auc, prec

def stats(X, y, clf, sample_weights = None):
    """
    args:
        X: features
        y: ground truths
        sample_weights: sample weights
        clf: Ski-kit classifier

    returns:
        auc: auc score
        prec: precision at .8 recall
    """

    # Get classifier data
    pred = clf.predict(X)
    probs = clf.decision_function(X)

    # Get scores
    if sample_weights is None:
        sample_weights = np.ones(len(y))
    precision, recall, thresholds = metrics.precision_recall_curve(y, probs, sample_weight = sample_weights)
    auc = metrics.auc(recall,precision)
    idx = (np.abs(recall - .8)).argmin()
    prec = precision[idx]
    return auc, prec