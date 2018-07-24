import copy
import logging
from pathlib import Path

import pandas as pd
import plotly.graph_objs as go

from .colors import cl
from .utils import detect_frequency, figure_handler, recursive_update

logger = logging.getLogger(__name__)


def read_finegrained_refs(path):
    """Read fine grained reference csv file."""
    if isinstance(path, str):
        path = Path(path).absolute()
    elif isinstance(path, Path):
        path = path.absolute()
    else:
        raise TypeError('path of type {} no handled'.format(type(path)))

    df = pd.read_csv(path.as_posix())
    df = df.dropna(how='all', axis=0)  # treat void lines in csv that help the reading

    predefined_colors = [c for c in dir(cl) if not callable(c)]
    colors = []
    if 'marker.color' in df.columns.tolist():
        for i, row in df.iterrows():
            color = row['marker.color']
            if color in predefined_colors:
                colors.append(cl.__dict__[color])
            else:
                raise NotImplementedError(color)  # TODO

    df['marker.color'] = colors
    return df


def csv_refs_to_plotly_dict(serie):
    """Convert line from reference csv into kwargs for plot.
    A dot in the column name of the reference means a separator for embed keys.

    Args:
        serie (pd.Series): row of the reference csv

    Returns: (dict)
    """
    dct = dict(serie)
    plottype = dct['plottype']
    plot_obj = go.__dict__[plottype]

    # Pop Meta info keys
    for e in ['column', 'plottype', 'name']:
        if e in dct.keys():
            dct.pop(e)

    result = copy.deepcopy(dct)
    # Recreate dict from keys with '.' in the name:
    for key in dct.keys():
        lst_keys = key.split('.')

        if not lst_keys[0] in dir(plot_obj()):
            logger.info('{} is not a valid key for {} plot and will be discarded.'
                        .format(lst_keys[0], plottype))
            continue

        tree_dict = dct[key]
        for k in reversed(lst_keys):
            tree_dict = {k: tree_dict}
        result.pop(key)

        result = recursive_update(result, tree_dict)

    return result


def _compute_single_trace(serie_data, serie_spec, auto_bar_width=True):
    """Compute a single plotly trace based on serie_spec.

    Args:
        df (pd.serie_datas): serie_data to be plotted.
        serie_spec (pd.serie_datas): serie_data containing serie_specs.
        auto_bar_width (bool): if should adapt bar width

    Returns:
        plotly.trace
    """

    x_values = serie_data.index.tolist()
    y_values = serie_data.tolist()

    kwargs = csv_refs_to_plotly_dict(serie_spec)

    plottype = serie_spec['plottype']
    plottype = plottype[:1].upper() + plottype[1:].lower()

    should_add_width = all([
        auto_bar_width,
        pd.api.types.is_datetime64_any_dtype(serie_data.index),
        plottype == 'Bar',
        len(serie_data.index) >= 2,
    ])

    if should_add_width:
        freq = detect_frequency(serie_data.index)
        kwargs['width'] = ([pd.Timedelta(freq).total_seconds() * 1000] *
                           len(serie_data.index))  # witdh in milliseconds
        kwargs['width'] = [0.9 * w for w in kwargs['width']]  # only 90% of max width

    return go.__dict__[plottype](
        x=x_values,
        y=y_values,
        name=serie_spec['name'],
        legendgroup=serie_spec['name'],
        **kwargs
    )


def get_fine_grained_traces(df, path_specdf, dropzeros=True, auto_bar_width=True):
    """Return a list of traces with specification coming from a csv file.

    Args:
        df (pd.DataFrame): the dataframe to be plotted.
        path_spec (str or pathlib.Path): path to csv file containing specifications.

    Note:
        The structure of the csv file is as follow\:

        | country  | mickey | do not matter | column   | name                | plottype | marker.color | yaxix  | xaxis  | opacity | line.dash | fill    |
        +==========+========+===============+==========+=====================+==========+==============+========+========+=========+===========+=========+
        | wathever | again  | really        | velocity | velocity [m/s]      | scatter  | red          | yaxis2 | xaxis1 | 0.9     |           | tozeroy |
        +----------+--------+---------------+----------+---------------------+----------+--------------+--------+--------+---------+-----------+---------+
        | fr       | won    | worldcup      | hype     | applause level [dB] | bar      | blue_lighter | yaxis1 | xaxis1 |         | 2         |         |
        +----------+--------+---------------+----------+---------------------+----------+--------------+--------+--------+---------+-----------+---------+


        Everything before 'column' column is gonna be ignored.
        ['column', 'name', 'plottype'] are mandatory, then everything is optional.

            - 'column': column label in df
            - 'name': label in the plot (if same name, legend is grouped)
            - 'plottype': among [scatter, bar] at the moment

    Returns: a list of traces
    """

    # Some checks on the DataFrame to be plotted:
    if df.columns.duplicated().any():
        raise ValueError('Your Dataframe contains duplicated column names: '
                         '{}'.format(df.columns[df.columns.duplicated()]))

    lst_cols_df = df.columns.tolist()

    df_spec = read_finegrained_refs(path_specdf)
    # Discard columns before 'column'
    lst_cols_to_keep = df_spec.columns.tolist()
    lst_cols_to_keep = lst_cols_to_keep[lst_cols_to_keep.index('column'):]
    df_spec = df_spec[lst_cols_to_keep]

    traces = []
    for col in df_spec['column'].tolist():

        # Getting spec for that col
        spec = df_spec[df_spec['column'] == col]
        spec = spec.iloc[0].dropna()

        if spec['column'] in lst_cols_df:
            serie = df[spec['column']]

            if dropzeros:
                serie = serie[serie != 0]

            traces.append(
                _compute_single_trace(serie_data=serie, serie_spec=spec,
                                      auto_bar_width=auto_bar_width)
            )

    return traces


def get_fine_grained_figure(df, path_specdf, layout={},
                            as_figure=False, as_image=False, as_url=False,
                            **kwargs):
    traces = get_fine_grained_traces(df=df, path_specdf=path_specdf, **kwargs)
    fig = {'data': traces, 'layout': layout}
    return figure_handler(fig=fig, as_figure=as_figure, as_image=as_image,
                          as_url=as_url)
