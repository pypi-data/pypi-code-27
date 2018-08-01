from copy import copy, deepcopy
import random
import os
import pandas as pd
import simplejson as json

import ipywidgets as wg

from traitlets import observe, Unicode, Dict, List, Int, Bool

from .util import Util
from .builder_params import BuilderParams
from .display import export_html_code
from .__meta__ import __version_js__

_semver_range_frontend_ = '~' + __version_js__


class Grid(wg.DOMWidget):
    """
    Ag-Grid widget
    """
    _model_name = Unicode('AgGridModel').tag(sync=True)
    _view_name = Unicode('AgGridView').tag(sync=True)
    _model_module = Unicode('ipyaggrid').tag(sync=True)
    _view_module = Unicode('ipyaggrid').tag(sync=True)
    _view_module_version = Unicode(_semver_range_frontend_).tag(sync=True)
    _model_module_version = Unicode(_semver_range_frontend_).tag(sync=True)

    _id = Int(0).tag(sync=True)

    width = Unicode('100%').tag(sync=True)
    height = Unicode('').tag(sync=True)

    theme = Unicode('').tag(sync=True)
    css_rules_down = List([]).tag(sync=True)
    license = Unicode('').tag(sync=True)

    quick_filter = Bool(True).tag(sync=True)
    export_csv = Bool(True).tag(sync=True)
    export_excel = Bool(True).tag(sync=True)
    index = Bool(False).tag(sync=True)
    keep_multiindex = Bool(True).tag(sync=True)
    hide_grid = Bool(False).tag(sync=True)
    compress_data = Bool(False).tag(sync=True)
    columns_fit = Unicode('').tag(sync=True)
    export_mode = Unicode('').tag(sync=True)
    _grid_data_down = List([]).tag(
        sync=True, to_json=Util.data_to_json)
    _grid_data_up = Dict({}).tag(
        sync=True, from_json=Util.data_from_json)
    show_toggle_delete = Bool(False).tag(sync=True)
    show_toggle_edit = Bool(True).tag(sync=True)
    to_eval = List([]).tag(sync=True)
    menu = Dict({}).tag(sync=True)
    user_params = Dict({}).tag(sync=True)

    _js_helpers_builtin = Unicode('').tag(sync=True, to_json=Util.options_to_json)
    js_helpers_custom = Unicode('').tag(sync=True, to_json=Util.options_to_json)
    js_helpers = Unicode('').tag(sync=True, to_json=Util.options_to_json)
    js_pre_helpers = List([]).tag(sync=True)
    js_pre_grid = List([]).tag(sync=True)
    js_post_grid = List([]).tag(sync=True)

    _is_grid_options_multi = Bool(False).tag(sync=True)
    _grid_options_mono_down = Unicode('').tag(sync=True,
        to_json=Util.options_to_json)
    _grid_options_multi_down = List([]).tag(sync=True,
        to_json=Util.multi_options_to_json)

    _counter_update_data = Int(0).tag(sync=True)
    export_data = Dict({}).tag(sync=True)
    _export_mode = Unicode('').tag(sync=True)

    grid_data_out = Dict({}).tag(sync=False)

    params = []

    def __init__(self,
                 width='100%',
                 height=0,
                 theme='ag-theme-fresh',
                 css_rules='',
                 quick_filter=False,
                 export_csv=False,
                 export_excel=False,
                 show_toggle_delete=False,
                 show_toggle_edit=False,
                 index=False,
                 keep_multiindex=True,
                 grid_data=[],
                 grid_options={},
                 grid_options_multi=[],
                 license='',
                 hide_grid=False,
                 compress_data=True,
                 columns_fit='size_to_fit',
                 export_mode='disabled',
                 js_helpers_custom='',
                 js_pre_helpers=[],
                 js_pre_grid=[],
                 js_post_grid=[],
                 menu=None,
                 user_params={}):
        """
        Instantiates the widget. See https://dgothrek.gitlab.io/ipyaggrid/guide/grid.html#parameters
        for more details.
        """

        self._id = random.randint(0, int(1e9))
        self.width_in = width
        self.height_in = height
        self.theme = theme
        self.css_rules = css_rules
        self.quick_filter = quick_filter
        self.export_csv = export_csv
        self.export_excel = export_excel
        self.index = index
        self.keep_multiindex = keep_multiindex
        self.grid_data_in = deepcopy(grid_data)
        self.grid_options = grid_options
        self.grid_options_multi = grid_options_multi
        self.license = license
        self.hide_grid = hide_grid
        self.compress_data = compress_data
        self.export_mode = export_mode
        self.columns_fit = columns_fit
        self.show_toggle_delete = show_toggle_delete
        self.show_toggle_edit = show_toggle_edit
        self.js_helpers_custom = js_helpers_custom
        self.js_pre_helpers = js_pre_helpers
        self.js_pre_grid = js_pre_grid
        self.js_post_grid = js_post_grid
        self.menu_in = menu
        self.user_params = user_params
        self.grid_data_out = {}
        self._is_df = False

        # Checking and building correctly from the parameters given.

        bwp = BuilderParams(self)
        bwp.valid()
        bwp.build()

        super().__init__()

    # Export functions

    def get_selected_rows(self):
        """
        Exports selected rows in grid_data_out['rows'].
        Works in rowSelection or rangeSelection enabled.
        """
        self._export_mode = 'rows'
        self._counter_update_data += 1

    def get_selected_columns(self):
        """
        Exports selected columns in grid_data_out['columns'].
        Only works in rangeSelection enabled.
        """
        self._export_mode = 'columns'
        self._counter_update_data += 1

    def get_grid(self):
        """
        Exports whole grid in grid_data_out['grid'].
        """
        self._export_mode = 'grid'
        self._counter_update_data += 1

    @observe('_grid_data_up')
    def export(self, change):
        if ('rows' in self._grid_data_up.keys()):
            if self._is_df:
                self.grid_data_out['rows'] = pd.DataFrame(
                    self._grid_data_up['rows'])
            else:
                self.grid_data_out['rows'] = self._grid_data_up['rows']
        if ('grid' in self._grid_data_up.keys()):
            data_up = self._grid_data_up['grid']
            to_df = {}
            if(len(data_up['index_rows']['names']) != 0):
                to_df['index'] = pd.MultiIndex.from_tuples(
                    *[data_up['index_rows']['values']], names=data_up['index_rows']['names'])
            to_df['columns'] = pd.MultiIndex.from_tuples(
                *[data_up['index_columns']])
            to_df['data'] = data_up['data']
            self.grid_data_out['grid'] = pd.DataFrame(**to_df)
        if ('range' in self._grid_data_up.keys()):
            if self._is_df:
                self.grid_data_out['range'] = pd.DataFrame(
                    self._grid_data_up['range'])
            else:
                self.grid_data_out['range'] = self._grid_data_up['range']
        if ('cols' in self._grid_data_up.keys()):
            if self._is_df:
                self.grid_data_out['cols'] = pd.DataFrame(
                    self._grid_data_up['cols'])
            else:
                self.grid_data_out['cols'] = self._grid_data_up['cols']
        x = 0
        if 'counter' in self.grid_data_out:
            x = self.grid_data_out['counter']
        x += 1
        self.grid_data_out.pop('counter', None)
        res = {'counter': x}
        res.update(self.grid_data_out)
        self.grid_data_out = res

    # Deleting rows

    def delete_selected_rows(self):
        """
        Deletes selected rows from the rowData.
        Works in rowSelection and rangeSelection modes.
        """
        self._export_mode = 'delete'
        self._counter_update_data += 1

    def update_grid_data(self, data):
        """
        Usage : data = list or pandas dataframe.
        Replaces the data of the whole grid by the new data.
        """
        self.grid_data_in = deepcopy(data)
        bwp = BuilderParams(self)
        bwp.valid()
        bwp.build()
        self.grid_data_out = {}

    def export_html(self, build=False):
        """
        If build==True, returns a str containing HTML code 
        for embedding as a standalone widget.
        If build==False, returns a dict containing 4 parts necessary
        to put several embed widgets in the same page.
        """
        if build:
            html = export_html_code(self)
            return (html['script_tags'] +
                    (html['html_state']).format(manager_state=json.dumps(html['manager_state'])) +
                    html['grid_div'])
        return export_html_code(self)

    def dump(self, path, mode='standalone'):
        """
        Similar as export_html, but create the files in the in the 'path' directory.
        """
        if mode == 'standalone':
            with open(path+"/export_grid_standalone"+str(self._id)+".html", 'w+') as f:
                f.write(self.export_html(build=True))
        elif mode == 'all':
            widget_export = self.export_html(build=False)
            with open(path+"/export_scripts.html", "w+") as f:
                f.write(widget_export['script_tags'])
            with open(path+"/export_html_state.html", "w+") as f:
                f.write(widget_export['html_state'])
            with open(path+"/export_state_"+str(self._id)+".json", "w+") as f:
                f.write(json.dumps(widget_export['manager_state']))
            with open(path+"/export_grid_"+str(self._id)+".html", "w+") as f:
                f.write(widget_export['grid_div'])

    def show_helpers(self):
        """
        """
        dic = json.loads(self.js_helpers)
        for k,v in dic.items():
            print('\n' +k+' : '+v)
