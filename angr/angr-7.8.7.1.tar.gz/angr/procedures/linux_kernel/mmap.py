import angr

import logging
l = logging.getLogger("angr.procedures.syscalls.mmap")


PROT_READ       = 0x1  #    /* Page can be read.  */
PROT_WRITE      = 0x2  #    /* Page can be written.  */
PROT_EXEC       = 0x4  #    /* Page can be executed.  */
PROT_NONE       = 0x0  #    /* Page can not be accessed.  */
MAP_SHARED      = 0x01 #    /* Share changes.  */
MAP_PRIVATE     = 0x02 #    /* Changes are private.  */
MAP_ANONYMOUS   = 0x20 #    /* Don't use a file.  */
MAP_FIXED       = 0x10 #    /* Interpret addr exactly.  */


class mmap(angr.SimProcedure):

    IS_SYSCALL = True

    def run(self, addr, length, prot, flags, fd, offset): #pylint:disable=arguments-differ,unused-argument
        #if self.state.se.symbolic(flags) or self.state.se.eval(flags) != 0x22:
        #   raise Exception("mmap with other than MAP_PRIVATE|MAP_ANONYMOUS unsupported")
        l.debug("mmap(%s, %s, %s, %s, %s, %s) = ...", addr, length, prot, flags, fd, offset)

        #
        # Length
        #

        if self.state.se.symbolic(length):
            size = self.state.se.max_int(length)
            if size > self.state.libc.max_variable_size:
                l.warn("mmap size requested of %d exceeds libc.max_variable_size. Using size %d instead.", size,self.state.libc.max_variable_size)
                size = self.state.libc.max_variable_size
        else:
            size = self.state.se.eval(length)

        #
        # Addr
        #

        # Not handling symbolic addr for now
        addrs = self.state.se.eval_upto(addr,2)
        if len(addrs) == 2:
            err = "Cannot handle symbolic addr argument for mmap."
            l.error(err)
            raise angr.errors.SimPosixError(err)

        addr = addrs[0]

        # Call is asking for system to provide an address
        if addr == 0:
            addr = self.allocate_memory(size)

        #
        # Flags
        #

        # Only want concrete flags
        flags = self.state.se.eval_upto(flags,2)

        if len(flags) == 2:
            err = "Cannot handle symbolic flags argument for mmap."
            l.error(err)
            raise angr.errors.SimPosixError(err)

        flags =  flags[0]

        # Sanity check. All mmap must have exactly one of MAP_SHARED or MAP_PRIVATE
        if (flags & MAP_SHARED and flags & MAP_PRIVATE) or flags & (MAP_SHARED | MAP_PRIVATE) == 0:
            l.debug('... = -1 (bad flags)')
            return self.state.se.BVV(-1, self.state.arch.bits)

        while True:
            try:
                self.state.memory.map_region(addr, size, prot[2:0], init_zero=bool(flags & MAP_ANONYMOUS))
                l.debug('... = %#x', addr)
                return addr

            except angr.SimMemoryError:
                # This page is already mapped

                if flags & MAP_FIXED:
                    l.debug('... = -1 (MAP_FIXED failure)')
                    return self.state.se.BVV(-1, self.state.arch.bits)

                # Can't give you that address. Find a different one and loop back around to try again.
                addr = self.allocate_memory(size)


    def allocate_memory(self,size):

        addr = self.state.libc.mmap_base
        new_base = addr + size

        if new_base & 0xfff:
            new_base = (new_base & ~0xfff) + 0x1000

        self.state.libc.mmap_base = new_base

        return addr

class old_mmap(mmap):
    def run(self, ptr):
        addr, length, prot, flags, fd, offset = self.state.mem[ptr].dword.array(6).resolved
        return super(old_mmap, self).run(addr, length, prot, flags, fd, offset)
