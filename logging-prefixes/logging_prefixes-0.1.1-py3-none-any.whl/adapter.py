import logging

import attr


@attr.s
class PrependAdapter(logging.LoggerAdapter):
    """This class ensures the path to the widget is represented in the log records."""

    logger = attr.ib()
    prefix = attr.ib()

    def process(self, msg, kwargs):
        # Sanitizing %->%% for formatter working properly
        sanitized_path = self.prefix.replace("%", "%%")
        return "[{}]: {}".format(sanitized_path, msg), kwargs

    def __repr__(self):
        return "{}({!r}, {!r})".format(
            type(self).__name__, self.logger, self.extra["widget_path"]
        )

    @classmethod
    def from_parent(cls, parent, suffix_for_prefix, joinby="/"):
        if isinstance(parent, cls):
            return type(parent)(
                logger=parent.logger, prefix=parent.prefix + joinby + suffix_for_prefix
            )
        else:
            return cls(logger=parent, prefix=suffix_for_prefix)

    def child_logger(self, child_name):
        return self.from_parent(self, child_name)

    def item_logger(self, item):
        return self.from_parent(self, "[{!r}]".format(item), joinby="")
