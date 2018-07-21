#！/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/6/19 14:38
# @Author   : Run (18817363043@163.com)
# @File     : warehouse_sketch.py
# @Software : PyCharm

import math
import re
from pyecharts.chart import Chart
import pyecharts.utils as utils

class Warehouse_Sketch(Chart):
    """
    <<< 仓库平面图 >>>
    仓库的平面草图，展示不同分区的货架及巷道信息
    """

    def __init__(self, title="", subtitle="", **kwargs):
        """

        :param title:
        :param subtitle:
        :param kwargs:
            color_library_list: 自己偏好的颜色设置（注意需要足够多，不能少于legend的组数）
        """

        super(Warehouse_Sketch, self).__init__(title, subtitle, **kwargs)

        # 用于存放一些自定义的设置
        self.my_option = {}

        # 标题设置
        self._option['title'][0]['left'] = 'center'
        self._option['title'][0]["textStyle"] = {
            "fontSize": 30
        }

        # 直角坐标系内绘图网格
        self._option['grid'] = {
            'left': '5%',
            'right': '5%',
            'top': '5%',
            'bottom': '2%'
        }

        # toolbox（默认不显示工具箱）
        try:
            if 'is_toolbox_show' not in kwargs:
                self._option.pop('toolbox')
            elif not kwargs['is_toolbox_show']:
                self._option.pop('toolbox')
            else:
                pass
        except:
            pass

        # tooltip
        self._option['tooltip'] = [{}]  # 如果不加这个，方格的tooltip无法正常显示

        # 预设足够的色彩，防止不同的数据组重色
        if 'color_library_list' in kwargs:
            self._option['color'] = kwargs['color_library_list']
        # self._option['color'] = ['#AC4343', '#8E323D', '#0CAAF3', '#2788FF', '#3B4CD0', '#745CD9', '#1C6FD4', '#077F9D',
        #                          '#8DBD5E', '#45B194', '#7A574A', '#1A8C82', '#DC5FDA', '#AC62C7', '#584389', '#B4665C',
        #                          '#E4B324', '#FFA324', '#C85948']

    def add_shelf(self,
                  data_df,
                  name_col=0, x_col=1, y_col=2, legend_col=None,
                  symbol='roundRect', symbol_size=10,
                  **kwargs):
        """

        :param data_df:
        :param name_col:
        :param x_col:
        :param y_col:
        :param legend_col:
        :param symbol:
        :param symbol_size:
        :param kwargs:
        :return:
        """

        # 数据去重
        data_df = data_df.drop_duplicates().reset_index(drop=True)

        # 调整数据列顺序
        if legend_col is None:
            ignore_col_list = [x_col, y_col, name_col]
        else:
            ignore_col_list = [x_col, y_col, name_col, legend_col]
        ignore_list = data_df.columns[ignore_col_list].tolist()
        columns_list = data_df.columns.tolist()
        short_columns_list = [x for x in columns_list if x not in ignore_list]
        shelf_columns_list = ignore_list + short_columns_list  # 调换顺序后的新表头
        self.my_option['shelf_columns_list'] = shelf_columns_list
        data_df = data_df[shelf_columns_list]

        # 确定各维度范围
        margin_rate = 0.02
        x_max, x_min = data_df.iloc[:, 0].max(), data_df.iloc[:, 0].min()
        x_range = x_max - x_min
        x_max, x_min = math.ceil(x_max + margin_rate * x_range), math.floor(x_min - margin_rate * x_range)
        #
        y_max, y_min = data_df.iloc[:, 1].max(), data_df.iloc[:, 1].min()
        y_range = y_max - y_min
        y_max, y_min = math.ceil(y_max + margin_rate * y_range), math.floor(y_min - margin_rate * y_range)

        # xAxis
        self._option['xAxis'] = [{
            'type': 'value',
            'show': False,
            'inverse': False,
            'min': x_min,
            'max': x_max
        }]
        # yAxis
        self._option['yAxis'] = [{
            'type': 'value',
            'show': False,
            'inverse': False,
            'min': y_min,
            'max': y_max
        }]

        # tooltip
        def tooltip_formatter1(params):
            value = params.value
            results_str = '<div style="border-bottom: 1px solid rgba(255,255,255,.3); ' \
                          'font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">' + \
                          value[2] + '</div>'
            for i in range(3, len(value)):
                results_str += shelf_columns_list[i] + '：' + value[i] + '<br>'
            return results_str
        #
        def tooltip_formatter2(params):
            value = params.value
            results_str = '<div style="border-bottom: 1px solid rgba(255,255,255,.3); ' \
                          'font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">' + \
                          value[2] + '</div>'
            for i in range(4, len(value)):
                results_str += shelf_columns_list[i] + '：' + value[i] + '<br>'
            return results_str

        # 添加数据
        if legend_col is None:
            self._option['series'] = [{
                'type': 'scatter',
                'data': data_df.values.tolist(),
                'symbol': symbol,
                'symbolSize': symbol_size,
                "itemStyle": {
                    "emphasis": {
                        "color": "yellow"
                    }
                },
                "label": {
                    "show": True,
                    "fontSize": symbol_size - 2,
                    "formatter": '{@[2]}'
                },
                "tooltip": {
                    'padding': 10,
                    'backgroundColor': "rgba(50,50,50,0.7)",
                    'borderColor': '#777',
                    'borderWidth': 1,
                    "formatter": tooltip_formatter1
                }
            }]
        else:
            legends = data_df.iloc[:, legend_col].unique().tolist()
            legends.sort()
            # legend
            self._option['legend'] = [{
                'data': legends,
                'top': '2%',
                'right': '5%',
                # "borderColor": '#ccc',
                # "borderWidth": 2,
            }]
            # series
            self._option['series'] = []
            for legend in legends:
                self._option['series'].append({
                    'name': legend,
                    'type': 'scatter',
                    'data': data_df[data_df.iloc[:, 3] == legend].values.tolist(),
                    'symbol': symbol,
                    'symbolSize': symbol_size,
                    "itemStyle": {
                        "emphasis": {
                            "color": "yellow"
                        }
                    },
                    "label": {
                        "show": True,
                        "fontSize": symbol_size - 2,
                        "fontWeight": 'lighter',
                        "formatter": '{@[2]}'
                    },
                    "tooltip": {
                        'padding': 10,
                        'backgroundColor': "rgba(50,50,50,0.7)",
                        'borderColor': '#777',
                        'borderWidth': 1,
                        "formatter": tooltip_formatter2
                    }
                })

    def add_lane(self,
                 data_df,
                 name_col=0, x_left_col=1, y_bottom_col=2, x_right_col=3, y_top_col=4, legend_col=None,
                 **kwargs):
        """

        :param data_df:
        :param name_col:
        :param x_left_col:
        :param y_bottom_col:
        :param x_right_col:
        :param y_top_col:
        :param legend_col:
        :param kwargs:
        :return:
        """
        # 数据去重
        data_df = data_df.drop_duplicates().reset_index(drop=True)

        # 调整数据列顺序
        if legend_col is None:
            ignore_col_list = [x_left_col, y_bottom_col, x_right_col, y_top_col, name_col]
        else:
            ignore_col_list = [x_left_col, y_bottom_col, x_right_col, y_top_col, name_col, legend_col]
        ignore_list = data_df.columns[ignore_col_list].tolist()
        columns_list = data_df.columns.tolist()
        short_columns_list = [x for x in columns_list if x not in ignore_list]
        lane_columns_list = ignore_list + short_columns_list  # 调换顺序后的新表头
        self.my_option['lane_columns_list'] = lane_columns_list
        data_df = data_df[lane_columns_list]

        # tooltip
        def tooltip_formatter3(params):
            value = params.value
            results_str = '<div style="border-bottom: 1px solid rgba(255,255,255,.3); ' \
                          'font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">' + \
                          value[4] + '</div>'
            for i in range(5, len(value)):
                results_str += lane_columns_list[i] + '：' + value[i] + '<br>'
            return results_str
        #
        def tooltip_formatter4(params):
            value = params.value
            results_str = '<div style="border-bottom: 1px solid rgba(255,255,255,.3); ' \
                          'font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">' + \
                          value[4] + '</div>'
            for i in range(6, len(value)):
                results_str += lane_columns_list[i] + '：' + value[i] + '<br>'
            return results_str

        # renderItem函数
        def renderItem(params, api):
            pointLeftBottom = api.coord([api.value(0), api.value(1)])
            pointRightTop = api.coord([api.value(2), api.value(3)])
            results = {
                'type': 'rect',
                'coordinateSystem': 'cartesian2d',
                'shape': {
                    'x': pointLeftBottom[0],
                    'y': pointLeftBottom[1],
                    'width': pointRightTop[0] - pointLeftBottom[0],
                    'height': pointRightTop[1] - pointLeftBottom[1]
                },
                'style': api.style({
                    'stroke': 'rgba(0,0,0,0.1)'
                }),
                'styleEmphasis': api.styleEmphasis()
            }
            return results

        # 添加数据
        if legend_col is None:
            self._option['series'].append(
                {
                    'type': 'custom',
                    'data': data_df.values.tolist(),
                    'renderItem': renderItem,
                    "itemStyle": {
                        "emphasis": {
                            "color": "red"
                        }
                    },
                    "label": {
                        "show": True,
                        # "fontSize": 10,
                        "formatter": '{@[4]}'
                    },
                    "tooltip": {
                        'padding': 10,
                        'backgroundColor': "rgba(50,50,50,0.7)",
                        'borderColor': '#777',
                        'borderWidth': 1,
                        "formatter": tooltip_formatter3
                    }
                }
            )
        else:
            legends = data_df.iloc[:, legend_col].unique().tolist()
            legends.sort()
            for legend in legends:
                self._option['series'].append({
                    'name': legend,
                    'type': 'custom',
                    'data': data_df[data_df.iloc[:, 5] == legend].values.tolist(),
                    'renderItem': renderItem,
                    "itemStyle": {
                        "emphasis": {
                            "color": "red"
                        }
                    },
                    "label": {
                        "show": True,
                        # "fontSize": 10,
                        "formatter": '{@[4]}'
                    },
                    "tooltip": {
                        'padding': 10,
                        'backgroundColor': "rgba(50,50,50,0.7)",
                        'borderColor': '#777',
                        'borderWidth': 1,
                        "formatter": tooltip_formatter4
                    }
                })

    def render(self, path="render.html", template_name="simple_chart.html", object_name="chart", **kwargs):
        """
        将图表保存成html文件，默认占满屏幕
        :param path:
        :param template_name:
        :param object_name:
        :param kwargs:
        :return:
        """

        # 调用父类的方法生成html文件
        super(Warehouse_Sketch, self).render(path, "simple_chart.html", "chart", **kwargs)
        with open(path, 'r', encoding="utf-8") as file:
            cont = file.read()

        # 使tooltip可以正常显示
        pos1 = re.search("myChart\w*.setOption(.*?);", cont).span()[1] +1
        cont = cont[: pos1] + "var shelf_columns_list = {0};\nvar lane_columns_list={1}\n".format(self.my_option['shelf_columns_list'], self.my_option['lane_columns_list']) + cont[pos1:]

        # 使图表全屏显示
        try:
            pos2 = re.search("<html>", cont).span()[1] - 1
            cont = cont[: pos2] + ' style="height: 100%"' + cont[pos2: ]
            pos2 = re.search("<body>", cont).span()[1] - 1
            cont = cont[: pos2] + ' style="height: 100%; margin: 0"' + cont[pos2:]
            pos3, pos4 = re.search('style="width:.*?;height:.*?;"', cont).span()
            cont = cont[: pos3] + ' style="width: 100%; height: 100%;"' + cont[pos4:]
        except:
            pass

        # 保存修改后的html文件
        utils.write_utf8_html_file(path, cont)