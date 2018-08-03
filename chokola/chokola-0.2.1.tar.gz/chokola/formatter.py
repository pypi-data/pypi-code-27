class Formatter():

    FREE = 0
    CENTER = 1
    LEFT = 2
    RIGHT = 3

    def col_header(self, text, col):
        return text

    def row_header(self, text, row):
        return text

    def alignment(self, row):
        return Formatter.FREE

    def cell(self, text, col, row):
        return text
