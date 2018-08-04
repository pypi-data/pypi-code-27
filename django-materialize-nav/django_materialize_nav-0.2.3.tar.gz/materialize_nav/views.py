from .utils import NavHeader, NavItem
from .search.nav_option_views import SearchOptions

from .navigation.views import TemplateMixin, TitleViewMetaclass, BaseNavOptions, TitleOptions, NavBarOptions, \
    SideBarOptions, BaseNavView

from .search.views import SearchNavView, SearchView

from .autocomplete.views import AutocompleteView

__all__ = ['TemplateMixin', 'NavHeader', 'NavItem', 'TitleViewMetaclass', 'BaseNavOptions', 'TitleOptions',
           'NavBarOptions', 'SideBarOptions', 'SearchOptions', 'BaseNavView',
           'SearchNavView', 'SearchView',
           'AutocompleteView',
           'NavView']


class NavView(SearchNavView):
    pass
