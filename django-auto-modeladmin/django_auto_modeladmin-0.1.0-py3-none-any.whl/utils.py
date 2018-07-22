def filter_list(list_to_check, list_to_include):
    """ Return a list with only items that matched an item in list_to_include.
    """
    filtered_list = []
    for checked in list_to_check:
        for included in list_to_include:
            if checked == included:
                filtered_list.append(checked)
    return filtered_list


def capitalize(string):
    """ helper function to create capitalized copy of string. """
    return string[:1].upper() + string[1:]
