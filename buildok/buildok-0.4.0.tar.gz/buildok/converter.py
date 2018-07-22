# Copyright 2018 Alexandru Catrina
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os

from buildok.converters.bash import BashConverter


class Converter(object):
    """Translate build steps to script files.

    Used as a converter wrapper for multiple scriping files.

    Args:
        workdir     (str): Working directory.
        conv_target (str): Choosen target to convert.
        tpl_target  (str): Unpacked holder for script parameters.
    """

    target_name, target_class = None, None
    workdir = os.getcwd()
    prefix = "convert_"

    @classmethod
    def prepare(cls, target):
        if target == "shell" or target == "bash":
            cls.target_class = BashConverter
            cls.target_name = "shell"
        elif target == "vagrant":
            raise Exception("Unsupported yet: %s" % target)
        elif target == "docker":
            raise Exception("Unsupported yet: %s" % target)
        elif target == "jenkins":
            raise Exception("Unsupported yet: %s" % target)
        elif target == "ansible":
            raise Exception("Unsupported yet: %s" % target)
        else:
            raise Exception("Unsupported target: %s" % target)

    @classmethod
    def check(cls):
        return cls.target_name is not None and cls.target_class is not None

    @classmethod
    def save(cls, steps):
        lines = []
        method = "%s%s" % (cls.prefix, cls.target_name)
        for step in steps:
            if not hasattr(step.action, method):
                continue
            if not isinstance(step.args, tuple):
                step.args = ()
            func = getattr(step.action, method)
            comment = "\n# %s" % step.step
            cmdline = func(*step.args, payload=step.payload)
            lines.append("%s\n%s" % (comment, cmdline))
        with open(os.path.join(cls.workdir, cls.target_class.filename), "w") as file_:
            data = cls.target_class.template.format(body="\n".join(lines))
            file_.write(data)
