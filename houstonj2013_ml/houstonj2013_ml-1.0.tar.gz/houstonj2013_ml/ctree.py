'''
Contact: jingbo.liu2013@gmail.com
Converting the tree module from python to cython in order to boost efficiency
'''
from collections import Counter
import math
import numpy as np
from time import time as now
from .cyfun import search_maxgain_mask

class TreeNode(object):
    '''
    A node class for a decision tree.
    '''
    def __init__(self):
        self.column = None  # (int)    index of feature to split on
        self.value = None  # value of the feature to split on
        self.categorical = True  # (bool) whether or not node is split on
                                 #  categorial feature
        self.name = None    # (string) name of feature (or name of class in the
                            #          case of a list)
        self.left = None    # (TreeNode) left child
        self.right = None   # (TreeNode) right child
        self.leaf = False   # (bool)   true if node is a leaf, false otherwise
        self.classes = Counter()  # (Counter) only necessary for leaf node:
                                  #           key is class name and value is
                                  #           count of the count of data points
                                  #           that terminate at this leaf

    def predict_one(self, x):
        '''
        INPUT:
            - x: 1d numpy array (single data point)
        OUTPUT:
            - y: predicted label
        Return the predicted label for a single data point.
        '''
        if self.leaf:
            return self.name

        col_value = x[self.column]
        if self.categorical:
            if col_value == self.value:
                return self.left.predict_one(x)
            else:
                return self.right.predict_one(x)
        else:
            if col_value < self.value:
                return self.left.predict_one(x)
            else:
                return self.right.predict_one(x)

    # This is for visualizing your tree. You don't need to look into this code.
    def as_string(self, level=0, prefix=""):
        '''
        INPUT:
            - level: int (amount to indent)
        OUTPUT:
            - prefix: str (to start the line with)
        Return a string representation of the tree rooted at this node.
        '''
        result = ""
        if prefix:
            indent = "  |   " * (level - 1) + "  |-> "
            result += indent + prefix + "\n"
        indent = "  |   " * level
        result += indent + "  " + str(self.name) + "\n"
        if not self.leaf:
            if self.categorical:
                left_key = str(self.value)
                right_key = "no " + str(self.value)
            else:
                left_key = "< " + str(self.value)
                right_key = ">= " + str(self.value)
            result += self.left.as_string(level + 1, left_key + ":")
            result += self.right.as_string(level + 1, right_key + ":")
        return result

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return self.as_string().strip()


class DecisionTreeClassifier(object):
    '''
    A decision tree class.
    Input to Decision tree should be either string for categorical feature or float for continuous features
    This module do not support boolean
    '''

    def __init__(self, impurity_criterion='gini', max_features=None, feature_names=None, feature_threshold=None,
                 max_depth=float('inf'), continous_variable_splits="unique", impurity_dict={}):
        '''
        Initialize an empty DecisionTree.
        '''

        self.root = None  # root Nodess
        self.feature_names = feature_names  # string names of features (for interpreting
                                   # the tree)
        self.categorical = None  # Boolean array of whether variable is
                                 # categorical (or continuous)
        self.max_features = max_features
        self.max_depth = max_depth
        self.feature_threshold_out_ = {}
        self.feature_threshold = feature_threshold
        self.impurity_criterion = self._entropy \
                                  if impurity_criterion == 'entropy' \
                                  else self._gini
        self.impurity_dict = impurity_dict
        self.continous_variable_splits = continous_variable_splits  ## Percentile of unique values
        self.feature_importance_ = None
        self.feature_selected_ = None
        self.time1 = 0  ## Time for choose split
        # self.n1 = 0     ## Number of calls choose split
        # self.time2 = 0  ## Time for make split
        # self.n2 = 0     ## Number of calls make split
        # self.time3 = 0  ## Time for information gain
        # self.n3 = 0     ## Number of calls information gain
        # self.time3_overhead = 0
        # self.time3_overhead2 = 0
        # self.time3_overhead3 = 0
        # self.time3_overhead4 = 0
        # self.time4 = 0
        # self.time5 = 0
        # self.time6 = 0

    def fit(self, X, y):
        '''
        INPUT:
            - X: 2d numpy array
            - y: 1d numpy array
            - feature_names: numpy array of strings
        OUTPUT: None
        Build the decision tree.
        X is a 2 dimensional array with each column being a feature and each
        row a data point.
        y is a 1 dimensional array with each value being the corresponding
        label.
        feature_names is an optional list containing the names of each of the
        features.
        '''
        ## Convert to numpy array for faster implementation
        ## This improves efficiency significantly
        X = np.array(X)
        y = np.array(y)
        sort_index =  np.argsort(y)
        X = X[sort_index, :]
        y = y[sort_index]

        self.feature_importance_ = np.zeros(X.shape[1])
        self.feature_selected_ = np.zeros(X.shape[1])
        ## If max_features is not specified, use all features
        if self.max_features is None:
            self.max_features = X.shape[1]

        if self.feature_names is None or len(self.feature_names) != X.shape[1]:
            self.feature_names = np.arange(X.shape[1])
            #print("warning: feature_names has different dimension with X")

        # Create True/False array of whether the variable is categorical
        is_categorical = lambda x: isinstance(x, str)
        self.categorical = np.vectorize(is_categorical)(X[0])
        # start = now()
        self.root = self._build_tree(X, y, depth=0)
        self.feature_importance_ = self.feature_importance_ / np.sum(self.feature_importance_) ## Normalized feature
        # end = now()
        # print("build tree takes", end - start)
        return self.impurity_dict

    def _build_tree(self, X, y, depth):
        '''
        INPUT:
            - X: 2d numpy array
            - y: 1d numpy array
        OUTPUT:
            - TreeNode
        Recursively build the decision tree. Return the root node.
        '''

        node = TreeNode()
        # start = now()
        index, value, splits = self._choose_split_index(X, y)
        # end = now()
        # self.time1 += end - start
        if index is None or len(np.unique(y)) == 1 or depth >= self.max_depth or len(y) == 1:
            node.leaf = True
            node.classes = Counter(y)
            node.name = node.classes.most_common(1)[0][0]
        else:
            X1, y1, X2, y2 = splits
            node.column = index
            node.name = self.feature_names[index]
            node.value = value
            node.categorical = self.categorical[index]
            node.left = self._build_tree(X1, y1, depth + 1)
            node.right = self._build_tree(X2, y2, depth + 1)
        return node

    def _choose_split_index(self, X, y):
        '''
        INPUT:
            - X: 2d numpy array
            - y: 1d numpy array
        OUTPUT:
            - index: int (index of feature)
            - value: int/float/bool/str (value of feature)
            - splits: (2d array, 1d array, 2d array, 1d array)
        Determine which feature and value to split on. Return the index and
        value of the optimal split along with the split of the dataset.
        Return None, None, None if there is no split which improves information
        gain.
        Call the method like this:
        >>> index, value, splits = self._choose_split_index(X, y)
        >>> X1, y1, X2, y2 = splits
        '''

        max_gain, split_index, split_value, splits = 0, None, None, None

        ## Choose the features to use
        if X.shape[1] == self.max_features:
            # print("No resamples")
            random_features = range(self.max_features)
        else:
            # print("Resamples")
            random_features = np.random.choice(range(X.shape[1]),self.max_features)

        ## Make splits
        for i in random_features:
            if self.feature_threshold is None:
                ## No user specified threshold provided, use threshold from data
                if self.categorical[i]:
                    values = np.unique(X[:, i])
                    if i not in self.feature_threshold_out_:
                        self.feature_threshold_out_[i] = values
                else:
                    if self.continous_variable_splits.lower() == "percentile".lower():
                        percentiles_ = np.arange(10, 100, 10)
                        values = np.percentile(X[:,i], percentiles_)
                    else:
                        values = np.unique(X[:,i])
                    if i not in self.feature_threshold_out_:
                        self.feature_threshold_out_[i] = list(values)
            else:
                ## Use user specified thresholds
                values = self.feature_threshold[i]
            if len(values) < 2:
                continue
            # max_gain, split_index, split_value, splits = self._search_max_gain(X, y, i, values, max_gain, split_index,
            #                                                                    split_value, splits)
            max_gain, split_index, split_value, splits = search_maxgain_mask(X, y, values, i, max_gain,
                                                                             split_index, split_value, splits,
                                                                             categorical=self.categorical[i],
                                                                             crit=self.impurity_criterion)
        if split_index is not None:
            # print(split_index, max_gain)
            self.feature_importance_[split_index] += max_gain * len(y)
            self.feature_selected_[split_index] += 1

        return split_index, split_value, splits

    def _search_max_gain(self, X, y, i, values, max_gain, split_index, split_value, splits):
        '''
        Search for max gain
        :param X:
        :param y:
        :param i:
        :param values:
        :param max_gain:
        :param split_index:
        :param split_value:
        :param splits:
        :return:
        '''
        start = now()
        for val in values:
            X1, y1, X2, y2 = self._make_split(X, y, i, val)
            # start_1 = now()
            gain = self._information_gain(y, y1, y2)
            # end_1 = now()
            # self.time3_overhead += end_1 - start_1
            if gain > max_gain and len(y1) > 0 and len(y2) > 0:
                max_gain = gain
                split_index, split_value = i, val
                splits = X1, y1, X2, y2
        end = now()
        self.time1 += end - start
        return max_gain, split_index, split_value, splits

    def _make_split(self, X, y, split_index, split_value):
        '''
        INPUT:
            - X: 2d numpy array
            - y: 1d numpy array
            - split_index: int (index of feature)
            - split_value: int/float/bool/str (value of feature)
        OUTPUT:
            - X1: 2d numpy array (feature matrix for subset 1)
            - y1: 1d numpy array (labels for subset 1)
            - X2: 2d numpy array (feature matrix for subset 2)
            - y2: 1d numpy array (labels for subset 2)
        Return the two subsets of the dataset achieved by the given feature and
        value to split on.
        Call the method like this:
        >>> X1, y1, X2, y2 = self._make_split(X, y, split_index, split_value)
        X1, y1 is a subset of the data.
        X2, y2 is the other subset of the data.
        '''
        # self.n2 += 1
        # start = now()
        split_col = X[:, split_index]
        if self.categorical[split_index]:
            mask = split_col == split_value
        else:
            mask = split_col < split_value
        result = X[mask, :], y[mask], X[~mask, :], y[~mask]
        # end = now()
        # self.time2 += end - start
        return result

    def _entropy(self, y):
        '''
        INPUT:
            - y: 1d numpy array
        OUTPUT:
            - float
        Return the entropy of the array y.
        '''
        n_y = float(len(y))
        cbincount = np.bincount(y)
        total = 0
        for val in cbincount:
            prob = val / n_y
            total += prob * math.log(prob)
        return -total

    def _gini(self, y):
        n_y = float(len(y))
        cbincount = np.bincount(y)
        total = 0
        for val in cbincount:
            total += (val/n_y) ** 2
        return 1 - total

    def _information_gain(self, y, y1, y2):
        '''
        INPUT:
            - y: 1d numpy array
            - y1: 1d numpy array (labels for subset 1)
            - y2: 1d numpy array (labels for subset 2)
        OUTPUT:
            - float
        Return the information gain of making the given split.
        Use self.impurity_criterion(y) rather than calling _entropy or _gini
        directly.
        '''
        total = self.impurity_criterion(y)
        for y_split in (y1, y2):
            ent = self.impurity_criterion(y_split)
            total -= len(y_split) * ent / float(len(y))
        return total

    def predict(self, X):
        '''
        INPUT:
            - X: 2d numpy array
        OUTPUT:
            - y: 1d numpy array
        Return an array of predictions for the feature matrix X.
        '''

        return np.array([self.root.predict_one(row) for row in X])

    def score(self, X, y):
        '''
        Return the accuracy of the Random Forest for the given test data and
        labels.
        '''
        y_pred = self.predict(X)
        n_right = np.sum(y == y_pred)
        n_total = len(y)
        return float(n_right)/n_total

    def __str__(self):
        '''
        Return string representation of the Decision Tree.
        '''
        return str(self.root)

    def __eq__(self, other):
        return self.root == other.root



