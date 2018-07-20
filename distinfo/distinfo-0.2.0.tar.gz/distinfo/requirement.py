import logging

from packaging.requirements import InvalidRequirement, Requirement as _Requirement

import pkg_resources

from .base import Base

log = logging.getLogger(__name__)


class Requirement(Base, _Requirement):

    def __init__(self, requirement_string):
        super().__init__(requirement_string)
        self.requirement_string = requirement_string

    def __hash__(self):
        # hack: makes it easy to check if a set contains the requirement
        return hash(self.name.lower())

    def __eq__(self, other):
        if isinstance(other, str):
            other = type(self)(other)
        elif not isinstance(other, type(self)):
            return False
        if self.name.lower() == other.name.lower():
            if self.specifier == other.specifier:
                return True
            if not self.specifier or not other.specifier:
                return True
        return False

    def __dump__(self):
        return str(self).split(";")[0]

    @classmethod
    def parse_file(cls, path):
        for line in pkg_resources.yield_lines(open(path)):
            try:
                yield cls(line)
            except InvalidRequirement as exc:
                log.warning("line %r of %r raised %r", line, path, exc)
