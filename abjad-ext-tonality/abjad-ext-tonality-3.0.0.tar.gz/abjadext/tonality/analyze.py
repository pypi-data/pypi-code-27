import abjad
from abjadext.tonality.TonalAnalysis import TonalAnalysis


def analyze(argument):
    """
    Makes tonal analysis agent.

    Returns tonal analysis agent.
    """
    leaves = abjad.select(argument).leaves()
    return TonalAnalysis(leaves)
