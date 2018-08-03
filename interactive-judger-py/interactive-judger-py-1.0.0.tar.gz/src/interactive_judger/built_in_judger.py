from .judge_result import Result


def _fabs(x: float):
    if x < 0.0:
        return -x
    return x


def integer_judger(expected, actual: int):
    if expected == actual:
        return Result.AC
    else:
        return Result.WA


equality_judger = integer_judger


def float_judger(expected: float, actual: float, boundless_error_accepted: float):
    if _fabs(expected - actual) <= boundless_error_accepted:
        return Result.AC
    else:
        return Result.WA


def charsequence_judger(expected: str, actual: str, multi_line=False,
                        omit_trailing_spaces=True, omit_trailing_newlines=True):
    '''
        This judger can be applied to judge single line or multi-line strings
    :param expected: expected answer
    :param actual: actual answer yielded by the program
    :param multi_line: whether the answer contains more than a line of strings
    :param omit_trailing_spaces: <-
    :param omit_trailing_newlines: <-
    :return: Judge result
    '''

    def resolve_empty_line(xs: list):
        while not xs[-1]:
            xs = xs[:-1]
        return xs

    def resolve_trailing_spaces(x: str):
        return x.rstrip()

    def resolve_trailing_newlines(x: str):
        while x[-1] == '\n':
            x = x[:-1]
        return x

    if multi_line:
        expected = expected.split('\n')
        actual = actual.split('\n')
        if omit_trailing_newlines:
            expected = resolve_empty_line(expected)
            actual = resolve_empty_line(actual)
        if len(expected) != len(actual):
            return Result.WA
        else:
            if omit_trailing_spaces:
                for (e, a) in zip(expected, actual):
                    if resolve_trailing_spaces(e) != resolve_trailing_spaces(a):
                        return Result.WA
                return Result.AC
            else:
                for (e, a) in zip(expected, actual):
                    if e != a:
                        if e.rstrip() == a.rstrip():
                            return Result.PE
                        else:
                            return Result.WA
                return Result.AC
    else:
        if omit_trailing_newlines:
            expected = resolve_trailing_newlines(expected)
            actual = resolve_trailing_newlines(actual)
            if omit_trailing_spaces:
                expected = resolve_trailing_spaces(expected)
                actual = resolve_trailing_spaces(actual)
        if expected == actual[-1]:
            return Result.PE
        return Result.AC if expected == actual else Result.WA


def iterative_judger(expected, actual, condiment={'boundless_error_accepted': 0.0, }):
    '''
        This judger is designed to judge an iterative object contains data with different data types
    :param expected:
    :param actual:
    :param condiment:
    :return:
    '''
    if len(expected) != len(actual):
        return Result.WA

    if type(expected) != type(actual):
        return Result.WA

    def next_judge(exp, act):
        '''
            Feed it with answer, and it will return the next judger that should be invoked
        '''
        return {
            list: lambda: iterative_judger(exp, act),
            tuple: lambda: iterative_judger(exp, act),
            str: lambda: charsequence_judger(exp, act),
            int: lambda: integer_judger(exp, act),
            float: lambda: float_judger(
                exp, act, condiment['boundless_error_accepted'])
        }.get(type(exp), lambda: Result.JE)

    if type(expected) in (list, tuple, set, str):
        for (e, a) in zip(expected, actual):
            if type(e) != type(a):
                return Result.WA
            judge_result = next_judge(e, a)()
            if judge_result != Result.AC:
                return judge_result
        return Result.AC

    if isinstance(expected, dict):
        for (e, a) in zip(expected, actual):
            if type(e) != type(a) or type(expected[e]) != type(actual[a]):
                return Result.WA
            judge_result = next_judge(e, a)()
            if judge_result != Result.AC:
                return judge_result
        return Result.AC
