from __future__ import absolute_import, unicode_literals

from builtins import super

from .errors import PexelsError
from .models import Photo
from .pexelspage import PexelsPage
from .settings import API_VERSION


class Search(PexelsPage):
    def __init__(self, api_key, url='/search', api_version=API_VERSION, **kwargs):

        if url.find('/search') == -1:
            raise PexelsError('Invalid _url for class Search(): %s' % url)

        if 'query' not in kwargs and 'query' not in url:
            raise PexelsError('Parameter "query" is mandatory for class Search()')

        valid_options = ['page', 'per_page', 'query']
        super().__init__(
            url=url,
            api_key=api_key,
            api_version=api_version,
            valid_options=valid_options,
            **kwargs)

    @property
    def entries(self):
        for entry in self.body.get('photos', []):
            yield Photo.parse(entry)
