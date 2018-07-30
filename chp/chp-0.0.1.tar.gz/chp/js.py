from chp.pyreact import *


def cjs(props, children): # create js element
    return ce('js', props, children)

def progn(content):
    return call_anonymous(def_func("f", "", content))

def call_anonymous(value):
    props = [
        cp('before', '('),
        cp('after', ')();'),
    ]
    children = value if type(value) is str else [value]
    return cjs(props, children)

def instruction(value):
    props = [
        cp('before', f'('),
        cp('after', ');'),
    ]
    children = value if type(value) is str else [value]
    return cjs(props, children)

def log(value):
    props = [
        cp('before', 'console.log('),
        cp('after', ')'),
    ]
    children = value
    return instruction(cjs(props, children))


def block(value):
    props = [
        cp('before', '{'),
        cp('after', '}'),
    ]
    children = value if type(value) is str else [value]
    return cjs(props, children)

def def_global(name, value):
    props = [
        cp('before', f'window.{name}='),
        cp('after', ''),
    ]
    children = [instruction(value)]
    return cjs(props, children)

def def_local(name, value):
    props = [
        cp('before', f'let {name}='),
        cp('after', ''),
    ]
    children = [instruction(value)]
    return cjs(props, children)

def assign(name, value):
    props = [
        cp('before', f'{name}='),
        cp('after', ''),
    ]
    children = [instruction(value)]
    return cjs(props, children)

def def_func(name, arguments, children):
    props = [
        cp('before', 'function(' + arguments + ') {'),
        cp('after', '}'),
    ]
    return cjs(props, children)

def If(condition, children):
    props = [
        cp('before', 'if(' + condition + ') {'),
        cp('after', '}'),
    ]
    return cjs(props, children)

def Return(children):
    props = [
        cp('before', 'return '),
        cp('after', ''),
    ]
    return cjs(props, [instruction(children)])

def op(operation, operand, operee):
    props = [
        cp('before', f'({operand} {operation} '),
        cp('after', f'{operee})'),
    ]
    children=""
    return cjs(props, children)


i = instruction(op('+', '1', '2')),
content = [
    def_local('x', 'document.getElementById(\'mySelect\').value'),
    assign('document.getElementById(\'demo\').innerHTML', op('+', "'You selected: '", 'x')),
]
ast = def_local('a', '1')
ast = call_anonymous(def_func("f", "", content))
js = render_js_element(ast)
