#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import math
import subprocess
import json
import warnings
import enum
import plotly
from . import core
from . import utils
from . import plotly_utils
from ._bench_validators import validate


class NotReadyError(Exception):
    '''Raised when a resource is not prepared.'''
    pass


class Dataset(core.Dataset):
    '''Dataset class.

    Args:
        factories (list):
        extra_args (dict): Extra arguments to pass to Kernel.
            This parameter slightly affects measurement results.
        title (str):
    '''
    def __init__(self, factories, *, extra_args=None, title=None):
        super().__init__(factories, extra_args=extra_args)
        self._title = '' if title is None else title

    @property
    def title(self):
        return self._title


class Kernel(core.Kernel):
    '''Kernel class.

    Args:
        stmt:
        setup:
        label (str):
    '''
    def __init__(self, stmt='pass', setup='pass', label=None):
        super().__init__(stmt=stmt, setup=setup)
        self._label = '' if label is None else label

    @property
    def label(self):
        return self._label


class LayoutSize(object):
    '''LayoutSize class.

    Args:
        width (int):
        height (int):
        label (str):
    '''

    def __init__(self, *, width=None, height=None, label=None):
        if (width is None) or (width > 0):
            self._width = width
        else:
            raise ValueError('`width` must be greater than 0.')

        if (height is None) or (height > 0):
            self._height = height
        else:
            raise ValueError('`height` must be greater than 0.')

        self._label = '' if label is None else label

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def label(self):
        return self._label


class MeasurementMode(enum.Enum):
    '''Measurement mode.'''
    STANDARD = 1  #: Perform minimum value based measurements.
    STATISTICS = 2  #: Perform statistics based measurements.


class Benchmark(object):
    '''This class measures execution speed of given code snippets.

    Args:
        datasets (list(:class:`Dataset`)):
        dataset_sizes (list(int)):
        kernels (list(:class:`Kernel`)):
        repeat (int): Number of times the measurement is repeated.
            When zero, this value is determined automatically.
        number (int): Number of loops to execute per measurement.
            When zero, this value is determined automatically.
        measurement_mode (:class:`MeasurementMode`):
        xlabel (str): The text for a x-axis label.
        title (str): The title for a figure.
        layout_sizes (list(:class:`LayoutSize`)):
        force_gc (bool): True if force garbage collection immediately
            after generating data False otherwise.
    '''
    def __init__(
            self, *,
            datasets,
            dataset_sizes,
            kernels,
            repeat=0,
            number=0,
            measurement_mode=MeasurementMode.STANDARD,
            xlabel=None,
            title=None,
            layout_sizes=None,
            force_gc=True
    ):
        self._datasets = datasets
        self._dataset_sizes = dataset_sizes
        self._kernels = kernels
        self._repeat = repeat
        self._number = number
        self._xlabel = '' if xlabel is None else xlabel
        self._title = '' if title is None else title

        self._layout_sizes = None
        if layout_sizes is not None:
            self._layout_sizes = [LayoutSize(label='auto')] + layout_sizes

        self._force_gc = force_gc
        self._measurement_mode = measurement_mode
        self._figure = None

        validate(
            datasets=self._datasets,
            dataset_sizes=self._dataset_sizes,
            kernels=self._kernels,
            repeat=self._repeat,
            number=self._number,
            layout_sizes=self._layout_sizes
        )

    def run(self, *, disable_tqdm=False):
        results = core.bench(
            datasets=self._datasets,
            dataset_sizes=self._dataset_sizes,
            kernels=self._kernels,
            repeat=self._repeat,
            number=self._number,
            disable_tqdm=disable_tqdm,
            enable_validation=False,
            force_gc=self._force_gc
        )
        self._figure = self._create_figure(benchmark_results=results)

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

    @staticmethod
    def _create_update_menus(
            layout,
            layout_sizes=None,
            has_multiple_subplots=False
    ):
        updatemenus = []
        pos_x = 0.0

        if layout_sizes is not None:
            updatemenus.append(
                dict(
                    active=0,
                    buttons=plotly_utils.make_layout_size_buttons(layout_sizes=layout_sizes),
                    direction='down',
                    showactive=True,
                    x=pos_x,
                    xanchor='left',
                    y=1.2,
                    yanchor='top'
                )
            )
            pos_x += 0.1

        updatemenus.append(
            dict(
                active=3,
                buttons=plotly_utils.make_scale_buttons(layout=layout),
                direction='down',
                showactive=True,
                x=pos_x,
                xanchor='left',
                y=1.2,
                yanchor='top'
            )
        )
        pos_x += 0.1

        if has_multiple_subplots:
            updatemenus.append(
                dict(
                    active=0,
                    buttons=plotly_utils.make_subplot_buttons(layout=layout),
                    direction='down',
                    showactive=True,
                    x=pos_x,
                    xanchor='left',
                    y=1.2,
                    yanchor='top'
                )
            )

        return updatemenus

    def _add_standard_traces(self, *, figure, benchmark_results):
        '''Add standard traces.'''
        ndatasets = len(self._datasets)
        for i, result in enumerate(benchmark_results):
            legendgroup = str(i)
            name = self._kernels[i].label
            color = self._color(index=i)
            for j, item in enumerate(result):
                index = j + 1
                x = self._dataset_sizes
                y = [tres.best for tres in item]

                if ndatasets > 1:
                    title = self._datasets[j].title
                    suffix = ' - ' + title if title else ''
                else:
                    suffix = ''

                trace = plotly.graph_objs.Scatter(
                    x=x,
                    y=y,
                    name=name + suffix,
                    text=[tres.report_standard_info() for tres in item],
                    hoverinfo='x+text+name',
                    showlegend=True,
                    legendgroup=legendgroup,
                    line=dict(color=color),
                )
                figure.add_trace(trace, row=index, col=1)

    def _add_statistical_traces(self, *, figure, benchmark_results):
        '''Add statistical traces.'''
        ndatasets = len(self._datasets)
        for i, result in enumerate(benchmark_results):
            legendgroup = str(i)
            name = self._kernels[i].label
            color = self._color(index=i)
            error_color = self._label_rgba(colors=plotly.colors.unlabel_rgb(color) + (0.5,))
            for j, item in enumerate(result):
                index = j + 1
                x = self._dataset_sizes
                y = [tres.average for tres in item]

                if ndatasets > 1:
                    title = self._datasets[j].title
                    suffix = ' - ' + title if title else ''
                else:
                    suffix = ''

                trace = plotly.graph_objs.Scatter(
                    x=x,
                    y=y,
                    name=name + suffix,
                    text=[tres.report_statistical_info() for tres in item],
                    hoverinfo='x+text+name',
                    showlegend=True,
                    legendgroup=legendgroup,
                    line=dict(color=color),
                    error_y=dict(
                        type='data',
                        array=[tres.stdev for tres in item],
                        visible=True,
                        color=error_color
                    )
                )
                figure.add_trace(trace, row=index, col=1)

    def _add_warning_traces(self, *, figure, benchmark_results):
        for i, result in enumerate(benchmark_results):
            legendgroup = str(i)
            for j, item in enumerate(result):
                index = j + 1
                x = self._dataset_sizes
                if self._measurement_mode == MeasurementMode.STANDARD:
                    y = [tres.best for tres in item]
                else:
                    y = [tres.average for tres in item]

                indices = [i for i, tres in enumerate(item) if not tres.is_reliable()]
                trace = plotly.graph_objs.Scatter(
                    x=[x[index] for index in indices],
                    y=[y[index] for index in indices],
                    text=[item[index].warning_message().replace('\n', '<br />') for index in indices],
                    hoverinfo='x+text',
                    showlegend=False,
                    legendgroup=legendgroup,
                    mode='markers',
                    marker=dict(
                        size=10,
                        color='rgb(255,0,0)',
                        symbol='x-open'
                    )
                )
                figure.add_trace(trace, row=index, col=1)

    def _create_figure(self, *, benchmark_results):
        '''Create a figure with multiple subplots.'''
        ndatasets = len(self._datasets)

        # Suppress warnings temporarily.
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            subplots = plotly.tools.make_subplots(
                rows=ndatasets,
                cols=1,
                shared_xaxes=True,
                subplot_titles=[dataset.title for dataset in self._datasets],
                print_grid=False
            )

        fig = plotly.graph_objs.FigureWidget(subplots)

        if self._measurement_mode == MeasurementMode.STANDARD:
            self._add_standard_traces(figure=fig, benchmark_results=benchmark_results)
        else:
            self._add_statistical_traces(figure=fig, benchmark_results=benchmark_results)

        self._add_warning_traces(figure=fig, benchmark_results=benchmark_results)

        # update the layout.
        layout = fig.layout

        layout.xaxis1.update(
            title=self._xlabel,
            type='log',
            autorange=True
        )
        for i, _ in enumerate(self._datasets):
            yaxis = 'yaxis' + str(i + 1)
            layout[yaxis].update(
                title='processing time',
                type='log',
                autorange=True
            )

        layout.title = self._title
        layout.updatemenus = self._create_update_menus(
            layout=layout,
            layout_sizes=self._layout_sizes,
            has_multiple_subplots=ndatasets > 1
        )

        return fig

    def plot(self, *, auto_open=True):
        '''Create a graph locally as an HTML document.

        Args:
            auto_open (bool): If True, open the saved file in a web browser after saving.
        '''
        if self._figure is None:
            raise NotReadyError('Benchmark results are not ready yet.')

        if utils.is_interactive():
            plotly.offline.init_notebook_mode()
            plotly.offline.iplot(self._figure, show_link=False)
        else:
            plotly.offline.plot(self._figure, show_link=False, auto_open=auto_open)

    def save_as_html(self, *, filepath='temp-plot.html'):
        '''Save as a html.

        Args:
            filepath (str): The local filepath to save the outputted chart to.
                If the filepath already exists, it will be overwritten.
        '''
        if self._figure is None:
            raise NotReadyError('Benchmark results are not ready yet.')

        plotly.offline.plot(self._figure, show_link=False, auto_open=False, filename=filepath)

    def save_as_png(self, *, filepath='plot_image.png', width=1280, height=960):
        '''Save as a png.

        Args:
            filepath (str): The local filepath to save the image to.
            width (int): Specifies the width of the image in `px`.
            height (int): Specifies the height of the image in `px`.

        Returns:
            bool: True if successful, false otherwise.
        '''
        if not utils.cmd_exists('orca'):
            warnings.warn('`orca` is not installed, this function can not be used.')
            return False

        dirpath, filename = os.path.split(filepath)
        if not dirpath:
            dirpath = '.'

        if self._figure is None:
            raise NotReadyError('Benchmark results are not ready yet.')

        dumps = json.dumps(self._figure, cls=plotly.utils.PlotlyJSONEncoder)
        try:
            subprocess.check_call([
                'orca',
                'graph', dumps,
                '-d', dirpath,
                '-o', filename,
                '--width', str(width),
                '--height', str(height)
            ])
            return True
        except subprocess.CalledProcessError:
            return False
