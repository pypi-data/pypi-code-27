from setuptools import setup

setup(name='TwrpBuilder',
      version='0.7',
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
      scripts=['TwrpBuilder/TwBuilder.py','TwrpBuilder/Cert.py','TwrpBuilder/Build.sh'],
      platform='linux',
      zip_safe=False)
