
def linreg_predict(X, beta):
    import numpy as np
    return np.dot(X,beta);

def linreg_residuals(y, X, beta):
    import numpy as np
    return y - np.dot(X,beta);
    #return y - linreg_predict(X, beta);

def linreg_ssr(y, X, beta):
    import numpy as np
    return np.sum( (y - np.dot(X,beta))**2 )
    #eps = linreg_residuals(y, X, beta);
    #return np.dot(eps.T, eps)
