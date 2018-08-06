from distutils.core import setup
setup(
  name = 'ybc_todo',
  packages = ['ybc_todo'],
  version = '1.0.1',
  description = 'Say What to do',
  long_description='Speech Recognition,voice2text,text2voice',
  author = 'KingHS',
  author_email = '382771946@qq.com',
  keywords = ['pip3', 'speech', 'python3','python','Speech Recognition'],
  license='MIT',
  install_requires=[
        'pyaudio',
        'wave',
        'requests',
        'ybc_pinyin'
    ],
)
