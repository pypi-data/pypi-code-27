from chp.components import *
from chp.js import *


def create_store(store_name, on_store_change, json_init_state):
    onchange_cb = store_name + "_cb"
    code = [
        def_global(onchange_cb, def_func("f", "obj, prop", on_store_change)),
        def_global(
            store_name,
            "!window.todoStore ? new Proxy(JSON.parse('" + json_init_state + "'), { set: (obj, prop, value) => {obj[prop]=value;window."+onchange_cb+"(obj, prop); return true } }) : window.todoStore"
        ),
    ]
    ast = progn(code)
    js = render_js_element(ast)
    return js

def patch_dom(patches):
    for patch in patches:
        type = patch["type"]
        chp_id = patch["chp-id"]
        if type == "props":
            props = patch["props"]
            for prop in props:
                el = document["querySelector"](f"[chp-id='{chp_id}']")
                if prop["name"] != "chp-id":
                    el.setAttribute(prop["name"], prop["value"])
                    if prop["name"] == "value": # value can't be set with setattr
                        el["value"] = prop["value"]
        elif type == "innerHTML":
            el = document["querySelector"](f"[chp-id='{chp_id}']")
            el.innerHTML = patch["html"]


def render_app(store_name, store_content_json):
    return progn([
        def_local("old_chp_ast", "window.chp_ast ? window.chp_ast : JSON.parse(document.querySelector(\"[chp-id='chp-ast']\").innerHTML)"),
        def_local("new_chp_ast", f"inject_ids(FormSchema(window.{store_name}, '{store_content_json}'))"),
        def_local("[patches, new_ast_from_diff]", "old_chp_ast ? window.diff_asts(old_chp_ast, new_chp_ast) : false"),
        def_global("chp_ast", "new_ast_from_diff"),
        progn("patch_dom(patches)"),
        progn("eval(document.querySelector('body script').innerHTML);"),
    ])


def AST(json_ast):
    children = json_ast
    props = [
        cp('style', 'display: none'),
        cp('chp-id', 'chp-ast'),
    ]
    return Div(props, children)


def injectAstIntoDOM(ast):
    window.chp_ast = ast


def Inject_ast_into_DOM(app, json_ast):
    children = [
        app,
        AST(json_ast),
        Script("window.chp_ast = JSON.parse(document.querySelector(\"[chp-id='chp-ast']\").innerHTML)"),
    ]
    return Div([], children)
