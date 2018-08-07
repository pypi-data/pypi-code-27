import numpy as np

from .LoadComponent import LoadComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class ThermalLoad(LoadComponent):
    """Thermal Load module.

    Parameters
    ----------
    data : dict or ndarray
        Dataset. Pass a dict with 'load' as the key for the hourly load demand
        [kW] for one year. An ndarray can be passed as well.
    rec_ratio : float
        Heat recovery ratio.
    name_line : str
        Label for the load demand. This will be used in generated graphs
        and files.
    color_line : str
        Hex code (e.g. '#33CC33') of the color for the load demand. This
        will be used in generated graphs.

    Other Parameters
    ----------------
    num_case : int
        Number of scenarios to simultaneously simulate. This is set by the
        Control module
    yr_proj : int
        Project lifetime [yr]. This is set by the Control module.

    """

    def __init__(self, data, rec_ratio=0.4, **kwargs):
        """Initializes the base class.

        """
        # base class parameters
        settings = {
            'name_line': 'Thermal Load',  # label for load
            'color_line': '#666666',  # color for load in powerflow
            'capex': 0.0,  # CapEx [USD/kWh]
            'opex_fix': 0.0,  # size-dependent OpEx [USD/kWh-yr]
            'opex_var': 0.0,  # output-dependent OpEx [USD/kWh-yr]            
            'infl': 0.0,  # no inflation rate needed, must not be None
            'size': 0.0,  # no size needed, must not be None
            'data': data  # dataset
        }
        settings.update(kwargs)  # replace default settings with input settings

        # initialize base class
        super().__init__(**settings)

        # extract dataset
        if isinstance(self.data, dict):  # pass dict
            self.load = self.data['load']  # load [kW]
        elif isinstance(self.data, np.ndarray):  # pass ndarray
            self.load = self.data

        # adjustable load parameters
        self.rec_ratio = rec_ratio

        # derivable load parameters
        self.pow_max = np.max(self.load)  # largest power in load [kW]
        self.enr_tot_yr = np.sum(self.load)  # yearly consumption [kWh]

        # update initialized parameters if essential data is complete
        self._update_config()

    def get_pow(self, hr):
        """Returns the power output [kW] at the specified time [h].

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        """
        # get data from the timestep
        return self.pow[hr, :]

    def cost_calc(self):
        """Calculates the cost of the component. This is here for functionality only.

        """
        pass

    def _config(self):
        """Updates other parameters once essential parameters are complete.

        """
        # generate an expanded array with hourly timesteps
        self.pow = np.repeat(
            self.load.reshape((8760, 1)),
            self.num_case, axis=1
        )
