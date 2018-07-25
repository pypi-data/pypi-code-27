from requests import Session, Response

API_VERSION = 'v1'
TASKS_ENDPOINT = f'/api/{API_VERSION}/tasks'


class OPTaaSError(RuntimeError):
    """Wrapper class for an error :class:`.Response` received from OPTaaS."""

    def __init__(self, response: Response) -> None:
        self.status_code = response.status_code
        try:
            self.message = response.json()['message']
        except BaseException:
            self.message = response.content
        super().__init__(self.message)


class OPTaaSResponse:
    """Wrapper class for a successful :class:`.Response` received from OPTaaS."""

    def __init__(self, response: Response) -> None:
        if response.ok:
            self.body = response.json()
        else:
            raise OPTaaSError(response)


class OPTaaSSession:
    """Wrapper class for a :class:`.Session` that makes requests to OPTaaS.

    Args:
        server_url (str): URL of your OPTaaS server
        api_key (str): Your personal API key
        keep_alive (bool, default True): Whether to set the `Connection` HTTP Header to "keep-alive".
    """

    def __init__(self, server_url: str, api_key: str, keep_alive: bool = True) -> None:
        self._session = Session()
        self._root_url = server_url
        self._headers = {'X-ApiKey': api_key, 'Connection': 'keep-alive' if keep_alive else 'close'}

    def post(self, endpoint: str, body: dict) -> OPTaaSResponse:
        """Make a POST request to OPTaaS with a JSON body.

        Args:
            endpoint (str): Endpoint for the request (will be appended to the server_url).
            body (dict): Request body in JSON format.

        Returns:
            The :class:`.OPTaaSResponse` to the request.

        Raises:
            :class:`.OPTaaSError` if an error response is received.
        """
        return OPTaaSResponse(self._session.post(self._root_url + endpoint, json=body, headers=self._headers))

    def put(self, endpoint: str, body: dict) -> OPTaaSResponse:
        """Make a PUT request to OPTaaS with a JSON body.

        Args:
            endpoint (str): Endpoint for the request (will be appended to the server_url).
            body (dict): Request body in JSON format.

        Returns:
            The :class:`.OPTaaSResponse` to the request.

        Raises:
            :class:`.OPTaaSError` if an error response is received.
        """
        return OPTaaSResponse(self._session.put(self._root_url + endpoint, json=body, headers=self._headers))

    def get(self, endpoint: str) -> OPTaaSResponse:
        """Make a GET request to OPTaaS

        Args:
            endpoint (str): Endpoint for the request (will be appended to the server_url).

        Returns:
            The :class:`.OPTaaSResponse` to the request.

        Raises:
            :class:`.OPTaaSError` if an error response is received.
        """
        return OPTaaSResponse(self._session.get(self._root_url + endpoint, headers=self._headers))

    def delete(self, endpoint: str) -> OPTaaSResponse:
        """Make a DELETE request to OPTaaS

        Args:
            endpoint (str): Endpoint for the request (will be appended to the server_url).

        Returns:
            The :class:`.OPTaaSResponse` to the request.

        Raises:
            :class:`.OPTaaSError` if an error response is received.
        """
        return OPTaaSResponse(self._session.delete(self._root_url + endpoint, headers=self._headers))
