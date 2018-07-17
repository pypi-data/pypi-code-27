from collections import OrderedDict
import pprint
from dplus.CalculationInput import CalculationInput

class CalculationResult(object):
    '''
    Stores the various aspects of the result for further manipulation
    '''
    def __init__(self, calc_data, result, job):
        self._raw_result = result #a json
        self._job=job #used for getting amps and pdbs
        self._calc_data = calc_data #gets x for getting graph. possibly also used for fitting.
        self._get_graph() #creates an ordered dict, key x val y.
        self._headers = OrderedDict()

    def __str__(self):
        return pprint.pformat(self._raw_result)

    @property
    def y(self):
        #TODO: replace with something better
        return self._raw_result['Graph']

    def _get_graph(self):
        graph = OrderedDict()
        x=self._calc_data.x
        try:
            if len(x)!=len(self._raw_result['Graph']):
                raise ValueError("Result graph size mismatch")
            for i in range(len(x)):
                graph[x[i]] = self._raw_result['Graph'][i]
        except KeyError: #sometimes Fit doesn't return a graph. Also every time Generate crashes.
            print("No graph returned")
        self._graph=graph

    @property
    def graph(self):
        return self._graph

    @property
    def headers(self):
        return self._headers

    def get_pdb(self, model_ptr, destination_folder=None):
        return self._job._get_pdb(model_ptr, destination_folder)

    def get_amp(self, model_ptr, destination_folder=None):
        return self._job._get_amp(model_ptr, destination_folder)

    @property
    def error(self):
        if "error" in self._raw_result:
            return self._raw_result["error"]
        return {"code":0, "message":"no error"}

    def save_to_out_file(self, filename):
        with open(filename, 'w') as out_file:
            domain_preferences = self._calc_data.DomainPreferences
            out_file.write("# Integration parameters:\n")
            out_file.write("#\tqmax\t{}\n".format(domain_preferences.q_max))
            out_file.write("#\tOrientation Method\t{}\n".format(domain_preferences.orientation_method))
            out_file.write("#\tOrientation Iterations\t{}\n".format(domain_preferences.orientation_iterations))
            out_file.write("#\tConvergence\t{}\n\n".format(domain_preferences.convergence))

            for value in self.headers.values():
                out_file.write(value)
            for key, value in self.graph.items():
                out_file.write('{:.5f}\t{:.20f}\n'.format(key,value))
            out_file.close()


class GenerateResult(CalculationResult):
    def __init__(self, calc_data, result, job):
        super().__init__(calc_data,result, job )
        self._parse_headers() #sets self._headers to a list of headers

    def _parse_headers(self):
        header_dict = OrderedDict()
        try:
            headers = self._raw_result['Headers']
            for header in headers:
                header_dict[header['ModelPtr']] = header['Header']
        except:  # TODO: headers don't appear in fit results?
            pass  # regardless, I'm pretty sure no one cares about headers anyway
        self._headers = header_dict


class FitResult(CalculationResult):
    def __init__(self, calc_data, result, job):
        super().__init__(calc_data,result, job )
        self._get_parameter_tree() #right now just returns value from result.
        self.create_state_results()

    def _get_parameter_tree(self):
        try:
            self._parameter_tree = self._raw_result['ParameterTree']
        except KeyError:
            raise ("ParameterTree doesn't exist")

    @property
    def parameter_tree(self):
        return self._parameter_tree


    def create_state_results(self):
        # Combine results returned from a Fit calculation
        def combine_model_parameters(parameters):
            # Combine parameters of just one model
            model_ptr = parameters['ModelPtr']
            model = self.__state_result.get_model(model_ptr)
            mutables = model.get_mutable_params() or []
            updated = 0
            for param in parameters['Parameters']:
                if param['isMutable']:
                    if updated >= len(mutables):
                        raise ValueError("Found more 'isMutable' params in ParameterTree than in our state")
                    mutables[updated].value = param['Value']
                    updated += 1
            if updated != len(mutables):
                raise ValueError(
                    "Found a mismatch between number of 'isMutable' params in the ParamterTree and in our state")

        def recursive(parameters):
            combine_model_parameters(parameters)
            for sub in parameters['Submodels']:
                recursive(sub)

        self.__state_result = CalculationInput.copy_from_state(self._calc_data)
        recursive(self.parameter_tree)

    @property
    def result_state(self):
        return self.__state_result