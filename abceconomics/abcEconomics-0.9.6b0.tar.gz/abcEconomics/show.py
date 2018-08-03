""" :code:`python -m abcEconomics.show` shows the simulation results in ./result/*  """
from .gui import graph
from .gui.gui_with_dash import newest_subdirectory

def show():
    graph(newest_subdirectory('./result', ''))


if __name__ == '__main__':
    show()
