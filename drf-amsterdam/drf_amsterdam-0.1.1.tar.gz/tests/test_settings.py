SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    "datapunt_api",
    "tests",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'tests.base_urls'

REST_FRAMEWORK = dict(
    PAGE_SIZE=100,

    MAX_PAGINATE_BY=100,
    DEFAULT_PAGINATION_CLASS='datapunt_api.pagination.HALPagination',

    DEFAULT_RENDERER_CLASSES=(
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    DEFAULT_FILTER_BACKENDS=(
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    COERCE_DECIMAL_TO_STRING=False,  # other Datapunt projects set this to True
    UNAUTHENTICATED_USER=None,
)


