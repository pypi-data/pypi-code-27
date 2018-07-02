import angr
import claripy
import logging

l = logging.getLogger('angr.procedures.linux_loader.sim_loader')

class LinuxLoader(angr.SimProcedure):
    NO_RET = True

    # pylint: disable=unused-argument,arguments-differ,attribute-defined-outside-init
    local_vars = ('initializers',)
    def run(self):
        self.initializers = self.project.loader.initializers
        self.run_initializer()

    def run_initializer(self):
        if len(self.initializers) == 0:
            self.project.simos.set_entry_register_values(self.state)
            self.jump(self.project.entry)
        else:
            addr = self.initializers[0]
            self.initializers = self.initializers[1:]
            self.call(addr, (self.state.posix.argc, self.state.posix.argv, self.state.posix.environ), 'run_initializer')

class IFuncResolver(angr.SimProcedure):
    NO_RET = True

    # pylint: disable=arguments-differ,unused-argument
    def run(self, funcaddr=None, gotaddr=None, funcname=None):
        resolve = self.project.factory.callable(funcaddr, concrete_only=True)
        try:
            value = resolve()
        except angr.errors.AngrCallableError:
            l.critical("Ifunc \"%s\" failed to resolve!", funcname)
            #import IPython; IPython.embed()
            raise
        self.state.memory.store(gotaddr, value, endness=self.state.arch.memory_endness)
        self.successors.add_successor(self.state, value, claripy.true, 'Ijk_Boring')

    def __repr__(self):
        return '<IFuncResolver %s>' % self.kwargs.get('funcname', None)
