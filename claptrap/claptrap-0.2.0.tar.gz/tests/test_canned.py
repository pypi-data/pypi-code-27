from claptrap import canned


def test_wubs():
    for n in range(1, 100):
        wub = canned.wub(n)
        assert n == len(wub) == len(wub.strip())
