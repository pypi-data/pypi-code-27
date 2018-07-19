#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
"""
    Plot the 3D graph from json file.
 
    Usage:
 
    >>> from gorille.sigplot import get3Dplot
    >>> get3Dplot(inputfile,outputfile)
"""

import optparse, json
from plotly.offline import plot
from plotly.graph_objs import Scatter3d, Line, Marker, Layout, Scene, XAxis, YAxis, ZAxis, Margin, Data, Figure

__all__ = ['get3Dplot']

def get3Dplot(inputData, filename, outtype3D='div'):
    nrcaseStrings = ["MATCH", "WHITE", "SPEC", "SMALL"]

    N = len(inputData['nodes'])
    L = len(inputData['edges'])
    Nodes = list(inputData['nodes'])
    Edges = [(Nodes.index(edge['source']),Nodes.index(edge['target'])) for edge in inputData['edges']] 
    group = [nrcaseStrings.index(inputData['nodes'][node]['result']) for node in Nodes]
    layt = [inputData['nodes'][k]['location'] for k in Nodes]

    Xn = [elt[0] for elt in layt]  # x-coordinates of nodes
    Yn = [elt[1] for elt in layt]  # y-coordinates
    Zn = [elt[2] for elt in layt]  # z-coordinates
    Xe = []
    Ye = []
    Ze = []
    for e in Edges:
        Xe += [layt[e[0]][0], layt[e[1]][0], None]  # x-coordinates of edge ends
        Ye += [layt[e[0]][1], layt[e[1]][1], None]
        Ze += [layt[e[0]][2], layt[e[1]][2], None]

    trace1 = Scatter3d(x=Xe, y=Ye, z=Ze,
                       mode='lines',
                       line=Line(color='rgb(125,125,125)', width=3),
                       hoverinfo='none'
                       )

    trace2 = Scatter3d(x=Xn,y=Yn,z=Zn,
                       mode='markers',
                       marker=Marker(symbol='dot',
                                     line=Line(color='rgb(50,50,50)', width=0.5),
                                     size=12,
                                     color=group,
                                     cmin=0,
                                     cmax=3,
                                     colorscale=[[0, 'rgb(151,70,133)'],
                                                 [0.25, 'rgb(151,70,133)'],
                                                 [0.25, 'rgb(255,255,255)'],
                                                 [0.5, 'rgb(255,255,255)'],
                                                 [0.5, 'rgb(89,138,187)'],
                                                 [0.75, 'rgb(89,138,187)'],
                                                 [0.75, 'rgb(150,150,150)'],
                                                 [1, 'rgb(150,150,150)']],
                                     ),
                       text=Nodes,
                       hoverinfo='text'
                       )

    axis = dict(showbackground=False,
                showline=True,
                zeroline=False,
                showgrid=True,
                showticklabels=False
                )

    layout = Layout(title="Cyber-Detect",
                    images=[dict(source="static/img/logo.png",
                                 xref="paper",
                                 yref="paper",
                                 x=0.2,
                                 y=0.9,
                                 sizex=0.2,
                                 sizey=0.2,
                                 xanchor="right",
                                 yanchor="bottom")],
                    showlegend=False,
                    scene=Scene(xaxis=XAxis(axis),
                                yaxis=YAxis(axis),
                                zaxis=ZAxis(axis),
                                ),
                    margin=Margin(t=100),
                    hovermode='closest'
                    )

    data = Data([trace1, trace2])
    fig = Figure(data=data, layout=layout)

    return plot(fig, output_type=outtype3D, show_link=False, filename=filename, auto_open=False)


def main():
    usage = "usage: %prog inputfile.json outputfile.html"
    parser = optparse.OptionParser(usage)
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("incorrect number of arguments, use --help for command information")
    f = open(args[0])
    inputData = json.loads(f.read())
    f.close()
    output_file = args[1]

    print (get3Dplot(inputData, output_file, outtype3D='file'))


if __name__ == "__main__":
    main()
