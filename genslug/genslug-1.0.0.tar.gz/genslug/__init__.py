import re

def slug(s):

    s = s.lower()

    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')

    s = re.sub('\W', '', s)
    s = s.replace('_', ' ')
    s = re.sub('\s+', ' ', s)
    s = s.strip()
    s = s.replace(' ', '-')

    return s
