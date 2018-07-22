from cffi import FFI

from iwlib._iwlib_build import structs, externs, defs, funcs

with open('/usr/include/fakeiwlib.h') as f:
    testing = f.read()

fake_ffibuilder = FFI()
fake_ffibuilder.cdef(structs + externs + defs + funcs + testing)

fake_ffibuilder.set_source("iwlib._fakeiwlib", "#include <iwlib.h>\n #include <fakeiwlib.h>", libraries=['fakeiw'], extra_link_args=['-L./fakeiw/'], extra_compile_args=['-Wall', '-I./fakeiw'])
fake_ffibuilder.compile()
