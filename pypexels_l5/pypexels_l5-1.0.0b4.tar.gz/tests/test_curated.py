from __future__ import absolute_import, print_function

import json
import os
from builtins import object

import responses

from pypexels import PyPexels

api_key = os.environ.get('API_KEY', None) or 'API_KEY'


class TestCurated(object):
    # TODO: avoid code duplication
    # Need to workout how to combine responses.activate so as to avoid
    # code duplication, as the testcases are pretty much the same for all

    root_path = os.environ.get('TRAVIS_BUILD_DIR', None) or os.getcwd()

    store_mapping = {
        'curated': os.sep.join([
            root_path,
            'tests',
            'resources',
            'resource__curated_per_page_5_page_2.json',
        ]),
    }

    @responses.activate
    def test_curated(self):
        index = 'curated'
        resource_filepath = self.store_mapping[index]
        stored_response = json.loads(open(resource_filepath).read())

        responses.add(
            responses.GET,
            'https://api.pexels.com/v1/curated?page=2&per_page=5',
            json=stored_response,
            status=200,
            content_type='application/json',
            adding_headers={'Authorization': api_key},
            match_querystring=True,
        )
        py_pexels = PyPexels(api_key=api_key)
        curated_results_page = py_pexels.curated(page=2, per_page=5)

        # Page properties
        print(curated_results_page.page)
        print(curated_results_page.per_page)
        print(curated_results_page.has_next)
        print(curated_results_page.has_previous)
        print(curated_results_page.link_self)
        print(curated_results_page.link_first)
        print(curated_results_page.link_last)
        print(curated_results_page.link_next)
        print(curated_results_page.link_previous)

        # Entries
        for photo in curated_results_page.entries:
            print(photo.id, photo.photographer, photo.width, photo.height, photo.url)
            print(photo.src)
