from setuptools.command.install import install
import os
import re
import sys
import sysconfig
import platform
import subprocess

from distutils.version import LooseVersion
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: " +
                ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)',
                                         out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = ['-DCMAKE_C_COMPILER=gcc',
                      '-DCMAKE_CXX_COMPILER=g++',
                      '-DCMAKE_FORTRAN_COMPILER=gfortran'
                      '-DCMAKE_CXX_FLAGS="${CMAKE_CXX_FLAGS} --std=c++11"',
                      '-DCMAKE_BUILD_TYPE=Release',
                      '-DBOOST_ROOT=${BOOST_ROOT}'
                      '-DISOGEOMETRIC_APPLICATION=ON',
                      '-DPYTHON_INCLUDE_DIR=/usr/include/python2.7',
                      '-DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython2.7.so',
                      '-DPYTHON_EXECUTABLE=/usr/bin/python2.7']

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        # if platform.system() == "Windows":
        #     cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(
        #         cfg.upper(),
        #         extdir)]
        #     if sys.maxsize > 2**32:
        #         cmake_args += ['-A', 'x64']
        #     build_args += ['--', '/m']
        # else:
        #     cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
        #     build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get('CXXFLAGS', ''),
            self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args,
                              cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args,
                              cwd=self.build_temp)
        print()  # Add an empty line for cleaner output

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        setup(
            name='PyIGA',
            version='0.0.5',
            author='Hoang-Giang Bui',
            author_email='giang.bui@rub.de',
            description='Isogeometric analysis in Python. Built upon KratosMultiphysics Kernel',
            long_description='',
             # tell setuptools to look for any packages under 'src'
             # tell setuptools that all packages will be under the 'src' directory
             # and nowhere else
            ext_modules=[CMakeExtension('Kratos/Kratos')],
             # add custom build_ext command
            cmdclass=dict(build_ext=CMakeBuild),
            zip_safe=False,
        )
        install.run(self)

setup(
    name='PyIGA',
    version='0.0.4',
    author='Hoang-Giang Bui',
    author_email='giang.bui@rub.de',
    description='Isogeometric analysis in Python. Built upon KratosMultiphysics Kernel',
    long_description='',
    cmdclass = dict(install=PostInstallCommand)
)


