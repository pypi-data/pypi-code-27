
import gzip
import base64

import simplejson as json
import pandas as pd

from copy import deepcopy as copy

from .util import Util
from .flexbox import FlexboxCSS


class BuilderParams:
    """
    Validating input parameters and building jsons for gridOptions and gridData
    """

    def __init__(self,
                 obj):
        """
        """
        self.obj = obj

    def valid(self):
        """
        Checks if the values for the given entries are valid.
        """

        msg = 'width must be an int (number of pixels) or a string'
        assert (isinstance(self.obj.width_in, int) or isinstance(self.obj.width_in, str)), msg

        msg = 'height must be an int (number of pixels)'
        assert isinstance(self.obj.height_in, int), msg

        li_theme=['ag-theme-fresh',
                    'ag-theme-dark',
                    'ag-theme-blue',
                    'ag-theme-material',
                    'ag-theme-bootstrap',
                    'ag-theme-balham',
                    'ag-theme-excel', ]
        msg='theme must be one of {}'.format(li_theme)
        assert self.obj.theme in li_theme, msg

        msg='css_rules must be a string'
        assert isinstance(self.obj.css_rules, str), msg

        msg='quick_filter must be a boolean'
        assert isinstance(self.obj.quick_filter, bool), msg

        msg='export_csv must be a boolean'
        assert isinstance(self.obj.export_csv, bool), msg

        msg='export_excel must be a boolean'
        assert isinstance(self.obj.export_excel, bool), msg

        msg='license must be a string'
        assert isinstance(self.obj.license, str), msg

        msg='hide_grid must be a boolean'
        assert isinstance(self.obj.hide_grid, bool), msg

        msg='keep_multiindex must be a boolean'
        assert isinstance(self.obj.keep_multiindex, bool), msg

        li_export=['disabled', 'auto', 'buttons']
        msg='export_mode must be one of {}'.format(li_export)
        assert self.obj.export_mode in li_export, msg

        li_fit=['', 'size_to_fit', 'auto']
        msg='columns_fit must be one of {}'.format(li_fit)
        assert self.obj.columns_fit in li_fit, msg

        msg='show_toggle_delete must be a boolean'
        assert isinstance(self.obj.show_toggle_delete, bool), msg

        msg='show_toggle_edit must be a boolean'
        assert isinstance(self.obj.show_toggle_edit, bool), msg

        msg='js_helpers_custom must be a str'
        assert isinstance(self.obj.js_helpers_custom, str), msg

        msg='js_pre_helpers must be a list of str'
        assert isinstance(self.obj.js_pre_helpers, list), msg
        if isinstance(self.obj.js_pre_helpers, list):
            msg='each element of js_pre_helpers must be a str'
            for e in self.obj.js_pre_helpers:
                assert isinstance(e, str), msg
        self.obj.js_pre_helpers=self.obj.js_pre_helpers

        msg='js_pre_grid must be a list of str'
        assert isinstance(self.obj.js_pre_grid, list), msg
        if isinstance(self.obj.js_pre_grid, list):
            msg='each element of js_pre_grid must be a str'
            for e in self.obj.js_pre_grid:
                assert isinstance(e, str), msg
        self.obj.js_pre_grid=self.obj.js_pre_grid

        msg='js_post_grid must be a list of str'
        assert isinstance(self.obj.js_post_grid, list), msg
        if isinstance(self.obj.js_post_grid, list):
            msg='each element of js_post_grid must be a str'
            for e in self.obj.js_post_grid:
                assert isinstance(e, str), msg
        self.obj.js_post_grid=self.obj.js_post_grid

        if self.obj.menu_in is None:
            self.obj.menu_in={}
        msg='menu must be a dict'
        assert isinstance(self.obj.menu_in, dict), msg
        if 'buttons' in self.obj.menu_in.keys():
            msg='menu["buttons"] must be a list'
            assert isinstance(self.obj.menu_in['buttons'], list), msg
            msg='each element of menu["buttons"] must be a dict with "name" and "action" as keys and string as values'
            for e in self.obj.menu_in['buttons']:
                assert 'name' in e, msg
                assert 'action' in e, msg
                assert isinstance(e['name'], str), msg
                assert isinstance(e['action'], str), msg

        msg='grid_data must be a list or a dataframe'
        assert isinstance(self.obj.grid_data_in,
                          (list, pd.core.frame.DataFrame)), msg
        if isinstance(self.obj.grid_data_in, list):
            msg='each element of grid_data must be a dict'
            for e in self.obj.grid_data_in:
                assert isinstance(e, dict), msg
            self.obj._is_df=False
        else:
            self.obj._is_df=True

        msg='both grid_options and grid_options_multi cannot be set'
        assert ((self.obj.grid_options == {}) or
                (self.obj.grid_options_multi == [])), msg

        msg='one exactly of grid_options or grid_options_multi mut be set'
        assert not((self.obj.grid_options == {}) and
                   (self.obj.grid_options_multi == [])), msg

        if self.obj.grid_options == {}:
            self.obj._is_grid_options_multi=True
        else:
            self.obj._is_grid_options_multi=False

        if self.obj.grid_options != {}:
            msg='grid_options must be a dict'
            assert isinstance(self.obj.grid_options, dict), msg

        if self.obj.grid_options_multi != []:
            msg='grid_options_multi must be a list or a tuple'
            assert isinstance(self.obj.grid_options_multi, (list, tuple)), msg
            msg1='each element of grid_options_multi must be a list or tuple of length 2'
            msg2='in each grid_options_multi element of length 2, the first one must be a string'
            msg3='in each grid_options_multi element of length 3, the second one must be a dict'
            for e in self.obj.grid_options_multi:
                assert isinstance(e, (list, tuple)) and len(e) == 2, msg1
                assert isinstance(e[0], str), msg2
                assert isinstance(e[1], dict), msg3

    def build(self):
        """
        """

        # Manage width
        if isinstance(self.obj.width_in, int):
            self.obj.width=str(self.obj.width_in) + 'px'
        else:
            self.obj.width=self.obj.width_in

        # Manage height
        if self.obj.height_in == 0:
            self.obj.height_in=350
        self.obj.height=str(self.obj.height_in) + 'px'

        if self.obj.theme == 'ag-theme-excel':
            self.obj.grid_options['suppressColumnVirtualisation']=True

        # Setting menu, depending on the gridOptions
        menu_in=self.obj.menu_in
        menu={'buttons': []}

        if not ('buttons' in menu_in):
            menu_in['buttons']=[]

        def addButton(menu_a, name, action):
            found=False
            for button in menu_a['buttons']:
                if button['name'] == name:
                    button['action']=action
                    found=True
            if not found:
                menu_a['buttons'].append({'name': name, 'action': action})

        # Add csv export
        if self.obj.export_csv:
            addButton(
                menu_in, 'Export to CSV',
                      'console.log("exporting to CSV"); helpers.exportToCsv(gridOptions);')

        # Add excel export
        if self.obj.export_excel:
            addButton(
                menu_in, 'Export to Excel',
                'console.log("exporting to Excel"); helpers.exportToExcel(gridOptions);')

        if self.obj.export_mode == 'buttons':
            # Add export data from selected range selection
            addButton(
                menu_in, 'Export Grid',
                'exportFunc.exportGrid(gridOptions, view, parseInt(inputAggregationLevel.value, 10))')

            if 'enableRangeSelection' in self.obj.grid_options and self.obj.grid_options[
                    'enableRangeSelection']:
                # Add export data from selected range selection
                addButton(menu_in, 'Export Range Data', 'exportFunc.exportData(gridOptions, view)')

                # Add export columns from selected range selection
                addButton(menu_in, 'Export Columns', 'exportFunc.exportColumns(gridOptions, view)')

                # Add export rows from selected range selection
                addButton(menu_in, 'Export Rows', 'exportFunc.exportRowsOfRange(gridOptions, view)')

            if 'rowSelection' in self.obj.grid_options:
                # Add export rows from selected rows
                addButton(menu_in, 'Export Rows', 'exportFunc.exportRows(gridOptions, view)')

        # Build button CSS
        menu_in['button_default_css']=FlexboxCSS(menu_in.get(
            'button_default_css', {'font-size': '12px', 'width': '150px'}), kind='item')

        for button in menu_in['buttons']:
            options={}
            if 'custom_css' in button:
                options=button['custom_css']
            if 'css' in button:
                button['css']=button['css'].build_css(button['name'].lower().replace(
                    ' ', '-')+'-'+str(self.obj._id), opt_dic=options)
            else:
                button['css']=menu_in['button_default_css'].build_css(
                    button['name'].lower().replace(' ', '-')+'-'+str(self.obj._id), opt_dic=options)
            menu['buttons'].append(button)

        # Manage menu CSS
        if not ('button_div_css' in menu_in):
            menu_in['button_div_css']=FlexboxCSS({}, kind='container')
        else:
            menu_in['button_div_css']=FlexboxCSS(menu_in['button_div_css'], kind='container')

        menu['button_div_css']=menu_in['button_div_css'].build_css(
            'button-div-' + str(self.obj._id))

        if not ('input_div_css' in menu_in):
            menu_in['input_div_css']=FlexboxCSS({}, kind='container')
        else:
            menu_in['input_div_css']=FlexboxCSS(menu_in['input_div_css'], kind='container')

        menu['input_div_css']=menu_in['input_div_css'].build_css('input-div-'+str(self.obj._id))

        if not ('menu_div_css' in menu_in):
            menu_in['menu_div_css']=FlexboxCSS({}, kind='container')
        else:
            menu_in['menu_div_css']=FlexboxCSS(menu_in['menu_div_css'], kind='container')

        menu['menu_div_css']=menu_in['menu_div_css'].build_css('menu-div-'+str(self.obj._id))

        self.obj.menu=menu

        # licence
        self.obj.license=Util.encode_b64(self.obj.license)

        # css rules down
        self.obj.css_rules_down=Util.build_css_rules(self.obj.css_rules)

        # manage multi options
        is_multi=True if self.obj.grid_options_multi != [] else False

        if is_multi:
            grid_options_multi_2=[]
            for name, options in self.obj.grid_options_multi:
                self.obj._grid_data_down, options_2=self.preprocess_input(
                    self.obj.grid_data_in,
                    options,
                    index=self.obj.index,
                    keep_multiindex=self.obj.keep_multiindex)
                grid_options_multi_2.append((name, options_2))
            self.obj.grid_options_multi_json=grid_options_multi_2

        else:
            self.obj._grid_data_down, self.obj.grid_options=self.preprocess_input(
                self.obj.grid_data_in,
                self.obj.grid_options,
                index=self.obj.index,
                keep_multiindex=self.obj.keep_multiindex)

        if is_multi:
            self.obj._grid_options_multi_down=Util.build_options(
                {'data': self.obj.grid_options_multi}, True)
        else:
            self.obj._grid_options_mono_down=Util.build_options(
                self.obj.grid_options, False)

        # js builtin helpers
        self.obj._js_helpers_builtin = Util.load_file('js','helpersBuiltin.js')
        
        # js custom helpers
        if self.obj.js_helpers_custom == '':
            self.js_helpers_custom = 'helpersCustom = {}'

    def preprocess_input(self,
                         grid_data,
                         grid_options,
                         index,
                         keep_multiindex):
        """
        """
        if Util.is_df(grid_data):
            self.obj._is_df=True
        else:
            self.obj._is_df=False

        if Util.is_multiindex_df(grid_data):
            grid_data_2, grid_options_2=Util.prepare_multiindex_df(
                grid_data,
                grid_options,
                index=index,
                keep_multiindex=keep_multiindex)

        elif Util.is_df(grid_data):
            grid_data_2, grid_options_2=Util.prepare_singleindex_df(
                grid_data,
                grid_options,
                index=index)

        else:
            grid_data_2, grid_options_2=grid_data, grid_options

        grid_options_2=Util.update_columnTypes(
            grid_options_2)

        return Util.build_data(grid_data_2), grid_options_2

    def to_dict(self):
        """
        """
        d=copy(self.__dict__)
        d={k: v for k, v in d.items() if v is not None}
        return d

    def pprint(self, indent=2):
        """
        """
        d=json.dumps(self.to_dict(),
                       sort_keys=True,
                       indent=indent)
        print(d)

    def __repr__(self):
        return str(self.to_dict())
