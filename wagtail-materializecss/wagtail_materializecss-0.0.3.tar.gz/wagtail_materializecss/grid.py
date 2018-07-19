import copy

from django.utils.html import format_html
from wagtail.core import blocks
from wagtail.core.blocks import BaseStreamBlock

__all__ = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'Row', 'Col', 'make_row_col_blocks']


class h1(blocks.CharBlock):
    def render_basic(self, value, context=None):
        if value:
            return format_html('<h1 class="scrollspy">{0}</h1>', value)
        else:
            return ''


class h2(blocks.CharBlock):
    def render_basic(self, value, context=None):
        if value:
            return format_html('<h2 class="scrollspy">{0}</h2>', value)
        else:
            return ''


class h3(blocks.CharBlock):
    def render_basic(self, value, context=None):
        if value:
            return format_html('<h3 class="scrollspy">{0}</h3>', value)
        else:
            return ''


class h4(blocks.CharBlock):
    def render_basic(self, value, context=None):
        if value:
            return format_html('<h4 class="scrollspy">{0}</h4>', value)
        else:
            return ''


class h5(blocks.CharBlock):
    def render_basic(self, value, context=None):
        if value:
            return format_html('<h5 class="scrollspy">{0}</h5>', value)
        else:
            return ''


class h6(blocks.CharBlock):
    def render_basic(self, value, context=None):
        if value:
            return format_html('<h6 class="scrollspy">{0}</h6>', value)
        else:
            return ''


class CustomStreamBlock(blocks.StreamBlock):
    """
    Identical to StreamBlock, except that we override the constructor to make it save self._base_blocks and
    self._dependencies, instead of self.base_blocks and self.dependencies. This lets us replace them with @properties.
    """

    def __init__(self, local_blocks=None, **kwargs):
        self._constructor_kwargs = kwargs

        # Note, this is calling BaseStreamBlock's super __init__, not FeatureCustomizedStreamBlock's. We don't want
        # BaseStreamBlock.__init__() to run, because it tries to assign to self.child_blocks, which it can't do because
        # we've overriden it with an @property. But we DO want Block.__init__() to run.
        super(BaseStreamBlock, self).__init__(**kwargs)

        # create a local (shallow) copy of base_blocks so that it can be supplemented by local_blocks
        self._child_blocks = self.base_blocks.copy()
        if local_blocks:
            for name, block in local_blocks:
                block.set_name(name)
                self._child_blocks[name] = block

        self._dependencies = self._child_blocks.values()

        # Additional blocks with circular dependencies
        self.additional_blocks = {}

    @property
    def child_blocks(self):
        blocks = {}
        blocks.update(self._child_blocks)
        blocks.update(self.additional_blocks)
        return blocks

    @property
    def dependencies(self):
        blocks = {}
        blocks.update(self._child_blocks)
        blocks.update(self.additional_blocks)
        return blocks

    def _check_name(self, **kwargs):
        """
        Helper method called by container blocks as part of the system checks framework,
        to validate that this block's name is a valid identifier.
        (Not called universally, because not all blocks need names)
        """
        errors = []
        return errors


class Row(CustomStreamBlock):
    """Row ('div' tags)

    See Also:
        make_row_col_blocks
    """
    def __init__(self, local_blocks=None, col_block=None, **kwargs):
        if local_blocks is None and col_block:
            local_blocks = col_block.child_blocks.copy()
        super().__init__(local_blocks, **kwargs)

        if col_block:
            self.additional_blocks['col'] = col_block
            try:
                col_block.additional_blocks['row'] = self
            except AttributeError:
                pass

    class Meta:
        template = 'wagtail_materializecss/grid/row.html'


class Col(blocks.StreamBlock):
    """Col ('div' tags)

    See Also:
        make_row_col_blocks
    """
    small = blocks.IntegerBlock(required=False, blank=True)
    medium = blocks.IntegerBlock(required=False, blank=True)
    large = blocks.IntegerBlock(required=False, blank=True)
    xl = blocks.IntegerBlock(required=False, blank=True)

    content = blocks.StreamBlock()

    class Meta:
        template = 'wagtail_materializecss/grid/col.html'


def make_row_col_blocks(local_blocks=None):
    """This function returns a list of StreamBlock arguments with row and col. Because row and col can be inside of
    each other there is a problem with cyclic dependencies."""
    col = Col(local_blocks)
    row = Row(local_blocks, col_block=col)

    return [('row', row), ('col', col)]
