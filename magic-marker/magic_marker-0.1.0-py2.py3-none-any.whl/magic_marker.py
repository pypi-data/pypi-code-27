# -*- coding: utf-8 -*-

"""MagicMarker is a tool that automatically marks pytests with a UUID"""
# ======================================================================================================================
# Imports
# ======================================================================================================================
from __future__ import absolute_import
from flake8.main.cli import main as flake8_main
from contextlib import contextmanager
import sys
import six
import json
import uuid
import re
import tempfile
import string
import random
import shutil
import errno
import os


class MagicMarker(object):

    def __init__(self, mark):
        """Crate a new MagicMarker object

        Args:
            mark (str): The mark to create
        """
        self._mark = mark
        dir_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
        self._backup_path = os.path.join(tempfile.gettempdir(), dir_name)

    @property
    def backup_path(self):
        return self._backup_path

    def run_flake8_and_mark(self, path):
        """Run flak8 and edit and fix errors

        Args:
            path (str): The path to target for the fix

        Returns:
            str: the message stating what was performed
        """

        args = [
            'flake8',
            path,
            "--format=json",
            "--pytest-mark1=name={},value_match=uuid".format(self._mark),
            "--select=M501"  # only covers case of no mark present
        ]

        with self.patch_sys_argv(args), self.captured_stdout() as stdout:
            try:
                flake8_main()
            except SystemExit:
                pass  # This is raised by flake8

        flake8_output = json.loads(stdout.getvalue())
        self._backup_whole_path(path)
        return self.fix_it(flake8_output)

    def _backup_whole_path(self, path):
        """Backup the entire target

        Args:
            path (str): the path to copy
        """
        try:
            shutil.copytree(path, self._backup_path)
        except OSError as exc:  # python >2.5
            if exc.errno == errno.ENOTDIR:
                # its a single file
                shutil.copy(path, self.backup_path)
            else:
                raise RuntimeError("Magic Marker was not able to backup the target {}".format(path))

    def fix_it(self, flake8_output):
        """Perform the fix

        Args:
            flake8_output (str): The parsed json data from flake8-json

        Returns:
            str: the message stating what was performed
        """
        message = ""
        for file_path in flake8_output:
            if flake8_output[file_path]:
                filname, fixcount = self._fix_file(flake8_output[file_path])
                if fixcount == 1:
                    message += "\n{} : {} test marked with UUID".format(filname, fixcount)
                else:
                    message += "\n{} : {} tests marked with UUID".format(filname, fixcount)
        if message:
            return message
        else:
            return "No changes made"

    def _fix_file(self, fixes_required):
        """Fixes an individual file

        Args:
            fixes_required (list[dict]): a list of the fixes required for this file

        Returns:
            tuple(str, str):  filename and number of fixes performed
        """
        filename = str(fixes_required[0]['filename'])
        with open(filename, 'r') as f:
            data = f.readlines()

        fixes_required.sort(key=lambda x: x['line_number'])
        fixes_required.reverse()  # work from the bottom of the file up
        for fix in fixes_required:
            fix_position = fix['line_number']
            if fix_position:
                fix_position += -1
            mark = self._match_indent(data[fix_position], self._uuid_mark())
            data.insert(fix_position, mark)

        with open(filename, 'w') as f:
            f.writelines(data)
        return filename, len(fixes_required)

    def _uuid_mark(self):
        """generate a UUID mark string

        Returns:
            str: the correctly formatted UUID mark string
        """
        return "@pytest.mark.{}('{}')\n".format(self._mark, str(uuid.uuid1()))

    @staticmethod
    def _match_indent(def_string, target_line):
        """Match the indent of the original string

        Args:
            def_string (str): the original string from the test definition
            target_line (str): the string that should be updated

        Returns:
            str : The new string updated with correct whitespace
        """
        whitespace = re.match('(^\s*)', def_string).group(1)
        if whitespace:
            target_line = whitespace + target_line
        return target_line

    @contextmanager
    def patch_sys_argv(self, new_argv):
        """Patch argv

        Args:
            new_argv (list): the desired argv

        Yields:
            None
        """
        orig = sys.argv
        sys.argv = new_argv
        yield
        sys.argv = orig

    @contextmanager
    def captured_output(self, stream_name):
        """Return a context manager used by captured_stdout/stdin/stderr
        that temporarily replaces the sys stream *stream_name* with a StringIO.

        Args:
            stream_name (str): The name of the stream to capture

        Yields:
            StringIO

        Note: This function and the following ``captured_std*`` are copied
              from CPython's ``test.support`` module."""
        orig_stdout = getattr(sys, stream_name)
        setattr(sys, stream_name, six.StringIO())
        try:
            yield getattr(sys, stream_name)
        finally:
            setattr(sys, stream_name, orig_stdout)

    def captured_stdout(self):
        """Capture the output of sys.stdout:
           with captured_stdout() as stdout:
               print("hello")
           self.assertEqual(stdout.getvalue(), "hello\n")

        Returns:
            GeneratorContextManager
        """
        return self.captured_output("stdout")
