#/*##########################################################################
# Copyright (C) 2004-2014 V.A. Sole, European Synchrotron Radiation Facility
#
# This file is part of the PyMca X-ray Fluorescence Toolkit developed at
# the ESRF by the Software group.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################*/
__author__ = "V.A. Sole - ESRF Data Analysis"
__contact__ = "sole@esrf.fr"
__license__ = "MIT"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
import os
import glob

def getPackages(directory):
    packages = []
    fileList = glob.glob(os.path.join(directory, "*", "__init__.py"))
    for fileName in fileList:
        dirName = os.path.dirname(fileName)
        packages.append(dirName)
        packages += getPackages(dirName)
    return packages

from .plotting import PyMca_Icons, PyMcaPrintPreview
from .plotting.PyMca_Icons import IconDict

# this is the package level directory PyMcaGui
baseDirectory = os.path.dirname(__file__)
__path__ += [baseDirectory]
for directory in ["io", "math", "misc",
                  "physics", "plotting", "pymca"]:
    tmpDir = os.path.join(baseDirectory, directory)
    if os.path.exists(os.path.join(tmpDir, "__init__.py")):
        __path__ += [tmpDir]
    __path__ += getPackages(tmpDir)
