from setuptools import setup

setup(
  name = 'modelchimp',
  packages = ['modelchimp'],
  version = '0.4.7',
  description = 'Python client to upload the machine learning models data to the model chimp cloud',
  author = 'Samir Madhavan',
  author_email = 'samir.madhavan@gmail.com',
  url = 'https://www.modelchimp.com',
  #download_url = 'https://github.com/samzer/modelchimp-client-python/archive/0.4.4.tar.gz',
  keywords = ['modelchimp', 'ai', 'datascience'],
  install_requires=[
          'requests',
          'future',
          'six',
          'websocket-client',
          'pytz',
          'cloudpickle'
      ],
  classifiers = [],
)
