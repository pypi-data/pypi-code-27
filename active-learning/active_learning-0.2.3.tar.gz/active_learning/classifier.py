import numpy as np
from collections import OrderedDict
import pdb
# import numpy as npg
import autograd
import autograd.numpy as npg
from autograd import grad
from scipy.optimize import minimize, OptimizeResult


class classifier(object):


    def __init__(self, num_cov=2, num_feat=3, num_clusters=2, interaction_terms=False):

        self.num_cov = num_cov
        self.num_feat = num_feat
        self.keep_prob = 1
        self.rule_directions = None
        self.scaling = None

        self.num_clusters = num_clusters
        # interaction_terms = {'cov':[[set1_indices], [set2 indices]], 'features':[[set1_indices], [set2 indices]]}
        self.interaction_terms = interaction_terms

        self.params = OrderedDict()
        self.params['alpha'] = {'shape':[self.num_feat, self.num_clusters],
                                'param':0.001*np.random.uniform(-1, 1, [self.num_feat, self.num_clusters])}
        self.params['alpha0'] = {'shape':[1, self.num_clusters],
                                'param':0.001*np.random.uniform(-1, 1, [1, self.num_clusters])}
        if self.interaction_terms and 'features' in self.interaction_terms:
            shape = len(self.interaction_terms['features'][0])
            self.params['alpha_interaction'] = {'shape':[shape, self.num_clusters],
                                                'param':0.001*np.random.uniform(-1, 1, [shape, self.num_clusters])}

        self.params['omega'] = {'shape':[self.num_cov, self.num_clusters],
                                'param':0.001*np.random.uniform(-1,1, [self.num_cov, self.num_clusters])}
        if self.interaction_terms and 'cov' in self.interaction_terms:
            shape = len(self.interaction_terms['cov'][0])
            self.params['omega_interaction'] = {'shape':[shape, self.num_clusters],
                                                'param':0.001*np.random.uniform(-1,1, [shape, self.num_clusters])}

        self.params['omega0'] = {'shape':[1, self.num_clusters],
                                 'param':0.00*np.random.randn(1, self.num_clusters)}

        # process params
        cnt = 0
        for param, param_dict in self.params.items():
            param_dict['size'] = np.prod(param_dict['shape'])
            param_dict['indices'] = np.arange(cnt, cnt+param_dict['size'])
            cnt += param_dict['size']

        self.num_params = np.sum([v['size'] for k,v in self.params.items()])

    def predict_proba(self, X):
        gamma = np.ones((len(X),1))
        proba, _ =  self.predict(gamma,X,per_cluster_prob=False)
        if isinstance(proba,autograd.numpy.numpy_boxes.ArrayBox):
            proba = proba._value
        pred_proba = np.concatenate([1-proba[:,None],proba[:,None]],1)
        return pred_proba
        
    def predict(self, gamma, X, per_cluster_prob=False):
        """
        gamma: [N, num_cov], X: [N, num_feat]
        """
        if self.keep_prob == 1:

            temp_pi = npg.dot(gamma, self.params['omega']['param']) # [N,C], [C,M] -> [N,M]

            if self.interaction_terms and 'cov' in self.interaction_terms:
                # R, C = npg.triu_indices(self.num_cov)
                R, C = self.interaction_terms['cov']
                interaction_covs = gamma[:,R] * gamma[:,C]
                temp_pi = temp_pi + npg.dot(interaction_covs, self.params['omega_interaction']['param'])

        else: # dropout
            # This is not quite right -- it zeros out the same feature across all clusters for every sample.
            # The alternative (zeroing out *different* features in each cluster is very expensive --can't use dot)
            dropout_g = npg.random.binomial([npg.ones_like(gamma)], self.keep_prob)[0] / self.keep_prob
            temp_pi = npg.dot(gamma * dropout_g, self.params['omega']['param'])

            if self.interaction_terms and 'cov' in self.interaction_terms:
                # R, C = npg.triu_indices(self.num_cov)
                R, C = self.interaction_terms['cov']
                interaction_covs = gamma[:,R] * gamma[:,C]
                dropout_covs = npg.random.binomial([npg.ones_like(interaction_covs)], self.keep_prob)[0] / self.keep_prob
                temp_pi = temp_pi + npg.dot(interaction_covs * dropout_covs, self.params['omega_interaction']['param'])

        if 'omega0' in self.params.keys():
            temp_pi = temp_pi + self.params['omega0']['param'] # [N,M]

        temp_pi = temp_pi - npg.max(temp_pi, 1, keepdims=True)

        pi = npg.exp(temp_pi)
        pi = pi / npg.sum(pi, 1, keepdims=True) # [N,M]

        if self.keep_prob == 1:

            temp_pred = npg.dot(X, self.params['alpha']['param']) # [N,F], [F,M] -> [N,M]

            if self.interaction_terms and 'features' in self.interaction_terms:
                # R, C = npg.triu_indices(self.num_cov)
                R, C = self.interaction_terms['features']
                interaction_feats = X[:,R] * X[:,C]
                temp_pred = temp_pred + npg.dot(interaction_feats, self.params['alpha_interaction']['param'])

        else: # dropout
            dropout_x = npg.random.binomial([npg.ones_like(X)], self.keep_prob)[0] / self.keep_prob
            temp_pred = npg.dot(X * dropout_x, self.params['alpha']['param']) + \
                                               self.params['alpha0']['param'] # [N,F], [F,M] -> [N,M]
            dropout_x = npg.random.binomial([npg.ones_like(X)], self.keep_prob)[0] / self.keep_prob
            temp_pred = temp_pred + npg.dot(X * dropout_x, 0*self.params['alpha']['param'])

            if self.interaction_terms and 'features' in self.interaction_terms:
                # R, C = npg.triu_indices(self.num_cov)
                R, C = self.interaction_terms['features']
                interaction_feats = X[:,R] * X[:,C]
                dropout_xx = npg.random.binomial([npg.ones_like(interaction_feats)], self.keep_prob)[0] / self.keep_prob
                temp_pred = temp_pred + npg.dot(interaction_feats * dropout_xx,
                                                self.params['alpha_interaction']['param'])

            if False: #self.num_absdelta_feat > 0:
                dropout_ix = npg.random.binomial([npg.ones_like(X_absdelta)], self.keep_prob)[0] / self.keep_prob
                temp_pred = temp_pred + npg.dot(npg.fabs(X_absdelta - self.params['c']['param']) * dropout_ix,
                                                self.params['alpha_c']['param'])

        pred = npg.where(temp_pred > 0, 1.0 / ( 1.0 + npg.exp(-temp_pred) ),
                                        npg.exp(temp_pred) / ( 1.0 + npg.exp(temp_pred)))

        if per_cluster_prob:
            return pred, pi
        else:
            return npg.sum(pi * pred, 1), pi

    def predict_memory_efficient(self, gamma, X, X_absdelta=None, chunk_size=10000, per_cluster_prob=False):

        if True:# self.interaction_terms:
            num_chunks = gamma.shape[0]/chunk_size
            inds = np.ceil(np.linspace(0, gamma.shape[0]+1, num_chunks)).astype(int)
            val_pred = np.zeros(gamma.shape[0])
            if num_chunks == 1:
                val_pred, _ = self.predict(gamma, X, X_absdelta)
            else:
                for ind_cnt, ind_end in enumerate(inds[1:]):
                    x_delta = None if X_absdelta is None else X_absdelta[inds[ind_cnt-1]:ind_end]
                    val_pred[inds[ind_cnt-1]:ind_end], _ = self.predict(gamma[inds[ind_cnt-1]:ind_end],
                                                                        X[inds[ind_cnt-1]:ind_end],
                                                                        X_absdelta=x_delta)
        else:
            val_pred, _ = self.predict(gamma, X, X_absdelta)

        return val_pred

    def compute_lkh(self, gamma, X, Y, batch_sample_weights=None):

        pred, _ = self.predict(gamma, X)

        if batch_sample_weights is None:
            Qi = npg.log(Y*pred + (1-Y)*(1-pred))
        else:
            Qi = npg.log(Y*pred + (1-Y)*(1-pred)) * batch_sample_weights

        lkh = npg.sum(Qi)

        return lkh

    def _flatten(self):

        x = npg.zeros(self.num_params)

        for param, param_dict in self.params.items():
            indices = param_dict['indices']
            try:
                transform = param_dict['transform']
            except KeyError:
                transform = None

            if transform == 'exp':
                x[indices] = npg.log(param_dict['param'].flatten())
            else:
                x[indices] = param_dict['param'].flatten()

        return x

    def _to_param(self, x):

        cnt = 0
        for param, param_dict in self.params.items():
            indices = param_dict['indices']
            try:
                transform = param_dict['transform']
            except KeyError:
                transform = None

            if transform == 'exp':
                param_dict['param'] = npg.exp(x[indices].reshape(param_dict['shape']))
            else:
                param_dict['param'] = x[indices].reshape(param_dict['shape'])

            cnt += param_dict['size']

    def obj_func(self, theta, gamma, X, Y, ind,batch_sample_weights=None):

        self._to_param(theta)
        log_loss  = self.compute_lkh(gamma, X, Y, batch_sample_weights=batch_sample_weights)
        if self.scaling is None:
            return log_loss
        else:
            return self.rule_loss(gamma,X,ind) + log_loss
    
    def rule_loss(self,gamma,X,ind):
        pred, _ = self.predict(gamma, X)
        y_minus_fx_sq = (pred[:,None]-self.rule_directions[None])**2
        tot_err = y_minus_fx_sq*self.scaling[ind]
        rule_loss = tot_err.mean().mean()
        
        return rule_loss
    
    def add_features(self,rule_directions,scaling):
            self.rule_directions = rule_directions
            self.scaling = scaling


    def _optimize_not_full_batch(self, gamma, X, Y, sample_weights=None, theta0=None, batch_size=-1, max_iters=1000, opt_method='bfgs', final_bfgs=True, ratio=-1):

        gradients = grad(self.obj_func)

        if theta0 is None:
            theta0 = self._flatten()

        if sample_weights is None:
            sample_weights = np.ones(X.shape[0])

        self.sgd_adjustment_factor = 1.0
        if opt_method == 'bfgs':
            options = dict(disp=True, maxiter=max_iters, ftol=1e-5, gtol=1e-5, maxcor=6, maxls=100)
            result = minimize(fun=self.obj_func, x0=theta0, method='L-BFGS-b', jac=gradients,
                           options=options, args=(gamma, X, Y, X_absdelta, ))
        else:
            if opt_method == 'adam':
                grad_accum = np.zeros(theta0.shape) + 1e-8
                grad_accum2 = np.zeros(theta0.shape) + 1e-8
                lr = 0.001
                beta1 = 0.5
                beta2 = 0.999
            else:
                grad_accum = np.zeros(theta0.shape) + 1e-6
                lr = 0.001

            theta = theta0.copy()
            loss = np.zeros(max_iters)
            track_theta = np.zeros((len(theta), max_iters))

            neg_ind = np.where(Y[:]==0)[0]
            pos_ind = np.where(Y[:]>0)[0]
            for i in range(max_iters):
                print(i)

                if batch_size == -1:
                    ind = np.arange(X.shape[0])
                else:
                    self.sgd_adjustment_factor = 1.0/float(X.shape[0])
                    if ratio == -1:
                        ind = np.random.choice(X.shape[0], batch_size, replace=True)
                    else:
                        num_pos_in_batch = int(max(1, ratio*batch_size))
                        pos_in_batch = np.random.choice(pos_ind, num_pos_in_batch)
                        neg_in_batch = np.random.choice(neg_ind, batch_size - num_pos_in_batch)
                        ind = np.union1d(pos_in_batch, neg_in_batch)

                batch_sample_weights = sample_weights[ind]
                batch_sample_weights *= len(ind) / np.sum(batch_sample_weights)

                jac = gradients(theta, gamma[ind], X[ind], Y[ind], ind,batch_sample_weights)
                loss[i] = self.obj_func(theta, gamma[ind], X[ind], Y[ind], ind,
                                        batch_sample_weights=batch_sample_weights)

                jac = np.where(np.isfinite(jac), jac, 0)

                if opt_method == 'adam':
                    grad_accum = beta1 * grad_accum + (1 - beta1) * jac
                    grad_accum2 = beta2 * grad_accum2 + (1 - beta2) * jac**2
                    m_hat = grad_accum/(1-beta1**(i+1))
                    v_hat = grad_accum2/(1-beta2**(i+1))
                    theta = theta - lr * m_hat / (np.sqrt(v_hat) + 1e-10)
                else:
                    grad_accum += jac ** 2
                    theta = theta - lr * jac / np.sqrt(grad_accum)

                track_theta[:,i] = theta
                if i > 2000:
                    if np.fabs((loss[i] - loss[i-1])/loss[i-1]) < 1e-5:
                        break

            result = {'loss':loss, 'x':theta, 'track_theta':track_theta[:i]}
            if final_bfgs:
                self.sgd_adjustment_factor = 1.0
                options = dict(disp=True, maxiter=max_iters, ftol=1e-5, gtol=1e-5, maxcor=6, maxls=100)
                result = minimize(fun=self.obj_func, x0=result['x'], method='L-BFGS-b', jac=gradients,
                               options=options, args=(gamma, X, Y, ))

        return result

    def _optimize_full_batch(self, gamma, X, Y, sample_weights=None, theta0=None, batch_size=-1, num_epochs=1000, opt_method='bfgs', final_bfgs=True, dropout_prob=0):
        """
        max_iters = num_epochs
        """

        gradients = grad(self.obj_func)

        self.keep_prob = 1.0 - dropout_prob ## will set to 1 at the end of training to make sure testing is correct.

        if theta0 is None:
            theta0 = self._flatten()

        if sample_weights is None:
            sample_weights = np.ones(X.shape[0])

        self.sgd_adjustment_factor = 1.0
        if opt_method == 'bfgs':
            options = dict(disp=True, maxiter=num_epochs, ftol=1e-5, gtol=1e-5, maxcor=6, maxls=100)
            result = minimize(fun=self.obj_func, x0=theta0, method='L-BFGS-b', jac=gradients,
                           options=options, args=(gamma, X, Y, ))
        else:
            self.sgd_adjustment_factor = 1.0/float(X.shape[0])
            if opt_method == 'adam':
                grad_accum = np.zeros(theta0.shape) + 1e-8
                grad_accum2 = np.zeros(theta0.shape) + 1e-8
                lr = 0.001
                beta1 = 0.5
                beta2 = 0.999
            elif opt_method == 'rmsprop':
                grad_accum2 = np.zeros(theta0.shape) #+ 1e-8
                lr = 0.0001
                beta = 0.99
            else:
                grad_accum = np.zeros(theta0.shape) + 1e-6
                lr = 0.001

            ## L1 update rules
            u_vec = np.zeros(theta0.shape)
            q_vec = np.zeros(theta0.shape)

            ##
            theta = theta0.copy()

            max_iters = int(np.ceil(X.shape[0]/float(batch_size)))*num_epochs

            loss = np.zeros(num_epochs)
            track_theta = np.zeros((num_epochs, theta.shape[0]))

            iteration = 0
            for iteration in range(num_epochs):
                print('On epoch: {}'.format(iteration + 1))

                # print ("iteration: %d" %iteration)
                perm_inds = np.random.permutation(X.shape[0])
                ## repeat a few samples to fix batch size
                extra_needed = batch_size - X.shape[0] % batch_size
                inds = np.arange(X.shape[0]).tolist()
                if extra_needed > 0:
                    extra_sampled = np.random.choice(X.shape[0], extra_needed, replace=False).tolist()
                    inds.extend(extra_sampled)

                inds = np.random.permutation(inds)

                num_batches = int(len(inds)/batch_size)

                cnt = 0
                for b in range(num_batches):

                    ind = inds[cnt:cnt+batch_size]
                    cnt += batch_size

                    batch_sample_weights = sample_weights[ind]
                    batch_sample_weights *= len(ind) / np.sum(batch_sample_weights)

                    jac = gradients(theta, gamma[ind], X[ind], Y[ind], ind,batch_sample_weights)
                    loss[iteration] = self.obj_func(theta, gamma[ind], X[ind], Y[ind], ind,
                                                    batch_sample_weights=batch_sample_weights)

                    jac = np.where(np.isfinite(jac), jac, 0) #/ batch_size

                    if opt_method == 'adam':
                        grad_accum = beta1 * grad_accum + (1 - beta1) * jac
                        grad_accum2 = beta2 * grad_accum2 + (1 - beta2) * jac**2
                        m_hat = grad_accum/(1-beta1**(i+1))
                        v_hat = grad_accum2/(1-beta2**(i+1))
                        effective_lr = lr / (np.sqrt(v_hat) + 1e-10)
                        sub_theta = theta + effective_lr * m_hat
                    elif opt_method == 'rmsprop':
                        grad_accum2 = beta * grad_accum2 + (1 - beta) * jac**2
                        effective_lr = lr / (np.sqrt(grad_accum2) + 1e-10)
                        sub_theta = theta + jac * effective_lr
                    else:
                        grad_accum += jac ** 2
                        effective_lr = lr / np.sqrt(grad_accum)
                        sub_theta = theta + jac * effective_lr

                    theta = np.where(np.isfinite(sub_theta), sub_theta, 0)

                track_theta[iteration,:] = theta

            result = {'loss':loss, 'x':theta, 'track_theta':track_theta[:iteration+1]}
            if final_bfgs:
                self.sgd_adjustment_factor = 1.0
                options = dict(disp=True, maxiter=num_epochs, ftol=1e-5, gtol=1e-5, maxcor=6, maxls=100)
                result = minimize(fun=self.obj_func, x0=result['x'], method='L-BFGS-b', jac=gradients,
                               options=options, args=(gamma, X, Y, ))

        self.keep_prob = 1.0

        return result

    def optimize(self, gamma, X, Y, sample_weights=None, theta0=None, batch_size=-1, max_iters=1000, opt_method='bfgs', final_bfgs=True, ratio=-1, full_batch=False, dropout_prob=0):

        if full_batch:
            return self._optimize_full_batch(gamma, X, Y, sample_weights=sample_weights, theta0=theta0, batch_size=batch_size, num_epochs=max_iters, opt_method=opt_method, final_bfgs=False, dropout_prob=dropout_prob)
        else:
            return self._optimize_not_full_batch(gamma, X, Y, sample_weights=sample_weights, theta0=theta0, batch_size=batch_size, max_iters=max_iters, opt_method=opt_method, final_bfgs=final_bfgs, ratio=ratio)


def log_sum(log_a, log_b):

    return np.where(log_a < log_b, log_b + np.log(1.0 + np.exp(log_a - log_b)),
                                   log_a + np.log(1.0 + np.exp(log_b - log_a)))