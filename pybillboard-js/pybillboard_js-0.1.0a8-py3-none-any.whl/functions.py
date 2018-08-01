# -*- coding: UTF-8 -*-
# import os
import os, sys; module_dir = os.path.dirname(os.path.abspath(__file__))
# import config
from . import config, query
# import logger
from .logger import Logger

# function update_res
def update_res():
    import requests
    
    Logger.info("Update resources")
    # get text of  billboard.min.js/css
    billboard_min_text = {
        "js": requests.get("https://naver.github.io/billboard.js/release/latest/dist/billboard.pkgd.min.js").text,
        "css": requests.get("https://naver.github.io/billboard.js/release/latest/dist/billboard.min.css").text
    }

    if config.search(query.NAME == "billboard-js") == []:
        config.insert({"NAME": "billboard-js", "VALUE": billboard_min_text["js"]})
    else:
        config.update({"VALUE": billboard_min_text["js"]}, query.NAME == "billboard-js")

    if config.search(query.NAME == "billboard-css") == []:
        config.insert({"NAME": "billboard-css", "VALUE": billboard_min_text["css"]})
    else:
        config.update({"VALUE": billboard_min_text["css"]}, query.NAME == "billboard-css")

    # change update_res to false
    config.update({"VALUE": False}, query.NAME == "UPDATE_RES")

    sys.stdout.write("\n")# write next-line for repl

# function get_config
def get_config(conf_name):
    try:
        return config.search(query.NAME == conf_name)[0]["VALUE"]
    except IndexError:
        from .exceptions import ConfigNotExistsError
        raise ConfigNotExistsError("{0} not exists!".format(conf_name))

# function get_raw_type
def get_raw_type(pybillboard_chart_type):
    chart_type_info = {
        "Line": "line",
        "Area": "area",
        "Bar": "bar",
        "Scatter": "scatter",
        "Pie": "pie",
        "Bubble": "bubble",
        "SpLine": "spline",
        "AreaSpLine": "area-spline",
        "Step": "step",
        "AreaStep": "area-step",
        "AreaLineRange": "area-line-range",
        "AreaSpLineRange": "area-spline-range",
        "Donut": "donut",
        "Gauge": "gauge",
        "Radar": "radar"
    }

    if pybillboard_chart_type in chart_type_info.keys():
        return chart_type_info[pybillboard_chart_type]
    else:
        from .exceptions import ChartTypeError
        raise ChartTypeError("invalid chart type: {0}".format(pybillboard_chart_type))

# function get_df_dimension
def get_df_dimension(dataframe):
    import numpy as np
    
    return len(np.array(dataframe.values.tolist()).shape)
