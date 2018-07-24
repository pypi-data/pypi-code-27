SECRET_KEY = 'whatever'

INSTALLED_APPS = [
    'djmoney',
    'djmoney_test',
]

DATABASES = {
        'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}
}
