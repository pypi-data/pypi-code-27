import contextlib


class _Reader:
    __slots__ = ['data', 'cursor', 'end', 'line_number']

    def __init__(self):
        pass

    def set_data(self, new_data, line=0):
        self.data = new_data
        self.cursor = 0
        self.end = len(self.data)
        self.line_number = line

    def peek(self):
        return None if self.cursor + 1 == self.end else self.data[self.cursor + 1]

    def last(self):
        return None if self.cursor == 0 else self.data[self.cursor - 1]

    def next(self):
        if self.cursor == self.end:
            return None
        result = self.data[self.cursor]
        self.cursor += 1
        return result

    def prev(self):
        if self.cursor == 0:
            return None
        result = self.data[self.cursor - 1]
        self.cursor -= 1
        return result

    def has_next(self):
        return self.cursor + 1 <= self.end

    def raise_illegal_character_exception(self):
        raise Exception('Illegal character @ {},{}'.format(self.line_number, self.cursor + 1))


_pos_reader = _Reader()


def parse_number(current):
    result = current
    while _pos_reader.has_next():
        cur = _pos_reader.next()
        if not cur.isdigit() and cur not in ('e', '+', '-', '.'):
            _pos_reader.prev()
            break
        result += cur
    if result.isdigit():
        return int(result)
    return float(result)


def parse_str() -> str:
    result = ''
    while _pos_reader.has_next():
        cur = _pos_reader.next()
        if cur == '"':
            break
        result += cur
    return result


def parse_list() -> list:
    result = []
    while _pos_reader.has_next():
        cur = _pos_reader.next()
        if cur == ']':
            break
        if cur in (',', ' '):
            continue
        if cur.isdigit():
            result.append(parse_number(cur))
        elif cur.isalpha() or cur == '"':
            result.append(parse_str()) if cur == '"' else result.append(cur + parse_str())
        elif cur == '[':
            result.append(parse_list())
        elif cur == '(':
            result.append(parse_tuple())
        else:
            _pos_reader.raise_illegal_character_exception()
    return result


def parse_tuple() -> tuple:
    result = []
    while _pos_reader.has_next():
        cur = _pos_reader.next()
        if cur == ')':
            break
        if cur in (',', ' '):
            continue
        if cur.isdigit():
            result.append(parse_number(cur))
        elif cur.isalpha() or cur == '"':
            result.append(parse_str()) if cur == '"' else result.append(cur + parse_str())
        elif cur == '[':
            result.append(parse_list())
        elif cur == '(':
            result.append(parse_tuple())
        else:
            _pos_reader.raise_illegal_character_exception()
    return tuple(result)


def parse_data(raw: str, line_num: int) -> tuple:
    _pos_reader.set_data(raw)
    result = []
    while _pos_reader.has_next():
        cur = _pos_reader.next()
        if cur in ('\n', '\t', ' ', '\r'):
            continue
        if cur == '(':
            result.append(parse_tuple())
        elif cur == '[':
            result.append(parse_list())
        elif cur == '"':
            result.append(parse_str())
        elif cur.isdigit():
            result.append(parse_number(cur))
        else:
            _pos_reader.raise_illegal_character_exception()
    return tuple(result)


class Loader:
    __slots__ = ['cnt_cases', 'cnt_params']

    def __init__(self, number_of_cases, number_of_params):
        self.cnt_cases = number_of_cases
        self.cnt_params = number_of_params

    def load_cases(self, file):
        with contextlib.closing(open(file, 'r')) as fp:
            test_cases = []
            for i in range(self.cnt_cases):
                line = fp.readline()
                test_cases.append(parse_data(line, i + 1))
                assert len(test_cases[-1]) == self.cnt_params
            assert len(test_cases) == self.cnt_cases
            return test_cases

    def load_answers(self, file):
        with contextlib.closing(open(file, 'r')) as fp:
            answers = []
            for i in range(self.cnt_cases):
                line = fp.readline()
                answers.append(parse_data(line, i + 1))
            return answers
