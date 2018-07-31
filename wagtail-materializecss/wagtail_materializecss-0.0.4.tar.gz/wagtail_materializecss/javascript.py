from django.utils.translation import ugettext_lazy as _

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


__all__ = ['Carousel']


class Carousel(blocks.ListBlock):
    """Breadcrumb that show the page hierarchy. This breadcrumb should be a list of links that point back to the
    root page.
    """
    def __init__(self, child_block=None, **kwargs):
        if child_block is None:
            child_block = ImageChooserBlock()
        super().__init__(child_block, **kwargs)

    class Meta:
        label = _('Carousel')
        icon = 'image'
        template = 'wagtail_materializecss/javascript/carousel.html'
