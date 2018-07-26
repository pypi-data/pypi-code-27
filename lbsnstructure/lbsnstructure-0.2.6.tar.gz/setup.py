from setuptools import setup

with open('README.md') as f:
    long_description = f.read()
        
setup(name='lbsnstructure',
      version='0.2.6',
      description='A common language independend and cross-network social-media datascheme.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://gitlab.vgiscience.de/lbsn/concept',
      author='Filip Krumpe; Alexander Dunkel',
      author_email='alexander.dunkel@tu-dresden.de',
      license='MIT',
      packages=['lbsnstructure'],
      install_requires=[
          'protobuf',
      ],
      zip_safe=False)