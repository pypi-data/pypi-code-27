from .micral_grain import grainSeparator

def analyse(images, plot=True, plotFull=False, plotDetails=None):
    return grainSeparator(images, plot, plotFull, plotDetails)