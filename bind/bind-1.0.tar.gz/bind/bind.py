"""
Bind: a one-line Python module to mimic os.path.join without reverting to root
"""
def bind(*args, sep='/'):
    """
    A function to join
    """
    return sep.join([str(i).strip(sep) for i in args])
