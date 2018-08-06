# REST API MixIn
# Author: Spencer Hanson, for Swimlane
import requests
from urlparse import urljoin


class RestAPIMixin(object):
    """
    Superclass Mix In, for custom APIs
    """

    def __init__(self, host, verify=True, proxy=None, auth=None, raise_for_status=True):
        """
        Create an API adapter class
        :param host: Full URL, including schema for the base of the API. Ex: http://google.com/v1/api
        :param verify: Optional boolean to verify SSL certificates in the requests, defaults to True
        :param proxy: Optional proxy for the requests session. A given string value will be used for both HTTP/HTTPS,
        otherwise it will set it directly
        :param auth: Optional requests session authentication
        :param raise_for_status: Optional to raise for status errors after each request, defaults to True
        """

        self.host = host
        self.session = requests.Session()
        self.session.verify = verify
        if proxy:
            if isinstance(proxy, str):
                self.session.proxies = {
                    "http": proxy,
                    "https": proxy
                }
            else:
                self.session.proxies = proxy

        self.session.auth = auth
        self.raise_for_status = raise_for_status

    def request(self, method, endpoint, **kwargs):
        """
        Make a request using the requests library, given a method, endpoint and keyword arguments
        :param method: HTTP Method to use to make the request
        :param endpoint: Endpoint to hit on the host, Ex: '/update'
        :param kwargs: Extra keyword arguments to add to the request func call
        :return: Requests response object
        """
        response = self.session.request(method, urljoin(self.host, endpoint), **kwargs)
        if self.raise_for_status:
            try:
                response.raise_for_status()
            except Exception as e:
                raise e  # For debugging, put a breakpoint here
        return response


class BasicRestEndpoint(RestAPIMixin):
    """
    Basic rest endpoint mix in, should be sufficient for most APIs
    """

    def get_endpoint(self):
        """
        Endpoint relative to the host, ie '/v2/update'
        """
        raise NotImplementedError

    def parse_response(self, response):
        """
        Given a requests response, process it
        :param response: Requests response object
        :return: dict
        """
        raise NotImplementedError

    def get_req_method(self):
        """
        Request method to use, valid: GET, POST, PUT, PATCH, DELETE
        :return: String for request method to use
        """
        raise NotImplementedError

    def get_kwargs(self):
        """
        Optional keyword arguments to pass to the request
        :return: dict
        """
        return {}

    def execute(self):
        """
        Run the request, and return the processed response
        :return: dict
        """
        response = self.request(self.get_req_method(), self.get_endpoint(), **self.get_kwargs())
        return self.parse_response(response)


class BasicRestPaginationEndpoint(BasicRestEndpoint):
    """
    If the API has pagination support, this class makes it easy to query them all
    Just define next_page which is run until it returns None, marking the end of the pages
    each request is run through parse_response.
    Then combine_pages is given the list of parsed responses, to finalize the operation
    """

    def get_next_page(self, parsed_response):
        """
        Function to return the next endpoint to hit, given the current response
        If it returns None, it's finished
        :param parsed_response: Output from the previous parsed requests response
        :return: URL to use for the next request call
        """
        raise NotImplementedError

    def combine_pages(self, results):
        """
        Take all the results from the pages and combine them into the final result
        :param results: List of output from parse_response
        :return: Combined responses for final output
        """
        raise NotImplementedError

    def execute(self):
        """
        Continually run the request, making sure to check if there are more pages, returns output from combine_pages
        :return:
        """
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


class GETMixin(BasicRestEndpoint):
    """
    Mixin for GET requests
    """

    def get_req_method(self):
        return "GET"


class POSTMixin(BasicRestEndpoint):
    """
    Mixin for POST requests
    """

    def get_req_method(self):
        return "POST"


class PUTMixin(BasicRestEndpoint):
    """
    Mixin for PUT requests
    """

    def get_req_method(self):
        return "PUT"


class DELETEMixin(BasicRestEndpoint):
    """
    Mixin for DELETE requests
    """

    def get_req_method(self):
        return "DELETE"


class PATCHMixin(BasicRestEndpoint):
    """
    Mixin for PATCH requests
    """

    def get_req_method(self):
        return "PATCH"
