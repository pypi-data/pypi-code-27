
import random
import ipywidgets as wg
import os

from traitlets import observe
from traitlets import Unicode, Dict, List, Int, Bool
import pandas as pd

from .__meta__ import __version_js__
from .builder_widget_params import BuilderWidgetParams

from copy import deepcopy as copy
import simplejson as json
from .util import Util
from .display import export_HTML_code


_semver_range_frontend_ = '~' + __version_js__

""" For more info on gridOptions, see https://www.ag-grid.com/documentation-main/documentation.php"""


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

    width = Int(0).tag(sync=True)
    height = Int(0).tag(sync=True)

    theme = Unicode("").tag(sync=True)
    css_rules = Unicode("").tag(sync=True)
    css_rules_use = List([]).tag(sync=True)
    license = Unicode('').tag(sync=True)

    quick_filter = Bool(True).tag(sync=True)
    export_csv = Bool(True).tag(sync=True)
    export_excel = Bool(True).tag(sync=True)
    index = Bool(False).tag(sync=True)
    keep_multiindex = Bool(True).tag(sync=True)
    hide_grid = Bool(False).tag(sync=True)
    compress_data = Bool(False).tag(sync=True)
    columns_fit = Unicode("").tag(sync=True)
    export_mode = Unicode("").tag(sync=True)
    grid_options = Dict({}).tag(sync=True)
    grid_options_multi = List([]).tag(sync=True)
    _grid_data_down = List([]).tag(
        sync=True, to_json=Util.data_to_json)
    _grid_data_up = Dict({}).tag(sync=True)
    key_delete = Bool(False).tag(sync=True)
    to_eval = List([]).tag(sync=True)
    edit_mode = Bool(True).tag(sync=True)

    # Used to parse gridData. Also using _is_df to remember the output type.
    _grid_options_json = Unicode('').tag(sync=True)
    _grid_options_multi_json = Unicode('').tag(sync=True)

    _counter_export = Int(0).tag(sync=True)
    _counter_update_data = Int(0).tag(sync=True)
    export_data = Dict({}).tag(sync=True)
    _export_mode = Unicode('').tag(sync=True)

    user_params = Dict({}).tag(sync=True)

    params = []

    def __init__(self,
                 width=0,
                 height=0,
                 theme='ag-theme-fresh',
                 css_rules="",
                 quick_filter=True,
                 export_csv=False,
                 export_excel=False,
                 key_delete=False,
                 edit_mode=False,
                 index=False,
                 keep_multiindex=True,
                 grid_data=[],
                 grid_options={},
                 grid_options_multi=[],
                 license="",
                 hide_grid=False,
                 compress_data=False,
                 columns_fit="size_to_fit",
                 export_mode="no-export",
                 verbose=False,
                 to_eval=[],
                 user_params={}):

        self._id = random.randint(0, int(1e9))

        self.width = width
        self.height = height
        self.theme = theme
        self.css_rules = css_rules
        self.quick_filter = quick_filter
        self.export_csv = export_csv
        self.export_excel = export_excel
        self.index = index
        self.keep_multiindex = keep_multiindex
        self.grid_data = []
        self.grid_data_in = copy(grid_data)
        self.grid_options = grid_options
        self.grid_options_multi = grid_options_multi
        self.license = license
        self.hide_grid = hide_grid
        self.compress_data = compress_data
        self.export_mode = export_mode
        self.columns_fit = columns_fit
        self.key_delete = key_delete
        self.edit_mode = edit_mode
        self.to_eval = to_eval
        self.user_params = user_params

        self.grid_data_out = {}
        self._is_df = False

        # Checking and building correctly from the parameters given.

        bwp = BuilderWidgetParams(self, verbose=verbose)
        bwp.valid()
        bwp.build()

        super().__init__()

    # Export functions

    def get_selected_rows(self):
        self._export_mode = 'rows'
        self._counter_update_data += 1

    def get_selected_columns(self):
        self._export_mode = 'columns'
        self._counter_update_data += 1

    def get_grid(self):
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
            to_df['columns'] = pd.MultiIndex.from_tuples(*[data_up['index_columns']])
            to_df['data'] = data_up['data']
            self.grid_data_out['grid'] = pd.DataFrame(**to_df)
        if ('range' in self._grid_data_up.keys()):
            if self._is_df:
                self.grid_data_out['range'] = pd.DataFrame(
                    self._grid_data_up['range'])
            else:
                self.grid_data_out['range'] = self._grid_data_up['range']
        if ('columns' in self._grid_data_up.keys()):
            if self._is_df:
                self.grid_data_out['columns'] = pd.DataFrame(
                    self._grid_data_up['columns'])
            else:
                self.grid_data_out['columns'] = self._grid_data_up['columns']

    # Deleting rows

    def delete_selected_rows(self):
        self._export_mode = 'delete'
        self._counter_update_data += 1

    def update_grid_data(self, data):
        self.grid_data_in = copy(data)
        bwp = BuilderWidgetParams(self, verbose=False)
        bwp.valid()
        bwp.build()
        self.grid_data_out = {}

    def export_HTML(self, build=False):
        if build:
            html = export_HTML_code(self)
            return (html['script_tags'] +
                    (html['html_state']).format(manager_state=json.dumps(html['manager_state'])) +
                    html['grid_div'])
        return export_HTML_code(self)

    def dumps_grid(self, path, mode='standalone'):
        if mode == 'standalone':
            with open(path+"/export_grid_standalone"+self._id+".html", 'w+') as f:
                f.write(self.export_HTML(build=True))
        elif mode == 'all':
            widget_export = self.export_HTML(build=False)
            with open(path+"/export_grid_scripts.html", "w+") as f:
                f.write(widget_export['script_tags'])
            with open(path+"/export_grid_html_state.html", "w+") as f:
                f.write(widget_export['html_state'])
            with open(path+"/export_grid_state_"+self._id+".json", "w+") as f:
                f.write(widget_export['manager_state'])
            with open(path+"/export_grid_grid_"+self._id+".html", "w+") as f:
                f.write(widget_export['grid_div'])
