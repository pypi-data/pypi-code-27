def get_prop(props=[], name=[]):
    for p in props:
        try:
            if p["name"] == name:
                return p
        except KeyError:
            return None

# returns a middleware. a middleware is a function that takes and ast element and returns an other ast element
# in the case of this middleware, we inspect the type of el and call it with a context.
# with this middlware a component can now return a function taking a context as argument and returning an el.
def context_middleware(context):

    def middleware(el):
        if callable(el):
            return el(context)
        else:
            return el
    return middleware

def default_middleware(el, _props = [], _children=[]):
    return el

import math
import random


def diff_asts(old, new):
    patches = []
    new_tree = {}
    old_name = old["name"]
    old_props = old["props"]
    new_name = new["name"]
    new_props = new["props"]

    # if elements not same name
        # request to patch innerHTML with chp-id of the old one

    if old_name != new_name:
        patches.append({
            "type": "replace-element",
            "chp-id": get_prop(old_props, "chp-id")["value"],
            "html": render_element(new),
        })
        new_tree = new
        # id = get_prop('chp-id', new_tree["props"])
        # id["value"] = get_prop('chp-id', new["props"])["value"]

    # else
        # go through props
        # excluding children
        # if props differ
            # request patching with new props (but keep old chp-id)

    else:
        i = 0
        props_differ = False
        if len(old_props) != len(new_props):
            props_differ = True

        if not props_differ:
            while i < len(new_props):
                c1 = old_props[i]["name"] != new_props[i]["name"]
                c2 = old_props[i]["value"] != new_props[i]["value"]

                if c1 or c2:
                    if new_props[i]["name"] != "children":
                        if new_props[i]["name"] != "chp-id":
                            props_differ = True
                i += 1


        if props_differ:
            id = get_prop(new_props, "chp-id")
            id["value"] = get_prop(old_props, "chp-id")["value"]
            patches.append({
                "type": "props",
                "chp-id": get_prop(old_props, "chp-id")["value"],
                "props" : new_props
            })
            new_tree = new
            new_tree["props"] = new_props
        else:
            new_tree = old


    nc = get_prop(new_props, "children")
    oc = get_prop(old_props, "children")
    new_children =  nc["value"] if nc else []
    old_children =  oc["value"] if oc else []

    if len(new_children) != len(old_children):
        html = ""
        if type(new_children) is str:
            html = new_children
        else:
            new_tree_children = get_prop(new_tree["props"], 'children') # ref to new_tree's props
            new_tree_children["value"] = []
            for c in new_children:
                html += render_element(c)
                # new_tree
                new_tree_children["value"].append(c)

        patches.append({
            "type": "innerHTML",
            "chp-id": get_prop(old_props, "chp-id")["value"],
            "html": html,
        })
    else:
        new_tree_children = get_prop(new_tree["props"], 'children') # ref to new_tree's props
        new_tree_children["value"] = get_prop(new["props"], 'children')["value"] # ref to new_tree's props
        if type(new_children) is str:
            new_tree_children["value"] = new_children
        else:
            new_tree_children["value"] = []
            i = 0
            while i < len(new_children):
                child_diff = diff_asts(old_children[i], new_children[i])
                ps = child_diff[0]
                for p in ps:
                    patches.append(p)
                i += 1

                new_tree_children["value"].append(child_diff[1])

    # go through children
        # if new one missing
            # request deletion of old node (with chp-id)

        # if old one missing
            # request creation of new node

    return [patches, new_tree]


def render_html(el, props, child):
    name = el["name"]

    children = ""
    for c in child:
        children += c

    props_str = ""
    for p in props:
        if p["name"] != "children":
            props_str += (p["name"] + "=\"" + p["value"] + "\"")

    self_closing_tags = ["input", "link", "img"]
    if name in self_closing_tags:
        return f"<{name} {props_str} />"

    return f"<{name} {props_str}>{children}</{name}>"

def render_js(el, props, child):
    name = el["name"]
    props_str = ""

    children = ""
    for c in child:
        children += c

    before=get_prop(props, "before")["value"]
    after=get_prop(props, "after")["value"]

    return f"{before}{children}{after}"

def id_middleware(ast):
    props = ast["props"]
    props.append({
        "name": "chp-id",
        "value": str(math.floor(random.random()*10000000))
    })
    return ast


def render_ast(ast, ast_middleware, render_middleware):
    ast = ast_middleware(ast)

    props = ast["props"]

    children = False
    for p in props:
        if p["name"] == "children":
            children = p["value"]

    child = []
    if not children:
        child = ""
    elif type(children) is str:
        child = children
    else:
        for c in children:
            child.append(render_ast(c, ast_middleware, render_middleware))

    return render_middleware(ast, props, child)

def inject_ids(ast):
    return render_ast(ast, id_middleware, default_middleware)

def render_js_element(ast):
    return render_ast(ast, default_middleware, render_js)

def render_element(ast, middleware=default_middleware):
    return render_ast(ast, middleware, render_html)

def create_element(name, props, children):
    props.append({
        "name": "children",
        "value": children,
    })

    return {
        "name": name,
        "props": props,
    }

def create_prop(name, value):
    return {
        "name": name,
        "value": value,
    }

def get_prop(props=[], name=[]):
    for p in props:
        try:
            if p["name"] == name:
                return p
        except KeyError:
            return None

def create_context(value):
    return [{
            "name": "__context",
            "value": value,
        }]


ce = create_element
cp = create_prop
