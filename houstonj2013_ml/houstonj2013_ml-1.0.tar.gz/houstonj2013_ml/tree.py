'''
Contact: jingbo.liu2013@gmail.com
This code includes the classical decision tree and random forest ideas and include a few more original ideas
1. Use percentiles instead of every value in node split, when evaluating continuous variables
2. Use user defined threshold values in node split, as a way to regularize overfiting.
3. Handle missing value in a similar way as C4.5.
https://www.quora.com/In-simple-language-how-does-C4-5-deal-with-missing-values
Implementation of handle the missing values:
1. In feature selection, missing values for that feature are ignored in calculating the information gain.
 Info Gain = P * (OldEntropy - NewEntropy)
2. Randomly spliting to children nodes for the instances with missing value, if the feature is chosen
3. When predicting and the selected feature has value missing, pursue all the possibility at that node
and aggregate the results
References: http://www.saedsayad.com/decision_tree_reg.htm
https://medium.com/@srnghn/the-mathematics-of-decision-trees-random-forest-and-feature-importance-in-
scikit-learn-and-spark-f2861df67e3
'''
from collections import Counter
from graphviz import Digraph
import math
import numpy as np
# from time import time as now

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


def test_square(x):
    return x ** 2


def tree_depth(tree_node):
    depth_ = 0
    node_queue_ = [tree_node]
    while node_queue_:
        new_queue_ = []
        depth_ += 1
        for node in node_queue_:
            if node.left is not None:
                new_queue_.append(node.left)
            if node.right is not None:
                new_queue_.append(node.right)
        node_queue_ = new_queue_
    return depth_


def tree_balance(tree_root):
    '''
    Given the root of a tree, return the depth of left and right child
    :param tree_root:
    :return:
    '''
    return tree_depth(tree_root.left) + 1, tree_depth(tree_root.right) + 1


def graphviz_tree(tree, render=False, format="pdf", X=None):
    '''
    :param : A  shell version of decision tree
    :return: dot graphviz
    '''
    root = tree.root
    if tree.feature_names is not None:
        features = tree.feature_names
        if type(tree.feature_names[0]) == np.int32:
            features = None
    else:
        features = None

    def node_to_str(node, node_id, level):
        if node.leaf == False:
            return "X[%s] < %s"%(str(node.column), str(node.value)) + "\nDepth " \
                   + str(level) + " nodeid "+ str(node_id)
        else:
            return "Leaf node\n Predicted class is %s"%(str(node.name)) + "\nDepth " + str(level) + \
                   " nodeid " + str(node_id)

    def node_to_label(node, level, features):
        if features is None:
            if node.leaf == False:
                if type(node.value) == str:
                    node_value = node.value
                    label = "X[%s] = %s"%(str(node.column), node_value) + "\nDepth " + str(level)
                else:
                    node_value = "%0.2f" % (node.value)
                    label = "X[%s] < %s" % (str(node.column), node_value) + "\nDepth " + str(level)
                return label
            else:
                return "Leaf node\n Predicted class is %s"%(str(node.name))
        else:
            if node.leaf == False:
                if type(node.value) == str:
                    node_value = node.value
                    label = "%s = %s"%(features[node.column], node_value) + "\nDepth " + str(level)
                else:
                    node_value = "%0.2f" % (node.value)
                    label = "%s < %s"%(features[node.column], node_value) + "\nDepth " + str(level)
                return label
            else:
                return "Leaf node\n Predicted class is %s"%(str(node.name))

    dot = Digraph(comment='Decision Tree', format=format, node_attr={'fontsize':'32'})
    dot.attr(size="500,500")
    # dot.graph_attr.update(size="10,10!")
    dot.attr(rankdir='TD')
    dot.attr('node', shape='box', style="rounded")
    node_id = 0
    p_level = 0
    node_name = node_to_str(root, node_id, p_level)
    node_label = node_to_label(root, p_level, features)
    if X is not None:
        dot.node(name=node_name, label=node_label, color="blue")
    else:
        dot.node(name=node_name, label=node_label)
    q = [(root, p_level, node_name, True)]
    while q:
        new_q = []
        for item in q:
            p_node, p_level, p_node_name, decision_path = item
            if p_node.leaf:
                # print(node_id, node.leaf)
                pass
            else:
                ## Highlight the tree path
                go_left, go_right = False, False
                if X is not None:
                    Xc_ = X[p_node.column]
                    if type(Xc_) == str:
                        if Xc_ == p_node.value:
                            go_left = True
                        else:
                            go_right = True
                    else:
                        if Xc_ < p_node.value:
                            go_left = True
                        else:
                            go_right = True
                go_left = go_left & decision_path
                go_right = go_right & decision_path
                #################################
                new_level = p_level + 1
                if p_node.left is not None:
                    node_id += 1
                    next_name = node_to_str(p_node.left, node_id, new_level)
                    next_label = node_to_label(p_node.left, new_level, features)
                    dot.edge(p_node_name, next_name)
                    if go_left:
                        dot.node(name=next_name, label=next_label, color="blue")
                        new_q.append((p_node.left, new_level, next_name, True))
                    else:
                        dot.node(name=next_name, label=next_label)
                        new_q.append((p_node.left, new_level, next_name, False))

                if p_node.right is not None:
                    node_id += 1
                    next_name = node_to_str(p_node.right, node_id, new_level)
                    next_label = node_to_label(p_node.right, new_level, features)
                    dot.edge(p_node_name, next_name)
                    if go_right:
                        dot.node(name=next_name, label=next_label, color="blue")
                        new_q.append((p_node.right, new_level, next_name, True))
                    else:
                        dot.node(name=next_name, label=next_label)
                        new_q.append((p_node.right, new_level, next_name, False))

        q = new_q
    if render:
        return dot.render(render, view=False)
    else:
        return dot


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
        # self.time1 = 0  ## Time for choose split
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
        self.feature_importance_ = self.feature_importance_  / np.sum(self.feature_importance_) ## Normalized feature
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

        split_index, split_value, splits = None, None, None
        max_gain = 0
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
            max_gain, split_index, split_value, splits = self._search_max_gain(X, y, i, values, max_gain, split_index,
                                                                               split_value, splits)
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
        c = Counter(y)
        total = 0
        for key, val in c.items():
            prob = val / n_y
            total += prob * math.log(prob)
        return -total

    def _gini(self, y):
        # start = now()
        n_y = float(len(y))
        c = Counter(y)
        total = 0
        for key, val in c.items():
            total += (val/n_y) ** 2
        # end = now()
        # self.time5 += end - start
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
        # total = self.impurity_criterion(y)
        # for y_split in (y1, y2):
        #     ent = self.impurity_criterion(y_split)
        #     total -= len(y_split) * ent / float(len(y))
        # return total
        # start = now()
        key = tuple(y)
        key1 = tuple(y1)
        key2 = tuple(y2)
        # end = now()
        # self.time3 += end - start

        # start2 = now()
        if key in self.impurity_dict:
            bf_split_ = self.impurity_dict[key]
        else:
            bf_split_ = self.impurity_criterion(y)
            self.impurity_dict[key] = bf_split_
        if key1 in self.impurity_dict:
            af_split1_ = self.impurity_dict[key1]
        else:
            af_split1_ = self.impurity_criterion(y1)
            self.impurity_dict[key1] = af_split1_
        if key2 in self.impurity_dict:
            af_split2_ = self.impurity_dict[key2]
        else:
            af_split2_ = self.impurity_criterion(y2)
            self.impurity_dict[key2] = af_split2_
        result = bf_split_ - len(y1) /float(len(y)) * af_split1_ - len(y2)/float(len(y)) * af_split2_
        # end2 = now()
        # self.time4 += end2 - start2
        return result

    # def _information_gain(self, y, y1, y2):
    #     '''
    #     INPUT:
    #         - y: 1d numpy array
    #         - y1: 1d numpy array (labels for subset 1)
    #         - y2: 1d numpy array (labels for subset 2)
    #     OUTPUT:
    #         - float
    #     Return the information gain of making the given split.
    #     Use self.impurity_criterion(y) rather than calling _entropy or _gini
    #     directly.
    #     '''
    #     # total = self.impurity_criterion(y)
    #     # for y_split in (y1, y2):
    #     #     ent = self.impurity_criterion(y_split)
    #     #     total -= len(y_split) * ent / float(len(y))
    #     # return total
    #     start = now()
    #     bf_split_ = self.impurity_criterion(y)
    #     af_split1_ = self.impurity_criterion(y1)
    #     af_split2_ = self.impurity_criterion(y2)
    #     result = bf_split_ - len(y1) /float(len(y)) * af_split1_ - len(y2)/float(len(y)) * af_split2_
    #     end = now()
    #     self.time4 += end - start
    #     return result

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

class RandomForestClassifier(object):
    '''A Random Forest class'''

    def __init__(self, n_estimators, max_features=None, max_depth=float('inf'),
                 continous_variable_splits="Percentile", feature_names=None, feature_threshold=None):
        '''
           num_trees:  number of trees to create in the forest:
        max_features:  the number of features to consider when choosing the
                           best split for each node of the decision trees
        '''
        self.num_trees = n_estimators
        self.max_features = max_features
        self.feature_names = feature_names
        self.feature_threshold = feature_threshold
        self.max_depth = max_depth
        self.continous_variable_splits = continous_variable_splits
        self.forest = None
        self.feature_importance_ = None
        self.feature_selected_ = None
        self.predict_ones = None
        self.impurity_dict ={}

    def fit(self, X, y):
        '''
        X:  two dimensional numpy array representing feature matrix
                for test data
        y:  numpy array representing labels for test data
        '''
        X = np.array(X)
        y = np.array(y)
        sort_index =  np.argsort(y)
        X = X[sort_index, :]
        y = y[sort_index]
        self.forest = self.build_forest(X, y)
        self.feature_importance_ = np.zeros(X.shape[1])
        self.feature_selected_ = np.zeros(X.shape[1])
        for tree_ in self.forest:
            self.feature_importance_ += tree_.feature_importance_
            self.feature_selected_ += tree_.feature_selected_
        #self.feature_importance_ = self.feature_importance_ / self.feature_selected_
        self.feature_importance_ = self.feature_importance_  / np.sum(self.feature_importance_)

    def build_forest(self, X, y):
        '''
        Return a list of num_trees DecisionTreeClassifiers.
        '''
        tree_list = []
        num_samples_ = X.shape[0]
        sample_index_ = np.arange(num_samples_)
        for i in range(self.num_trees):
            # start = now()
            dt = DecisionTreeClassifier(max_features=self.max_features, max_depth=self.max_depth,
                              feature_names=self.feature_names,
                              continous_variable_splits=self.continous_variable_splits,
                              feature_threshold=self.feature_threshold,
                              impurity_dict= self.impurity_dict)
            tree_index = np.random.choice(sample_index_, num_samples_, replace=True)
            X_tree = X[tree_index, :]
            y_tree = y[tree_index]
            dt.fit(X_tree, y_tree)
            # self.impurity_dict.update(dt.fit(X_tree, y_tree))
            # print(len(self.impurity_dict))
            # end = now()
            # print("Build Tree %i takes %f" % (i, end - start))
            tree_list.append(dt)
        return tree_list

    def predict(self, X):
        '''
        Return a numpy array of the labels predicted for the given test data.
        '''
        if len(X.shape) == 1:
            n_rows = 1
        else:
            n_rows = X.shape[0]
        y_pred_list = []
        for j in range(n_rows):
            if n_rows == 1:
                y_pred_ones = [tree_.root.predict_one(X) for tree_ in self.forest]
            else:
                y_pred_ones = [tree_.root.predict_one(X[j]) for tree_ in self.forest]
            y_pred_list.append(Counter(y_pred_ones).most_common(1)[0][0])
        self.predict_ones = y_pred_ones
        return np.array(y_pred_list)

    def score(self, X, y):
        '''
        Return the accuracy of the Random Forest for the given test data and
        labels.
        '''
        y_pred = self.predict(X)
        n_right = np.sum(y == y_pred)
        n_total = len(y)
        return float(n_right)/n_total

class DecisionTreeRegressor(object):
    '''
    A decision tree regressor class.
    Input to Decision tree should be either string for categorical feature or float for continuous features
    This module do not support boolean
    '''

    def __init__(self, impurity_criterion='variance', max_features=None, feature_names=None, feature_threshold=None,
                 max_depth=float('inf'), continous_variable_splits="unique"):
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
        self.impurity_criterion = self.variance
        self.continous_variable_splits = continous_variable_splits  ## Percentile or unique values
        self.feature_importance_ = None
        self.feature_selected_ = None
        self.min_split = 1
        self.CV_threshold = 0
        # self.time1 = 0  ## Time for choose split
        # self.n1 = 0     ## Number of calls choose split
        # self.time2 = 0  ## Time for make split
        # self.n2 = 0     ## Number of calls make split
        # self.time3 = 0  ## Time for information gain
        # self.n3 = 0     ## Number of calls information gain
        # self.time3_overhead = 0
        # self.time3_overhead2 = 0
        # self.time3_overhead3 = 0
        # self.time3_overhead4 = 0

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
        self.feature_importance_ = self.feature_importance_ / np.sum(self.feature_importance_)
        # end = now()
        # print("build tree takes", end - start)

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
        index, value, splits = self._choose_split_index(X, y)
        if index is None or self.coef_var(y) <= self.CV_threshold \
                or depth >= self.max_depth \
                or len(y) <= self.min_split:
            ### Leaf nodes
            node.leaf = True
            node.name = np.mean(y)  ## Prediction value
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

        split_index, split_value, splits = None, None, None
        max_gain = 0
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
                    if len(values) < 2:
                        continue
                    for val in values:
                        # start_1 = now()
                        temp_splits = self._make_split(X, y, i, val)
                        X1, y1, X2, y2 = temp_splits
                        gain = self._information_gain(y, y1, y2)
                        # end_1 = now()
                        # self.time3_overhead += end_1 - start_1
                        if gain > max_gain and len(y1) > 0 and len(y2) > 0:
                            max_gain = gain
                            split_index, split_value = i, val
                            splits = temp_splits
                else:
                    if self.continous_variable_splits.lower() == "percentile".lower():
                        percentiles_ = np.arange(10, 100, 10)
                        vals = np.percentile(X[:,i], percentiles_)
                    else:
                        vals = np.unique(X[:,i])
                    threshold_ = []
                    for val in vals:
                        threshold_.append(val)
                        # start_1 = now()
                        temp_splits = self._make_split(X, y, i, val)
                        # end_2 = now()
                        # self.time3_overhead += end_2 - start_1
                        X1, y1, X2, y2 = temp_splits
                        # end_3 = now()
                        # self.time3_overhead2 += end_3 - end_2
                        gain = self._information_gain(y, y1, y2)
                        # end_1 = now()
                        # self.time3_overhead3 += end_1 - end_3
                        if gain > max_gain and len(y1) > 0 and len(y2) > 0:
                            max_gain = gain
                            split_index, split_value = i, val
                            splits = temp_splits
                    if i not in self.feature_threshold_out_:
                        self.feature_threshold_out_[i] = threshold_
            else:
                ## Use user specified thresholds
                values = self.feature_threshold[i]
                if len(values) < 2:
                    continue
                for val in values:
                    temp_splits = self._make_split(X, y, i, val)
                    X1, y1, X2, y2 = temp_splits
                    # start_1 = now()
                    gain = self._information_gain(y, y1, y2)
                    # end_1 = now()
                    # self.time3_overhead += end_1 - start_1
                    if gain > max_gain and len(y1) > 0 and len(y2) > 0:
                        max_gain = gain
                        split_index, split_value = i, val
                        splits = temp_splits
        if split_index is not None:
            # print(split_index, max_gain)
            self.feature_importance_[split_index] += max_gain * len(y)
            self.feature_selected_[split_index] += 1
        return split_index, split_value, splits

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
        split_col = X[:, split_index]
        if self.categorical[split_index]:
            mask = split_col == split_value
        else:
            mask = split_col < split_value
        return X[mask, :], y[mask], X[~mask, :], y[~mask]

    def variance(self, y):
        '''
        INPUT:
            - y: 1d numpy array
        OUTPUT:
            - float
        Return the entropy of the array y.
        '''
        return np.std(y)

    def coef_var(self, y):
        return self.variance(y) / np.mean(y) * 100

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
        # total = self.impurity_criterion(y)
        # for y_split in (y1, y2):
        #     ent = self.impurity_criterion(y_split)
        #     total -= len(y_split) * ent / float(len(y))
        # return total
        bf_split_ = self.impurity_criterion(y)
        af_split1_ = self.impurity_criterion(y1)
        af_split2_ = self.impurity_criterion(y2)
        return bf_split_ - len(y1) /float(len(y)) * af_split1_ - len(y2)/float(len(y)) * af_split2_

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
        Return the R^2 of the prediction
        '''
        y_pred = self.predict(X)
        u = np.sum(((y - y_pred) ** 2))
        v = np.sum(((y - y.mean()) ** 2))
        return 1 - u/v

    def __str__(self):
        '''
        Return string representation of the Decision Tree.
        '''
        return str(self.root)

class RandomForestRegressor(object):
    '''A Random Forest class'''

    def __init__(self, n_estimators, max_features="auto", max_depth=float('inf'),
                 continous_variable_splits="Percentile", feature_names=None, feature_threshold=None):
        '''
           num_trees:  number of trees to create in the forest:
        max_features:  the number of features to consider when choosing the
                           best split for each node of the decision trees
        '''
        self.num_trees = n_estimators
        self.max_features = max_features
        self.feature_names = feature_names
        self.feature_threshold = feature_threshold
        self.max_depth = max_depth
        self.continous_variable_splits = continous_variable_splits
        self.forest = None
        self.feature_importance_ = None
        self.feature_selected_ = None
        self.predict_ones = None

    def fit(self, X, y):
        '''
        X:  two dimensional numpy array representing feature matrix
                for test data
        y:  numpy array representing labels for test data
        '''
        X = np.array(X)
        y = np.array(y)
        self.forest = self.build_forest(X, y)
        self.feature_importance_ = np.zeros(X.shape[1])
        self.feature_selected_ = np.zeros(X.shape[1])
        for tree_ in self.forest:
            self.feature_importance_ += tree_.feature_importance_
            self.feature_selected_ += tree_.feature_selected_
        #self.feature_importance_ = self.feature_importance_ / self.feature_selected_
        self.feature_importance_ = self.feature_importance_  / np.sum(self.feature_importance_)

    def build_forest(self, X, y):
        '''
        Return a list of num_trees DecisionTreeClassifiers.
        '''
        tree_list = []
        num_samples_ = X.shape[0]
        sample_index_ = np.arange(num_samples_)
        if self.max_features == "auto":
            self.max_features = int(math.sqrt(X.shape[1]))
        for i in range(self.num_trees):
            # start = now()
            dt = DecisionTreeRegressor(max_features=self.max_features, max_depth=self.max_depth,
                              feature_names=self.feature_names,
                              continous_variable_splits=self.continous_variable_splits,
                              feature_threshold=self.feature_threshold)
            tree_index = np.random.choice(sample_index_, num_samples_, replace=True)
            X_tree = X[tree_index, :]
            y_tree = y[tree_index]
            dt.fit(X_tree, y_tree)
            # end = now()
            # print("Build Tree %i takes %f" % (i, end - start))
            tree_list.append(dt)
        return tree_list

    def predict(self, X):
        '''
        Return a numpy array of the labels predicted for the given test data.
        '''
        if len(X.shape) == 1:
            n_rows = 1
        else:
            n_rows = X.shape[0]
        y_pred_list = []
        for j in range(n_rows):
            if n_rows == 1:
                y_pred_ones = [tree_.root.predict_one(X) for tree_ in self.forest]
            else:
                y_pred_ones = [tree_.root.predict_one(X[j]) for tree_ in self.forest]
            y_pred_list.append(np.mean(y_pred_ones))
        self.predict_ones = y_pred_ones
        return np.array(y_pred_list)

    def score(self, X, y):
        '''
        Return the R^2 of the prediction
        '''
        y_pred = self.predict(X)
        u = np.sum(((y - y_pred) ** 2))
        v = np.sum(((y - y.mean()) ** 2))
        return 1 - u/v