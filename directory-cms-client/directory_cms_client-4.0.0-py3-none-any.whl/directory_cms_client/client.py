import directory_client_core.base

from django.conf import settings

from directory_cms_client.version import __version__


class DirectoryCMSClient(directory_client_core.base.AbstractAPIClient):
    endpoints = {
        'page-by-type': '/api/pages/lookup-by-type/{page_type}/',
        'page-by-slug': '/api/pages/lookup-by-slug/{slug}/',
        'pages-by-type': '/api/pages/'
    }
    version = __version__

    def __init__(self, base_url, api_key, sender_id, timeout, service_name):
        super().__init__(base_url, api_key, sender_id, timeout)
        self.service_name = service_name

    def get(self, language_code, draft_token, params=None, *args, **kwargs):
        params = params or {}
        if language_code:
            params['lang'] = language_code
        if draft_token:
            params['draft_token'] = draft_token
        return super().get(params=params, *args, **kwargs)

    def lookup_by_slug(
            self,
            slug,
            fields=None,
            draft_token=None,
            language_code=None,
    ):
        params = {
            'fields': fields or ['*'],
            'service_name': self.service_name
        }
        return self.get(
            url=self.endpoints['page-by-slug'].format(slug=slug),
            params=params,
            draft_token=draft_token,
            language_code=language_code
        )

    def list_by_page_type(
        self, page_type, fields=None, draft_token=None, language_code=None
    ):
        return self.get(
            url=self.endpoints['pages-by-type'],
            params={
                'fields': fields or ['*'],
                'type': page_type,
            },
            draft_token=draft_token,
            language_code=language_code,
        )


cms_api_client = DirectoryCMSClient(
    base_url=settings.DIRECTORY_CMS_API_CLIENT_BASE_URL,
    api_key=settings.DIRECTORY_CMS_API_CLIENT_API_KEY,
    sender_id=settings.DIRECTORY_CMS_API_CLIENT_SENDER_ID,
    timeout=settings.DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,
    service_name=settings.DIRECTORY_CMS_API_CLIENT_SERVICE_NAME
)
