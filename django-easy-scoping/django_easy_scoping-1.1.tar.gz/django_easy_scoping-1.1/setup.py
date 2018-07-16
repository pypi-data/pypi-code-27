import setuptools

setuptools.setup(
    name='django_easy_scoping',
    version='1.1',
    author='Robert Wells',
    author_email='wellsroberte@gmail.com',
    packages=setuptools.find_packages(),
    url='https://github.com/net-prophet/django-easy-scoping',
    description='A mixin to allow users to create scopes on Django models.',
    license='BSD',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=[
        'Django>=1.11,<3.0',
    ],
)
