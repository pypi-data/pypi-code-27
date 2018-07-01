#!/usr/bin/env python3

import os
import sys

import glob

from cffi import FFI
from pycparser import c_parser, c_ast, parse_file, c_generator

import shutil
import subprocess
import platform
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve
import zipfile

SDL2_VERSION = os.environ.get('SDL_VERSION', '2.0.8')
TDL_NO_SDL2_EXPORTS = os.environ.get('TDL_NO_SDL2_EXPORTS', '0') == '1'

CFFI_HEADER = 'tcod/cffi.h'
CFFI_EXTRA_CDEFS = 'tcod/cdef.h'

BITSIZE, LINKAGE = platform.architecture()

def walk_sources(directory):
    for path, dirs, files in os.walk(directory):
        for source in files:
            if not source.endswith('.c'):
                continue
            yield os.path.join(path, source)

def find_sources(directory):
    return [os.path.join(directory, source)
            for source in os.listdir(directory)
            if source.endswith('.c')]

def get_sdl2_file(version):
    if sys.platform == 'win32':
        sdl2_file = 'SDL2-devel-%s-VC.zip' % (version,)
    else:
        assert sys.platform == 'darwin'
        sdl2_file = 'SDL2-%s.dmg' % (version,)
    sdl2_local_file = os.path.join('dependencies', sdl2_file)
    sdl2_remote_file = 'https://www.libsdl.org/release/%s' % sdl2_file
    if not os.path.exists(sdl2_local_file):
        print('Downloading %s' % sdl2_remote_file)
        urlretrieve(sdl2_remote_file, sdl2_local_file)
    return sdl2_local_file

def unpack_sdl2(version):
    sdl2_path = 'dependencies/SDL2-%s' % (version,)
    if sys.platform == 'darwin':
        sdl2_dir = sdl2_path
        sdl2_path += '/SDL2.framework'
    if os.path.exists(sdl2_path):
        return sdl2_path
    sdl2_arc = get_sdl2_file(version)
    print('Extracting %s' % sdl2_arc)
    if sdl2_arc.endswith('.zip'):
        with zipfile.ZipFile(sdl2_arc) as zf:
            zf.extractall('dependencies/')
    else:
        assert sdl2_arc.endswith('.dmg')
        subprocess.check_call(['hdiutil', 'mount', sdl2_arc])
        subprocess.check_call(['mkdir', '-p', sdl2_dir])
        subprocess.check_call(['cp', '-r', '/Volumes/SDL2/SDL2.framework',
                                           sdl2_dir])
        subprocess.check_call(['hdiutil', 'unmount', '/Volumes/SDL2'])
    return sdl2_path

module_name = 'tcod._libtcod'
include_dirs = [
    '.',
    'libtcod/include/',
    'libtcod/src/png/',
    'libtcod/src/zlib/',
]

extra_parse_args = []
extra_compile_args = []
extra_link_args = []
sources = []

libraries = []
library_dirs = []
define_macros = []

sources += walk_sources('tcod/')
sources += walk_sources('tdl/')
sources += ['libtcod/src/libtcod_c.c']
sources += ['libtcod/src/png/lodepng.c']
sources += glob.glob('libtcod/src/zlib/*.c')

if TDL_NO_SDL2_EXPORTS:
    extra_parse_args.append('-DTDL_NO_SDL2_EXPORTS')

if sys.platform == 'win32':
    libraries += ['User32', 'OpenGL32']
    define_macros.append(('TCODLIB_API', ''))
    define_macros.append(('_CRT_SECURE_NO_WARNINGS', None))

if 'linux' in sys.platform:
    libraries += ['GL']

if sys.platform == 'darwin':
    extra_link_args += ['-framework', 'OpenGL']
    extra_link_args += ['-framework', 'SDL2']
else:
    libraries += ['SDL2']

# included SDL headers are for whatever OS's don't easily come with them

if sys.platform in ['win32', 'darwin']:
    SDL2_PATH = unpack_sdl2(SDL2_VERSION)
    include_dirs.append('libtcod/src/zlib/')

if sys.platform == 'win32':
    include_dirs.append(os.path.join(SDL2_PATH, 'include'))
    ARCH_MAPPING = {'32bit': 'x86', '64bit': 'x64'}
    SDL2_LIB_DIR = os.path.join(SDL2_PATH, 'lib/', ARCH_MAPPING[BITSIZE])
    library_dirs.append(SDL2_LIB_DIR)
    SDL2_LIB_DEST = os.path.join('tcod', ARCH_MAPPING[BITSIZE])
    if not os.path.exists(SDL2_LIB_DEST):
        os.mkdir(SDL2_LIB_DEST)
    shutil.copy(os.path.join(SDL2_LIB_DIR, 'SDL2.dll'), SDL2_LIB_DEST)

def fix_header(filepath):
    """Removes leading whitespace from a MacOS header file.

    This whitespace is causing issues with directives on some platforms.
    """
    with open(filepath, 'r+') as f:
        current = f.read()
        fixed = '\n'.join(line.strip() for line in current.split('\n'))
        if current == fixed:
            return
        f.seek(0)
        f.truncate()
        f.write(fixed)

if sys.platform == 'darwin':
    HEADER_DIR = os.path.join(SDL2_PATH, 'Headers')
    fix_header(os.path.join(HEADER_DIR, 'SDL_assert.h'))
    fix_header(os.path.join(HEADER_DIR, 'SDL_config_macosx.h'))
    include_dirs.append(HEADER_DIR)
    extra_link_args += ['-F%s/..' % SDL2_PATH]
    extra_link_args += ['-rpath', '%s/..' % SDL2_PATH]
    extra_link_args += ['-rpath', '/usr/local/opt/llvm/lib/']

if sys.platform not in ['win32', 'darwin']:
    extra_parse_args += subprocess.check_output(['sdl2-config', '--cflags'],
                                              universal_newlines=True
                                              ).strip().split()
    extra_compile_args += extra_parse_args
    extra_link_args += subprocess.check_output(['sdl2-config', '--libs'],
                                               universal_newlines=True
                                               ).strip().split()

class CustomPostParser(c_ast.NodeVisitor):

    def __init__(self):
        self.ast = None
        self.typedefs = None

    def parse(self, ast):
        self.ast = ast
        self.typedefs = []
        self.visit(ast)
        return ast

    def visit_Typedef(self, node):
        if node.name in ['wchar_t', 'size_t']:
            # remove fake typedef placeholders
            self.ast.ext.remove(node)
        else:
            self.generic_visit(node)
            if node.name in self.typedefs:
                print('warning: %s redefined' % node.name)
                self.ast.ext.remove(node)
            self.typedefs.append(node.name)

    def visit_EnumeratorList(self, node):
        """Replace enumerator expressions with '...' stubs."""
        for type, enum in node.children():
            if enum.value is None:
                pass
            elif isinstance(enum.value, (c_ast.BinaryOp, c_ast.UnaryOp)):
                enum.value = c_ast.Constant('int', '...')
            elif hasattr(enum.value, 'type'):
                enum.value = c_ast.Constant(enum.value.type, '...')

    def visit_ArrayDecl(self, node):
        if not node.dim:
            return
        if isinstance(node.dim, (c_ast.BinaryOp, c_ast.UnaryOp)):
            node.dim = c_ast.Constant('int', '...')

    def visit_Decl(self, node):
        if node.name is None:
            self.generic_visit(node)
        elif (node.name and 'vsprint' in node.name or
              node.name in ['SDL_vsscanf',
                            'SDL_vsnprintf',
                            'SDL_LogMessageV']):
            # exclude va_list related functions
            self.ast.ext.remove(node)
        elif node.name in ['screen']:
            # exclude outdated 'extern SDL_Surface* screen;' line
            self.ast.ext.remove(node)
        else:
            self.generic_visit(node)

    def visit_FuncDef(self, node):
        """Exclude function definitions.  Should be declarations only."""
        self.ast.ext.remove(node)

def get_cdef():
    generator = c_generator.CGenerator()
    return generator.visit(get_ast())

def get_ast():
    global extra_parse_args
    if 'win32' in sys.platform:
        extra_parse_args += [r'-I%s/include' % SDL2_PATH]
    if 'darwin' in sys.platform:
        extra_parse_args += [r'-I%s/Headers' % SDL2_PATH]

    ast = parse_file(filename=CFFI_HEADER, use_cpp=True,
                     cpp_args=[r'-Idependencies/fake_libc_include',
                               r'-DDECLSPEC=',
                               r'-DSDLCALL=',
                               r'-DTCODLIB_API=',
                               r'-DSDL_FORCE_INLINE=',
                               r'-U__GNUC__',
                               r'-D_SDL_thread_h',
                               r'-DDOXYGEN_SHOULD_IGNORE_THIS',
                               r'-DMAC_OS_X_VERSION_MIN_REQUIRED=1060',
                               r'-D__attribute__(x)=',
                               r'-D_PSTDINT_H_INCLUDED',
                               ] + extra_parse_args)
    ast = CustomPostParser().parse(ast)
    return ast

# Can force the use of OpenMP with this variable.
try:
    USE_OPENMP = eval(os.environ.get('USE_OPENMP', 'None').title())
except Exception:
    USE_OPENMP = None

tdl_build = os.environ.get('TDL_BUILD', 'RELEASE').upper()

MSVC_CFLAGS = {
    'DEBUG': ['/Od'],
    'RELEASE': ['/GL', '/O2', '/GS-'],
}
MSVC_LDFLAGS = {
    'DEBUG': [],
    'RELEASE': ['/LTCG'],
}
GCC_CFLAGS = {
    'DEBUG': ['-O0'],
    'RELEASE': ['-flto', '-O3', '-fPIC'],
}

if sys.platform == 'win32' and '--compiler=mingw32' not in sys.argv:
    extra_compile_args.extend(MSVC_CFLAGS[tdl_build])
    extra_link_args.extend(MSVC_LDFLAGS[tdl_build])

    if USE_OPENMP is None:
        USE_OPENMP = sys.version_info[:2] >= (3, 5)

    if USE_OPENMP:
        extra_compile_args.append('/openmp')
else:
    extra_compile_args.extend(GCC_CFLAGS[tdl_build])
    extra_link_args.extend(GCC_CFLAGS[tdl_build])
    if USE_OPENMP is None:
        USE_OPENMP = sys.platform != 'darwin'

    if USE_OPENMP:
        extra_compile_args.append('-fopenmp')
        extra_link_args.append('-fopenmp')

ffi = FFI()
ffi.cdef(get_cdef())
ffi.cdef(open(CFFI_EXTRA_CDEFS, 'r').read())
ffi.set_source(
    module_name, '#include <tcod/cffi.h>',
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    sources=sources,
    libraries=libraries,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    define_macros=define_macros,
)

if __name__ == "__main__":
    ffi.compile()
