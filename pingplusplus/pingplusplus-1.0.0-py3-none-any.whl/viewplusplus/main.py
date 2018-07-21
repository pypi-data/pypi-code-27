from datetime import datetime
import pathlib
import csv
from werkzeug.serving import run_simple
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .settings import get_settings, get_argument_parser


#
#  Reference : https://plot.ly/python/reference/
#

#    Nice colors
# 
#    '#1f77b4',  // muted blue
#    '#ff7f0e',  // safety orange
#    '#2ca02c',  // cooked asparagus green
#    '#d62728',  // brick red
#    '#9467bd',  // muted purple
#    '#8c564b',  // chestnut brown
#    '#e377c2',  // raspberry yogurt pink
#    '#7f7f7f',  // middle gray
#    '#bcbd22',  // curry yellow-green
#    '#17becf'   // blue-teal
#


class TrendApplication():
    def __init__(self, glob):
        self.root_path = pathlib.Path(".")
        self.glob = glob
        self.dashapp = dash.Dash()
        self.dashapp.title = 'Ping++ Data Visualization'
        self.dashapp.css.config.serve_locally = True
        self.dashapp.scripts.config.serve_locally = True
        self.get_csv_filenames()
        self.init_html()
    
    def run(self, host, port):
        application = self.dashapp.server
        run_simple(
            host,
            port,
            application,
            use_reloader=False,
            use_debugger=False,
            threaded=True)

    def get_csv_filenames(self):
        return list(sorted(self.root_path.glob(self.glob)))
    
    def get_values_from_csv(self, filename):
            abs_csvfile = str(pathlib.Path(self.root_path).joinpath(filename))
            with open(abs_csvfile) as csvfile:
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                reader = csv.reader(csvfile, dialect)
                headers = next(reader)
                headers = list(h.lower() for h in headers)
                assert headers == ["name", "time", "avg", "max", "errors", "tries"]
                for name, time_s, avg_s, max_s, err_s, len_s in reader:
                    time_t = datetime.strptime(time_s, "%Y-%m-%d %H:%M")
                    avg_f = float(avg_s)
                    max_f = float(max_s)
                    err_f = float(err_s) / float(len_s) * 100
                    yield time_t, avg_f, max_f, err_f

    
    def init_html(self):
        self.dashapp.layout = html.Div([
            html.Div([
                html.H3('CSV data'),
                dcc.Dropdown(
                    id='csv-file-list',
                    searchable=False
                )
            ]),

            html.Div(children=[
                dcc.Graph(
                    id='trend-graph',
                    figure={
                        'data': [
                            {'x': [], 'y': [], 'type': 'scatter'},
                        ],
                        'layout': {
                            'title': 'Data Visualization',
                            'yaxis': {
                                'rangemode': 'tozero'
                            }
                        }
                    }
                )
            ])
        ])

        app = self.dashapp

        @app.callback(Output('csv-file-list', 'options'),
              [Input('csv-file-list', 'value')])
        def update_filelist(value):
            csv_file_list = self.get_csv_filenames()
            return [
                {'label': '{}'.format(str(i)), 'value': str(i)} for i in csv_file_list
            ]

        @app.callback(
            Output('trend-graph', 'figure'),
            [Input('csv-file-list', 'value')])
        def update_trend(value):
            if value:
                data = list(self.get_values_from_csv(value))
                x, y1, y2, y3 = zip(*data)
            else:
                x = [0]
                y1 = [0]
                y2 = [0]
                y3 = [0]

            return {
                'data': [
                    {'x': x, 'y': y2, 'line':{'color':'#ff7f0e'}, 'type': 'scatter', 'mode': 'line', 'name': 'Max'},
                    {'x': x, 'y': y1, 'line':{'color':'#1f77b4'}, 'type': 'scatter', 'mode': 'line', 'name': 'Average'},
                ],
                'layout': {
                    'title': '{}'.format(value or "Ping++ Data Visualization"),
                    'yaxis': {
                        'rangemode': 'tozero'
                    }
                }
            }

def run():
    args = get_argument_parser()

    if 'help' in args:
        return

    settings = get_settings(args)
    trendapp = TrendApplication(settings.glob)
    trendapp.run(settings.host, settings.port)

if __name__ == '__main__':
    run()
