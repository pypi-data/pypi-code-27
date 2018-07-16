class Token:

    def __init__(self, word, part_of_speech):
        self.word = word
        self.part_of_speech = part_of_speech

    def __repr__(self):
        return f'{self.word}({self.part_of_speech})'

    def __str__(self):
        return self.__repr__()
