from django import template
from django.utils.safestring import mark_safe
from wagtail.core.blocks import BoundBlock
from wagtail.core.models import Page

from .parse_token import parse_tag
from ..components import LinkBlock, Preloader

register = template.Library()


def get_page_context(context):
    """Return the site name and url."""
    self = context.get('self', None)
    page = context.get('page', self)
    request = context.get('request', None)
    try:
        site = page.get_site()
        site_name = site.site_name
        site_url = site.root_url
    except:
        site_name = None
        site_url = None
    if not site_name:
        site_name = page.title
        site_url = page.url
    return {'value': page, 'page': page, 'self': self, 'request': request,
            'site_name': site_name, 'site_url': site_url}


@register.inclusion_tag('wagtail_materializecss/dynamic_css.html', takes_context=True)
def include_dynamic_css(context, *lines):
    ctx = get_page_context(context)
    ctx['lines'] = lines
    return ctx


@register.inclusion_tag('wagtail_materializecss/components/navbar.html', takes_context=True)
def include_navbar(context, hide_links=False):
    ctx = get_page_context(context)
    ctx['hide_links'] = hide_links
    return ctx


@register.inclusion_tag('wagtail_materializecss/components/footer.html', takes_context=True)
def include_footer(context):
    ctx = get_page_context(context)
    return ctx


@register.inclusion_tag('wagtail_materializecss/javascript/scrollspy.html', takes_context=True)
def include_table_of_contents(context):
    """Create a table of contents using scrollspy. This depends on header blocks with class="scrollspy"."""
    ctx = get_page_context(context)
    return ctx


@register.inclusion_tag('wagtail_materializecss/components/preloader.html', takes_context=True)
def make_preloader(context, circular=True, determinate=False, color=''):
    ctx = get_page_context(context)
    preloader = BoundBlock(Preloader(), {'circular': circular, 'determinate': determinate, 'color': color,
                                         'page': ctx['page'], 'request': ctx['request'], 'site': ctx['site']})
    ctx['value'] = preloader
    return ctx


@register.inclusion_tag('wagtail_materializecss/javascript/parallax.html')
def make_parallax(image):
    context = {'value': {'image': image}}
    return context


@register.inclusion_tag('wagtail_materializecss/components/card.html')
def make_card(title=None, content=None, actions=None,
              size=None, horizontal=False, image=None, background_color=None, text_color=None, classname=None):
    # Check the given actions
    if actions is not None:
        try:
            iter(actions)
        except TypeError:
            # Make object iterable
            actions = [actions]

    value = {
        'title': title, 'content': content, 'actions': actions,
        'size': size, 'horizontal': horizontal, 'image': image,
        'background_color': background_color, 'text_color': text_color,
        }
    return {'value': value, 'classname': classname}


@register.simple_tag
def make_link(icon=None, text=None, url=None):
    value = {'icon': icon or '', 'text': text, 'url': url}
    if isinstance(url, Page):
        value['page'] = url
        value['url'] = url.url
    else:
        value['external_url'] = url
    link = BoundBlock(LinkBlock(), value)
    return link


@register.tag(name='row')
def do_row(parser, token):
    tag_name, args, kwargs = parse_tag(token, parser)
    nodelist = parser.parse(('end_replace',))
    parser.delete_first_token()
    return RowNode(nodelist, classname=kwargs.get('class', ''), style=kwargs.get('style', ''))


class RowNode(template.Node):
    TAG = 'div'

    def __init__(self, nodelist, classname='', style=''):
        self.nodelist = nodelist
        self.classname = classname
        self.style = style

    def render(self, context):
        content = self.nodelist.render(context)
        classname = ''
        if self.classname:
            classname = ' class="{0}"'.format(self.classname)
        style = ''
        if self.style:
            style = ' style="{0}"'.format(self.style)
        tag = "<{tag}{classname}{style}>{content}</tag>".format(tag=self.TAG, classname=classname, style=style,
                                                                content=content)
        return mark_safe(tag)


@register.tag(name='col')
def do_col(parser, token):
    tag_name, args, kwargs = parse_tag(token, parser)
    nodelist = parser.parse(('end_replace',))
    parser.delete_first_token()
    return ColNode(nodelist, s=kwargs.get('s', 0), m=kwargs.get('m', 0), l=kwargs.get('l', 0), xl=kwargs.get('xl', 0),
                   classname=kwargs.get('class', ''), style=kwargs.get('style', ''))


class ColNode(template.Node):
    TAG = 'div'

    def __init__(self, nodelist, s=0, m=0, l=0, xl=0, classname='', style=''):
        self.nodelist = nodelist
        self.s = s
        self.m = m
        self.l = l
        self.xl = xl
        self.classname = classname
        self.style = style

    def render(self, context):
        content = self.nodelist.render(context)
        classname = ' class="{0}"'.format(' '.join((item[0] + str(item[1])
                                                    for item in [('s', self.s), ('m', self.m), ('l', self.l),
                                                                 ('xl', self.xl), ('', self.classname)]
                                                    if item[1]))
                                          )
        style = ''
        if self.style:
            style = ' style="{0}"'.format(self.style)
        tag = "<{tag}{classname}{style}>{content}</tag>".format(tag=self.TAG, classname=classname, style=style,
                                                                content=content)
        return mark_safe(tag)
