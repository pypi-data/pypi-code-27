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


class Guide(object):
    """A guide is a collection of topics.

    Class arguments:
        __guides (list): Private list of guides.

    Args:
        topics (tuple): Imutable list of topics.
    """

    __guides = []

    def __init__(self, topics=None):
        self.topics = topics
        self.__guides.append(self)

    def add_topic(self, topic):
        """Appends topic to guide instance.

        Args:
            topic (str): Topic managed by current guide.
        """
        if self.topics is None:
            self.topics = []
        self.topics.append(topic)

    def set_topics(self, value):
        """Guide setter for topics list.

        Args:
            value (list): Topics list.

        Raises:
            TypeError: If value is not a valid list.
        """
        if not isinstance(value, list):
            raise TypeError("Unsupported topics list")
        self.topics = value

    def get_topics(self):
        """Guide getter for topics list.

        Returns:
            list: List of topics.
        """
        return self.topics

    def get_topic_by_title(self, title):
        """Lookup topic by title and return instance.

        Returns:
            mixt: Instance of topic or None.
        """
        for t in self.topics:
            if t.get_title().lower() == title.lower():
                return t
        return None

    @classmethod
    def get_all_guides(cls):
        """Return stored guide instances.

        Returns:
            list: List of stored guides.
        """
        return cls.__topics

    def __repr__(self):
        return unicode(self.__dict__)
