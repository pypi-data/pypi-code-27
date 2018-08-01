from typing import List, Tuple


class Injector:

    @staticmethod
    def inject(tagged_words: List[Tuple[str, str]], values: List[str], label: str) -> List[Tuple[str, str]]:
        """
        Tagged word contains list of the pairs.
        The method switches the pair like <LABEL, _> to the pair like <VALUE, LABEL> with the given values and label.

        Parameters
            tagged_words: List[Tuple[str, str]]
                list of words with labels
            values: List[str]
                list of values to insert instead of label
            label: str
                replaced tag

        Return
            List[Tuple[str, str]]
                tagged words (with replaced date tags)
        """
        counter = 0
        for i, x in enumerate(tagged_words):
            if x[0] == label:
                tagged_words[i] = (values[counter], label)
                counter += 1
        return tagged_words
