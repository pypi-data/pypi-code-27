# REST API MixIn
# Author: Spencer Hanson, for Swimlane
import requests
from urlparse import urljoin


# Superclass Mix In, for custom APIs
class RestAPIMixin(object):
    def __init__(self, host, verify, http_proxy=None, auth=None, raise_for_status=True):
        self.host = host
        self.session = requests.Session()
        self.session.verify = verify
        self.session.proxies = {
            "http": http_proxy,
            "https": http_proxy
        }
        self.session.auth = auth
        self.raise_for_status = raise_for_status

    def request(self, method, endpoint, **kwargs):
        response = self.session.request(method, urljoin(self.host, endpoint), **kwargs)
        if self.raise_for_status:
            try:
                response.raise_for_status()
            except Exception as e:
                raise e  # For debugging, can put a breakpoint here
        return response


# Basic rest endpoint mix in, should be sufficient for most APIs
class BasicRestEndpoint(RestAPIMixin):
    # Endpoint relative to the host, ie '/v2/update'
    def get_endpoint(self):
        raise NotImplementedError

    # Given a requests response, process it
    def parse_response(self, response):
        raise NotImplementedError

    # Method to use, valid include GET,POST,PUT,PATCH,DELETE
    def get_req_method(self):
        raise NotImplementedError

    # Optional keyword arguments to pass to the request
    def get_kwargs(self):
        return {}

    # Run the request, and return the processed response
    def execute(self):
        response = self.request(self.get_req_method(), self.get_endpoint(), **self.get_kwargs())
        return self.parse_response(response)


# If the API has pagination support, this class makes it easy to query them all
class BasicRestPaginationEndpoint(BasicRestEndpoint):
    # Function to return the next endpoint to hit, given the current response
    # If it returns None, it's finished
    def get_next_page(self, parsed_response):
        raise NotImplementedError

    # Take all the results from the pages and combine them into the final result
    def combine_pages(self, results):
        raise NotImplementedError

    # Continually run the request, making sure to check if there are more pages, returns output from combine_pages
    def execute(self):
        results = []

        response = self.request(self.get_req_method(), self.get_endpoint(), **self.get_kwargs())
        result = self.parse_response(response)
        results.append(result)
        next_page = self.get_next_page(result)
        while next_page:
            response = self.request(self.get_req_method(), next_page, **self.get_kwargs())
            result = self.parse_response(response)
            results.append(result)
            next_page = self.get_next_page(result)
        return self.combine_pages(results)


# Mixin for GET requests
class BasicGETRestEndpoint(BasicRestEndpoint):
    def get_req_method(self):
        return "GET"


# Mixin for POST requests
class BasicPOSTRestEndpoint(BasicRestEndpoint):
    def get_req_method(self):
        return "POST"


# Mixin for PUT requests
class BasicPUTRestEndpoint(BasicRestEndpoint):
    def get_req_method(self):
        return "PUT"


# Mixin for DELETE requests
class BasicDELETERestEndpoint(BasicRestEndpoint):
    def get_req_method(self):
        return "DELETE"


# Mixin for PATCH requests
class BasicPATCHRestEndpoint(BasicGETRestEndpoint):
    def get_req_method(self):
        return "PATCH"
