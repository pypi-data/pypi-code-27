def _filter(data, fields):
    out = {}

    for field in fields:
        key, *rest = field.split('.')

        if rest:
            many = isinstance(data[key], list)
            sub_element = query(data[key], rest, many=many)

            existing_element = out.get(key, [] if many else {})
            if many and existing_element:
                for current, new in zip(out[key], sub_element):
                    current.update(new)
            elif not many and existing_element:
                out[key].update(sub_element)
            else:
                out[key] = sub_element
        else:
            out[key] = data[key]

    return out


def query(data, fields, *, many=False):
    if isinstance(data, list) and many is False:
        raise AssertionError(
            'if querying a list is desired, then you must pass many=True!')
    elif isinstance(data, dict) and many is True:
        raise AssertionError(
            'if querying a dict is desired, then you must not pass many=True!')

    if many:
        return [_filter(d, fields) for d in data]
    else:
        return _filter(data, fields)
