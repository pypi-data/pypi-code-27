def flatten_generator(list_to_flatten):
    """Child method to flatten multi-dimension lists into a single list

    Args:
        list_to_flatten (list): List of lists to flatten

    Returns:
        list()

    """
    for elem in list_to_flatten:
        if isinstance(elem,(list, tuple)):
            for x in flatten(elem):
                yield x
        else:
            yield elem

def flatten(list_to_flatten):
    """Parent method to flatten multi-dimension lists into a single list

    Args:
        list_to_flatten (list): List of lists to flatten

    Returns:
        list()

    """
    if isinstance(list_to_flatten, basestring):
        return [list_to_flatten]
    return list(flatten_generator(list_to_flatten))
