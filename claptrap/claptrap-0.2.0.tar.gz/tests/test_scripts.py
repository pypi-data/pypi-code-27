import shlex

from claptrap.scripts import script_phrase_helper


LOOPS = 20
MIN_RANGE = range(1, 40)
MAX_LEN = 100


def test_drac_phrase():
    corp = "drac"
    for n in MIN_RANGE:
        for phrase in script_phrase_helper(corp, "{}".format(n), LOOPS):
            assert len(phrase) == n
        for phrase in script_phrase_helper(corp, "{}-{}".format(n, MAX_LEN), LOOPS):
            assert n <= len(phrase) <= MAX_LEN


def test_wub_phrase():
    corp = "wub"
    for n in MIN_RANGE:
        for phrase in script_phrase_helper(corp, "{}".format(n), LOOPS):
            assert len(phrase) == n
        for phrase in script_phrase_helper(corp, "{}-{}".format(n, MAX_LEN), LOOPS):
            assert n <= len(phrase) <= MAX_LEN
