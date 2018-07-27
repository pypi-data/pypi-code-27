"""This module contains all the methods to obtain information about the
model uncertainty.

"""

def rfunc_uncertainty(ml, rfunc, alpha):
    """

    Parameters
    ----------
    ml: pastas.Model
        Pastas model instance
    rfunc: pastas.rfunc.RfuncBase
        Pastas response function
    alpha: float
        float between 0 and 1 that indicates the

    Returns
    -------

    """

    return series



import numpy as np
import pandas as pd


class Uncertainty:
    def __init__(self, ml):
        # Save a reference to the model.
        self.ml = ml

    def multivariate(self, n=1000):
        # parameter waarden random getrokken uit een multivariabele verdeling
        # met behulp van de covariantie matrix uit lmfit.
        par = self.ml.parameters.optimal.values
        par = np.random.multivariate_normal(par, self.ml.fit.covar, n)

        data = {}

        for i in range(n):
            data[i] = self.ml.simulate(parameters=par[i])

        data = pd.DataFrame(data)
        return data

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("First run example.py before running this file!")

ml.solve()
ml.uncertainty = Uncertainty(ml)
df = ml.uncertainty.multivariate(100)

ml.simulate().plot(color="k")
plt.fill_between(df.index, df.quantile(q=0.025, axis=1)
, df.quantile(q=0.975, axis=1))
