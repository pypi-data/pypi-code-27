from setuptools import setup, find_packages

setup(
      name='dicomraw',
      version='0.4.0.3',
      description='encapsulates arbitrary binary data in a valid dicom file,'
                  ' with the option of archiving it in a zip archive, using streaming.',
      url='https://gitlab.com/cfmm/dicomraw',
      author='Igor Solovey',
      author_email='isolovey@robarts.ca',
      license='MIT',
      packages=find_packages(),
      scripts=['bin/dicomunwrap'],
      zip_safe=False,
      install_requires=[
            'zipstream>=1.1.4',
            'pydicom==1.1.0'
      ],
      tests_require=[
            'nose==1.3.7',
            'nose-parameterized==0.5.0'
      ]
)
