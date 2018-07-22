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


class Parser(object):
    """General purpose parser.

    Used to extract various text lines of statements from a provided context
    source. E.g. extract accepted statements from action handlers.
    """

    @classmethod
    def lookahead(cls, ctx, header, start_line=-1, first_only=True):
        """Context parser.

        Args:
            ctx (str or list): Context to scan.
            header      (str): Needle to lookup in context.
            start_line  (int): Context offset.

        Returns:
            list: List of statements extracted from context.
        """

        if isinstance(ctx, (str, unicode)):
            ctx = ctx.splitlines()
        for idx, line in enumerate(ctx):
            text = line.strip()
            if start_line > -1 and not text:
                return ctx[start_line+1:idx]
            if text.lower().startswith(header):
                if first_only and start_line > -1:
                    continue
                start_line = idx
        return []
