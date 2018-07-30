from .micral_harmonic_core import harmonicMeasurementCore

def analyse(images, plot=False, plotTimeline=None):
    return harmonicMeasurementCore(images, plot, plotTimeline)