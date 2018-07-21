#！/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/6/4 23:58
# @Author   : Run (18817363043@163.com)
# @File     : map_bin_bubble.py
# @Software : PyCharm

import math
import re
import pandas as pd
from pyecharts_plus import Map_Bin_Scatter
import pyecharts.utils as utils


class Map_Bin_Bubble(Map_Bin_Scatter):
    """
    <<< 散点图的变种 >>>
    背景是地图，中间层是方格热力图，前景是气泡图（4D）

    注意：
        1. 添加数据时，必须先添加方格热力图，后添加散点图 （待提高）
        2. 一张图里只能有一条时间轴，方格热力图的时间轴不可以和散点图的热力图共存 （不可提高）
        3. 无论在方格热力图还是在散点图中指定了添加搜索框功能，该搜索功能既可以用于搜索方格也可以用于搜索散点
    """

    def __init__(self, title="", subtitle="", **kwargs):
        """

        :param title:
        :param subtitle:
        :param kwargs:
        """

        super(Map_Bin_Bubble, self).__init__(title, subtitle, **kwargs)
        # self._option['color'] = ['#AC4343', '#8E323D', '#0CAAF3', '#2788FF', '#3B4CD0', '#745CD9', '#1C6FD4', '#077F9D',
        #                          '#8DBD5E', '#45B194', '#7A574A', '#1A8C82', '#DC5FDA', '#AC62C7', '#584389', '#B4665C',
        #                          '#E4B324', '#FFA324', '#C85948']

    def add_bubble(self,
                   data_df,
                   name_col=0, lgt_col=1, lat_col=2, size_col=None, lightness_col=None, legend_col=5,
                   time_line_col=None, time_line_order=None, checkpoint_symbol='circle',
                   search_box=True):
        """

        :param data_df:
        :param name_col:
        :param lgt_col:
        :param lat_col:
        :param size_col:
        :param lightness_col:
        :param legend_col:
        :param time_line_col:
        :param time_line_order:
        :param checkpoint_symbol:
        :param search_box:
        :return:
        """

        # 时间轴冲突性检测
        if self.my_option['binmap_time_line_col'] is not None and time_line_col is not None:
            raise Exception("timeline contradict!")

        # 没有时间轴
        if self.my_option['binmap_time_line_col'] is None and time_line_col is None:

            # 气泡图数据组数
            self.my_option['scatter_group_num'] = len(data_df.iloc[:, legend_col].unique())
            # 预设visualMap的模板
            self.my_option['visualMap_size'] = {
                "backgroundColor": "#f4f4f4",
                "borderWidth": 2,
                "borderColor": "#e3e3e3",
                "seriesIndex": list(range(1, self.my_option['scatter_group_num'] + 1)),
                "right": 10,
                "calculable": True,
                "controller": {
                    "inRange": {
                        "color": [
                            "#c23531"
                        ]
                    },
                    "outOfRange": {
                        "color": [
                            "#444"
                        ]
                    }
                },
                "inRange": {
                    "symbolSize": [
                        10,
                        100
                    ]
                },
                "textGap": 30,
                "outOfRange": {
                    "symbolSize": [
                        10,
                        100
                    ],
                    "color": [
                        "rgba(255,255,255,.2)"
                    ]
                },
                "textStyle": {
                    "color": "#333"
                },
                "precision": 0.1
            }
            self.my_option['visualMap_lightness'] = {
                "backgroundColor": "#f4f4f4",
                "borderWidth": 2,
                "borderColor": "#e3e3e3",
                "seriesIndex": list(range(1, self.my_option['scatter_group_num'] + 1)),
                "right": 10,
                "calculable": True,
                "controller": {
                    "inRange": {
                        "color": [
                            "#c23531"
                        ]
                    },
                    "outOfRange": {
                        "color": [
                            "#444"
                        ]
                    }
                },
                "inRange": {
                    "colorLightness": [
                        1,
                        0.5
                    ]
                },
                "textGap": 30,
                "precision": 0.1,
                "outOfRange": {
                    "color": [
                        "rgba(255,255,255,.2)"
                    ]
                },
                "textStyle": {
                    "color": "#333"
                }
            }

            # 调整数据列顺序/设置visualMap
            if size_col is None and lightness_col is None:
                ignore_col_list = [lgt_col, lat_col, name_col, legend_col]
            elif size_col is not None and lightness_col is None:
                ignore_col_list = [lgt_col, lat_col, name_col, legend_col, size_col]
                #
                size_max = data_df.iloc[:, size_col].max()
                size_min = data_df.iloc[:, size_col].min()
                size_range = size_max - size_min
                size_max = math.ceil(size_max + 0.05 * size_range)
                size_min = math.floor(size_min - 0.05 * size_range)
                #
                self._option['visualMap'].append(self.my_option['visualMap_size'])
                self._option['visualMap'][1]['text'] = ['圆形大小：{0}'.format(data_df.columns[size_col])]
                self._option['visualMap'][1]['dimension'] = 4
                self._option['visualMap'][1]['max'] = size_max
                self._option['visualMap'][1]['min'] = size_min
            elif size_col is None and lightness_col is not None:
                ignore_col_list = [lgt_col, lat_col, name_col, legend_col, lightness_col]
                #
                lightness_max = data_df.iloc[:, lightness_col].max()
                lightness_min = data_df.iloc[:, lightness_col].min()
                lightness_range = lightness_max - lightness_min
                lightness_max = math.ceil(lightness_max + 0.05 * lightness_range)
                lightness_min = math.floor(lightness_min - 0.05 * lightness_range)
                #
                self._option['visualMap'].append(self.my_option['visualMap_lightness'])
                self._option['visualMap'][1]['text'] = ['颜色明暗：{0}'.format(data_df.columns[lightness_col])]
                self._option['visualMap'][1]['dimension'] = 4
                self._option['visualMap'][1]['max'] = lightness_max
                self._option['visualMap'][1]['min'] = lightness_min
            elif size_col != lightness_col:
                ignore_col_list = [lgt_col, lat_col, name_col, legend_col, size_col, lightness_col]
                #
                size_max = data_df.iloc[:, size_col].max()
                size_min = data_df.iloc[:, size_col].min()
                size_range = size_max - size_min
                size_max = math.ceil(size_max + 0.05 * size_range)
                size_min = math.floor(size_min - 0.05 * size_range)
                #
                lightness_max = data_df.iloc[:, lightness_col].max()
                lightness_min = data_df.iloc[:, lightness_col].min()
                lightness_range = lightness_max - lightness_min
                lightness_max = math.ceil(lightness_max + 0.05 * lightness_range)
                lightness_min = math.floor(lightness_min - 0.05 * lightness_range)
                #
                self._option['visualMap'].append(self.my_option['visualMap_size'])
                self._option['visualMap'][1]['text'] = ['圆形大小：{0}'.format(data_df.columns[size_col])]
                self._option['visualMap'][1]['dimension'] = 4
                self._option['visualMap'][1]['max'] = size_max
                self._option['visualMap'][1]['min'] = size_min
                self._option['visualMap'][1]['top'] = '15%'
                #
                self._option['visualMap'].append(self.my_option['visualMap_lightness'])
                self._option['visualMap'][2]['text'] = ['颜色明暗：{0}'.format(data_df.columns[lightness_col])]
                self._option['visualMap'][2]['dimension'] = 5
                self._option['visualMap'][2]['max'] = lightness_max
                self._option['visualMap'][2]['min'] = lightness_min
                self._option['visualMap'][2]['bottom'] = '15%'
            else:
                ignore_col_list = [lgt_col, lat_col, name_col, legend_col, size_col]
                #
                size_max = data_df.iloc[:, size_col].max()
                size_min = data_df.iloc[:, size_col].min()
                size_range = size_max - size_min
                size_max = math.ceil(size_max + 0.05 * size_range)
                size_min = math.floor(size_min - 0.05 * size_range)
                #
                self._option['visualMap'].append(self.my_option['visualMap_size'])
                self._option['visualMap'][1]['text'] = ['圆形大小：{0}'.format(data_df.columns[size_col])]
                self._option['visualMap'][1]['dimension'] = 4
                self._option['visualMap'][1]['max'] = size_max
                self._option['visualMap'][1]['min'] = size_min
                self._option['visualMap'][1]['top'] = '15%'
                #
                self._option['visualMap'].append(self.my_option['visualMap_lightness'])
                self._option['visualMap'][2]['text'] = ['颜色明暗：{0}'.format(data_df.columns[lightness_col])]
                self._option['visualMap'][2]['dimension'] = 4
                self._option['visualMap'][2]['max'] = size_max
                self._option['visualMap'][2]['min'] = size_min
                self._option['visualMap'][2]['bottom'] = '15%'
            #
            ignore_list = data_df.columns[ignore_col_list].tolist()
            bubble_columns_list = data_df.columns.tolist()
            short_columns_list = [x for x in bubble_columns_list if x not in ignore_list]
            bubble_columns_list = ignore_list + short_columns_list  # 调换顺序后的新表头
            self.my_option['bubble_columns_list'] = bubble_columns_list

            data_df = data_df[bubble_columns_list]

            #
            self.add_scatter(data_df, lgt_col=0, lat_col=1, name_col=2, legend_col=3, time_line_col=time_line_col, time_line_order=time_line_order,
                         checkpoint_symbol=checkpoint_symbol, search_box=search_box)
            self.my_option['scatter_columns_list'] = bubble_columns_list

            # 去除气泡图数据中对symbol大小和形状的设置
            for i in range(1, self.my_option['scatter_group_num'] + 1):
                del self._option['series'][i]['symbol'], self._option['series'][i]['symbolSize']












