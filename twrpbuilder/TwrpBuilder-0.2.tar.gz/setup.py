from setuptools import setup

setup(name='TwrpBuilder',
      version='0.2',
      description='Wrapper for building Twrp',
      author='Android Lover',
      author_email='androidlover5842@gmail.com',
      license='MIT',
      packages=['TwrpBuilder'],
      install_requires=[
            'firebase_admin',
            'tqdm'
      ],
      keywords='Twrp Root Android',
      scripts=['TwrpBuilder/Builder.py'],
      platform='Linux',
      zip_safe=False)
