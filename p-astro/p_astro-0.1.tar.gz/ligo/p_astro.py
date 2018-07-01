"""Module containing the computation of p_astro by source category
"""
import itertools
from copy import deepcopy

import numpy as np
from scipy.special import la_roots
from numpy.polynomial.hermite import hermgauss


class CountPosteriorElements(object):
    '''
    Class that collects information of the candidate events on
    which the FGMC counts posterior is to be built. This information
    is not specific to a source type.
    '''

    def __init__(self, f_divby_b, buff=1e-15, verbose=True):
        '''
        Parameters
        ----------
        f_divby_b : list, tuple
            iterable of real numbers, foreground to background ratio
        buff : float
            Surrogate for zero, to avoid singularities in the
            counts posterior. Default value 1e-15
        verbose : bool
        '''
        self.f_divby_b = f_divby_b
        self.buffer = buff
        self.verbose = verbose


class SourceType(object):
    '''
    Class that collects source-type specific information of
    candidate events. Instances of this class will be passed
    to the :class:`Posterior` class to instantiate the latter.
    '''

    def __init__(self, label, w_fgmc):
        '''
        Parameters
        ----------

        label : str
            label associated with a class instance, like, "BNS", "bns", "BBH"
        w_fgmc : float
            In the **course-grained method**, `w_fgmc` is defined as
            p(SVD bin #|source-type), derived from the distribution of
            recovered parameters across SVD bins during an injection
            campaign targeted at a source-type. In the **fine-grained method**,
            `w_fgmc` is defined as p(template|source-type).
        '''
        self.label = label
        self.w_fgmc = w_fgmc


class Posterior(CountPosteriorElements):
    '''
    Class that constructs the **FGMC** counts posterior.

    Attributes
    ----------
    args_fixed : list
        list of object instances whose labels match
        keys of ``fix_sources`` dictionary.
    args_free : list
        list of object instances whose labels do not
        match the keys of fix_sources dictionary.
    arg_terr : :class:`SourceType`
        pertaining to the terrestrial source
    args_astro : tuple
        instances of :class:`SourceType` that correspond to
        astrophysical categories.
    keys_all : list
        list of labels of instances of all :class:`SourceType` instances.
    key_terr : list
        subset of ``key_all`` with terrestrial source type
    keys_astro : list
        subset of ``key_all`` with astrophysical source type
    keys_fixed : list
        list of labels of pinned :class:`SourceType` instances.
    keys_free : list
        list of labels of free :class:`SourceType` instances.
    n : int
        number of terms in the `gauss-laguerre` and `gauss-hermite`
        quadrature integrals, hard coded to 20.
    N : int
        number of candidate events
    roots : iter
        abcissa of `gauss-laguerre` quadrature
    weights : iter
        weights of `gauss-laguerre` quadrature
    hroots : iter
        abcissa of `gauss-hermite` quadrature
    hweights : iter
        weights of `gauss-hermite` quadrature
    reg_const : float
        regularization constant to avoid numerical over/under flows
    norm : float
        normalization constant for counts posterior, determined
        post regularization
    terr_jacobian : float
        constant to be tacked on when integrating terrestrial counts via
        `gauss-hermite` quadrature
        This can only be done after variable transformation.
    priorDict : dict
        dictionary of priors keyed on *Uniform* and *Jeffreys*
    '''
    def __init__(self, f_divby_b, prior_type, terr_source,
                 fix_sources={},
                 buff=1e-15,
                 mcmc=False,
                 verbose=True,
                 **astro_sources):
        '''
        Parameters
        ----------
        f_divby_b : list, tuple
            iterable of real numbers, foreground to background ratio
        prior_type : str
            **Uniform** or **Jeffreys**
        terr_source : :class:`SourceType`
            pertaining to the terrestrial source
        fix_sources : dict
            fixed lambda values, keyed on source labels.

            Example: :code:`{"Terr":value}`
            Note that the keys *must* match the labels
            used for :class:`SourceType` instances.
        buff : float
            Surrogate for zero, to avoid singularities in the
            counts posterior.
        verbose : bool
        astro_sources : dict
            dictionary of :class`:SourceType, pertaining to
            astrophysical sources
        '''

        CountPosteriorElements.__init__(self, f_divby_b, buff, verbose)

        assert (astro_sources != {}), \
            "Need at least one astrophysical source."
        assert (terr_source != {}), "Terrestrial source required."

        self.args_astro = astro_sources.values()
        self.arg_terr = terr_source
        self.args_all = list(self.args_astro) + [self.arg_terr]
        self.keys_all = [arg.label for arg in self.args_all]
        self.key_terr = self.arg_terr.label
        self.keys_astro = [arg.label for arg in self.args_astro]
        self.fix_sources = fix_sources
        self.keys_fixed = self.fix_sources.keys()
        self.mcmc = mcmc

        assert (
            len(self.f_divby_b) ==
            int(np.sum([len(arg.w_fgmc) for arg in self.args_all]) /
                len(self.args_all))), \
            "Lengths of f_divby_b vector, and w_fgmc vectors, must match"
        assert (self.key_terr not in self.keys_astro), \
            ("Terrestrial SourceType must be input separately, "
             "via terr_source field")
        if self.fix_sources != {}:
            assert (
                len(set(self.keys_all) & set(self.keys_fixed)) ==
                len(self.keys_fixed)), \
                ("Label(s) of fix_sources don't match labels of "
                 "astro/terr source instances")

        self.args_fixed = \
            [list(filter(lambda x: x.label == label, self.args_all))[0] for
             label in self.keys_fixed]

        self.args_free = list(set(self.args_all)-set(self.args_fixed))
        self.keys_free = [arg.label for arg in self.args_free]
        self.prior_type = prior_type
        self.n = 20
        self.N = len(list(self.args_astro)[0].w_fgmc)
        self.terr_jacobian = np.sqrt(2*self.N)

        if self.prior_type == "Uniform":
            self.roots, self.weights = la_roots(n=self.n, alpha=0)
        if self.prior_type == "Jeffreys":
            self.roots, self.weights = la_roots(n=self.n, alpha=-0.5)
        self.hroots, self.hweights = hermgauss(deg=self.n)

        if not self.mcmc:
            self.norm_array = self.regularize()
            self.reg_const = np.max(self.norm_array)
            self.norm = self.normalize()

        self.priorDict = {}
        self.priorDict["Uniform"] = Posterior.priorUniform
        self.priorDict["Jeffreys"] = Posterior.priorJeffreys

        if self.verbose:
            print("Posterior class instantiation complete.")

    def reduced_log_likelihood_terr(self, **lambdas):
        '''
        The log of the FGMC posterior divided by
        (np.exp(-np.sum(lambdas))*lambda_terr**N)
        Takes the lambdas as input variables. One of the lambdas
        *must* be ``lambda_terr``.
        Also, the keys on lambdas *must* match the labels of the
        :class:`SourceType` instances.

        Evaluating the reduced posterior at ``lambda_bns = 5``
        will need to be passed as BNS=5, if "BNS" is the label of
        the corresponding instance of SourceType.
        Returns the value of the reduced log posterior for a
        set of lambda values.
        '''
        return np.sum(np.log(self.arg_terr.w_fgmc +
                      np.outer(1/lambdas[self.key_terr], self.f_divby_b) *
                      np.sum([np.outer(lambdas[arg.label], arg.w_fgmc)
                             for arg in self.args_astro], axis=0)), axis=1)

    def reduced_log_likelihood_astro(self, **lambdas):
        '''
        The log of the FGMC posterior divided by
        (np.exp(-np.sum(lambdas))*((N**N)*exp(-N)))
        Takes the lambdas as input variables. One of the
        lambdas *must* be ``lambda_terr``.
        Also, the keys on lambdas *must* match the labels of
        the :class:`SourceType` instances.
        So, evaluating the reduced posterior at ``lambda_bns = 5``
        will need to be passed as BNS=5, if "BNS" is the label of
        the corresponding instance of SourceType. Returns
        the value of the reduced log posterior for a set of lambda values.
        '''
        return (self.reduced_log_likelihood_terr(**lambdas) +
                self.N*np.log(lambdas[self.key_terr]) -
                self.N*(np.log(self.N) - 1))

    def TerrVarTransform(self, x, shift_amount="Default"):  # noqa: N802
        '''
        Variable transformation for lambda_terr. Used when
        marginalizing over ``lambda_terr`` via Gauss-Hermite quadrature.

        Parameters
        ----------
        x : float
            Variable to be transformed
        shift_amount : float
            If shift amount is ``a``, function will transform
            a Gaussian with ``mu=a``, ``sigma=np.sqrt(a)``
            to a Gaussian that goes like ``exp(-x**2)``

        Returns
        -------
        float
            transformed variable
        '''
        if shift_amount == "Default":
            return x*np.sqrt(2*self.N)+self.N
        else:
            return x*np.sqrt(2*shift_amount)+shift_amount

    def marginalize_gq(self, func, categories,
                       shift_amount="Default", **pinned_lambdas):
        '''
        Function to marginalize posterior on counts using Gaussian quadrature
        Gauss-Laguerre for marginalization over astrophysical counts
        Gauss-Hermite for marginalization over terrestrial counts

        Notes
        -----
            Astrophyical Counts Marginalization (Gauss-Laguerre Quadrature):

                :math:`f(x) = P(x)e^{-x}`
                
                :math:`\int_{0}^{\infty}f(x)dx = \sum_{i=1}^{n}w_iP(r_i)
                = \sum_{i=1}^{n}e^{\log(w_i)+\log(P(r_i))}`

            where :math:`w_i, r_i` are the Gauss-Laguerre weights and abscissa.

            Terrestrial Counts Marginalization (Gauss-Hermite):

                :math:`f(x) = P(x)e^{-x^2}`
            
                :math:`\int_{-\infty}^{+\infty}f(x)dx = \sum_{i=1}^{n}w_iP(r_i)
                = \sum_{i=1}^{n}e^{\log(w_i)+\log(P(r_i))}`

            where :math:`w_i, r_i` are the Gauss-Hermite weights and abscissa.

        Parameters
        ----------

        func : callable
            log of function to be marginalized divided by the Gauss-Laguerre
            weighting factor.
        categories : list
            list of source types to be marginalized over. Strings *must*
            match labels of instances of SourceType.
        shift_amount : float
            same as shift amount in :meth:`TerrVarTransform`,
            used for marginalizing over lambda_terr
        pinned_lambdas : dict
            values of lambdas that are not to be marginalized over.
            keys *must* match labels of instances of SourceType class.

        Returns
        -------

        list
            list of values, which when exponentiated and summed,
            give the value of the marginalized posterior.
        '''

        thelist = []  # Initialize list
        lambdas = deepcopy(pinned_lambdas)  # Set dictionary to pinned_lambdas

        # Iterate over range of quadrature roots & weights terms, for every
        # category to be marginalized over
        for idx in itertools.product(range(self.n), repeat=len(categories)):
            sum_log_weights = 0  # initialize log of quadrature weights
            for key, root, weight, hroot, hweight in zip(
                    categories,
                    self.roots[list(idx)],
                    self.weights[list(idx)],
                    self.hroots[list(idx)],
                    self.hweights[list(idx)]):
                # Use Gauss-Hermite quadrature to integrate terrestrial counts
                if key == self.key_terr:
                    lambdas[key] = self.TerrVarTransform(hroot, shift_amount)
                    sum_log_weights += np.log(hweight)
                # Gauss-Laguerre quadrature to integrate astrophysical counts
                else:
                    lambdas[key] = root
                    sum_log_weights += np.log(weight)
            # exponentiate and sum to give the marginalization value
            thelist.append(func(**lambdas)+sum_log_weights)

        if self.key_terr in categories:
            return np.array(thelist)+np.log(self.terr_jacobian)
        else:
            return np.array(thelist)

    def regularize(self):
        '''
        Function to regularize FGMC posterior to avoid numerical
        over-/under-flows.
        It simply invokes marginalize_gq and applies it on the reduced
        log posterior. The regularization constant is simply the max value
        of the array returned by this function.
        '''
        if self.verbose:
            print("Regularizing FGMC posterior to avoid ",
                  "numerical over-/under-flows ...")
        if self.key_terr in self.keys_free:
            return self.marginalize_gq(
                self.reduced_log_likelihood_terr,
                self.keys_free,
                **self.fix_sources)
        else:
            return self.marginalize_gq(
                self.reduced_log_likelihood_astro,
                self.keys_free,
                **self.fix_sources)

    def normalize(self):
        '''
        Function to normalize FGMC posterior.
        This is simply the sum of the array (exponentiated)
        returned by the regularize function,
        with the regularization constant removed.
        '''
        if self.verbose:
            print("Normalizing FGMC posterior ...")
        return np.sum(np.exp(self.norm_array-self.reg_const))

    def poissonLogWeight(self, **lambdas):  # noqa: N802
        '''
        Function that returns the log of the Poisson weights: log(e^(-x)) = -x

        Parameters
        ----------
        lambdas : dict
            dictionary of counts and their values

        Returns
        -------
        float
            log of the Poisson weights
        '''
        return np.sum(-np.array(lambdas.values()), axis=0)

    def gaussianLogWeight(self, terr_count):  # noqa: N802
        '''
        Function that returns the log of the Hermite weights:
        log(e^(-(x-N)^2/(2N)))

        Parameters
        ----------

        terr_count : float
            terrestrial count value

        Returns
        -------

        float
            log of the Gaussian with mean and variance N
        '''

        return -(terr_count-self.N)**2/(2*self.N)

    @staticmethod
    def priorUniform(**lambdas):  # noqa: N802
        '''
        Uniform Prior on Counts. Takes dictionary of
        counts. Keys *must* match labels of instances
        of SourceType class.
        '''
        return 1

    @staticmethod
    def priorJeffreys(**lambdas):  # noqa: N802
        '''
        Jeffreys Prior on Counts. Takes dictionary of
        counts. Keys *must* match labels of instances
        of SourceType class.
        '''
        return 1/(np.prod(np.sqrt(lambdas.values()), axis=0))

class MarginalizedPosterior(Posterior):

    '''
    Class that provides the marginalized FGMC posterior on counts, 
    for any number of dimensions up to the max dimensions allowed
    by the original multidimensional FGMC posterior. Inherits from
    the Posterior class.
    Computes astrophysical probability p_astro, by source category.
    '''

    '''
    Attributes
    ----------
    args_fixed : list
        list of object instances whose labels match
        keys of ``fix_sources`` dictionary.
    args_free : list
        list of object instances whose labels do not
        match the keys of fix_sources dictionary.
    arg_terr : :class:`SourceType`
        pertaining to the terrestrial source
    args_astro : tuple
        instances of :class:`SourceType` that correspond to
        astrophysical categories.
    keys_all : list
        list of labels of instances of all :class:`SourceType` instances.
    key_terr : list
        subset of ``key_all`` with terrestrial source type
    keys_astro : list
        subset of ``key_all`` with astrophysical source type
    keys_fixed : list
        list of labels of pinned :class:`SourceType` instances.
    keys_free : list
        list of labels of free :class:`SourceType` instances.
    n : int
        number of terms in the `gauss-laguerre` and `gauss-hermite`
        quadrature integrals, hard coded to 20.
    N : int
        number of candidate events
    roots : iter
        abcissa of `gauss-laguerre` quadrature
    weights : iter
        weights of `gauss-laguerre` quadrature
    hroots : iter
        abcissa of `gauss-hermite` quadrature
    hweights : iter
        weights of `gauss-hermite` quadrature
    reg_const : float
        regularization constant to avoid numerical over/under flows
    norm : float
        normalization constant for counts posterior, determined
        post regularization
    terr_jacobian : float
        constant to be tacked on when integrating terrestrial counts via
        `gauss-hermite` quadrature
        This can only be done after variable transformation.
    priorDict : dict
        dictionary of priors keyed on *Uniform* and *Jeffreys*
    '''

    def __init__(self,f_divby_b,prior_type,terr_source,fix_sources={},
                 buff=1e-15,mcmc=False,verbose=True,**astro_sources):
        
        '''
        Parameters
        ----------
        f_divby_b : list, tuple
            iterable of real numbers, foreground to background ratio
        prior_type : str
            **Uniform** or **Jeffreys**
        terr_source : :class:`SourceType`
            pertaining to the terrestrial source
        fix_sources : dict
            fixed lambda values, keyed on source labels.
            Example: :code:`{"Terr":value}`
            Note that the keys *must* match the labels
            used for :class:`SourceType` instances.
        buff : float
            Surrogate for zero, to avoid singularities in the
            counts posterior.
        verbose : bool
        astro_sources : dict
            dictionary of :class`:SourceType, pertaining to
            astrophysical sources
        '''

        Posterior.__init__(self,f_divby_b,prior_type,terr_source,fix_sources,buff,mcmc,verbose,**astro_sources)
        if self.verbose:
            print ("MarginalizedPosterior class instantiation complete.")
    
    def posterior(self,**lambdas):

        '''
        FGMC Counts Posterior function. Takes dictionary of
        counts. Keys *must* match labels of instances
        of SourceType class.
        
        Posterior can have any dimensionality up to max allowable
        dimensionality, as determined by the number of SourceType 
        instances passed to the MarginalizedPosterior class.
        
        Parameters
        ----------
        
        lambdas : dict
            counts:value dictionary pairs.
            Keys *must* match labels of instances of SourceType
            class.
        
        Returns
        -------

        float
            posterior evaluated at values supplied in the lambda dictionary
        
        Example code: posterior(BNS=5) 
        This will give the value for the 
        corresponding 1-dimensional marginalized posterior

        Example code: posterior(BBH=1,NSBH=3) 
        This will give the value for the 
        corresponding 2-dimensional marginalized posterior.
        
        '''
        
        assert(len(set(self.keys_all)&set(lambdas.keys()))==len(lambdas.keys())),"Counts label(s) passed to posterior function don't match labels of astro/terr source instances"
        
        # keys corresponding to sources to be marginalized over
        self.keys_marg = set(self.keys_free)-set(lambdas.keys())
        # counts corresponding to sources that are pinned
        pinned_lambdas = deepcopy(self.fix_sources)
        pinned_lambdas.update(lambdas)
        # initialize list
        thelist = []

        # If there are no sources to marginalize over
        if len(self.keys_marg) == 0:
            log_likelihood = self.poissonLogWeight(**lambdas)+self.reduced_log_likelihood_astro(**pinned_lambdas)
            likelihood = np.exp(log_likelihood-self.reg_const)
            return self.priorDict[self.prior_type](**lambdas)*likelihood/self.norm
        else:
            # If one of the sources to marginalize over is terrestrial
            if self.key_terr in self.keys_marg:
                thelist = self.marginalize_gq(self.reduced_log_likelihood_terr,self.keys_marg,**pinned_lambdas)
            # If none of the sources to marginalize over is terrestrial
            else:
                thelist = self.marginalize_gq(self.reduced_log_likelihood_astro,self.keys_marg,**pinned_lambdas)
            # Regularize and normalize
            thelist += self.poissonLogWeight(**lambdas)-np.log(self.norm)-self.reg_const
            return self.priorDict[self.prior_type](**lambdas)*np.sum(np.exp(thelist),axis=0)

    def pastro_numerator(self,trigger_idx,categories,**lambdas):
        '''
        Function returns :math:`\sum_{\\alpha}\Lambda_{\\alpha}w_{\\alpha}(j)\\frac{f(j)}{b(j)}`
        
        for a trigger j.
        
        Parameters
        -----------
        
        trigger_idx: int or array of ints: 
            index (indices) of trigger(s) whose p(astro) value is sought
            indices map to the foreground/background values in the f_divby_b vector supplied
        categories:list
            list of category labels. Labels *must* match
            labels of instances of SourceType class
        lambdas:dict
            Counts dictionary. Keys *must* match
            labels of instances of SourceType class.
        
        Returns
        -------
        
        float:
            Value of pastro_numerator evaluated at lambdas.values()
        
        '''
        
        # Distill instances corresponding to categories list
        args = [list(filter(lambda x: x.label == label, self.args_all))[0] for label in categories]
        # Return \Sigma_{\alpha}lambda_{\alpha}*w_{\alpha}(j)*f(j)/b(j)
        # for \alpha iterated over categories provided
        return (np.sum([lambdas[arg.label]*arg.w_fgmc[trigger_idx]
                       for arg in args],axis=0)*self.f_divby_b[trigger_idx])
    
    def pterr_numerator(self,trigger_idx,lambda_terr):
        '''
        Function returns :math:`\Lambda_{\mathrm{terr}}w_{\mathrm{terr}}(j)`
        for a trigger j.
        
        Parameters
        -----------
        
        trigger_idx: int or array of ints: 
            index (indices) of trigger(s) whose p(astro) value is sought
            indices map to the foreground/background values in the f_divby_b vector supplied
        lambda_terr:float
            value of terrestrial count
        
        Returns
        -------
       
        float:
            Value of pterr_numerator evaluated at lambda_terr 
        
        '''
        return lambda_terr*self.arg_terr.w_fgmc[trigger_idx]
    
    def p_numerator(self,trigger_idx,categories,**lambdas):
 
        '''
        Function combines pastro_numerator and pterr_numerator,
        depending on list of categories over which p_astro is
        to be computed

        Parameters
        -----------

        trigger_idx: int or numpy array of ints: 
            index (indices) of trigger(s) whose p(astro) value is sought
            indices map to the foreground/background values in the f_divby_b vector supplied
        categories:list
            list of category labels. Labels *must* match
            labels of instances of SourceType class
        lambdas:dict
            Counts dictionary. Keys *must* match
            labels of instances of SourceType class. 
        
        Returns
        --------
        
        float or numpy array of floats:
            Value of p_numerator evaluated at lambdas.values()
        '''
        
        val = 0 # initialize p_numerator value
        if self.key_terr in categories:
            # Add pterr_numerator if terrestrial category is supplied
            val += self.pterr_numerator(trigger_idx,lambdas[self.key_terr])
            # Return value if *only* terrestrial category is supplied
            if len(lambdas.keys()) == 1:
                return val
        categories_astro = list(set(categories)-set([self.key_terr]))
        # Add pastro_numerator for all astrophysical categories supplied
        val += self.pastro_numerator(trigger_idx,categories_astro,**lambdas)
        return val       
    
    def p_denominator(self,trigger_idx,**lambdas):

        '''
        Function returns :math:`\Lambda_{\mathrm{terr}}w_\mathrm{terr}(j)+\\frac{f(j)}{b(j)}\sum_{\\alpha}\Lambda_{\\alpha}w_{\\alpha}(j))`
        
        Parameters
        ----------
        
        trigger_idx: int or numpy array of int
            index of trigger whose p_astro value is sought
        lambdas: dict 
            Counts dictionary. Keys *must* match
            labels of instances of SourceType class.
        
        Returns
        -------
        
        int or numpy array of ints
            value of p_denominator  
        '''

        return lambdas[self.key_terr]*(self.arg_terr.w_fgmc[trigger_idx]+
                       self.f_divby_b[trigger_idx]/lambdas[self.key_terr]*np.sum([lambdas[arg.label]*
                       arg.w_fgmc[trigger_idx] for arg in self.args_astro],axis=0))
    
    def p_integrand(self,trigger_idx,categories,**lambdas):

        '''
        Function combines `meth`:p_numerator and `meth`:p_denominator,
        along with posterior, to construct the integrand for p(astro).

        Parameters
        ----------
       
        trigger_idx: int or numpy array of ints: 
            index (indices) of trigger(s) whose p(astro) value is sought
            indices correspond to those of f_divby_b numpy array
        categories:list
            list of category labels. Labels *must* match
            labels of instances of `class`:SourceType.
        lambdas:dict
            Counts dictionary. Keys *must* match
            labels of instances of `class`:SourceType.  
        
        Returns
        -------
        
        float or numpy array of floats:
            Value of p_integrand       
        '''
        
        pinned_lambdas = deepcopy(self.fix_sources)
        if self.key_terr not in pinned_lambdas.keys():
            return (self.reduced_log_likelihood_terr(**lambdas)+
                   np.log(self.p_numerator(trigger_idx,categories,**lambdas))-
                   np.log(self.p_denominator(trigger_idx,**lambdas)))
        else:
            return (self.reduced_log_likelihood_astro(**lambdas)+
                   np.log(self.p_numerator(trigger_idx,categories,**lambdas))-
                   np.log(self.p_denominator(trigger_idx,**lambdas)))
    
    def pastro(self,trigger_idx,categories):

        '''
        Function invokes marginalize_gq to integrate p_integrand
        and thus determine p(astro)
        
        Parameters
        ----------
        
        trigger_idx: int or numpy array of ints
            index (indices) of trigger(s) whose p_astro value is sought
            indices correspond to those of f_divby_b numpy array
        categories: list 
            Category labels. These labels *must* match
            those of the instances of the SourceType class.
        
        Returns
        -------
        
        float or numpy array of floats:
            Value of p_astro
        
        '''
        
        assert(len(set(self.keys_all)&set(categories)) == len(categories)),"categories passed to pastro function don't match labels of the astro/terr source instances"
        
        pinned_lambdas = deepcopy(self.fix_sources)
        func = lambda **x: self.p_integrand(trigger_idx,categories,**x)
        thelist = self.marginalize_gq(func,self.keys_free,**pinned_lambdas)
        thelist += -np.log(self.norm) -self.reg_const
        return np.sum(np.exp(thelist),axis=0)
