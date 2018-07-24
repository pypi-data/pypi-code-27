## class libary file for all classes related to ontologies with owlready2
#
# @file		    classes.py
# @author	    Tobias Ecklebe efos@ecklebe.de
# @date		    23.07.2018
# @version	    0.1.0
# @note		    To use this file:  from pylibcklb.ontology.classes import SomeClassOrFunction\n     
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
from multiprocessing import Pool

class convert_owl2sqlite3(object):

    def __init__(self, source_dir, db_dir):
        self.source         = source_dir
        self.db_dir         = db_dir
        self.results        = []

        if not os.path.isdir(self.db_dir):
            ret = FL.CreateDir(self.db_dir)    

    def convert_worker(self, filename):      
        db_path = os.path.join(self.db_dir, '.'.join((os.path.splitext(os.path.basename(filename))[0], "sqlite3")))
        if not os.path.isfile(db_path):
            print('Convert: '+ db_path)
            my_world = World()
            my_world.set_backend(filename = db_path)
            my_world.get_ontology('file://'+filename).load()
            my_world.save()
        return db_path

    def process_convert(self):
        pool = Pool()
        self.results = pool.map(self.convert_worker, FL.get_list_of_files(self.source, 'owl'))
        pool.close() 
        pool.join()

    def get_list_of_owl_databases(self):
        return self.results
