"""
Main module of the activeLearning project. Encapsulates the data and the various methods and steps
required to perform active learning using rich feedback. Convert this cell into module after dev.
"""

import pickle
import autograd
import lime
import lime.lime_tabular
import numpy as np
import pandas as pd
import active_learning.classifier as cf
from active_learning.utils import inverse_sigmoid
from sklearn import base
from sklearn import metrics
from sklearn.linear_model import LogisticRegression


class Session():
    """

    Parameters
    ----------
    dataset : Pandas dataframe
        Underlying dataset for active learning. Does not contain any labels -- strictly data.
    budget : Int
        Number of active learning iterations to perform.
    predictions: Current y predictions (for continued training)
    gt: Which have ground truths
    AF: acquisition function
        random - random
        mlp - most likely positive
        us - uncertainty sampling
        mixed - ensemble
    epochs - Number of epochs for training
    """

    def __init__(self,
                 dataset=None,
                 budget=None,
                 base_classifier=None,
                 sentences=None,
                 gt = None,
                 classifier = None,
                 AF = 'mixed',
                 epochs = 10
                 ):

        self.dataset = dataset
        self.budget = budget
        self.base_classifier = base_classifier
        if classifier is None:
            self.classifier = cf.classifier(
                num_cov=1, num_feat=self.dataset.shape[1], num_clusters=2)
        else:
            self.classifier = classifier
        self.loss = None
        self.features = None
        self.rules = set()
        self.sentences = sentences
        self.gt = gt
        self.AF = AF
        #Slow when greater than 10 on my machine but doesnt train much, I used 2
        #For testing, it really should be more like 1000, perhaps faster on Rambo?
        self.epochs = epochs


    def initialize(self):

        self.features = list(self.dataset.columns)
        self.feat_mapping = dict(zip(np.arange(len(self.features)),self.features))
        # Build classifications based on baseline classifier
        self.predictions = self.base_classifier.predict(self.dataset)
        self.gt = np.zeros(self.dataset.shape[0])

        # Fit classifier on baseline classifier's predictions
        #self.classifier.fit(self.dataset, self.predictions)
        #Hosseins code
        theta0 = self.classifier._flatten()
        result = self.classifier.optimize(np.ones((len(self.dataset),1)), self.dataset.values, self.predictions,
                             sample_weights=None, batch_size=100, theta0=theta0,
                             max_iters=self.epochs, opt_method='rmsprob', final_bfgs=False, full_batch=True, dropout_prob=0.5)
        self.classifier._to_param(result['x'])

        self.explainer = lime.lime_tabular.LimeTabularExplainer(
            self.dataset.values, feature_names=self.features,
            class_names=['Not Baseball','Baseball'], discretize_continuous=True)
        self.scaling = None
        self.rule_directions = None
        #haven't implemented rule weights yet
        self.rule_weights = None
        return


    def parse_rule(self, rule_string):
        rule_list = pd.Series(rule_string.split('&')).str.strip().str.split(' ')
        rule_tup = [tuple(x) for x in rule_list.values]

        return rule_tup

    def apply_rule(self,rule):
        if rule[0] is None:
            return None
        rule_name = None
        S_r, feat_gt_thresh = self.create_scaling_series(rule[0])
        if S_r is None:
            return None
        rule_name = self.get_rule_name(feat_gt_thresh)
        if rule_name in self.rules:
            return None
        if self.scaling is None:
            self.scaling = S_r.copy()
        else:
            self.scaling = pd.concat([self.scaling,S_r],1)
        if self.rule_directions is None:
            self.rule_directions = [rule[1]]
            self.rule_directions = np.array(self.rule_directions)
        else:
            self.rule_directions = list(self.rule_directions)
            self.rule_directions.append(rule[1])
            self.rule_directions = np.array(self.rule_directions)
        return rule_name


    def create_scaling_series(self,rule_part):
        """Create S(x,xc) term for each rule
        Args:
            rule_part - the part of the rule that is features and thresholds

        """
        rule_frac = np.zeros(len(self.dataset))
        feats = []
        threshs = []
        gts = []
        for inp in rule_part:
            feat = inp[0]
            if feat not in self.features:
                continue
            feat = self.features.index(feat)
            feats.append(feat)
            gt = inp[1]=='>'
            gts.append(gt)
            thresh = float(inp[2])
            threshs.append(thresh)
            if gt:
                temp = (self.dataset.iloc[:,feat]>thresh).astype(float)
            else:
                temp = (self.dataset.iloc[:,feat]<=thresh).astype(float)
            rule_frac = rule_frac + temp/len(rule_part)
        if len(feats)==0:
            return None,None
        feats = np.array(feats)
        threshs = np.array(threshs)
        euclid = np.sqrt(((self.dataset.iloc[:,feats]-threshs)**2).sum(1))
        S_r = 1/2*np.exp(-euclid) + 1/2*np.exp(-rule_frac)

        return S_r, (feats,gts,threshs)

    def get_rule_name(self,rule_tups):
        rule_frame = pd.DataFrame(np.array(rule_tups).T)
        rule_frame.iloc[:,0] = rule_frame.iloc[:,0].map(self.feat_mapping)

        rule_frame.iloc[:,1][rule_frame.iloc[:,1]==True]='>'
        rule_frame.iloc[:,1][rule_frame.iloc[:,1]==False]='<='
        rule_series = (
            rule_frame.iloc[:,0].astype(str) + ' ' +
            rule_frame.iloc[:,1].astype(str) + ' ' + rule_frame.iloc[:,2].astype(str)
        )
        rule_name = ' & '.join(rule_series.tolist())
        return rule_name

    def get_expert_input(self, sample, index):
        """
        Function for asking user for input (label for the sample as well as a rule). Parses rule into a tuple
        and adds it to the list of rules to evaluate. Rules should be entered as [feature] [operator] [value]
        triplet separated by spaces. Multiple rules should be separated by special char: '&'
        Example: X1 < 15.37 & X3 < 3.2

        params:
        -------
            sample : Pandas series
                single sample from dataset that will be evaluated by the expert.

        returns:
        -------
            sampleLabel : int in set{0,1}
                label of the sample passed as input.
            rules : list of rules
                rules are tuples the first term is the rule which is a tuple - (features,sign,threshold)
                the second term is which what the rule indicates, a 1 indicates positive, a 0 negative, and 0.5
                irrelevant
        """
        rules = []
        print(self.sentences[index])
        while(True):
            sampleLabel = input("Enter the class for this sample: ")
            if sampleLabel == '1':
                rule_string = input("Enter a rule for why this example is positive ('None' to enter no rule): ")
                if rule_string == 'None':
                    break
                rule_tup = self.parse_rule(rule_string)
                rule = (rule_tup,1)
                rules.append(rule)
                break

            elif sampleLabel == '0':
                rule_string = input("Enter a rule for why this example is negative ('None' to enter no rule): ")
                if rule_string == 'None':
                    break
                rule_tup = self.parse_rule(rule_string)
                rule = (rule_tup,0)
                rules.append(rule)
                break

            print('Enter a 0 or 1 please!')

        rules_list=self.feedback(index)
        for rule in rules_list:
            if rule[0] is not None:
                rules.append(rule)

        if len(rules):
            return (sampleLabel, rules)
        else:
            return (sampleLabel, None)

    def question(self, showed_pos):
        print('We will now ask you 3 questions it is okay to leave some blank, get ready.\n')
        if showed_pos:
            print('Which of these features (with their corresponding threshold) would make you predict BASEBALL?)')
            pos = input('List these features seprated by commas (Enter None for nothing): ')
            print('Which of these features (with their corresponding threshold) would make you predict NOT BASEBALL?)')
            neg = input('List these features seprated by commas (Enter None for nothing): ')
        else:
            print('Which of these features (with their corresponding threshold) would make you predict NOT BASEBALL?)')
            neg = input('List these features seprated by commas (Enter None for nothing): ')
            print('Which of these features (with their corresponding threshold) would make you predict BASEBALL?)')
            pos = input('List these features seprated by commas (Enter None for nothing): ')
        print('Which of these features (with their corresponding threshold) would not help you make a prediction?)')
        irr = input('List these features seprated by commas (Enter None for nothing): ')

        return pos,neg,irr

    def feedback(self, index):
        exp = self.explainer.explain_instance(
            self.dataset.values[index], self.classifier.predict_proba, num_features=5, top_labels=1)
        pred = np.argmax(exp.predict_proba)
        feat_thres = np.array(exp.as_list(label=pred))
        pos_feats = feat_thres[:,0][feat_thres[:,1].astype(float)>0]
        neg_feats = feat_thres[:,0][feat_thres[:,1].astype(float)<0]
        if pred == 1:
            if len(pos_feats):
                print('Our model believe this example IS about baseball because: ')
                for feat in pos_feats:
                    print(feat)
                pos,neg,irr = self.question(True)
                pos1 = (self.parse_feedback(feat_thres,pos),1)
                neg1 = (self.parse_feedback(feat_thres,neg),0)
                irr1 = (self.parse_feedback(feat_thres,irr),0.5)
            else:
                pos1 = (None,1)
                neg1 = (None,0)
                irr1 = (None,0.5)
            if len(neg_feats):
                print('\nOur model believes this example IS NOT about baseball because: ')
                for feat in neg_feats:
                    print(feat)
                pos,neg,irr = self.question(False)
                pos2 = (self.parse_feedback(feat_thres,pos),1)
                neg2 = (self.parse_feedback(feat_thres,neg),0)
                irr2 = (self.parse_feedback(feat_thres,irr),0.5)
            else:
                pos2 = (None,1)
                neg2 = (None,0)
                irr2 = (None,0.5)
        if pred == 0:
            if len(pos_feats):
                print('Our model believe this example IS NOT about baseball because: ')
                for feat in pos_feats:
                    print(feat)
                pos,neg,irr = self.question(False)
                pos1 = (self.parse_feedback(feat_thres,pos),1)
                neg1 = (self.parse_feedback(feat_thres,neg),0)
                irr1 = (self.parse_feedback(feat_thres,irr),0.5)
            else:
                pos1 = (None,1)
                neg1 = (None,0)
                irr1 = (None,0.5)
            if len(neg_feats):
                print('\nOur model believes this example IS about baseball because: ')
                for feat in neg_feats:
                    print(feat)
                pos,neg,irr = self.question(True)
                pos2 = (self.parse_feedback(feat_thres,pos),1)
                neg2 = (self.parse_feedback(feat_thres,neg),0)
                irr2 = (self.parse_feedback(feat_thres,irr),0.5)
            else:
                pos2 = (None,1)
                neg2 = (None,0)
                irr2 = (None,0.5)
        return pos1,neg1,irr1,pos2,neg2,irr2

    def parse_feedback(self, feat_thres,feats):
        if feats=='None':
            return None
        feats=pd.Series(feats.split(',')).str.strip().str.lower()
        rules = pd.Series(np.array(feat_thres[:,0])).str.split(' ',expand=True)
        words = rules[0].str.strip()
        signs = rules[1].str.strip()
        signs[signs=='<=']='<'
        thres = rules[2].str.strip()
        rules = pd.DataFrame([words,signs,thres]).T
        rules = rules[words.isin(feats)]
        return [tuple(x) for x in list(rules.values)]

    #def rule_loss(self):
    #    num_rules = len(self.rules)
    #    if num_rules == 0:
    #        return 0
    #    probs = self.classifier.predict_proba(self.dataset)
    #    probs = probs[:,1]
    #    y_minus_fx_sq = (probs[:,None]-self.rule_directions[None])**2
    #    tot_err = y_minus_fx_sq*self.scaling
    #    rule_loss = tot_err.mean.mean()

     #   return rule_loss

    #def custom_loss(self):
    #    lloss = metrics.log_loss(self.predictions,self.classifier.predict_proba(self.dataset.values))
    #    rloss = self.rule_loss()
    #    return lloss + rloss()

    def query_function(self, fitted_classifier, X, fnc='mlp', mlp_weight = 1):
        """Return ranked list of examples to query as well as scores

        Args:
            fitted_classifier - a classifier fit on X data
            X: data
            fnc (optional): type of query function options are:
                mlp - "most likely positive:"
                    chose examples most likely to be from the positive class
                mln - "most likely negative:"
                    chose examples most likely to be from the negative class
                us:
                    chose examples most uncertain about
                mixed:
                    weighted average of mlp and us
        Returns:
            queries: ranked indices (first best) of examples to query
            in X
            scores: scores for each X ordered in same order as queries.

            """

        proba, _ = self.classifier.predict(np.ones((len(self.dataset),1)), self.dataset.values)
        if isinstance(proba,autograd.numpy.numpy_boxes.ArrayBox):
            proba = proba._value
        dec_f = inverse_sigmoid(proba)
        if (fnc == 'us'):
            dists = np.abs(dec_f)
            queries = np.argsort(dists)
            scores = dists[queries]
        elif (fnc == 'mlp'):
            probs = dec_f
            inds = np.argsort(probs)
            queries = np.flip(inds, 0)
            scores = (probs[queries] - np.max(probs)) * -1
            scores += 1e-4
        elif (fnc == 'mln'):
            probs = dec_f
            queries = np.argsort(probs)
            scores = probs[queries] - np.min(probs)
            scores += 1e-4
        elif (fnc == 'mixed'):
            scores_clh = np.abs(dec_f)
            scores_mlp = dec_f
            scores_mlp = (scores_mlp - np.max(scores_mlp)) * -1
            scores = mlp_weight*scores_mlp + (1-mlp_weight)*scores_clh
            queries = np.argsort(scores)
            scores = scores[queries]

        return queries, scores

    def decay_pmf(self, scores, it):

        # Exponential Decay Function
        pk = np.exp(-it * scores) / (sum(np.exp(-it * scores)))

        # Fix Rounding Errors
        rem = 1 - sum(pk)
        pk[np.argmax(pk)] += rem

        return pk

    def sample_from_pmf(self, queries, pk, N):
        samp = np.random.choice(queries, N, p=pk)
        return samp

    def acquisition(self, i):
        """Test how accuracy vs number of examples given to classifier

        Args:
            i: iteration of the algorithm
            X: data
            predictions: predictions from rule based classifier
            y_gt: ground truths already obtained
            init_classifier: classifier to do train on rule based labels
            final_classifier: type classifier we want to be the final classifier we train on at
            end of task

        Returns:
            example: indice of query
            used: updated indicies of used examples
        """


        X = self.dataset.copy()
        predictions = self.predictions.copy()
        clf = self.classifier

        ## Choose the index of the example
        inds = np.arange(self.dataset.shape[0])
        used = set()
        if (i != 0):
            used = set(inds[self.gt == 1])
        used_arr = np.array(list(used))
        not_used=np.setdiff1d(np.arange(len(predictions)),used_arr)

        ###START anything else
        #probs = clf.decision_function(X)
        proba, _ = self.classifier.predict(np.ones((len(self.dataset),1)), self.dataset.values)
        if isinstance(proba,autograd.numpy.numpy_boxes.ArrayBox):
            proba = proba._value
        print('Max')
        print(proba.max())
        probs = inverse_sigmoid(proba)
        if self.AF == 'mixed':
            diff = np.sum(self.predictions[self.gt==1]==0) - np.sum(self.predictions[self.gt==1]==1)
            weight = np.tanh(diff)
            weight = (weight+1)/2
            queries, scores = self.query_function(clf, X.iloc[not_used], fnc=self.AF, mlp_weight = weight)
        elif self.AF == 'random':
            inds = np.arange(len(not_used))
            ind = np.random.choice(inds)
            example_id = not_used[ind]
            example = self.dataset.iloc[example_id]
            return (example, example_id)
        else:
            queries, scores = self.query_function(clf, X.iloc[not_used], fnc=self.AF)
        pk = self.decay_pmf(scores, (len(used)+1)*1)
        example_id = self.sample_from_pmf(queries, pk, 1)[0]
        #Surface an example
        example_id = not_used[example_id]
        print('Ours')
        print(proba[example_id])
        example = self.dataset.iloc[example_id]

        return (example, example_id)
        ###END

    def iteration(self, i):
        """
        A single iteration of the active learning process.


        Params:
        -------
        i : int
            iteration index of the algorithm

        """

        ## Get the best sample for the current iteration
        sample, index = self.acquisition(i)

        return (sample, index)

    def train(self):
        """
        Execute the active learning algorithm from start to finish.

        ** NOTE **
        Current not implemented to allow for exploration and testing within the notebook. The logic of train will
        be included in the subsequent cells.
        """


        for i in range(self.budget):
            print('\n Traning on example: {}\n'.format(i))
            sample, index = self.iteration(i)
            label, rules = self.get_expert_input(sample, index)
            self.predictions[index] = label
            self.gt[index] = 1

            #num_trained = np.sum(self.gt)
            #sample_weights = np.ones(self.dataset.shape[0])
            #sample_weights += self.gt * np.min([100, self.dataset.shape[0] / num_trained])

            if rules is None:
                print('None')
                continue

            for rule in rules:
                rule_name = self.apply_rule(rule)
                if rule_name is None:
                    continue
                self.rules.add(rule_name)
                self.classifier.add_features(self.rule_directions,self.scaling.values)


            #self.classifier.fit(self.dataset,self.predictions)
            theta0 = self.classifier._flatten()
            result = self.classifier.optimize(np.ones((len(self.dataset),1)), self.dataset.values, self.predictions,
                                 sample_weights=None, batch_size=100, theta0=theta0,
                                 max_iters=self.epochs, opt_method='rmsprob', final_bfgs=False, full_batch=True, dropout_prob=0.5)
            self.classifier._to_param(result['x'])
        return self.classifier, self.dataset, self.predictions, self.gt
