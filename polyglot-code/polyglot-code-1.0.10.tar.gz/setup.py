from setuptools import find_packages, setup

setup (
  name = "polyglot-code",
  version = "1.0.10",
  description = "Write console logs in 'any' programming language",
  long_description = open("README.rst").read(),
  author = "Kike Fontan (@CosasDePuma)",
  author_email = "kikefontanlorenzo@gmail.com",
  maintainer = "Kike Fontan (@CosasDePuma)",
  maintainer_email = "kikefontanlorenzo@gmail.com",
  url = "https://github.com/cosasdepuma",
  # package_dir = { '': 'lib' }, packages = [ '' ]
  packages = find_packages(),
  py_modules = [ "polyglot" ],
  license = "Apache-2.0",
  keywords = [ "log", "debug", "console", "anyprint", "polyglot" ]
)