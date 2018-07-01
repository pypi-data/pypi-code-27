import numpy as np
from ...cl_routines.sampling.base import AbstractRWMSampler
from mot.kernel_data import KernelArray

__author__ = 'Robbert Harms'
__date__ = "2014-02-05"
__license__ = "LGPL v3"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


class AdaptiveMetropolisWithinGibbs(AbstractRWMSampler):

    def __init__(self, model, starting_positions, proposal_stds, target_acceptance_rate=0.44,
                 batch_size=50, damping_factor=1, min_val=1e-15, max_val=1e3, **kwargs):
        r"""An implementation of the Adaptive Metropolis-Within-Gibbs (AMWG) MCMC algorithm [1].

        This scales the proposal parameter (typically the std) such that it oscillates towards the chosen acceptance
        rate. We implement the delta function (see [1]) as: :math:`\delta(n) = \sqrt{1 / (d*n)}`.
        Where n is the current batch index and d is the damping factor. As an example, with a damping factor of 500,
        delta reaches a scaling of 0.01 in 20 batches. At a batch size of 50 that would amount to 1000 samples.

        In principal, AMWG can be used as a final MCMC algorithm if and only if the adaption is effectively zero.
        That is when delta gets close enough to zero to no longer influence the proposals.

        Args:
            model (SampleModelInterface): the model to sample.
            starting_positions (ndarray): the starting positions for the sampler. Should be a two dimensional matrix
                with for every modeling instance (first dimension) and every parameter (second dimension) a value.
            proposal_stds (ndarray): for every parameter and every modeling instance an initial proposal std.
            target_acceptance_rate (float): the target acceptance rate between 0 and 1.
            batch_size (int): the size of the batches inbetween which we update the parameters
            damping_factor (int): how fast the function moves to zero
            min_val (float): the minimum value the standard deviation can take
            max_val (float): the maximum value the standard deviation can take

        References:
            [1] Roberts GO, Rosenthal JS. Examples of adaptive MCMC. J Comput Graph Stat. 2009;18(2):349-367.
                doi:10.1198/jcgs.2009.06134.
        """
        super(AdaptiveMetropolisWithinGibbs, self).__init__(model, starting_positions, proposal_stds, **kwargs)
        self._target_acceptance_rate = target_acceptance_rate
        self._batch_size = batch_size
        self._damping_factor = damping_factor
        self._min_val = min_val
        self._max_val = max_val
        self._acceptance_counter = np.zeros((self._nmr_problems, self._nmr_params), dtype=np.uint64, order='C')

    def _get_kernel_data(self, nmr_samples, thinning, return_output):
        kernel_data = super(AdaptiveMetropolisWithinGibbs, self)._get_kernel_data(nmr_samples, thinning, return_output)
        kernel_data.update({
            '_acceptance_counter': KernelArray(self._acceptance_counter, is_writable=True, ensure_zero_copy=True)
        })
        return kernel_data

    def _at_acceptance_callback_c_func(self):
        return '''
            void _sampleAccepted(mot_data_struct* data, ulong current_iteration, uint parameter_ind){
                data->_acceptance_counter[parameter_ind]++;
            }
        '''

    def _get_proposal_update_function(self, nmr_samples, thinning, return_output):
        kernel_source = '''
            void _updateProposalState(mot_data_struct* data, ulong current_iteration,
                                      local mot_float_type* current_position){    
                if(current_iteration > 0 && current_iteration % ''' + str(self._batch_size) + ''' == 0){
                    mot_float_type delta = sqrt(1.0/
                            (''' + str(self._damping_factor) + ''' * 
                            (current_iteration / ''' + str(self._batch_size) + ''')));
                            
                    for(uint k = 0; k < ''' + str(self._nmr_params) + '''; k++){
                        if(data->_acceptance_counter[k] / (mot_float_type)''' + str(self._batch_size) + ''' 
                                > ''' + str(self._target_acceptance_rate) + '''){
                            data->_proposal_stds[k] *= exp(delta);
                        }
                        else{
                            data->_proposal_stds[k] /= exp(delta);
                        }
        
                        data->_proposal_stds[k] = clamp(data->_proposal_stds[k], 
                                                        (mot_float_type)''' + str(self._min_val) + ''', 
                                                        (mot_float_type)''' + str(self._max_val) + ''');
        
                        data->_acceptance_counter[k] = 0;
                    }
                }             
            }
        '''
        return kernel_source
