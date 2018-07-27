from functools import partial

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter
from tkinter import Tk, Frame, Canvas, Button, Label, Entry, \
OptionMenu, Scrollbar, Checkbutton, \
StringVar, DoubleVar, BooleanVar, IntVar
import numpy as np

if __name__=='__main__':
    run_hwaves_gui()

def run_hwaves_gui():
    gui = Tk()
    gui.title('hydrogenic wavefunction plotter')
    
    plot_canvas = Canvas(gui, width=800, height=1600)
    plot_canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES)

    # set up axes for radial wf and isosurface plots
    # ax_rwf = 
    # ax_surf = 
    # etc...

    # draw initial plots
    # draw_plots(plot_canvas,ax_rwf,ax_surf)

    # draw control widgets
    control_frame = Frame(gui,relief=tkinter.RAISED)
    # etc...

    # connect control widgets
    # ...

    # start the tk loop
    gui.mainloop()

def draw_plots(plot_canvas,ax_rwf,ax_surf):
    ax_rwf.clear()
    ax_surf.clear()
    plot_canvas.draw()

