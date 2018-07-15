import numpy as np


__title__ = "pandas-refract"
__version__ = "1.2.1"
__author__ = "Nicholas Lawrence"
__license__ = "MIT"
__copyright__ = "Copyright 2018-2019 Nicholas Lawrence"


def refract(df, conditional, reset_index=True):
    """

    Return pair of Dataframes split against Truthy and Falseyness of provided array. Option to reset index in place.

    / >>> data = {'temperature': ['high', 'low', 'low', 'high'],
                  'overcast': [True, False, True, False]
                  }

    / >>> df = pandas.DataFrame(data)

    / >>> hot_df, cold_df = refract(df, df.temperature == 'high')

    / >>> overcast_df, not_overcast_df = refract(df, df.overcast, reset_index=True)

    / >>> print(overcast_df.iloc[0], not_overcast_df.iloc[0])

    """
    _conditional = np.asarray(conditional, bool)
    _true_df = df[_conditional]
    _false_df = df[~_conditional]

    if reset_index:
        _true_df = _true_df.reset_index(drop=True)
        _false_df = _false_df.reset_index(drop=True)

    return _true_df, _false_df


def disperse(df, label, reset_index=True):
    """

    Return dictionary where key is a unique value in given dataframe series and value is dataframe where given column is
    key value.

    / >>> data = {'temperature': ['high', 'low', 'low', 'high', 'medium', 'medium'],
                  'overcast'   : [True, False, True, False, False, True]
                  }

    / >>> df = pd.DataFrame(data)

    / >>> prism = disperse(df, 'temperature')

    / >>> {'high':   temperature  overcast
                    0      high      True
                    1      high     False,

           'low':   temperature  overcast
                    0       low     False
                    1       low      True,

           'medium':   temperature  overcast
                    0    medium     False
                    1    medium      True
          }

    """
    _notnulls, _nulls = refract(df, df[label].notnull())
    _unique_values = set(_notnulls[label])

    _prism = {}

    if reset_index:
        for val in _unique_values:
            _prism[val] = _notnulls[_notnulls[label] == val].reset_index(drop=True)

    else:
        for val in _unique_values:
            _prism[val] = _notnulls[_notnulls[label] == val]

    if not _nulls.empty:
        _prism[None] = _nulls

    return _prism
