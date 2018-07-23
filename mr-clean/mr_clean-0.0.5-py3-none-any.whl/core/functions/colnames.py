# -*- coding: utf-8 -*-

def smart_colnames(df, cutoff = .5):
    """ Replace spaces and dashes with underscores and make everything lowercase
    remove underscores before and after
    replace multiple underscores with just one
    Create dictionary of taken words, with counts cooresponding to occurence rate
    Loop:
        Find words/phrases common among large portion of columns (according to cutoff)
        For each word/phrase:
            Replace each word in phrase with a single letter
            Loop:
                If already in dictionary:
                    add another letter to the abbrev. based on the original word phrase
                    try again
                else:
                    break
            replace phrase with abbreviation for all instances.
            Remove words of phrase from dictionary
            add abbreviation to the dictionary
            add (phrase,abbreviation) to list
    """
    pass