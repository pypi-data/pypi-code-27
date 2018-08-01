"""
Abstract class
Describes the entity that extracts from the text the components that satisfy the rule.
"""


from typing import List, Tuple


class Extractor:

    def __init__(self, keyword: str):
        """
        Parameters
            keyword: str
                keyword for an extracted entities
        """
        pass

    def extract(self, text: str) -> Tuple[str, List[str]]:
        """
        Parameters
            text: str
                input text

        Return
            Tuple[str, List[str]]
                processed text and detected matches
        """
        raise NotImplementedError
