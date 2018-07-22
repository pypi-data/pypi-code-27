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

import re


class Topic(object):
    """A topic is a word or a small phrase to identify proper build steps.

    Class arguments:
        TOPIC         (str): Project topic to lookup.
        TOPIC_MXLIMIT (int): Max. string limit for topic lookup.
        TOPIC_PATTERN (exp): Regular expression to match topci pattern.
        PATTERN     (RegEx): Compiled regex.
        __topics     (list): Private list of topic instances.

    Args:
        order   (int): Order of appearance in build steps.
        title   (str): Topic name as found by pattern matching.
        steps  (list): List of instructions.
    """

    TOPIC = r""
    TOPIC_MXLIMIT = 24
    TOPIC_PATTERN = None
    PATTERN = None

    __topics = []

    def __init__(self, order=None, title=None, steps=None):
        self.order = order
        self.title = title
        self.steps = steps
        self.__topics.append(self)

    def set_position(self, value):
        """Topic position setter.

        Args:
            value (int): Topic position order.

        Raises:
            TypeError: If value is not an unsigned interger.
        """

        if not isinstance(value, int) or value < 0:
            raise TypeError("Position must be an unsigned integer")
        self.order = value

    def get_position(self):
        """Topic position getter.

        Returns:
            int: Topic order.
        """

        return self.order

    def set_title(self, value):
        """Topic setter for title.

        Args:
            value (str): Topic title.

        Raises:
            TypeError: If value is not a string.
        """

        if not isinstance(value, (str, unicode)):
            raise TypeError("Unsupported title")
        self.title = value

    def get_title(self):
        """Topic getter for title.

        Returns:
            str: Title of topic.
        """

        return self.title

    def has_step(self, step):
        """Lookup step string in steps list.

        Args:
            step (str): Step string to lookup.

        Returns:
            bool: True if step exists, otherwise False.
        """

        for s in self.steps:
            if s.get_step().lower() == step.lower():
                return True
        return False

    def add_step(self, step):
        """Appends step to topic instance.

        Args:
            step (str): Step string managed by current topic.
        """

        if self.steps is None:
            self.steps = []
        self.steps.append(step)

    def set_steps(self, value):
        """Topic setter for instructions list.

        Args:
            value (list): Instructions list.

        Raises:
            TypeError: If value is not a valid list.
        """

        if not isinstance(value, list):
            raise TypeError("Unsupported instructions list")
        self.steps = value

    def get_steps(self):
        """Topic getter for instructions list.

        Returns:
            list: List of instructions.
        """

        return self.steps

    @classmethod
    def get_all_topics(cls):
        """Return stored topic instances.

        Returns:
            list: List of stored topics.
        """

        return cls.__topics

    @classmethod
    def set_project_topic_pattern(cls, topic_pattern):
        """Change project topic pattern.

        A project topic pattern is a regular expression used to find and extract
        topics from a build file. By default it matches all lines containing the
        word "build" in the first 10 characters.

        Args:
            pattern (str): New topic pattern.

        Raises:
            ValueError: If project topic is not a string.
            Exception:  If project topic exceeds MAX_TOPIC_LIMIT.
        """

        if not isinstance(topic_pattern, (str, unicode)):
            raise ValueError("Project topic pattern must be string")
        cls.TOPIC_PATTERN = topic_pattern

    @classmethod
    def set_project_topic(cls, project_topic):
        """Change project topic.

        A project topic is a word or a phrase to lookup when scanning the
        entire build file. Default is "build instructions".

        Args:
            project_topic (str): New project topic.

        Raises:
            ValueError: If project topic is not a string.
            Exception:  If project topic exceeds MAX_TOPIC_LIMIT.
        """

        if not isinstance(project_topic, (str, unicode)):
            raise ValueError("Project topic must be string")
        if len(project_topic) > cls.TOPIC_MXLIMIT:
            raise Exception("Project topic exceeds characters limit")
        cls.TOPIC = project_topic

    @classmethod
    def prepare(cls, default=r"\w+"):
        """Prepare filter.

        Args:
            default (str): A default pattern to fallback.

        Returns:
            Topic: class instance.
        """

        if cls.TOPIC_PATTERN is None:
            cls.TOPIC_PATTERN = default
        cls.PATTERN = re.compile(cls.TOPIC_PATTERN, re.I)
        return cls

    def __repr__(self):
        return unicode(self.__dict__)
