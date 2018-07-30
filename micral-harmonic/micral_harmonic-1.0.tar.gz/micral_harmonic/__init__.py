from .micral_harmonic import harmonicMeasurement

def analyse(images, plot=False, plotTimeline=None):
    return harmonicMeasurement(images, plot, plotTimeline)