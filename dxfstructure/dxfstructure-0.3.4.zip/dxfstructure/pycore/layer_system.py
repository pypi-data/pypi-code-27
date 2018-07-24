'''
--------------------------------------------------------------------------
Copyright (C) 2017-2018 Lukasz Laba <lukaszlab@o2.pl>

This file is part of DxfStructure (structural engineering dxf drawing system).

DxfStructure is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

DxfStructure is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''
#                                           [color, line_weight, linetype, plot]                                        

logiclayers =   {   'DS_CBAR' :             [231, 30, 'CONTINUOUS', 1],
                    'DS_CBAR_UNPLOTTED' :   [230, 30, 'CONTINUOUS', 0],
                    'DS_CTEXT' :            ['yellow', 20, 'CONTINUOUS', 1],
                    'DS_STEXT' :            [4, 20, 'CONTINUOUS', 1],
                    'DS_DEPLINE' :          [46, 15,'CONTINUOUS', 0],
                    'DS_ELEMENT' :          [234, 20, 'CONTINUOUS', 1],
                    'DS_RANGE' :            [92, 18, 'CONTINUOUS', 1],
                    'DS_SCHEDULECONCRETE' : ['yellow', 20, 'CONTINUOUS', 1],
                    'DS_SCHEDULESTEEL' :    ['yellow', 20, 'CONTINUOUS', 1],
                    'DS_COMMAND' :          [62, 15, 'CONTINUOUS', 1],
                    'DS_TMPCHECK' :         [186, 15, 'CONTINUOUS', 0]
                }

drawlayers =    {   'DS_DRAW_PROFILE' :     ['green', 20, 'CONTINUOUS', 1],
                    'DS_DRAW_FORMWORK' :    [4, 18, 'CONTINUOUS', 1],
                    'DS_DRAW_BOLT' :        [52, 18, 'CONTINUOUS', 1],
                    'DS_DRAW_WELD' :        [233, 18,'CONTINUOUS', 1],
                    'DS_DRAW_DIM' :         ['red', 15, 'CONTINUOUS', 1],
                    'DS_DRAW_REMARK' :      ['yellow', 18, 'CONTINUOUS', 1],
                    'DS_DRAW_AXIS' :        [9, 15, 'CONTINUOUS', 1]
                }

layers = dict(logiclayers.items() + drawlayers.items())

layer_name_list = layers.keys()

def color_for_layer(layer_name):
    return layers[layer_name][0]
    
def width_for_layer(layer_name):
    return layers[layer_name][1]
    
def linetype_for_layer(layer_name):
    return layers[layer_name][2]

def plot_for_layer(layer_name):
    return layers[layer_name][3]
    
# Test if main        
if __name__ == "__main__":  
    print layer_name_list
        
# Test if main        
if __name__ == "__main__":
    print layer_name_list
    print color_for_layer('DS_DRAW_DIM')
    print width_for_layer('DS_DRAW_DIM')
    print linetype_for_layer('DS_DRAW_DIM')
    
    
    
    
    
    
    
    
    
    
    