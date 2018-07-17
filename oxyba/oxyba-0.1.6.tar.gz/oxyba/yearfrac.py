
def yearfrac(dates, cutoffdt):
    """compute the maturities a year fractional
    """

    #load modules
    import numpy as np
    from datetime import datetime

    if not isinstance(dates, np.ndarray):
        raise ValueError("'dates' is not an np.array")
    
    if not isinstance(dates[0], datetime):
        raise ValueError("'dates' elements are no datetime objects")        
    
    if not isinstance(cutoffdt, datetime):
        raise ValueError("'eordt' is no datetime objects")
    
    # result
    return np.array([(dt - cutoffdt).days for dt in dates]) / 365.2425