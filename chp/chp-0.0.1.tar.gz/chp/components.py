from chp.pyreact import *


def Div(props, children):
    children = children or []
    return ce('div', props, children)

def Button(props, children):
    children = children or []
    return ce('div', props, children)

def Script(string = ""):
    return ce('script', [], string)

def ScriptBefore(children, script_text):
    children = children or []
    script = [Script(script_text)]
    children =  script.append(children)
    return Div([], children)


def Grid(children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-grid__inner')
    ]
    return Div(props, children)

def Row(children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-grid__inner')
    ]
    return Div(props, children)

def Cell(children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-grid__cell')
    ]
    return Div(props, children)

def Errors():
    props = []
    children='''
    '''
    return Div(props, children)

def Form(children):
    props = [
        cp('class', 'mdc-layout-grid__cell')
    ]
    errors=Errors()
    children.append(errors)
    return ce('form', props, children)


def Field(children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-field')
    ]
    return Div(props, children)


def Checkbox(is_checked):
    props = [
        cp('class', 'mdc-checkbox__native-control'),
        cp('type', 'checkbox'),
        cp('id', '{{ id }}'),
        cp('checked' if is_checked else '', ''),
    ]
    return ce('input', props, [])

def Label(name):
    def c(context):
        props = [
        ]
        return ce('label', props, context["label"] + " " + name)
    return c

def CheckboxField(isChecked):
    def c(context):
        children = []
        props = [
            cp('class', 'mdc-form-field')
        ]
        children.append(Div(
                [cp("class", "mdc-checkbox")],
                [
                    Checkbox(isChecked),
                    Div(
                        [cp("class", "mdc-checkbox-background")],
                        []
                    ),
                    Label('Checkbox'),
                    Label(context["label"])
                ]
            ))
        return Div(props, children)
    return c
