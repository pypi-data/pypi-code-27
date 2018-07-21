#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 12:02:46 2018
"""

# Author: Chendi Huang <elimpalm@gmail.com>
#         Xinwei Sun <sxwxiaoxiao@pku.edu.cn>
#         Jiechao Xiong <xjctzdyh@126.com>
#         Yuan Yao <yuany@ust.hk>

# References:
#
#    Huang C, Sun X, Xiong J, et al.
#    Split LBI: An Iterative Regularization Path with Structural Sparsity.
#    Advances In Neural Information Processing Systems. 2016: 3369-3377.
#
#    Vaiter S, Peyré G, Dossal C, et al. Robust sparse analysis regularization.
#    IEEE Transactions on information theory, 2013, 59(4): 2001-2016.
#
#    Osher S, Ruan F, Xiong J, et al.
#    Sparse recovery via differential inclusions.
#    Applied and Computational %Harmonic Analysis, 2016, 41(2): 436-469.





import numpy as np
from sklearn.model_selection import StratifiedKFold,KFold
from .base import predict_error_gaussian,predict_error_binomial
from .linear import LBI_Linear
from .logistic import LBI_Logit


def LB(X,y,ind_true=None,auc_compute=False,roc_plot=True,path_plot=True,family='gaussian',kappa=10,
       alpha=None,t0=None,t_ratio=100,t_num=500,t_seq=None,fit_intercept=False,normalize=False,
       copy_X=True,fast_init=False,group_index=None,verbose=True):
     
     """
     Linearized Bregman Iteration for l1 Problem.
     
     Parameters
     ----------
     X: array_like, the design matrix, with shape (n_samples,n_features)
     
     y: array_like, the label, with shape (n_samples,)
     
     ind_true: array_like, the true signal set (for auc computation), default None since it's unknown
          it should be set if the auc_compute is true.
          
     auc_compute: boolean, optional, default False
         whether compute auc to measure the model selection consistency.
         
     roc_plot: boolean, optional, default True
         whether plot roc curve when compute auc
         
     path_plot: boolean, optional, default True
         whether plot regularization solution path
         
     family: string, "gaussian" or "binomial", default "gaussian"
         the distribution of y
         
     kappa : int, default 10, Damping factor
     
     alpha : float, the step size which satisfies
         kappa * alpha * || X^{\star}X ||_2 < 2
         
     t0 : float, the regularization parameter at which
         the non-zeros variables start to come out.
         It can be determined by calculating the 
         MLE estimator
         
     t_ratio: float, default 100,
          the length of the path: t0 * t_ratio.
          
     t_num: int, Default 500, 
          the number of saved estimators in the path. 
          
     t_seq: array_like, the saved estimators in the path. 
     
     fit_intercept : boolean, optional, default True
         whether to calculate the intercept during the path. If set
         to False, no intercept will be used in calculations
         (e.g. data is expected to be already centered).
         
     normalize : boolean, optional, default False
         This parameter is ignored when ``fit_intercept`` is set to False.
         If True, the regressors X will be normalized before regression by
         subtracting the mean and dividing by the l2-norm.
         If you wish to standardize, please use
         :class:`sklearn.preprocessing.StandardScaler` before calling ``fit`` on
         an estimator with ``normalize=False``.
         
     copy_X : boolean, optional, default True
         If True, X will be copied; else, it may be overwritten.
         
     fast_init : boolean, optional, default False
         Whether use the MLE estimator of intercept as initialization.
         
     group_index: array, optional, default None
         specify the group of each variable.
         
     verbose: boolean, optional, default True
         whether show the procession of iteration.
         
     Returns
     ----------
     obj : returns an instance of self. 
     The attributes can be refered to LBI_linear or LBI_logistic 
     
     """
     
     class_dict = {'gaussian':LBI_Linear,'binomial':LBI_Logit}
     
     
     obj = class_dict.get(family)(kappa,alpha,t0,t_ratio,t_num,t_seq,fit_intercept,
                         normalize,copy_X,fast_init,group_index,verbose)
     obj.fit(X,y)
     
     if auc_compute is True:
          if ind_true is None:
               raise ValueError('Should provide the true signal set if compute AUC!')
          else:
               obj.auc = obj.ROC_AUC(ind_true,roc_plot)
     
     if path_plot is True:
          obj.Solution_path(ind_true)
     
     return obj


             
def cv_LB(X,y,kfolds=5,random_seed=1,ind_true=None,auc_compute=False,roc_plot=True,path_plot=True,
          family='gaussian',kappa=10,alpha=None,t0=None,t_ratio=100,t_num=500,t_seq=None,
          fit_intercept=False,normalize=False,copy_X=True,fast_init=False,
          group_index=None,verbose=True):
    """
    Cross validation
    
    Parameters (in addition to the ones in LB)
    ----------
    kfolds: the number of folds in cross-valdation
    random_seed: the random seed for partition of the dataset
    
    Attributes (in addtion to the ones in LB):
    ----------
    predict_error_cv: the prediction error by cross-validation
    ind_cv: the regularization parameter which returns the minimum prediction error
    """
    
    ## Kfolds
    if isinstance(kfolds,int) is False or kfolds < 2:
         raise ValueError('The kfolds must be int and greater than 2!')
    if kfolds > X.shape[0]:
         raise ValueError('The kfolds should be less or equal than the number of samples!')
        
    ## Random Seed for partition
    np.random.seed(random_seed)
    
    ## Partition (X,y) into kfolds
    partition_dict = {'gaussian':KFold,'binomial':StratifiedKFold}
    skf = partition_dict.get(family)(n_splits=kfolds)
    skf.get_n_splits(X, y)
    
    ## Calculate prediction error on train dataset
    class_dict = {'gaussian':LBI_Linear,'binomial':LBI_Logit}
    obj = class_dict.get(family)(kappa,alpha,t0,t_ratio,t_num,t_seq,fit_intercept,
                         normalize,copy_X,fast_init,group_index,verbose)
    obj.initialize_paras(X,y)
    if family == 'binomial':
         y_new = obj.y
    else:
         y_new = y
         
    
    predict_error_cv = np.zeros((len(obj.t_seq),))
    for (fold,(train_index, test_index)) in enumerate(skf.split(X, y_new)):
         print('\x1b[6;30;42m' + 'Cross-validation: the %s-th fold'%(fold+1) + '\x1b[0m')
         X_train, X_test = X[train_index,:], X[test_index,:]
         y_train, y_test = y_new[train_index], y_new[test_index]
         obj.fit(X_train,y_train)
         
         if family == 'gaussian':
              y_est = obj.predict(X_test)
              predict_error_cv += predict_error_gaussian(y_test,y_est)
              
         elif family == 'binomial':
              prob = obj.predict(X_test)
              predict_error_cv += predict_error_binomial(y_test,prob,pos_label=1) * X_test.shape[0] / X.shape[0]
              
    obj.predict_error_cv = predict_error_cv
    ## Pick up the regularization parameter which gives the minimum prediction error
    obj.ind_cv = np.argmin(predict_error_cv)
     
    ## Training on the whole dataset
    print('\x1b[0;30;46m' + 'Training on the whole dataset' + '\x1b[0m')
    obj.fit(X,y)
    
    
     
    return obj
     
              
              
              
         
         
    
        

    

     
