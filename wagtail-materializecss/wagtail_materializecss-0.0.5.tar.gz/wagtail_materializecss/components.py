from django.utils.translation import ugettext_lazy as _
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


__all__ = ['LinkBlock', 'Badge', 'Button', 'FAB', 'Breadcrumb', 'Card', 'Collection', 'Icon', 'Preloader']


class LinkStructValue(blocks.StructValue):
    def url(self):
        external_url = self.get('external_url')
        page = self.get('page')
        if external_url:
            return external_url
        elif page:
            return page.url


class LinkBlock(blocks.StructBlock):
    """Link block ('a' tag) with the options to link to a page or external url. This block also has an icon option."""
    icon = blocks.CharBlock(max_length=50, required=False,
                            help_text='Material-Icons icon name')
    text = blocks.CharBlock(label="link text", required=True)
    page = blocks.PageChooserBlock(label="page", required=False,
                                   help_text="Link to an existing page.")
    external_url = blocks.URLBlock(label="external URL", required=False,
                                   help_text="Alternative external link if a page is not set.")

    class Meta:
        icon = 'site'
        value_class = LinkStructValue
        template = 'wagtail_materializecss/components/link_block.html'
        label = _('Link')


class Badge(blocks.StructBlock):
    """Badge ('span' tag) that notifies user that an item is unread."""
    number = blocks.IntegerBlock()
    is_new = blocks.BooleanBlock()

    class Meta:
        label = _('Badge')
        template = 'wagtail_materializecss/components/badge.html'


class Button(LinkBlock):
    """Button ('a' tag) is a link block that can have a set color."""
    color = blocks.CharBlock(max_length=25, default='', blank=True, required=False)

    class Meta:
        icon = 'link'
        value_class = LinkStructValue
        label = _('Button')
        template = 'wagtail_materializecss/components/button.html'


class FAB(blocks.StructBlock):
    """Floating action button. This block only has an icon, color, and link. This block has no text!"""
    color = blocks.CharBlock(max_length=25, default='', blank=True, required=False)
    icon = blocks.CharBlock(max_length=50, required=False,
                            help_text='Material-Icons icon name')
    page = blocks.PageChooserBlock(label="page", required=False,
                                   help_text="Link to an existing page.")
    external_url = blocks.URLBlock(label="external URL", required=False,
                                   help_text="Alternative external link if a page is not set.")

    class Meta:
        icon = 'plus-inverse'
        value_class = LinkStructValue
        template = 'wagtail_materializecss/components/fab.html'
        label = _('Floating Action Button')


class Breadcrumb(blocks.ListBlock):
    """Breadcrumb that show the page hierarchy. This breadcrumb should be a list of links that point back to the
    root page.
    """
    def __init__(self, child_block=None, **kwargs):
        if child_block is None:
            child_block = LinkBlock()
        super().__init__(child_block, **kwargs)

    class Meta:
        label = _('Breadcrumb')
        template = 'wagtail_materializecss/components/breadcrumb.html'


class Card(blocks.StructBlock):
    """Card to display content in many different ways."""
    title = blocks.CharBlock(default='', blank=True)
    content = blocks.RichTextBlock(default='', blank=True)
    actions = blocks.ListBlock(LinkBlock(label=_('Card Action')), default=[], blank=True, reqiured=False)

    CARD_SIZES = [
        ('', 'Not Set'),
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ]
    size = blocks.ChoiceBlock(choices=CARD_SIZES, default=CARD_SIZES[0][0], required=False)
    horizontal = blocks.BooleanBlock(default=False, required=False, blank=True)
    image = ImageChooserBlock(required=False)
    background_color = blocks.CharBlock(max_length=25, default='', blank=True, required=False)
    text_color = blocks.CharBlock(max_length=25, default='', blank=True, required=False)

    class Meta:
        label = _('Card')
        template = 'wagtail_materializecss/components/card.html'


class CollectionItem(blocks.StructBlock):
    """CollectionItem ('li' tag) is a list item that belongs in a stylized collection."""
    title = blocks.CharBlock()
    secondary_icon = blocks.CharBlock(default='', required=False, blank=True)

    class Meta:
        label = _('Collection Item')
        icon = 'list-ul'
        template = 'wagtail_materializecss/components/collection_item.html'


class CollectionLink(CollectionItem):
    """CollectionLink ('li' tag) is a link inside of list item that belongs in a stylized collection."""
    page = blocks.PageChooserBlock(label="page", required=False,
                                   help_text="Link to an existing page.")
    external_url = blocks.URLBlock(label="external URL", required=False,
                                   help_text="Alternative external link if a page is not set.")

    class Meta:
        label = _('Collection Link')
        icon = 'link'
        value_class = LinkStructValue
        template = 'wagtail_materializecss/components/collection_link.html'


class CollectionHeader(CollectionItem):
    """CollectionHeader ('li' tag) is a large header for a stylized collection."""
    class Meta:
        label = _('Collection Header')
        icon = 'title'
        template = 'wagtail_materializecss/components/collection_header.html'


class CollectionAvatar(blocks.StructBlock):
    """CollectionAvatar ('li' tag) is a bigger collection item that includes an image or icon."""
    image = ImageChooserBlock(required=False, blank=True, help_text="Main image (icon is an alternative option)")
    icon = blocks.CharBlock(required=False, blank=True, help_text="Main image as an icon instead of an image.")

    title = blocks.CharBlock()
    content = blocks.RichTextBlock(default='', required=False, blank=True)
    secondary_icon = blocks.CharBlock(default='', required=False, blank=True)

    class Meta:
        label = _('Collection Avatar')
        icon = 'user'
        template = 'wagtail_materializecss/components/collection_avatar.html'


class Collection(blocks.StreamBlock):
    """Collection ('ul' tag) is a stylized list containing different collection items."""
    header = CollectionHeader(required=False, blank=True)
    link = CollectionLink(required=False, blank=True)
    item = CollectionItem(required=False, blank=True)
    avatar = CollectionAvatar(required=False, blank=True)

    class Meta:
        label = _('Collection')
        icon = 'list-ul'
        # value_class = HasHeaderValue
        template = 'wagtail_materializecss/components/collection.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        value.has_header = any((block.block_type == 'header' for block in context['value']))
        return context


class Icon(blocks.CharBlock):
    """Simple icon tag for Material Icons."""
    class Meta:
        label = _('Icon')
        template = 'wagtail_materializecss/components/icon.html'


class PageColorStructValue(blocks.StructValue):
    def color_value(self):
        color = self.get('color')
        page = self.get('page')
        if color:
            return color
        elif page:
            try:
                return page.color
            except AttributeError:
                pass


class Preloader(blocks.StructBlock):
    """Preloader ('div' tag) progress bar."""
    determinate = blocks.BooleanBlock(default=False, required=False, blank=True)
    circular = blocks.BooleanBlock(default=True, required=False, blank=True)
    color = blocks.CharBlock(required=False, blank=True, help_text='Preloader color (leave blank to use page color.)')

    class Meta:
        label = _('Preloader')
        icon = 'spinner'
        value_class = PageColorStructValue
        template = 'wagtail_materializecss/components/preloader.html'
