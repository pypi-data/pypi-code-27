from setuptools import setup
from setuptools.extension import Extension

long_description = """SVIM (pronounced SWIM) is a structural variant caller for long reads. It is able to detect and classify six different classes of structural variants. Unlike existing methods, SVIM integrates information from across the genome to precisely distinguish similar events, such as duplications and cut&paste insertions. In our experiments on simulated and real PacBio data, SVIM reached consistently better results than competing methods, particularly on low-coverage datasets. Furthermore, it is unique in its capability of extracting both the genomic origin and destination of insertions and duplications."""

setup(name='svim',
      version='0.3',
      description='A structural variant caller for long reads.',
      long_description=long_description,
      url='https://github.com/eldariont/svim',
      author='David Heller',
      author_email='heller_d@molgen.mpg.de',
      license='GPLv3',
      classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Intended Audience :: Science/Research',
      'Topic :: Scientific/Engineering :: Bio-Informatics',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Programming Language :: Python :: 3.6'
      ],
      keywords='svim SV PacBio structural variation caller',
      packages=['svim'],
      zip_safe=False,
      install_requires=['pysam', 'numpy', 'scipy', 'biopython', 'networkx', 'matplotlib'],
      scripts=['svim/SVIM.py'])
