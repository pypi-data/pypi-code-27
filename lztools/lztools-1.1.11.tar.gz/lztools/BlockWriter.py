from lztools.text import create_line, wall_text

default_horizontal_symbol = "-"
default_vertical_symbol = "|"
default_fill_symbol = " "

class BlockWriter(object):
    roof_str = None
    wall_str = None
    manual_print = False
    fill_char = None
    started = False
    bufferd = True
    buffer = None
    width = -1
    padding_h = -1

    def __init__(self, width:int=80, horizontal_symbol:str=default_horizontal_symbol, vertical_symbol:str=default_vertical_symbol, fill_symbol:str=default_fill_symbol, bufferd:bool=True, manual_print:bool=False, padding_h:int=2):
        self.roof_str = horizontal_symbol
        self.wall_str = vertical_symbol
        self.manual_print = manual_print
        self.fill_char = fill_symbol
        self.bufferd = bufferd
        self.width = width
        self.padding_h = padding_h
        if bufferd:
            self.buffer = []

    def _wall_len(self):
        return len(self.wall_str)

    def split(self) -> None:
        w = self.width - 2 * self._wall_len()
        self.buffer.append(f"{self.wall_str}{create_line(width=w)}{self.wall_str}")

    def seperate(self):
        self.write_text(" ")

    def square_text(self, text:str, text_alignment="^") -> None:
        w = self.width - 2 * self._wall_len()
        if not self.started:
            self.started = True
            self.buffer.append(create_line(self.roof_str, self.width))
        else:
            self.buffer.append(f"{self.wall_str}{create_line(width=w)}{self.wall_str}")
        self.seperate()
        self.write_text(text, text_alignment=text_alignment)
        self.seperate()
        self.buffer.append(f"{self.wall_str}{create_line(width=w)}{self.wall_str}")

    def write_text(self, text:str, text_alignment="<", colorizer=None) -> None:
        if not self.started:
            self.buffer.append(create_line(self.roof_str, self.width))
            self.started = True
        self.buffer.append(wall_text(text, self.width, self.wall_str, text_alignment=text_alignment, h_padding=self.padding_h, colorizer=colorizer))

    def flush(self) -> None:
        self.buffer.append(create_line(self.roof_str, self.width))
        for line in self.buffer:
            print(line)