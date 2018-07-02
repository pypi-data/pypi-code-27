from hashlib import md5

from django import template
from django.conf import settings
from django.urls import reverse

from django_adminlte.compat import is_authenticated

register = template.Library()


@register.simple_tag()
def logout_url():
    return getattr(settings, 'LOGOUT_URL', '/logout/')


@register.simple_tag(takes_context=True)
def avatar_url(context, size=None, user=None):
    # TODO: Make behaviour configurable
    user = context['request'].user if user is None else user
    return 'https://www.gravatar.com/avatar/{hash}?s={size}&d=mm'.format(
        hash=md5(user.email.encode('utf-8')).hexdigest() if is_authenticated(user) else '',
        size=size or '',
    )


@register.simple_tag(takes_context=True)
def add_active(context, url_name, *args, **kwargs):
    exact_match = kwargs.pop('exact_match', False)
    not_when = kwargs.pop('not_when', None)

    path = reverse(url_name, args=args, kwargs=kwargs)
    current_path = context.request.path

    if not_when and str(not_when) in current_path:
        return ''

    if not exact_match and current_path.startswith(path):
        return ' active '
    elif exact_match and current_path == path:
        return ' active '
    else:
        return ''
