# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

import glob
import os
import sys
import inspect
import subprocess
import datetime
from textwrap import dedent
from ruamel.std.pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import PreservedScalarString

Bugs = """\
- check empty documents. E.g. !python that only has code in !pre, and !stdout
  without any introductory text
- running with python2 on ruamel.yaml doc will raise str vs unicode issue
"""

ToDo = """\
- some mechanism to show the name, leave option for 'skipping'/'converting'
  comment and push out newline later. Test incombination with verbosity
- specify Python interpreter, or create virtualenv + package installs, in a better
  way than using RYD_PYTHON env var.
- formalize temporary directory
- store (prefixed) program, only execute when !stdout is requested.
- parse messages like:
  README.rst:72: (ERROR/3) Inconsistent literal block quoting.
  and show output context
- zoom in on errors that have no line number: `some name <>`__
- document handling of :: in RST, and need for |+ in stdraw
- describe yaml comments after `|+ # `
- support code-block directive  http://rst2pdf.ralsina.me/handbook.html#syntax-highlighting
- list structure of the .ryd file
- process documents using xyz:prog  matching the document tag xyz by rt piping through prog
- why do toplevel PreservedScalarString dumps have |2, it is not even correct!
"""


class RYD(object):
    def __init__(self, args, config):
        self._args = args
        self._config = config
        self._name_printed = False
        self._current_path = None

    def convert(self):
        for file_name in self._args.file:
            self._name_printed = False
            if '*' in file_name or '?' in file_name:
                for exp_file_name in sorted(glob.glob(file_name)):
                    self.convert_one(Path(exp_file_name))
                continue
            self.convert_one(Path(file_name))

    def clean(self):
        for file_name in self._todo():
            self.convert_one(file_name, clean=True)

    def _todo(self):
        todo = []
        for file_name in self._args.file:
            self._name_printed = False
            if file_name[0] == '*':
                for exp_file_name in sorted(Path('.').glob(file_name)):
                    todo.append(exp_file_name)
                    continue
            if '*' in file_name or '?' in file_name:
                for exp_file_name in sorted(glob.glob(file_name)):
                    todo.append(Path(exp_file_name))
                continue
            todo.append(Path(file_name))
        # print('todo', todo)
        return todo

    def name(self):
        """print name of file only once (either verbose or on error)"""
        if self._name_printed:
            return
        self._name_printed = True
        print(self._current_path)

    def convert_one(self, path, clean=False):
        self._current_path = path
        if self._args.verbose > 0:
            self.name()
        yaml = YAML()
        convertor = None
        for x in yaml.load_all(path):
            if convertor is None:
                assert 0.099 < float(x['version']) < 0.101
                if x['output'] == 'rst':
                    convertor = RSTConvertor(self, yaml, x, path)
                else:
                    raise NotImplementedError
                continue
            if clean:
                convertor.clean()
                return
            if not convertor(x):  # already up-to-date
                sys.stdout.flush()
                return
        if convertor.updated:
            print('updated')
        convertor.write()
        # convertor.dump()
        sys.stdout.flush()

    def from_rst(self):
        for file_name in (Path(f) for f in self._args.file):
            ryd_name = file_name.with_suffix('.ryd')
            if ryd_name.exists() and not self._args.force:
                print('skipping', ryd_name)
                continue
            print('writing', ryd_name)
            rst = reStructuredText(file_name)
            rst.analyse_sections()
            with ryd_name.open('w') as fp:
                fp.write(
                    dedent("""\
                ---
                version: 0.1
                output: rst
                fix_inline_single_backquotes: true
                # pdf: true
                --- |
                """)
                )
                fp.write(rst.update_sections())

    def roundtrip(self):
        for file_name in self._todo():
            self.round_trip_one(file_name)

    def round_trip_one(self, path):
        self._current_path = path
        if self._args.verbose > 0:
            self.name()
        yaml = YAML()
        convertor = None
        for x in yaml.load_all(path):
            if convertor is None:
                convertor = RoundTripConvertor(self, yaml, x, path)
                continue
            convertor(x)
        if convertor.updated:
            convertor.write()


class reStructuredText(object):
    def __init__(self, path):
        self._path = path
        self._lines = None
        self._blank = set([-1])  # in case you have a divider on the first line
        self._section_lines = {}
        self._divider_lines = set()
        self._double_section = ""  # above and below
        self._double_section_lines = {}
        self._single_section = ""  # only below
        self._single_section_lines = {}

    @property
    def lines(self):
        if self._lines is None:
            self._lines = self._path.read_text().splitlines()
        return self._lines

    def analyse_sections(self):
        non_alpha = '\'"#*=-^+'
        non_alpha = '=-`:\'"~^_*+#<>.'

        def char_repeats(line):
            """assume a stripped line, check if the first character is repeated"""
            idx = len(line)
            while idx > 1:
                idx -= 1
                if line[idx] != line[0]:
                    return False
            return True

        # for x in ['===', '==', '=', 'x=']:
        #    print(x, char_repeats(x))
        current_level = 0  # NOQA
        previous_blank = False  # NOQA
        for line_number, line in enumerate(self.lines):
            s_line = line.strip()
            if not s_line:
                self._blank.add(line_number)
                previous_blank = True
                continue  # empty line
            fc = line[0]  # first character
            if fc not in non_alpha or not char_repeats(s_line):
                previous_blank = False  # NOQA
                continue
            self._section_lines[line_number] = s_line
        # print(self._blank)
        for line_number in self._section_lines:
            if (line_number - 1) in self._blank and (line_number + 1) in self._blank:
                self._divider_lines.add(line_number)
        for line_number in self._divider_lines:
            del self._section_lines[line_number]
        # cleaned up, now analyse
        line_numbers = sorted(self._section_lines.keys())
        idx = -1
        single_level = 0
        while idx < len(line_numbers) - 1:
            idx += 1
            line_number = line_numbers[idx]
            line = self._section_lines[line_number]
            # print(line_number, self._section_lines[line_number])
            if line_number + 2 in self._section_lines:
                if line[0] == self._section_lines[line_number + 2][0]:
                    pass
                    # print('double', line_number)
                else:
                    print('non-matching over-under-line', line_number)
                    sys.exit(1)
                idx += 1  # skip the matching underline
                if not self._double_section and self._single_section:
                    print("don't know how to handle over-under-line after under-line")
                    sys.exit(1)
                if line[0] not in self._double_section:
                    self._double_section += line[0]
                self._double_section_lines.setdefault(line[0], []).extend(
                    [line_number, line_number + 2]
                )
                single_level = 0
                continue
            if line[0] not in self._single_section:
                if single_level != len(self._single_section):
                    print('unexpected underline level', line_number, single_level)
                    sys.exit(1)
                self._single_section += line[0]
                single_level += 1
            else:
                single_level = self._single_section.index(line[0]) + 1
            self._single_section_lines.setdefault(line[0], []).append(line_number)

        print('double:', self._double_section)
        print('       ', self._double_section_lines)
        print('single:', self._single_section)
        print('       ', self._single_section_lines)

    def update_sections(self):
        # almost the Python recomendation, but not using '-' for sections
        double = '#*'
        single = '=+^"'
        assert len(double) >= len(self._double_section)
        assert len(single) >= len(self._single_section)
        for level, ch in enumerate(self._double_section):
            new_ch = double[level]
            for line_number in self._double_section_lines[ch]:
                self.lines[line_number] = new_ch * len(self.lines[line_number])
        for level, ch in enumerate(self._single_section):
            new_ch = single[level]
            for line_number in self._single_section_lines[ch]:
                self.lines[line_number] = new_ch * len(self.lines[line_number])
        return '\n'.join(self.lines)


##############################################################################


class RydDoc(PreservedScalarString):
    @classmethod
    def from_yaml(cls, constructor, node):
        return cls(node.value)

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_preserved_scalarstring(cls.yaml_tag, node.value)


# class BashRaw(RydDoc):
#     """Invoke bash on the document as script.
#     """
#     yaml_tag = '!bash-raw'


class Code(RydDoc):
    """Include program in text. Do not mark as executable, doesn't influence ``!stdout``
    """

    yaml_tag = '!code'


class Comment(RydDoc):
    """The whole document will be discarded, i.e. not included in the output.

    This allows commenting out complete sections in an output independent way.
    """

    yaml_tag = '!comment'


class IncRaw(RydDoc):
    """Include the listed files raw (i.e. without processing) into the output.

    If a file name doesn't start with ``/``, it is considered to be relative to the
    directory of the output path.
    """

    yaml_tag = '!incraw'


class Python(RydDoc):
    """Include Python program in text. Prefix and mark as executable.
    """

    yaml_tag = '!python'


class PythonPre(RydDoc):
    """Prefix all following ``!python`` documents with this document (e.g. used for imports)

    This part will not be be shown. The content should be a python program, that
    will be used as prefix for following programs which can be incomplete.
    This is useful for  suppressing repetive import statements.
    """

    yaml_tag = '!python-pre'


class Stdout(RydDoc):
    """Include output from last executable document (e.g. ``!python``) as code.

    """

    yaml_tag = '!stdout'


class StdoutRaw(RydDoc):
    """
    Include output from the last program, as source for the output format.

    This can be used to e.g. have a program generate an definition list programmatically.
    """

    yaml_tag = '!stdout-raw'


##############################################################################


class Convertor:
    def __init__(self, ryd):
        self._ryd = ryd
        self._tempdir = None
        self._tmpfile_nr = 0
        self._tag_obj = {}
        self._tag_doc = {}
        for _name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj) and obj is not RydDoc and issubclass(obj, RydDoc):
                self._tag_obj[obj.yaml_tag] = obj
                d = obj.__doc__ if obj.__doc__ is not None else 'N/A\n  N/A'
                d1, d2 = d.lstrip().split('\n', 1)
                d1 = d1.strip()
                d2 = dedent(d2).lstrip()
                self._tag_doc[obj.yaml_tag] = [d1, d2]
        # for k in sorted(self.tags):
        #     print(k, '->', self.tags[k])

    @property
    def tempdir(self):
        from ruamel.std.pathlib.tempdir import TempDir

        if self._tempdir is None:
            self._tempdir = TempDir(prefix='ryd', keep=3)
        return self._tempdir

    def get_tags(self):
        return self._tag_doc

    def update(self, s):
        return s

    def clean(self):
        assert self._path.exists()
        if self._out_path.exists():
            self._out_path.unlink()

    python_exe = os.environ.get('RYD_PYTHON', 'python')

    def check_output(self, s):
        p = self.tempdir.directory / 'tmp_{}.py'.format(self._tmpfile_nr)
        self._tmpfile_nr += 1
        p.write_text(s)
        try:
            return subprocess.check_output(
                [self.python_exe, str(p)], stderr=subprocess.STDOUT
            ).decode('utf-8')
        except subprocess.CalledProcessError as e:  # NOQA
            res = e.output.decode('utf-8')
            sys.stdout.write(res)
            if 'ImportError: No module named ryd.ryd' in res:
                print(
                    '\nWhen generating ryd documentation use:\n'
                    '  RYD_PYTHON=/opt/util/ryd/bin/python ryd ...'
                )
            return None


class RSTConvertor(Convertor):
    def __init__(self, ryd, yaml, md, path):
        super().__init__(ryd)
        self._yaml = yaml
        for v in self._tag_obj.values():
            yaml.register_class(v)
        self._md = md
        self._path = path
        self._out_path = self._path.with_suffix('.rst')
        self.data = []
        self.last_output = ""
        self.updated = False
        self.python_pre = ""
        # register all defined classes and store tag + comment

    def __call__(self, s):
        # the read is at the end
        if (
            not self._ryd._args.force
            and self._out_path.exists()
            and self._path.stat().st_mtime < self._out_path.stat().st_mtime
        ):
            if self._ryd._args.verbose > 0:
                print('skipping', end=' ')
                self._ryd.name()
            return False
        self._line = self._yaml.reader.line - s.count('\n') + 1
        sx = self.update(s)
        if sx:
            self.updated = True
            self.data.append(sx)
        else:
            self.data.append(s)
        return True

    def update(self, s):
        # if isinstance(s, RydDoc) and not isinstance(s, Python):
        #     print(type(s))
        if isinstance(s, Python):
            return None
        # find all backquotes in document
        bqs = []
        lines = [0]  # character index in file to beginning of each line
        line = 0
        col = 0
        for idx, ch in enumerate(s):
            if ch == '`':
                bqs.append((idx, line, col))
            elif ch == '\n':
                lines.append(idx + 1)
                line += 1
                col = 0
                continue
            col += 1
        lines.append(None)  # for last line
        bqidx = 0
        last_line_displayed = -1
        while bqidx < len(bqs):
            lnr = bqs[bqidx][1]
            # ``pair of double backquotes`` -> code
            try:
                if s[lines[lnr]] == ' ' and s[lines[lnr] + 1] == ' ':
                    # first characters on line are spaces -> code/ryd example
                    bqidx += 1
                    continue
            except IndexError:
                print('error')
                pass
            if (
                bqidx + 3 <= len(bqs)
                and bqs[bqidx][0] + 1 == bqs[bqidx + 1][0]
                and bqs[bqidx + 2][0] + 1 == bqs[bqidx + 3][0]
            ):
                bqidx += 4
                continue
            # unmatched double backquotes
            # if bqidx + 1 <= len(bqs) and \
            #    bqs[bqidx][0] + 1 ==  bqs[bqidx+1][0]:

            # :cmd:`some string`
            if bqidx > 0 and s[bqs[bqidx][0] - 1] == ':':
                bqidx += 2
                continue
            # `some <url>`_
            try:
                if bqidx + 1 < len(bqs) and s[bqs[bqidx + 1][0] + 1] == '_':
                    bqidx += 2
                    continue
            except IndexError:
                pass  # probably end of file
            self._ryd.name()
            if lnr != last_line_displayed:
                print(
                    '{}: {}'.format(lnr + self._line, s[lines[lnr] : lines[lnr + 1]]), end=""
                )

                last_line_displayed = lnr
            print(' ' * (-1 + len(str(lnr + self._line)) + bqs[bqidx][2]), '--^')
            bqidx += 1
        return None

    def rst2pdf(self, file_path):
        fn = str(file_path)
        return subprocess.check_output(['rst2pdf', fn, '-s', 'freetype-sans,eightpoint'])

    def write(self):
        with self._out_path.open('w') as fp:
            self.dump(fp, base_dir=self._out_path.parent)
        if self._ryd._args.pdf is False:  # can be None
            return
        if self._ryd._args.pdf or self._md.get('pdf'):
            self.rst2pdf(self._out_path)
            if self._md.get('encrypt'):
                pw = self._md['encrypt']['passwd']
                # print('pw', pw, file=sys.stderr)
                pdf_file = self._out_path.with_suffix('.pdf')
                enc_file = self._out_path.with_suffix(
                    '.{:%Y%m%d}.pdf'.format(datetime.date.today())
                )
                # self._out_path.rename(tmp_file)
                subprocess.check_output(
                    ['pdftk', str(pdf_file), 'output', str(enc_file), 'user_pw', pw]
                )

    def dump(self, fp=sys.stdout, base_dir=None):
        last_ended_in_double_colon = False
        last_code = False
        for d in self.data:
            if isinstance(d, IncRaw):
                if last_code:
                    last_code = False
                    print(file=fp)
                for line in d.strip().splitlines():
                    if not line:
                        continue
                    if base_dir is not None and line[0] != '/':
                        p = base_dir / line
                    else:
                        p = Path(line)
                    print(p.read_text(), file=fp, end="")
            elif isinstance(d, (Python, Code)):
                if d:
                    if not last_ended_in_double_colon:
                        print('::\n', file=fp)
                    for line in d.strip().splitlines():
                        print(' ', line, file=fp)
                    last_code = True
                if isinstance(d, Python):
                    self.last_output = self.check_output(self.python_pre + d)
                    if self._ryd._args.verbose > 1:
                        print('=========== output =========')
                        print(self.last_output, end="")
                        print('============================')
                    if self.last_output is None:
                        sys.exit(1)
            elif isinstance(d, PythonPre):
                self.python_pre = d
            elif isinstance(d, Comment):
                pass
            else:
                drs = d.rstrip()
                if drs.endswith('::'):
                    last_ended_in_double_colon = True
                    d = type(d)(drs + '\n\n')
                if last_code:
                    last_code = False
                    print(file=fp)
                print(d, file=fp, end="")
                if isinstance(d, (Stdout, StdoutRaw)):
                    prefix = "" if isinstance(d, StdoutRaw) else '  '
                    for line in self.last_output.strip().splitlines():
                        print('{}{}'.format(prefix, line), file=fp)
                    last_code = True
                elif type(d) != PreservedScalarString:
                    print('found unknown document type:', d.yaml_tag)
                    sys.exit(1)
                # print(file=fp)


class RoundTripConvertor(Convertor):
    def __init__(self, ryd, yaml, md, path):
        super().__init__(ryd)
        self._yaml = yaml
        # for v in self._tag_obj.values():
        #     yaml.register_class(v)
        self._md = md
        self._path = path
        self._out_path = self._path  # .with_suffix('.ryd.new')
        self.data = [md]
        self.last_output = ""
        self.updated = False

    def __call__(self, x):
        if not self._ryd._args.oitnb:
            self.data.append(x)
            return
        try:
            v = x.tag.value
        except AttributeError:
            self.data.append(x)
            return
        if not v.startswith('!python') or not x.value.strip():
            self.data.append(x)
            return
        # only python with a real body
        y = subprocess.check_output(['oitnb', '-q', '-'], input=bytes(x.value, 'utf-8'))
        y = y.decode('utf-8')
        if x.value != y:
            print(x.value, y)
            self.updated = True
            x.value = y + '\n'
        self.data.append(x)

    def write(self):
        print('writing')
        self._yaml.explicit_start = True
        self._yaml.dump_all(self.data, self._out_path)
        # self._yaml.dump_all(self.data, sys.stdout)
