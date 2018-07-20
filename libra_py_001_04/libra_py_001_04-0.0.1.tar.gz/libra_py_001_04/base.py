#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 16:35:44 2018

@author: sxwxiaoxiao
"""

import numpy as np
from scipy import sparse
import warnings
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.utils.validation import check_X_y
from sklearn.utils.sparsefuncs import mean_variance_axis, inplace_column_scale
FLOAT_DTYPES = (np.float64, np.float32, np.float16)

def sigmoid(x):
     
     """
     Sigmoid function.
     
     Parameters
     ----------
     x: vector or matrix
     
     Returns
     -------
     e^x / (1 + e^x)
     
     """
     return 1 / (1 + np.exp(-x))

def check_binomial(y):
     """
     Check if the y has two discrete values and transfer them to -1 and 1
     
     Parameters
     ----------
     y: Original response variable
     
     Returns
     -------
     The response variable with binomial values.
     """
     y_binomial = y.copy()
     y_unique = np.unique(y)
     if len(y_unique) != 2:
          raise ValueError('The response variable should be only have 2 discrete numbers!')
     else:
          y_binomial[np.where(y == y_unique[0])] = -1
          y_binomial[np.where(y == y_unique[1])] = 1
     return y_binomial
     

def safe_sparse_dot(a,b):
     """
     Dot product that handle the sparse matrix case correctly.
     
     Parameters
     ----------
     a : array or sparse matrix
     b : array or sparse matrix
     
     Returns
     -------
     dot_product : array or sparse matrix
        sparse if ``a`` or ``b`` is sparse.
     """
     if sparse.issparse(a) or sparse.issparse(b):
          return a * b
     else:
          return np.dot(a,b)
     

def _rescale_data(X, y, sample_weight):
     
    """
    Rescale data in terms of sample_weight
    
    Parameters
    ----------
    X: Design matrix
    y: Response variable
    
    Returns
    rescaled X and y
    """
    
    n_samples = X.shape[0]
    sample_weight = np.sqrt(sample_weight)
    sw_matrix = sparse.dia_matrix((sample_weight, 0),
                                  shape=(n_samples, n_samples))
    X = safe_sparse_dot(sw_matrix,X)
    y = safe_sparse_dot(sw_matrix,y)
    return X, y

def _rescale_data_binomial(a,sample_weight):
     
    """
    Rescale data in terms of sample_weight in logit model
    
    Parameters
    ----------
    a: vector or matrix
    
    Returns
    rescaled a
    """
    
    n_samples = a.shape[0]
    if sample_weight is not None:
         sw_matrix = sparse.dia_matrix((sample_weight, 0),
                                  shape=(n_samples, n_samples))
         a = safe_sparse_dot(sw_matrix,a)
    
    return a
     


def _preprocess_data(X, normalize=False, copy=True):
    
    """
    Preprocessing X if the normalize is True
    
    Parameters
    ----------
    X: Design matrix
    
    Returns
    normalized X with the variance of each column equal to 1 if normalize is True.
    """

    if normalize:
        if sparse.issparse(X):
            _, X_var = mean_variance_axis(X, axis=0)
            X_scale = np.sqrt(X_var)
            inplace_column_scale(X, 1. / X_scale) 
        else:   
            X_std = np.var(X,axis=0)
            XX = X.T / X_std[:,np.newaxis]
            X = XX.T
            
    return X


def linear_mle_tmle(X,y,group_index,sample_weight=None):
     
     """
     MLE estimator of linear model.
    
     Parameters
     ----------
     X: Design matrix
     y: Response variable
     
     Returns
     Intercept (=0 if fit_intercept is False),coefficients of MLE;
     the regularization parameter before which the variable is not selected
     """
     
     # Compute intercept
     intercept = np.mean(y)
     # Compute gradient
     d_beta = safe_sparse_dot(X.T,intercept-y) / X.shape[0]
     # Compute tmle
     G = len(np.unique(group_index))
     tmle = 1 / np.max([np.linalg.norm(d_beta[np.where(group_index==g)[0]],2) for g in range(0,G)])
     
     return intercept,d_beta,tmle



def logistic_mle_tmle(X,y,group_index,sample_weight):
     
     """
     MLE estimator of logit model.
    
     Parameters
     ----------
     X: Design matrix
     y: Binomial response variable
     
     Returns
     Intercept (=0 if fit_intercept is False),coefficients of MLE;
     the regularization parameter before which the variable is not selected
     """
     
     # Compute intercept
     y_pos = np.sum(sample_weight[y==1])
     y_neg = np.sum(sample_weight[y==-1])
     intercept = np.log(y_pos / y_neg)
     # Compute gradient
     tmp = -y / (1 + np.exp(intercept * y))
     tmp = _rescale_data_binomial(tmp,sample_weight)
     d_beta = safe_sparse_dot(X.T,tmp) / X.shape[0]
     # Compute tmle
     G = len(np.unique(group_index))
     tmle = 1 / np.max([np.linalg.norm(d_beta[np.where(group_index==g)[0]],2) for g in range(0,G)]) 
     
     return intercept,d_beta,tmle



def compute_alpha(X,kappa):
     """
     The step size of iteration
    
     Parameters
     ----------
     X: Design matrix
     kappa: Damping factor
     
     Returns
     step size
     """
     return X.shape[0] / kappa / np.linalg.norm(X,2) ** 2 

def gradient_linear_intercept(X,y,beta,intercept):
     """
     Gradient of the intercept of linear model
    
     Parameters
     ----------
     X: Design matrix
     y: Response variable
     beta: the coefficients at the current step 
     
     Returns
     the gradient of the intercept
     """
     return intercept + np.mean(safe_sparse_dot(X,beta) - y)

def gradient_logistic_intercept(X,y,beta,intercept,sample_weight):
     """
     Gradient of the intercept of logit model
    
     Parameters
     ----------
     X: Design matrix
     y: Response variable
     beta: the coefficients at the current step 
     
     Returns
     the gradient of the intercept
     """
     Xbeta_intercept = safe_sparse_dot(X,beta) + intercept
     tmp = - y / (1 + np.exp(Xbeta_intercept * y))
     tmp = _rescale_data_binomial(tmp,sample_weight)
     return np.mean(tmp)

def gradient_linear(X,y,beta,intercept):
     """
     Gradient of the intercept of linear model
    
     Parameters
     ----------
     X: Design matrix
     y: Response variable
     beta: the coefficients at the current step 
     intercept: the intercept at the current step
     
     Returns
     the gradient of the beta
     """
     
     Xbeta = safe_sparse_dot(X,beta)
     return safe_sparse_dot(X.T,Xbeta + intercept - y) / X.shape[0]



def gradient_logistic(X,y,beta,intercept,sample_weight):
     """
     Gradient of the intercept of linear model
    
     Parameters
     ----------
     X: Design matrix
     y: Response variable
     beta: the coefficients at the current step 
     intercept: the intercept at the current step
     
     Returns
     the gradient of the beta
     """
     Xbeta_intercept = safe_sparse_dot(X,beta) + intercept
     tmp = - y / (1 + np.exp(Xbeta_intercept * y))
     tmp = _rescale_data_binomial(tmp,sample_weight)
     return np.sum(tmp) / np.sum(sample_weight),safe_sparse_dot(X.T,tmp) / X.shape[0] 


def shrinkage(z):
     """
     Soft-thresholding
    
     Parameters
     ----------
     z: rho + beta / kappa ( rho \in \partial(||z||_1) )
     
     Returns
     beta = argmin_x 1/2 * || x - z ||^2 + ||z||_1
     """
     return np.sign(z) * np.array([np.max([0,np.abs(zz)-1]) for zz in z])

def shrinkage_group(z,group_index):
     """
     Group wise Soft-thresholding
    
     Parameters
     ----------
     z_g (g = 1,..,G): rho_g + beta_g / kappa ( rho_g \in \partial(||z_g||_2) )
     
     Returns
     beta_g = argmin_x 1/2 * || x - z_g ||^2 + ||z_g||_2
     """
     z_shrink = np.zeros((len(z),))
     G = len(np.unique(group_index))
     for g in range(G):
          g_ind = np.where(group_index == g)[0]
          z_gind_norm = np.linalg.norm(z[g_ind],2)
          if z_gind_norm == 0:
               z_shrink[g_ind] = 0
          else:
               z_shrink[g_ind] = np.max([0, 1 - 1 / z_gind_norm]) * z[g_ind]
          
     return z_shrink
          


def variable_path(beta_current,var_hist,var_step,num_iter,group_index):
     """
     record the variables that are selected and the step at which they are selected
    
     Parameters
     ----------
     beta_current: the coefficients at the current step
     var_hist: the history set of variables that have been selected at least once
     var_step: the earlest step at which each variable in var_hist is selected.
     
     Returns
     updated var_hist and var_step
     """
     var_current = np.unique(group_index[np.where(np.abs(beta_current) > 1e-6)])
     var_new = np.setdiff1d(var_current,var_hist)
     if len(var_new) > 0:
          var_hist.extend(list(var_new))
          var_step.extend(list(num_iter * var_new))
     return var_hist,var_step
     
def predict_error_gaussian(X,y,beta_,intercept_):
     
     """
     Compute the prediction error of the path in linear model.
     
     Parameters
     ----------
     X: the design matrix, with shape (n_samples,n_features)
     y: true response variable, with shape (n_samples,)
     beta_: the path coefficients, with shape (n_features, n_knots)
     intercept_: the path intercept, with shape(n_knots,)
     
     Returns
     prediction error of the path
     """
     n_samples,n_features = X.shape
     if y.shape[0] != n_samples:
          raise ValueError('The row number design matrix and the label should be the same!')
     if beta_.shape[0] != n_features:
          raise ValueError('The row number of beta_ should be equal to the p (the number of features)!')
     if intercept_.shape[0] != beta_.shape[1]:
          raise ValueError('The number of knots in beta_ and intercept_ should be the same!')
     
     # estimate y     
     y_est_path = X.dot(beta_) + intercept_
     # y_est_path - y
     err_path = (y_est_path.T - y.T)
     
     return np.linalg.norm(err_path,ord=2,axis=1)

def predict_error_binomial(X,y,beta_,intercept_):
     
     """
     Compute the prediction error of the path in logit model.
     
     Parameters
     ----------
     X: the design matrix, with shape (n_samples,n_features)
     y: true response variable, with shape (n_samples,)
     beta_: the path coefficients, with shape (n_features, n_knots)
     intercept_: the path intercept, with shape(n_knots,)
     
     Returns
     prediction error of the path
     """
     n_samples,n_features = X.shape
     if y.shape[0] != n_samples:
          raise ValueError('The row number design matrix and the label should be the same!')
     if beta_.shape[0] != n_features:
          raise ValueError('The row number of beta_ should be equal to the p (the number of features)!')
     
     # compute probability
     xbeta_path = X.dot(beta_) + intercept_
     prob_path = sigmoid(xbeta_path)
     # estimat y
     y_est_path = (prob_path >= 0.5) * 1
     y_est_path[y_est_path == 0] = -1
     # y_est_path - y
     err_path = (y_est_path.T - y.T)
     
     if err_path.ndim == 1:
          err_path = err_path[np.newaxis,:]
     
     return np.sum(err_path!=0,axis=1)


class LBI():
     
     """
      Base class for Linearized Bregman Iteration.
     """

    
     def __init__(self,kappa=10,alpha=None,t0=None,t_ratio=100,t_num=500,t_seq=None,
                fit_intercept=False,normalize=False,copy_X=True,fast_init=False,
                group_index=None,verbose=True):
          
          """
           Initialization of the parameters.
          """
          try:
               self.kappa = float(kappa)
          except:
               raise ValueError('The dtype of kappa should be convertible to float')
          if self.kappa <= 0:
               raise ValueError('The Damping Factor kappa should be geater than 0!')
             
          self.alpha = alpha
          self.t0 = t0
          try:
               self.t_ratio = int(t_ratio)
               self.t_num = int(t_num)
          except:
               raise ValueError('The dtype of t_ratio and t_num should be convertible to int')
          if self.t_ratio <= 1 or self.t_num < 1:
               raise ValueError('The t_ratio (t_num) should be geater (or equal) than 1!')
          
          self.t_seq = t_seq
          
          try:
               self.fit_intercept = bool(fit_intercept)
               self.normalize = bool(normalize)
               self.copy_X = bool(copy_X)
               self.fast_init = bool(fast_init)
               self.verbose = bool(verbose)
          except:
               raise ValueError('The dtype of fit_intercept,normalize,copy_X,fast_init,auc and verbose should be convertible to bool!')
          self.group_index = group_index
          
          
     def initialize_paras(self,X,y,sample_weight):
          
          """
           Initialization of the parameters which don't provided, 
           i.e. step size, t_seq and group_index.
          """
          
          # Check the format of X and y
          X, y = check_X_y(X, y, accept_sparse=['csr', 'csc', 'coo'],
                           y_numeric=True, multi_output=True)
        
          # The sample_weight should be a vector
          if sample_weight is not None:
              try:
                   self.sample_weight = np.abs(np.array([float(sw) for sw in sample_weight]))
              except:
                   raise ValueError('The sample weight should be a 1D array and can be convertible to float!')
              if len(sample_weight) != X.shape[0]:
                   raise ValueError("The dimension of sample weight should be equal to the number of samples!")
              if np.max(sample_weight) == 0:
                   raise ValueError('At least one sample has the weight greater than 0!')
              else:
                   if np.isinf(np.max(sample_weight)):
                        inf_ind = np.isinf(sample_weight)
                        self.sample_weight = np.zeros((X.shape[0],))
                        self.sample_weight[inf_ind] = 1
                   else:
                        self.sample_weight = sample_weight / np.mean(sample_weight)
          else:
               self.sample_weight = np.ones((X.shape[0],))
               
          
          
          if self.t0 is not None:
               try:
                    self.t0 = float(self.t0)
               except:
                    raise ValueError('The dtype of t0 should be convertible to float!')
               if self.t0 < 0:
                    raise ValueError('The t0 should be geater than 0!')
          
          if self.t_seq is not None:
               try:
                    self.t_seq = np.array([float(t) for t in self.t_seq])
               except:
                    raise ValueError('The dtype of regularization parameter should be convertible to float!')
               if np.min(self.t_seq) < 0 or np.isinf(np.max(self.t_seq)):
                    raise ValueError('The vector of regularization parameters should be greater than 0 and less than inf!')
        
          if self.group_index is None:
             self.group_index = np.array(range(0,X.shape[1]))
          else:
             try:
                  self.group_index = np.asarray([float(gi) for gi in self.group_index])
             except:
                  raise ValueError('The group index should be a vector of number that the order of each one indicating the which group the corresponding variable belongs to!')
             if len(self.group_index) != X.shape[1]:
                  raise ValueError('The dimension of group_index must be equal to p (the number of features!')
             else:
                  index_sort = np.unique(np.sort(self.group_index))
                  self.group_index = np.array([np.where(index_sort==ind)[0][0] for ind in self.group_index])
         
          group_index_unique = np.unique(self.group_index)
          if len(group_index_unique) < len(self.group_index):
               self.group_ornot = True
          else:
               self.group_ornot = False
               
          
          
          
             
          
     def initialize_estimator(self,X,y):
          
          """
           The initialization of the beta,z in the regularization solution path.
           
          """
          
          (n_samples,n_features) = X.shape
          n_samples_y = len(y)
          if n_samples_y != n_samples:
               raise ValueError('The number of samples of X and y should be the same!')
          
          # Initialize the path 
          self.beta_ = np.zeros((n_features,self.t_num))
          self.intercept_ = np.zeros((self.t_num,))
          self.z_ = np.zeros((n_features,self.t_num))
          self.var_hist = []
          self.var_order = []
          
          
     def MLE_initialization(self,X,y,sample_weight):
          
          """
           The initialization of the beta,z in the regularization solution path.
           
          """
          mle_dict = {'gaussian':linear_mle_tmle,'binomial':logistic_mle_tmle}
          self.beta = np.zeros((X.shape[1],))
          self.z = np.zeros((X.shape[1],))
          self.intercept = 0
          
          if self.fast_init is True:
               intercept,d_beta,t_mle = mle_dict[self.family](X,y,self.group_index,sample_weight)
               self.t_mle = t_mle
               if self.t0 >= self.t_mle:
                    self.intercept = intercept
                    self.z = -self.t_mle * d_beta
                    self.t0 = t_mle
               else:
                    self.t0 = 0
                    warnings.warn('Not use MLE to initialize since it causes the t_seq to be incomplete!')  
          else:
               self.t0 = 0
               
               
     
     
     def ROC_AUC(self,ind_true,roc_plot=True):
          
          """ 
          Compute the AUC of the regularization solution path
          The ROC Curve is also plotted if roc_plot is True.
          
          """
          if self.group_ornot:
               n_features = len(np.unique(self.group_index))
          else:
               n_features = len(self.beta)
          try:
               ind_true = np.unique(np.asarray([int(it) for it in ind_true]))
               ind_true = np.reshape(ind_true,(ind_true.shape[0],))
          except:
               raise ValueError('The ind_true is the index of the true signal set, which should be int!')
          if len(ind_true) <= n_features:
               if np.max(ind_true) >= n_features or np.min(ind_true) < 0:
                    raise ValueError('The index should be >=0 and <= p (the number of features)!')
          else:
               raise ValueError('The number of true signal set should be less or equal than p!')
               
          # True label
          labels = np.zeros((n_features,1))
          labels[ind_true] = 1
          # Score which measures the order of selected variables
          scores = np.max(np.min(self.var_order) / np.max(self.var_order) - 0.01,0) * np.ones((n_features,))
          scores[self.var_hist] = np.sort(self.var_order)[::-1] / np.max(self.var_order)
          # Compute AUC
          fpr, tpr, thresholds = metrics.roc_curve(labels, scores, pos_label=1)
          AUC = metrics.auc(fpr, tpr)
    
          # Plot the ROC Curve
          if roc_plot is True:
               plt.figure()
               lw = 2
               plt.plot(fpr, tpr, color='red',
                        lw=lw, label='ROC curve (area = %0.5f)' % AUC)
               plt.plot([0, 1], [0, 1], color='black', lw=lw, linestyle='--')
               plt.xlim([-0.01, 1.0])
               plt.ylim([-0.01, 1.05])
               plt.xlabel('False Positive Rate')
               plt.ylabel('True Positive Rate')
               plt.title('Receiver Operating Characteristic')
               plt.legend(loc="lower right")
               plt.grid(True)
               plt.show()
          
          return AUC 
     
     def Solution_path(self,ind_true=None):
          """ 
          Plot the solution path
          
          """
          if ind_true is None:
               ind_true = []
          else:
               if self.group_ornot is True:
                    ind_true = [list(np.where(self.group_index == ind)[0]) for ind in ind_true]
                    ind_true = sum(ind_true,[])
          plt.figure()
          plt.rc('text', usetex=True)
          for i in range(self.beta_.shape[0]):
               if i in ind_true:
                    plt.plot(self.t_seq,self.beta_[i,:],'-')
               else:
                    plt.plot(self.t_seq,self.beta_[i,:],'--')
                    
          plt.xlim([-0.01, np.max(self.t_seq) * 1.01])
          plt.ylim([np.min(self.beta_) - 0.05 * np.abs(np.min(self.beta_)), np.max(self.beta_) + 0.05 * np.abs(np.max(self.beta_))])
          plt.xlabel('regularization parameter t')
          plt.ylabel(r'$\beta$')
          plt.grid(True)
          plt.title('Regularization Solution Path')
          plt.show()
          
     
          
     
     
     