## class libary file for all classes related to work on and with images
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
import pylibcklb.FunctionLibrary as FL
from pylibcklb.ClassLibrary import cDebug
import imgkit

class convert_html2jpg(cDebug):

    def __init__(self, debug_level:int=cDebug.LEVEL_DEVELOPMENT, source_dir:str='', dest_dir:str='', exception_text:str='', options = {'width':'2800'}):
        cDebug.__init__(self, Level=debug_level)
        self.source             = source_dir
        self.dest_dir           = dest_dir
        self.options            = options
        self.exception_text     = exception_text
    
        if not os.path.isdir(self.dest_dir):
            print(self.dest_dir)
            FL.CreateDir(self.dest_dir)

    def convert_worker(self, filename_origin):  
        img_path = os.path.join(self.dest_dir, '.'.join((os.path.splitext(os.path.basename(filename_origin))[0], "jpg")))
        if not os.path.isfile(img_path):
            FL.CreateDir(img_path)
            self.Print(cDebug.LEVEL_DEVELOPMENT,'Convert html to jpg: '+ filename_origin +' to '+img_path) 
            imgkit.from_file(filename_origin, img_path, self.options)   

    def process(self):
        pool = Pool()
        filelist = []
        for file in FL.get_list_of_files(self.source,'html'):
            if not self.exception_text in file:
                filelist.append(file)
        pool.map(self.convert_worker, filelist)
        pool.close() 
        pool.join()