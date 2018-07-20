
HEADER = '\033[40;223m'
BLUE = '\033[40;38;5;39m'
GREEN = '\033[40;92m'
YELLOW = '\033[40;93m'
ERROR = '\033[40;38;5;9m'
UNDERLINE = '\033[4m'
ORANGE = '\033[40;38;5;214m'

BOLD = '\033[1m'
END = '\033[0m'


def cmd(*value):
    log(*value, color=HEADER)

def success(*value):
    log(*value, color=GREEN)

def choice(*value):
    log(*value, color=BLUE)

def info(*value):
    log(*value, color=HEADER)

def ask(*value):
    log(*value, color=YELLOW)

def comment(*value):
    log(*value, color=HEADER)

def warning(*value):
    log(*value, color=ORANGE)

def error(*value):
    log(*value, color=ERROR)

def log(*value, **kwargs):
    color = kwargs.pop('color' ,YELLOW)
    value = " " + " ".join([str(v) for v in value]) + " "
    value = '{}{}{}'.format(color, value, END)
    value = value.replace('<b>', BOLD).replace('</b>', END + color)
    print(value.strip())