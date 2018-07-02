import angr

######################################
# bind (but not really)
######################################
import logging
l = logging.getLogger("angr.procedures.posix.bind")

class bind(angr.SimProcedure):
    #pylint:disable=arguments-differ

    def run(self, fd, addr_ptr, addr_len): #pylint:disable=unused-argument
        return self.state.se.Unconstrained('bind', self.state.arch.bits, key=('api', 'bind'))
