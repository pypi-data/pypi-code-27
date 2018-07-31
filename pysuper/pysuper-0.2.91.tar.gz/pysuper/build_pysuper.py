import os
import cffi

ffibuilder = cffi.FFI()

ffibuilder.cdef("""struct arguments{
  int verbose;
  unsigned threads;
  unsigned coil;
  unsigned n_query;
  char **query;
  char *search_database;
  FILE *output;
  float threshold;
};""")

ffibuilder.cdef("""struct query_data {
  struct db_vector *centered;
  float *norm;
  char *sequence;
  unsigned size;
  unsigned divider;
};""")

ffibuilder.cdef("""struct super_runner{
  uint32_t n_pipelines;
  struct pipeline* pipelines;
  struct db* db;
  struct query_data* query;
  struct vector_set* ref;
  struct result* results;
};
""")

ffibuilder.cdef("""struct result {
  struct result* next;
  char ID[4];
  uint32_t meta_offset;
  uint32_t size;
  float rmsd;
  char chain;
};""")

ffibuilder.cdef("""struct db_meta{
  int16_t residueID;
  char slc;
  char icode;
};""")

ffibuilder.cdef("""int
super_runner_setup(struct super_runner* super,
                   const struct arguments* args);""")

ffibuilder.cdef("""int
super_runner_run(struct super_runner* super);""")

ffibuilder.cdef("""void
super_runner_destroy(struct super_runner* super);""")

ffibuilder.cdef("""const struct db_meta*
db_meta_by_index(struct db* database, uint32_t index);""")

ffibuilder.set_source("pysuper._pysuper",
                      "#include <super_runner.h>",
                      libraries=["super"],
                      include_dirs=["src",],
                      library_dirs=[os.path.dirname(__file__),],
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
