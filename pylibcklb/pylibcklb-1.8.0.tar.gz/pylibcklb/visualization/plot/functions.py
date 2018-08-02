## functions libary file for all functions that can be used to plot data
#
# @file		    functions.py
# @author	    Tobias Ecklebe
# @date		    23.07.2018
# @version	    0.1.0
# @note		    To use this file:  from pylibcklb.plot.functions import SomeClassOrFunction\n     
#               
# @pre          The library was developed with python 3.6 64 bit 
#
# @bug          No bugs at the moment.
#
# @copyright    pylibcklb package
#               Copyright (C) 2017  Tobias Ecklebe
#
#               This program is free software: you can redistribute it and/or modify
#               it under the terms of the GNU Lesser General Public License as published by
#               the Free Software Foundation, either version 3 of the License, or
#               (at your option) any later version.
#
#               This program is distributed in the hope that it will be useful,
#               but WITHOUT ANY WARRANTY; without even the implied warranty of
#               MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#               GNU Lesser General Public License for more details.
#
#               You should have received a copy of the GNU Lesser General Public License
#               along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from matplotlib import pyplot as plt

def create_barh(self, x_list, x_name, y_list, y_name):
    subsize_x:int=1
    subsize_y:int=1
    sub_nr:int=1

    fig = plt.figure()
    ax = fig.add_subplot(subsize_x, subsize_y, sub_nr)
    ax.barh(x_list, y_list)
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    plt.show()