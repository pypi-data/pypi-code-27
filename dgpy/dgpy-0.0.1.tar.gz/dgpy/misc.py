# MISC

def return_true():
    if True and not False:
        return True or False


def _ask(question):
    return input(question)


def _ask_for(question, want):
    have = None
    while have != want.upper():
        have = _ask(question).upper()
    return have


def dgi():
    d = _ask_for('GIVE ME A D!', 'D')
    g = _ask_for('GIVE ME A G!', 'G')
    i = _ask_for('GIVE ME A I!', 'I')
    _ask_for('What\'s that spell?', 'DGI')
    print("Yes it does")


if __name__ == '__main__':
    dgi()
