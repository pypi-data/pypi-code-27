import shutil
from setuptools import setup, find_packages
from pathlib import Path

with open('README.md', 'r') as f:
      README = f.read()

setup(name='astrosql',
      version='0.3.0',
      description='Simple API to access to existing astronomical MySQL database',
      long_description = README,
      long_description_content_type = "text/markdown",
      url='https://github.com/ketozhang/astroSQL',
      author='Keto Zhang, Weikang Zheng',
      author_email='keto.zhang@gmail.com',
      packages=['astrosql'],
      # data_files=[
      #       ('astrosql/', ['astrosql/config.yml'])
      # ],
      install_requires=['peewee', 'termcolor', 'pymysql', 'astropy', 'numpy', 'pandas', 'pyyaml'],
      include_package_data=True,
      zip_safe=False)

config_file = (Path(__file__).parent/'astrosql'/'config.yml').resolve()
(Path.home()/'.astrosql').mkdir(exist_ok = True)
if not (Path.home()/'.astrosql'/'config.yml').exists():
      new_file = Path.home()/'.astrosql'/'config.yml'
      shutil.copyfile(str(config_file), str(new_file))
