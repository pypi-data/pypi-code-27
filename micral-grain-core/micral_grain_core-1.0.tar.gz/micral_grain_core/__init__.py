from .micral_grain_core import grainSeparatorCore

def analyse(images, plot=True, plotFull=False, plotDetails=None):
    return grainSeparatorCore(images, plot, plotFull, plotDetails)