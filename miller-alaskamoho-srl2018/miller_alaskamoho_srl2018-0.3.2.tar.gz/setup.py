## To install locally: python setup.py build && python setup.py install
## (If there are problems with installation of the documentation, it may be that
##  the egg file is out of sync and will need to be manually deleted - see error message
##  for details of the corrupted zip file. )
##
## To push a version through to pip.
##  - Make sure it installs correctly locally as above
##  - Update the version information in this file
##  - python setup.py sdist upload -r pypitest  # for the test version
##  - python setup.py sdist upload -r pypi      # for the real version
##
## (see http://peterdowns.com/posts/first-time-with-pypi.html)



from setuptools import setup, find_packages


if __name__ == "__main__":
    setup(name = 'miller_alaskamoho_srl2018',
          author            = "Louis Moresi",
          author_email      = "louis.moresi@unimelb.edu.au",
          # url               = "https://github.com/University-of-Melbourne-Geodynamics/litho1pt0",
          # download_url      = "",
          version           = "0.3.2",
          description       = "Python interface to Miller SRL 2018 Alaska Moho model - requires stripy",
          packages          = ['miller_alaskamoho_srl2018'],
          package_dir       = {'miller_alaskamoho_srl2018': 'miller_alaskamoho_srl2018'},
          package_data      = {'miller_alaskamoho_srl2018': ['Models/*.npz',
                                                             'Notebooks/*ipynb',
                                                             'Notebooks/ShadedRelief/*.tif',
                                                             'Notebooks/ModelConstruction/B*ipynb',
                                                             'Notebooks/ModelConstruction/Data/Moho-Alaska/*.txt'
                                                            ]},
          include_package_data = True,
          install_requires=['stripy', 'litho1pt0', 'numpy'],



          )
