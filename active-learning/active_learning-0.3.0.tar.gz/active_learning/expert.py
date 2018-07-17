"""
Expert class for AL. Allows us to simulate human expert.
"""

from active_learning.datasets import twentynews_tfidf
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import lime
import lime.lime_tabular

class Expert():
    
    """
    Parameters
    ----------
    X: X (as a dataframe with features as column names)
    y: Real y values
    classifier: 
        Sklearn classifier to train to completion. Use best possible for task.
        Default is logistic regression.
    lime_append: Number of LIME features to use in rule append.
    lime_diagnose: Number of LIME features to use in model diagnostic phase.
    """
    
    def __init__(self, X, y, 
                 classifier = None, 
                 lime_append = 3, 
                 lime_diagnose = 10
                ):
        self.X = X
        self.y = y
        if classifier is None:
            self.classifier = LogisticRegression()
        else:
            self.classifier = classifier
        self.lime_append = lime_append
        self.lime_diagnose = lime_diagnose
        self.initialize()
        
    
    def initialize(self):
        """Fit classifier and create lime explainer"""
        self.classifier.fit(self.X,self.y)
        self.features = self.X.columns
        #The baseball part is hard coded but doesn't have to be
        self.explainer = lime.lime_tabular.LimeTabularExplainer(
            self.X.values, feature_names=self.features,
            class_names=['Not Baseball','Baseball'], discretize_continuous=True)
        
    def rule_append(self,sample):
        """Return sampleLabel, rule_string tuple that are usually gotten as user inputs in 
        rich_feedback.get_expert_input. I know this code is gross.
        
        Args:
            sample - sample to get rule for - should be array [n_features,]
        
        Returns:
            sampleLabel - '0' or '1' depending on what our classifier predicts
            rule_string - Rule of form '{feature_1} > {threshold_1} & {rule_2} > {threshold_2} & ...''
            """
        self.exp = self.explainer.explain_instance(
            sample, self.classifier.predict_proba, num_features=self.lime_append, top_labels=1)
        pred = np.argmax(self.exp.predict_proba)
        sampleLabel = str(pred)
        feat_thres = np.array(self.exp.as_list(label=pred))
        feat_thres = feat_thres[feat_thres[:,1].astype(float)>0]
        rule_string = ' & '.join(list(feat_thres[:,0]))
    
        return (sampleLabel, rule_string)
    
    def rule_diagnose(self,rf_exp,sample=None,retrain=False):
        """Simulate rich_feedback.feedback specifically the rich_feedback.question part
        
        Args:
            rf_exp - LIME explainer from rich_feedback.
            sample - sample to get rule for - should be array [n_features,].
                Only need if retrain
            retrain - 
                retrain the expaliner, we often don't need to as we call this
                right after rule_append.
            
        Returns:
            pos1, pos2 - features that make us predict 1
            neg1, neg2 - features that make us predict 0
            irr1, irr2 - irrelevant features (predict 0.5)
            
            These are in the exact form we'd get from rich_feedback.question
        """
        
        if retrain:
            self.exp = self.explainer.explain_instance(sample,classifier.predict_proba, num_features=self.lime_diagnose, top_labels=1)
        pred = np.argmax(self.exp.predict_proba)
        feat_thres = np.array(self.exp.as_list(label=pred))
        rf_pred = np.argmax(rf_exp.predict_proba)
        rf_feat_thres = np.array(rf_exp.as_list(label=pred))

        pos1=[]
        pos2=[]
        neg1=[]
        neg2=[]
        irr1=[]
        irr2=[]
        if rf_pred == pred:
            feat_thres_pos = feat_thres[feat_thres[:,1].astype(float)>0]  
            feat_thres_pos = pd.Series(feat_thres_pos[:,0]).str.split(' ',expand = True)
            rf_feat_thres_pos = rf_feat_thres[rf_feat_thres[:,1].astype(float)>0]
            for i in rf_feat_thres_pos:
                rule = i[0].split(' ')
                word = rule[0]
                ind = list(self.features).index(word)
                mean_feat = self.X.iloc[:,ind].mean()
                dire = rule[1]
                thresh = rule[2]
                rf_side = float(thresh)<mean_feat
                if len(feat_thres_pos)==0:
                    irr1.append(word)
                elif word not in list(feat_thres_pos[0]):
                    irr1.append(word)
                else:
                    row = feat_thres_pos[feat_thres_pos[0]==word]
                    if row[1].values[0] != dire:
                        if rf_pred == 1:
                            neg1.append(word)
                        else:
                            pos1.append(word)
                    else:
                        our_side = (row[2].astype(float)<mean_feat).values[0]
                        if rf_side == our_side:
                            if rf_pred == 1:
                                pos1.append(word)
                            else:
                                neg1.append(word)

            feat_thres_neg = feat_thres[feat_thres[:,1].astype(float)<0]  
            feat_thres_neg = pd.Series(feat_thres_neg[:,0]).str.split(' ',expand = True)
            rf_feat_thres_neg = rf_feat_thres[rf_feat_thres[:,1].astype(float)<0]
            for i in rf_feat_thres_neg:
                rule = i[0].split(' ')
                word = rule[0]
                ind = list(self.features).index(word)
                mean_feat = self.X.iloc[:,ind].mean()
                dire = rule[1]
                thresh = rule[2]
                rf_side = float(thresh)<mean_feat
                if len(feat_thres_neg)==0:
                    irr2.append(word)
                elif word not in list(feat_thres_neg[0]):
                    irr2.append(word)
                else:
                    row = feat_thres_neg[feat_thres_neg[0]==word]
                    if row[1].values[0] != dire:
                        if rf_pred == 1:
                            pos2.append(word)
                        else:
                            neg2.append(word)
                    else:
                        our_side = (row[2].astype(float)<mean_feat).values[0]
                        if rf_side == our_side:
                            if rf_pred == 1:
                                neg2.append(word)
                            else:
                                pos2.append(word)

        else:
            #As they don't agree rfs positive is our negative
            feat_thres_pos = feat_thres[feat_thres[:,1].astype(float)<0]  
            feat_thres_pos = pd.Series(feat_thres_pos[:,0]).str.split(' ',expand = True)
            rf_feat_thres_pos = rf_feat_thres[rf_feat_thres[:,1].astype(float)>0]
            for i in rf_feat_thres_pos:
                rule = i[0].split(' ')
                word = rule[0]
                ind = list(self.features).index(word)
                mean_feat = self.X.iloc[:,ind].mean()
                dire = rule[1]
                thresh = rule[2]
                rf_side = float(thresh)<mean_feat
                if len(feat_thres_pos)==0:
                    irr1.append(word)
                elif word not in list(feat_thres_pos[0]):
                    print(word)
                    irr1.append(word)
                else:
                    row = feat_thres_pos[feat_thres_pos[0]==word]
                    if row[1].values[0] != dire:
                        if rf_pred == 1:
                            neg1.append(word)
                        else:
                            pos1.append(word)
                    else:
                        our_side = (row[2].astype(float)<mean_feat).values[0]
                        if rf_side == our_side:
                            if rf_pred == 1:
                                pos1.append(word)
                            else:
                                neg1.append(word)

            feat_thres_neg = feat_thres[feat_thres[:,1].astype(float)>0]  
            feat_thres_neg = pd.Series(feat_thres_neg[:,0]).str.split(' ',expand = True)
            rf_feat_thres_neg = rf_feat_thres[rf_feat_thres[:,1].astype(float)<0]
            for i in rf_feat_thres_neg:
                rule = i[0].split(' ')
                word = rule[0]
                ind = list(self.features).index(word)
                mean_feat = self.X.iloc[:,ind].mean()
                dire = rule[1]
                thresh = rule[2]
                rf_side = float(thresh)<mean_feat
                if len(feat_thres_neg==0):
                    irr2.append(word)
                elif word not in list(feat_thres_neg[0]):
                    irr2.append(word)
                else:
                    row = feat_thres_neg[feat_thres_neg[0]==word]
                    if row[1].values[0] != dire:
                        if rf_pred == 1:
                            pos2.append(word)
                        else:
                            neg2.append(word)
                    else:
                        our_side = (row[2].astype(float)<mean_feat).values[0]
                        if rf_side == our_side:
                            if rf_pred == 1:
                                neg2.append(word)
                            else:
                                pos2.append(word)
                                
        if (len(pos1)):
            pos1 = ','.join(pos1)
        else:
            pos1 = 'None'
        if (len(pos2)):
            pos2 = ','.join(pos2)
        else:
            pos2 = 'None'
        if (len(neg1)):
            neg1 = ','.join(neg1)
        else:
            neg1 = 'None'
        if (len(neg2)):
            neg2 = ','.join(neg2)
        else:
            neg2 = 'None'  
        if (len(irr1)):
            irr1 = ','.join(irr1)
        else:
            irr1 = 'None'
        if (len(irr2)):
            irr2 = ','.join(irr2)
        else:
            irr2 = 'None'
        
        return (pos1, pos2, neg1, neg2, irr1, irr2) 

