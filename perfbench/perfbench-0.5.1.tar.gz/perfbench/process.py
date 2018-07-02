#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import timeit
import itertools
import math
import subprocess
import json
import warnings
import plotly
from IPython.core.magics.execution import TimeitResult
from . import utils
from . import plotly_utils


try:
    if utils.is_interactive():
        from tqdm import tqdm_notebook as tqdm
    else:
        from tqdm import tqdm

except ImportError:
    tqdm = lambda x: x


def _determine_number(timer):
    '''Determine number so that 0.2 <= total time < 2.0'''
    number = 0
    for index in range(0, 10):
        number = 10 ** index
        time_number = timer.timeit(number=number)
        if time_number >= 0.2:
            break

    return number


def _bench(datasets, dataset_sizes, kernels, number=0, repeat=0, disable_tqdm=False):
    if repeat == 0:
        default_repeat = 7 if timeit.default_repeat < 7 else timeit.default_repeat
        repeat = default_repeat

    shape = (len(kernels), len(datasets))
    res = utils.create_empty_array_of_shape(shape)
    for i, j in itertools.product(range(shape[0]), range(shape[1])):
        res[i][j] = []

    for i, dataset in enumerate(tqdm(datasets, disable=disable_tqdm)):
        s_stmt = dataset.get('stmt')
        old_s_stmt = dataset.get('func')
        if old_s_stmt is not None:
            warnings.warn('`func` is deprecated. Use `stmt`.')
            s_stmt = old_s_stmt

        for j, dataset_size in enumerate(tqdm(dataset_sizes, disable=disable_tqdm)):
            data = s_stmt(dataset_size)
            for k, kernel in enumerate(kernels):
                k_stmt = kernel.get('stmt')
                old_k_stmt = kernel.get('func')
                if old_k_stmt is not None:
                    warnings.warn('`func` is deprecated. Use `stmt`.')
                    k_stmt = old_k_stmt

                timer = timeit.Timer(stmt=lambda: k_stmt(data))
                loops = number if number > 0 else _determine_number(timer)

                all_runs = timer.repeat(repeat=repeat, number=loops)
                best = min(all_runs) / loops
                worst = max(all_runs) / loops

                res[k][i].append(TimeitResult(loops, repeat, best, worst, all_runs, 0, 3))

    return res


class Benchmark(object):

    def __init__(self, *,
                 datasets=None,
                 setups=None,
                 dataset_sizes=None,
                 ntimes=None,
                 kernels,
                 number=0,
                 repeat=0,
                 xlabel=None,
                 title=None,
                 logx=False):
        self._datasets = datasets
        if setups is not None:
            warnings.warn('`setups` is deprecated. Use `datasets`.')
            self._datasets = setups
        self._dataset_sizes = dataset_sizes
        if ntimes is not None:
            warnings.warn('`ntimes` is deprecated. Use `dataset_sizes`.')
            self._dataset_sizes = ntimes
        self._kernels = kernels
        self._number = number
        self._repeat = repeat
        self._xlabel = '' if xlabel is None else xlabel
        self._title = '' if title is None else title
        self._logx = logx
        self._results = None

    def run(self, disable_tqdm=False):
        self._results = _bench(
            datasets=self._datasets,
            dataset_sizes=self._dataset_sizes,
            kernels=self._kernels,
            number=self._number,
            repeat=self._repeat,
            disable_tqdm=disable_tqdm
        )

    @property
    def _xaxis_type(self):
        return 'log' if self._logx else '-'

    @classmethod
    def _default_colors(cls):
        return plotly.colors.DEFAULT_PLOTLY_COLORS

    @classmethod
    def _color(cls, *, index):
        colors = cls._default_colors()
        return colors[index % len(colors)]

    @staticmethod
    def _axis_range(sequence, use_log_scale=False):
        ar = [min(sequence), max(sequence)]
        if use_log_scale:
            ar[0] = math.log10(ar[0])
            ar[1] = math.log10(ar[1])
        return ar

    @staticmethod
    def _label_rgba(colors):
        return 'rgba({}, {}, {}, {})'.format(colors[0], colors[1], colors[2], colors[3])

    @staticmethod
    def _calc_filled_line(x, y, delta):
        x_rev = x[::-1]
        y_upper = [a + b for a, b in zip(y, delta)]
        y_lower = [a - b for a, b in zip(y, delta)]
        y_lower = y_lower[::-1]
        return x+x_rev, y_upper+y_lower

    def _create_figure(self):
        '''Create a figure with multiple subplots.'''
        ndatasets = len(self._datasets)
        fig = plotly.tools.make_subplots(
            rows=ndatasets,
            cols=1,
            shared_xaxes=True,
            subplot_titles=[dataset.get('title', '') for dataset in self._datasets],
            print_grid=False
        )

        # for averages.
        for i, result in enumerate(self._results):
            legendgroup = str(i)
            name = self._kernels[i].get('label', '')
            color = self._color(index=i)
            for j, item in enumerate(result):
                index = j + 1
                x = self._dataset_sizes
                y = [tres.average for tres in item]

                if ndatasets > 1:
                    title = self._datasets[j].get('title', '')
                    suffix = ' - ' + title if title else ''
                else:
                    suffix = ''

                trace = plotly.graph_objs.Scatter(
                    x=x,
                    y=y,
                    name=name + suffix,
                    text=[tres.__str__() for tres in item],
                    hoverinfo='x+text+name',
                    showlegend=True,
                    legendgroup=legendgroup,
                    line=dict(color=color)
                )
                fig.append_trace(trace, index, 1)

        # for standard deviations.
        for i, result in enumerate(self._results):
            legendgroup = str(i)
            color = self._color(index=i)
            for j, item in enumerate(result):
                index = j + 1
                x = self._dataset_sizes
                y = [tres.average for tres in item]
                fillcolor = self._label_rgba(colors=plotly.colors.unlabel_rgb(color) + (0.1,))
                fx, fy = self._calc_filled_line(x=x, y=y, delta=[tres.stdev for tres in item])
                trace = plotly.graph_objs.Scatter(
                    x=fx,
                    y=fy,
                    hoverinfo='x',
                    showlegend=False,
                    legendgroup=legendgroup,
                    line=dict(color='rgba(255,255,255,0)'),
                    fill='tozerox',
                    fillcolor=fillcolor
                )
                fig.append_trace(trace, index, 1)

        # update the layout.
        fig['layout']['xaxis1'].update(
            title=self._xlabel,
            type=self._xaxis_type,
            range=self._axis_range(sequence=self._dataset_sizes, use_log_scale=self._logx)
        )
        for i, _ in enumerate(self._datasets):
            yaxis = 'yaxis' + str(i + 1)
            fig['layout'][yaxis].update(
                title='processing time',
                type='log',
                autorange=True
            )

        if ndatasets > 1:
            updatemenus = list([
                dict(
                    active=0,
                    buttons=plotly_utils.make_subplot_buttons(fig),
                    direction='down',
                    showactive=True,
                    x=0.0,
                    xanchor='left',
                    y=1.2,
                    yanchor='top'
                )
            ])
        else:
            updatemenus = []

        fig['layout'].update(title=self._title, updatemenus=updatemenus)

        return fig

    def show(self):
        '''for backward compatibility.'''
        warnings.warn('This function will be removed soon.')
        self.plot()

    def plot(self, *, auto_open=True):
        fig = self._create_figure()
        if utils.is_interactive():
            plotly.offline.init_notebook_mode()
            plotly.offline.iplot(fig, show_link=False)
        else:
            plotly.offline.plot(fig, show_link=False, auto_open=auto_open)

    def save_as_html(self, *, filepath='temp-plot.html'):
        fig = self._create_figure()
        plotly.offline.plot(fig, show_link=False, auto_open=False, filename=filepath)

    def save_as_png(self, *, filepath='plot_image.png'):
        if not utils.cmd_exists('orca'):
            warnings.warn('`orca` is not installed, this function can not be used.')
            return False

        fig = self._create_figure()
        dumps = json.dumps(fig)
        try:
            subprocess.check_call(['orca', 'graph', dumps, '-o', filepath])
            return True
        except subprocess.CalledProcessError:
            return False
