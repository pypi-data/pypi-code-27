import ast
import sys
import os
from configparser import ConfigParser
import re
from inspect import getsource


def evaluate(text):
    return eval(text)

def viewcode(obj):
    return str(getsource(obj))


from dateutil import parser
from datetime import datetime

def parse_date(d, dayfirst=True):
    if not d: return False
    d = d.replace("/", "-")

    if dayfirst:
        fmt = '%d-%m-%Y'
        if not re.match(r"\d{2}-\d{2}-\d{4}", d):
            return False
    else:
        fmt = '%Y-%m-%d'
        if not re.match(r"\d{4}-\d{2}-\d{2}", d):
            return False
    try:
        parse=parser.parse(d, dayfirst=dayfirst)
    except Exception as e:
        return str(e)
    return datetime.strptime(d, fmt).strftime(fmt)


def as_datetime(d, fmt):
    return repr(datetime.strptime(d, fmt))


def as_datetime_str(dt, fmt):
    return repr(dt.strftime(fmt))


def as_date(d, fmt):
    return repr(datetime.strptime(d, fmt).date())


def as_date_str(dateobj, fmt):
    print(str(dateobj))


class Dosage:
    def __init__(self, number=None):
        self.number = number
        self.digit=None
        self.unit=None
        self.allowed_units=['kg','g','mg','mcg','ng','pg','ml']

        self.pg  = 0.000000001
        self.ng  = 0.000001
        self.mcg = 0.001
        self.mg  = 1 # Taken as a standard unit
        self.g   = 1000
        self.kg  = 1000000
        self.ml  = 1 # Mils should not be converted, >>unity

        self.compile()

    @property
    def units(self):
        return self.unit

    @property
    def value(self):
        return self.digit

    def compile(self):
        if self.number is None:
            self.digit=None
            self.unit = None
            return

        digit_regex = re.compile(r"\d+")
        float_regex = re.compile(r"\d+[.]\d+")
        units_regex = re.compile(r'((mg)|(mcg)|(pg)|(kg)|(ng)|(g)|(ml))', re.IGNORECASE)

        digit = digit_regex.search (self.number)
        double= float_regex.search(self.number)
        unit= units_regex.search(self.number)

        if double and unit:
            self.digit=double.group()
            self.unit=unit.group().lower()
        elif digit and unit:
            self.digit=digit.group()
            self.unit=unit.group().lower()
        else:
            self.digit=None
            self.unit = None

    def to_mg(self, number):
        if number.units is not None:
            unit= getattr(self, number.units)
            n = float(number.value) * float(unit)
            return n

    def __truediv__(self, other):
        numerator= self.to_mg(self)
        denominator= self.to_mg(other)
        if numerator and denominator:
            return round(numerator/denominator,2)

def calculate_dose(formulation, dose):
    '''
    Returns the number or proportion of tables as an float
    for the patient to swallow,
    given the drug formulation and a dose prescribed.
    '''
    return Dosage(dose)/Dosage(formulation)


from fractions import Fraction
def fraction(x,y):
    return Fraction(x,y)


def converters(n):
    simple = ["thousand", "mi", "bi", "tri", "quadri", "quinti", "sexti", "septi", "octi", "noni"]
    units = ["", "un", "do", "tre", "quattuor", "quin", "sex", "septen", "octo", "novem"]
    tens = ["", "dec", "vigin", "trigin", "quadragin", "quinquagin", "sexagin", "septuagin", "octogin", "nonagin"]
    hundreds = ["", "cen", "ducen", "trecen", "quadringen", "quingen", "sescen", "septingen", "octingen", "nongen"]

    suffixes = {
        "i": "llion",
        "c": "illion",
        "a": "tillion",
        "e": "tillion",
        "m": "tillion",
        "n": "tillion",
        "o": "tillion",
        "r": "tillion",
        "x": "tillion",
        "d": "",
    }

    results = []
    if n < 10:
        results.append(simple[n])
    else:
        thousands = 0
        while n:
            n, unit = divmod(n, 10)
            n, ten = divmod(n, 10)
            n, hun = divmod(n, 10)
            if hun or ten or unit:
                results.extend(["millia"] * thousands)
            if n or (hun, ten, unit) != (0, 0, 1):
                results.extend(filter(None, [tens[ten], units[unit], hundreds[hun]]))
            thousands += 1
    results.insert(0, suffixes[results[0][-1]])
    return str.join("", reversed(results))


def nn1000(number):
    # Tables
    names = {
        0: None,
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine',
        10: 'ten',
        11: 'eleven',
        12: 'twelve',
        13: 'thirteen',
        14: 'forteen',
        15: 'fifteen',
        16: 'sixteen',
        17: 'seventeen',
        18: 'eighteen',
        19: 'nineteen',
        20: 'twenty',
        30: 'thirty',
        40: 'forty',
        50: 'fifty',
        60: 'sixty',
        70: 'seventy',
        80: 'eighty',
        90: 'ninety',
        100: 'hundred',
    }

    hundreds = tens = None
    if number >= 100:
        h, number = divmod(number, 100)
        hundreds = names[h] + ' hundred'
    if number >= 20:
        tens = names[number - (number % 10)]
        number %= 10
    result = names[number]
    if tens: result = result and (tens + '-' + result) or tens
    if hundreds: result = result and (hundreds + ' ' + result) or hundreds
    return result


def num2words(number):
    negative = number < 0
    if negative:
        number = -number
    if not number:
        return 'zero'

    groups = []
    thousands = 0
    while number:
        number, n = divmod(number, 1000)
        if n:
            name = nn1000(n)
            if thousands:
                name += " " + converters(thousands - 1)
            groups.insert(0, name)
        thousands += 1
    result = str.join(", ", groups)

    if negative:
        result = "negative " + result
    return result


import os
class WorkingDir:
    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.origdir = os.getcwd()

    def __enter__(self):
        os.chdir(self.working_dir)
        return self.run_manager

    def __exit__(self, *args):
        os.chdir(self.origdir)


class InitMeta(type):
    def __call__(self, *args, **kwargs):
        clsobj = type.__call__(self, *args)
        for name, value in kwargs.items():
            setattr(obj, name, value)
        return clsobj


from functools import wraps
def silence_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return "Error in function %s: %s"%(func.__name__, str(e))

    return wrapper



def silence_all_class_errors(cls):
    for name, func in vars(cls).items():
        if callable(func):
            setattr(cls, name, silence_errors(func))

    return cls


def sqlite3(db=":memory:"):
    import sqlite3
    con = sqlite3.connect(db)
    con.isolation_level = None
    cur = con.cursor()

    buffer = ""

    print("Enter your SQL commands to execute in sqlite3 on database: ", db)
    print("Enter q to exit.")

    while True:
        line = input(">> ")
        if line == "q":
            break

        buffer += str(line).replace(">>","")
        if sqlite3.complete_statement(buffer):
            try:
                buffer = buffer.strip()

                cur.execute(buffer)
                if buffer.lstrip().upper().startswith("SELECT"):
                    print(cur.fetchall())

                print("%s ROWS AFFECTED"%cur.rowcount)

            except sqlite3.Error as e:
                print(buffer)
                print("An error occurred:", e.args[0])

            buffer = ""

    con.close()


import code
def interactive_console():
    code.interact()


import console
def shell():
    console.run()


import webbrowser
def browse(url):
    webbrowser.open(url)

def google():
    browse('www.google.com')

def mysite():
    browse('www.abiiranathan.pythonanywhere.com')


from configparser import ConfigParser
class ConfigReader:
    def __init__(self, filename):
        self.config = ConfigParser()
        self.config.optionxform = str
        self.config.read(filename)

    def get(self, section, name):
        return self.config.get(section, name)

    def sections(self):
        return [section for section in self.config.sections()]
    
    def options(self, section):
        return self.config.options(section)

    def as_dict(self):
        d= {}
        for section in self.sections():
            for option in self.options(section):
                value = self.config.get(section, option)
                d[option] = value

        return d

    def __getitem__(self, key):
        return self.as_dict()[key]

    def __getattr__(self, name):
        return self.config.__getattribute__(name)


from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

def compute_age(dob, deceased=False, dod=""):
    today = datetime.today().date()
    dob = dob.replace("/", "-")
    try:
        start = datetime.strptime(str(dob), '%Y-%m-%d')
    except ValueError:
        return ("", "", "")

    end = datetime.strptime(str(today),'%Y-%m-%d')
    if deceased and dod:
        end = datetime.strptime(str(dod), '%Y-%m-%d %H:%M')

    rdelta = relativedelta(end, start)

    years = rdelta.years
    months= rdelta.months
    days= rdelta.days
    return (years, months, days)



all = [
'ConfigReader',
'shell', 'browse', 'mysite', 'google','silence_errors', 
'silence_all_class_errors', 'console',
'sqlite3', 'InitMeta', 'WorkingDir',
'Diagnosis', 'BP', 'num2words', 'parse_date',
'as_date', 'as_datetime', 'as_date_str', 
'as_datetime_str', 'interactive_console',
'evaluate','viewcode','Treeview','showToolTip',
'SearchEngine', 'GUIFramework', 'calculate_dose', 'fraction']
