"""
Linearized Bregman Iteration for Lasso problem

"""


import numpy as np
import time
from .base import _rescale_data, _preprocess_data,gradient_linear,gradient_linear_intercept, shrinkage,shrinkage_group,variable_path,linear_mle_tmle,LBI,compute_alpha

class LBI_Linear(LBI):
     """
     Linearized Bregman Iteration for l1 Problem in linear model.
     
     """

    
     def __init__(self,kappa=10,alpha=None,t0=None,t_ratio=100,t_num=500,t_seq=None,
                fit_intercept=False,normalize=False,copy_X=True,fast_init=False,
                group_index=None,verbose=True):
          
          """
           Initialization of hyper-parameters.
          """
          
          super().__init__(kappa,alpha,t0,t_ratio,t_num,t_seq,fit_intercept,
                       normalize,copy_X,fast_init,group_index,verbose)
          self.family = 'gaussian'
          
          
          
     def initialize_paras(self,X,y,sample_weight=None):
          
        """
         Initialization of t_seq.
         The estimation of t0 and beta with fast initialization.
         
        """
        
        super().initialize_paras(X,y,sample_weight)
        
        
        # Preprocessing data  
        X = _preprocess_data(X,self.normalize,self.copy_X) 
        # Sample weight can be implemented via a simple rescaling.
        X, y = _rescale_data(X, y, self.sample_weight)
        
        if self.alpha is None:
             self.alpha = compute_alpha(X,self.kappa)
        else:
             try:
                  self.alpha = float(self.alpha)
             except:
                  raise ValueError('The dtype of alpha should be convertible to float')
             if self.alpha <= 0:
                  raise ValueError('The step size alpha should be geater than 0!')
        
        if self.t_seq is None:
            if self.t0 is None:
                 intercept,d_beta,t_mle = linear_mle_tmle(X,y,self.group_index)
                 self.t_mle = t_mle
                 self.t0 = t_mle
                 self.t_max = self.t0 * self.t_ratio
                 self.t_seq = np.logspace(np.log(self.t0),np.log(self.t_max),self.t_num,base=np.e) 
                 
            else:
                 self.t_max = self.t0 * self.t_ratio
                 self.t_seq = np.logspace(np.log(self.t0),np.log(self.t_max),self.t_num,base=np.e) 
                 
                                
        else:
             self.t_seq = np.sort(self.t_seq)
             self.t_max = np.max(self.t_seq)
             self.t0 = np.min(self.t_seq)
             self.t_num = len(self.t_seq)
             
             
        self.MLE_initialization(X,y,self.sample_weight)
             
             
          
     
     def fit(self, X, y, sample_weight=None):
          
        """
        Return regularization solution path of LBI.
        Parameters
        ----------
        X : numpy array or sparse matrix of shape [n_samples,n_features]
            Training data
        y : numpy array of shape [n_samples, n_targets]
            Target values. Will be cast to X's dtype if necessary
        sample_weight : numpy array of shape [n_samples]
            Individual weights for each sample
            .. versionadded:: 0.19
               parameter *sample_weight* support to LinearRegression.
        Returns
        -------
        self : returns an instance of self.
        """
        
        
        # Hyper-Parameter Setting
        self.initialize_paras(X,y,sample_weight)
        # Initialization 
        self.initialize_estimator(X,y)
        
        # Setting the number of iteration and the time point we save
        rec_cur = 0
        steps_remain = np.int(np.ceil( (self.t_max - self.t0) / self.alpha ))
        print('The number of whole iteration: %d \n' %(steps_remain))
        if self.verbose:
             print('Linearized Bregman Iteration: %s' %self.family)
             
        # Start Iteration
        start_time = time.time()
        for step in range(0,steps_remain):
             if rec_cur >= self.t_num:
                  break
             # Update intercept
             if self.fit_intercept:
                  partial_intercept = gradient_linear_intercept(X,y,self.beta,self.intercept)
                  self.intercept -= self.kappa * self.alpha * partial_intercept
             partial_beta = gradient_linear(X,y,self.beta,self.intercept)
             # Update z
             self.z -= self.alpha * partial_beta
             # Update beta
             if self.group_ornot is True:
                  self.beta = self.kappa * shrinkage_group(self.z,self.group_index)
             else:
                  self.beta = self.kappa * shrinkage(self.z)
             # Update var_hist and var_order
             self.var_hist,self.var_order = variable_path(self.beta,self.var_hist,self.var_order,rec_cur,self.group_index)
             
             # Save 
             while True:
                  dt = (step+1) * self.alpha + self.t0 - self.t_seq[rec_cur] 
                  if dt < 0:
                       break
                  # Save intercept
                  if self.fit_intercept:
                       self.intercept_[rec_cur] = self.intercept + self.kappa * self.alpha * partial_intercept
                  # Save z
                  self.z_[:,rec_cur] = self.z + self.alpha * partial_beta
                  # Save beta
                  if self.group_ornot is True:
                       self.beta_[:,rec_cur] = self.kappa * shrinkage_group(self.z_[:,rec_cur],self.group_index)
                  else:
                       self.beta_[:,rec_cur] = self.kappa * shrinkage(self.z_[:,rec_cur])
                       
                  # Update the index in t_seq
                  rec_cur += 1
                  if rec_cur >= self.t_num:
                       break
             if self.verbose and (step + 1) in np.ceil([steps_remain / x for x in [100,50,20,10,5,2,1]]):
                  print('Process: %0.0f%%. Time: %f' % ((step+1) / steps_remain * 100, time.time() - start_time))
    
     def ROC_AUC(self,ind_true,roc_plot=True):
          return super().ROC_AUC(ind_true,roc_plot)
     
     def Solution_path(self,ind_true=None):
          super().Solution_path(ind_true)
    
         
                       
                       
                       
             
             
             
             
        
            
     
     
     
     
     
     
          
