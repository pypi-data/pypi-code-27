def logpdf(z, x, S):

    if np.isscalar(z) and np.isscalar(x) and np.isscalar(S):
        return math.log(math.exp(-0.5 * (z-x)**2) / math.sqrt(2*math.pi*S))

    y = (np.asanyarray(z) - np.asanyarray(x)).flatten()
    S = np.atleast_2d(S)
    k = len(y)

    # if we are nearly singular the forthcoming inv(S) creates an absurdly
    # large
    det = np.linalg.det(S)

    den = np.sqrt((2*np.pi)**k * np.linalg.det(S))
    return (-.5 * y.T @ np.linalg.inv(S) @ y) - math.log(den)



# code for a naive implementation of logpdf. doesn't work when S near singular


for _ in range(1000000):
    x = np.random.randn(2)
    z = np.random.randn(2)
    S = np.random.randn(2,2)
    S = np.dot(S, S.T) # make it positive definite
    try:
        logpdf2(x, z, S)
    except np.linalg.LinAlgError:
        print('fuck')
        print(x, z, S)
        print(multivariate_normal.logpdf(x.flatten(), z.flatten(), S, allow_singular=True))
        print(logpdf(x, z, S))

        return

    np.testing.assert_allclose(logpdf(x, z, S), logpdf2(x, z, S))


