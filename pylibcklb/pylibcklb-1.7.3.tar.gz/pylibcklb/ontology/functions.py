## functions libary file for all functions related to ontologies with owlready2
#
# @file		    functions.py
# @author	    Tobias Ecklebe
# @date		    23.07.2018
# @version	    0.1.0
# @note		    To use this file:  from pylibcklb.ontology.functions import SomeClassOrFunction\n     
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

from owlready2 import World, Ontology
import pylibcklb.FunctionLibrary as FL
import os

def get_ontology_from_database(iri, db_dir_name, exclusive=True) -> Ontology:
    my_world = World()
    my_world.set_backend(filename = db_dir_name, exclusive=exclusive)
    return my_world.get_ontology(iri).load()

def get_ontology_from_local_file(filename:str='', db_dir:str='', db_dir_name:str='', use_owl_world:bool=True) -> Ontology:
    filename_with_prefix = 'file://'+filename

    if use_owl_world:
        if not os.path.isdir(db_dir):
            ret = FL.CreateDir(db_dir)  
        my_world = World()         
        my_world.set_backend(filename = db_dir_name)

        return my_world.get_ontology(filename_with_prefix).load()
    else:
        return get_ontology(filename_with_prefix).load()

def get_onto_object_name(onto_object) -> str:
    return str(onto_object.is_a[0]).split('.')[1]

