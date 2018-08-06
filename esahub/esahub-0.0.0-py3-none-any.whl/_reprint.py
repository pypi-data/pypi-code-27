from reprint import reprint
from reprint.reprint import is_atty, overflow_flag, last_output_lines
from reprint import output
import sys
import time


# -----------------------------------------------------------------------------
# Monkey patch reprint
# -----------------------------------------------------------------------------

def _new__setitem__(self, key, value):
    global is_atty
    with self.lock:
        super(output.SignalDict, self).__setitem__(key, value)
        if not is_atty:
            print("{}".format(value))
        else:
            self.parent.refresh(int(time.time()*1000), forced=False)


def _new_print_multi_line(content, force_single_line, sort_key):
    """
    'sort_key' 参数只在 dict 模式时有效
    'sort_key' parameter only available in 'dict' mode
    """

    global last_output_lines
    global overflow_flag
    global is_atty

    if not is_atty:
        if isinstance(content, list):
            for line in content:
                print(line)
        elif isinstance(content, dict):
            for k, v in sorted(content.items(), key=sort_key):
                print("{}".format(v))
        else:
            raise TypeError("Excepting types: list, dict. Got: {}".format(
                type(content)))
        return

    columns, rows = reprint.get_terminal_size()
    lines = reprint.lines_of_content(content, columns)
    if force_single_line is False and lines > rows:
        overflow_flag = True
    elif force_single_line is True and len(content) > rows:
        overflow_flag = True

    # 确保初始输出位置是位于最左处的
    # to make sure the cursor is at the left most
    print("\b" * columns, end="")

    if isinstance(content, list):
        for line in content:
            _line = reprint.preprocess(line)
            reprint.print_line(_line, columns, force_single_line)
    elif isinstance(content, dict):
        for k, v in content.items():
            _k, _v = map(reprint.preprocess, (k, v))
            reprint.print_line("{}".format(_v), columns, force_single_line)
    else:
        raise TypeError("Excepting types: list, dict. Got: {}".format(
            type(content)))

    # 输出额外的空行来清除上一次输出的剩余内容
    # do extra blank lines to wipe the remaining of last output
    print(" " * columns * (last_output_lines - lines), end="")

    # 回到初始输出位置
    # back to the origin pos
    print(reprint.magic_char * (max(last_output_lines, lines)-1), end="")
    sys.stdout.flush()
    last_output_lines = lines


output.SignalDict.__setitem__ = _new__setitem__
reprint.print_multi_line = _new_print_multi_line
