import traceback
import os
from .plot_with_plotly import generate_graph_layout
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output, State


def gen(simulation, parameter_mask, names, title, header, truncate_rounds, texts, pages):
    form = [html.P("scroll down to start")]

    inputs = []
    converter = []

    for parameter, value in list(parameter_mask.items()):
        try:
            title = names[parameter]
        except KeyError:
            title = parameter

        if value is None:
            form.append(dcc.Markdown(title))
            continue

        inputs.append(State(parameter, 'value'))

        if isinstance(value, bool):
            form.append(html.Div(children=[title, dcc.RadioItems(id=parameter,
                                                                 options=[{'label': 'True', 'value': True},
                                                                          {'label': 'False', 'value': False}],
                                                                 value=value,
                                                                 labelStyle={'display': 'inline-block'})]))
            converter.append(bool)

        elif isinstance(value, list):
            options = []
            for option in value:
                options.append({'label': option, 'value': option})

            form.append(html.Div(children=[title, dcc.RadioItems(id=parameter,
                                                                 options=options,
                                                                 value=value[0])]))
            converter.append(lambda x: x)

        elif isinstance(value, str):
            form.append(html.Div(children=[title, dcc.Textarea(id=parameter,
                                     placeholder=title,
                                     value=value)]))
            converter.append(str)

        elif isinstance(value, int):
            form.append(html.Div(children=[title,
                                           dcc.Input(id=parameter,
                                                     placeholder=value,
                                                     type='numeric',
                                                     value=value)]))
            converter.append(int)

        elif isinstance(value, float):
            form.append(html.Div(children=[title,
                                           dcc.Input(id=parameter,
                                                     placeholder=value,
                                                     type='numeric',
                                                     value=value)]))
            converter.append(float)
        else:

            if isinstance(value, tuple):
                try:
                    min_value, default, max_value, step = value
                except ValueError:
                    min_value, default, max_value = value
                    step = (max_value - min_value) / 100

                if (isinstance(min_value, float) or
                    isinstance(default, float) or
                    isinstance(max_value, float) or
                    isinstance(step, float)):
                        dspstep = (max_value - min_value) / 10
                        form.append(html.Div(children=[title,
                            dcc.Slider(id=parameter,
                                       min=min_value, max=max_value, step=step, value=default,
                                       marks={n: str(n)
                                              for n in np.arange(min_value, max_value, dspstep)})]))
                        converter.append(float)
                else:
                    dspstep = max(1, int((max_value - min_value) / 10))
                    form.append(html.Div(children=[title,
                                                   dcc.Slider(id=parameter,
                                                              min=min_value, max=max_value, step=step, value=default,
                                                              marks={n: str(n)
                                                                     for n in range(min_value, max_value, dspstep)})]))
                    converter.append(int)


    form.append(html.Button('Run Simulation', id='run_btn', type="submit"))

    form.append(html.Div(children=[dcc.Textarea(id='saveas',
                                                placeholder="Save as",
                                                value='abcEconomicsSim'),
                                   html.Button('Save', id='save_btn')]))

    try:
        graphs = generate_graph_layout('')
    except FileNotFoundError:
        graphs = html.Div()

    layout = html.Div(children=[
        html.H1(children=title),
        dcc.Markdown(header),
        dcc.Tabs(id='graphs', children=[
                 dcc.Tab(label='Run', children=html.Div(children=form), value=10),
                 dcc.Tab(id='result', label='Result', children=graphs, value=1)],
                 value=10)])

    return layout, inputs, converter


def newest_subdirectory(directory='.', name=''):
    """ Returns the newes subdirectory in the 'directory/name' directory """
    directory = os.path.abspath(directory)
    all_subdirs = [os.path.join(directory, name)
                   for name in os.listdir(directory)
                   if os.path.isdir(os.path.join(directory, name))]
    all_subdirs = sorted(all_subdirs, key=os.path.getmtime, reverse=True)
    for subdir in all_subdirs:
        if name in subdir:
            return subdir + '/'
    raise Exception('No result/* directory')


def dashgui(simulation, parameter_mask, names, title, header, truncate_rounds, texts, pages):
    app = dash.Dash()

    app.layout, inputs, converter = gen(simulation, parameter_mask, names, title, header, truncate_rounds, texts, pages)

    @app.callback(Output('result', 'children'),
                  [Input('run_btn', 'n_clicks')],
                  inputs)
    def call_simulation(clicks, *parameters):
        print("HERE")
        if clicks is not None:
            params = []
            for i, param in enumerate(parameters):
                try:
                    params.append(converter[i](param))
                except Exception as e:
                    problem = "Parameter %s not of type %s: %s " % (list(parameter_mask.keys())[i], str(converter[i]), str(e))
                    print(problem)
                    return html.Div(children=[problem])

            params = dict(zip(parameter_mask.keys(), params))
            print(params)
            try:
                simulation(params)
            except Exception as e:
                traceback.print_exc()
                return html.Div(children=["The simulation produced an error with this particular parameterisation", str(type(e)), str(e)])

            return generate_graph_layout(newest_subdirectory('./result', ''))
        else:
            return html.Div()

    app.run_server(debug=True, use_reloader=False)
