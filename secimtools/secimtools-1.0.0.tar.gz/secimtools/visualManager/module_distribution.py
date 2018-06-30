########################################################################
# Date: 2016/July/11
#
# Module: module_distribution.py
# 
# Version: 0.9
#
# Author: Matt Thoburn (mthoburn@ufl.edu)
#
# Description: This module contains a method to plot a 
#                  kernel density estimate function
########################################################################
import pandas as pd


def plotDensityDF(data,ax,colors,lb=""):
    """
    Plots a density plot from a dataframe

    :Arguments:
        :type data: pandas dataframe
        :param data: data to be plotted

        :type ax: matplotlib axis
        :param ax: axis to be drawn on

        :type colors: list of colors
        :param colors: colors to be used in differentiating plots 

        :type lb: string
        :param lb: optional label for legend
    """
    #Plot density plot
    data.plot(kind="density",ax=ax,legend=False,color=colors,label=lb,grid=False)

    #Adjust xlim if not negative values
    xmin, xmax = ax.get_xlim()
    if xmin <= 0:
        ax.set_xlim(0, xmax)
 