import pkg_resources as pkg
import tifffile
import pickle

# To be removed once we move everything to "clean way"
import os
spamToolBaseDir = os.path.join(os.path.dirname(__file__), "../../../../../")


## Generic functions ##

def loadtiff(filepath):
    data_file_path = 'data/' + filepath
    if (pkg.resource_exists('spam', data_file_path)):
        f = pkg.resource_filename('spam', data_file_path)
        return tifffile.imread(f)
    else:
        raise IOError("File %s not found" % data_file_path)

def load(filepath):
    data_file_path = 'data/' + filepath
    if (pkg.resource_exists('spam', data_file_path)):
        f = pkg.resource_filename('spam', data_file_path)
        return open(f, 'r')
    else:
        raise IOError("File %s not found" % data_file_path)

def loadPickle(filepath):
    data_file_path = 'data/' + filepath
    if (pkg.resource_exists('spam', data_file_path)):
        f = pkg.resource_filename('spam', data_file_path)
        return pickle.load( open( f, 'r' ) ) 
    else:
        raise IOError("File %s not found" % data_file_path)


# Usage example ##

# def loadtiffexample():
#    print("print something funny")
#    return loadtiff('image.tiff')


def loadsomething():
    #print("print something funny")
    return load('placeholder.txt')


def loadSnow():
    #print("spam.datasets.snow(): Brrr, enjoy this cold data")
    return loadtiff("snow/snow.tif")

def loadStructuredMesh():
    return loadPickle("mesh/structuredMesh.p")

def loadUnstructuredMesh():
    return loadPickle("mesh/unstructuredMesh.p")

def loadConcreteXr():
    return loadtiff("concrete/concrete_x-ray-bin16.tif")

def loadConcreteNe():
    return loadtiff("concrete/concrete_neutron-bin16.tif")


# Legacy way ##


def loadV4two():
    return tifffile.imread(spamToolBaseDir+"/tools/data/V4sandstone/V4-02-b1.tif")


