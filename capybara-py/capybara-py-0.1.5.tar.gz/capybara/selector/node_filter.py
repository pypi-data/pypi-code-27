from warnings import warn

from capybara.selector.abstract_filter import AbstractFilter


class NodeFilter(AbstractFilter):
    def matches(self, node, value):
        """
        Returns whether the given node matches the filter rule with the given value.

        Args:
            node (Element): The node to filter.
            value (object): The desired value with which the node should be evaluated.

        Returns:
            bool: Whether the given node matches.
        """

        if self.skip(value):
            return True

        if not self._valid_value(value):
            msg = "Invalid value {value} passed to filter {name} - ".format(
                value=repr(value),
                name=self.name)

            if self.default is not None:
                warn(msg + "defaulting to {}".format(self.default))
                value = self.default
            else:
                warn(msg + "skipping")
                return True

        return self.func(node, value)
