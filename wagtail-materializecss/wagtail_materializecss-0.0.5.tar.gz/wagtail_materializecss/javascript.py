from django.utils.translation import ugettext_lazy as _

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


__all__ = ['Carousel', 'Parallax']


class Carousel(blocks.ListBlock):
    """Carousel ('div' tag) to cycle through different images."""
    def __init__(self, child_block=None, **kwargs):
        if child_block is None:
            child_block = ImageChooserBlock()
        super().__init__(child_block, **kwargs)

    class Meta:
        label = _('Carousel')
        icon = 'image'
        template = 'wagtail_materializecss/javascript/carousel.html'


class Parallax(blocks.StructBlock):
    """Multiple parallaxes on a page will make a fun scroll effect."""
    image = ImageChooserBlock(required=True)

    class Meta:
        label = _('Parallax')
        icon = 'image'
        template = 'wagtail_materializecss/javascript/parallax.html'
