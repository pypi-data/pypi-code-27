import json
from aiohttp import ClientSession
from yarl import URL

from .exceptions import RestClientError, JsonRestError, PlainRestError


class AsyncRESTClient:

    def __init__(self, url, *, admin_prefix=None, headers=None, loop=None):
        self._url = URL(url)
        self._session = ClientSession(loop=loop)
        self._headers = headers or {'Content-Type', 'application/json'}

    RestClientError = RestClientError
    JsonRestError = JsonRestError

    @property
    def base_url(self):
        return self._url

    async def request(self, method, path, data=None, params=None,
                      headers=None,  **kwargs):
        url = self._url / path
        if data is not None:
            data = json.dumps(data).encode('utf-8')

        h = self._headers.copy()
        if headers:
            h.update(headers)
        resp = await self._session.request(method, str(url),
                                           params=params, data=data,
                                           headers=h, **kwargs)
        return resp

    async def handle_response(self, resp):
        body = await resp.read()
        if resp.status in (200, 201):
            jsoned = await resp.json()
            return jsoned
        elif resp.status == 500:
            raise PlainRestError(body.decode('utf-8'))
        else:
            try:
                jsoned = await resp.json(encoding='utf-8')
            except ValueError:
                raise PlainRestError(body.decode('utf-8'))
            else:
                raise JsonRestError(resp.status, jsoned)

    async def close(self):
        if self._session:
            await self._session.close()

    async def model_list(self):
        url = 'models'
        resp = await self.request('GET', url)
        answer = await self.handle_response(resp)
        return answer

    async def model_detail(self, model_name):
        url = f'models/{model_name}'
        resp = await self.request('GET', url)
        answer = await self.handle_response(resp)
        return answer

    async def model_predict(self, model_name, payload):
        url = f'models/{model_name}'
        resp = await self.request('POST', url, data=payload)
        answer = await self.handle_response(resp)
        return answer
