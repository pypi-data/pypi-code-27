## class libary file for all classes related to ontologies with owlready2
#
# @file		    classes.py
# @author	    Tobias Ecklebe
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
import pylibcklb.ontology.functions as OFL
import os
from multiprocessing import Pool
from pylibcklb.ClassLibrary import cDebug

class convert_owl2sqlite3(cDebug):

    def __init__(self, debug_level:int=cDebug.LEVEL_ZERO, source_dir:str='', db_dir:str=''):
        cDebug.__init__(self, Level=debug_level)
        self.source             = source_dir
        self.db_dir             = db_dir
        self.results            = []
        self.converted_fils     = []

        if not os.path.isdir(self.db_dir):
            ret = FL.CreateDir(self.db_dir)    

    def convert_worker(self, filename):      
        db_path = os.path.join(self.db_dir, '.'.join((os.path.splitext(os.path.basename(filename))[0], "sqlite3")))
        if not os.path.isfile(db_path):
            self.Print(cDebug.LEVEL_DEVELOPMENT, 'Convert: '+ db_path)
            my_world = World()
            my_world.set_backend(filename = db_path)
            my_world.get_ontology('file://'+filename).load()
            my_world.save()
        return db_path

    def process(self):
        pool = Pool()
        self.results = pool.map(self.convert_worker,  FL.get_list_of_files(self.source, 'owl'))
        pool.close() 
        pool.join()

    def get_list_of_owl_databases(self):
        return self.results

# Note: not ready at the moment, because the load ontologie function returns different ontology objects even if the filecontent is the same
class compare_ontologies(cDebug):

    def __init__(self, debug_level:int=cDebug.LEVEL_ZERO, filelist_of_ontolgies:list=[], iri:str=''):
        cDebug.__init__(self, Level=debug_level)
        self.filelist_of_ontolgies          = filelist_of_ontolgies
        self.cleaned_filelist_of_ontolgies  = filelist_of_ontolgies
        self.iri                            = iri
        self.process_results                = []

    def process_on_databases(self) -> None:      
        pool = Pool()
        self.process_results = pool.map(self.compare_worker, self.filelist_of_ontolgies)
        pool.close() 
        pool.join()
        
    def clean_filelist(self):
        for item in self.process_results:
            if item != []: 
                origin = item[0]
                dublicated_files = item[1]
                for file in dublicated_files:
                    self.Print(cDebug.LEVEL_DOKU, str('remove ' + file + ' from filelist'))
                    self.cleaned_filelist_of_ontolgies.remove(file)

    def compare_worker(self, db_file_origin):
        results = [db_file_origin]
        dublicated_files = []
        onto_origin = OFL.get_ontology_from_database(self.iri, db_file_origin, exclusive = False)
        for db_file_compare in self.filelist_of_ontolgies:
            if db_file_origin != db_file_compare:
                onto_compare = OFL.get_ontology_from_database(self.iri, db_file_compare, exclusive = False)
                if onto_origin == onto_compare:
                    self.Print(cDebug.LEVEL_DOKU, str(db_file_origin + ' and ' + db_file_compare + ' have the same constellation'))
                    dublicated_files.append(db_file_compare)

        if len(dublicated_files) > 1:
            results.append(dublicated_files)
            return results
        else:
            return []

    def get_cleaned_filelist_of_ontolgies(self) -> list:
        self.clean_filelist()
        return self.cleaned_filelist_of_ontolgies

    def get_raw_filelist_of_ontolgies(self) -> list:
        return self.filelist