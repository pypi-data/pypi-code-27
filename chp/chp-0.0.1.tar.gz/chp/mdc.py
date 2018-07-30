


def Grid(*children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-grid__inner')
    ]
    return Div(props, children)

def Row(*children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-grid__inner')
    ]
    return Div(props, children)

def Cell(*children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-grid__cell')
    ]
    return Div(props, children)
