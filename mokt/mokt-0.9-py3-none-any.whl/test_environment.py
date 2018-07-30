import pyopencl as cl
import numpy as np


class TestEnvironment(object):
    def __init__(self):
        """Wraps global state for test execution.

        OpenCL context and command queue are instantiated in the __init__ method
        and are available for the lifetime of an environment object.
        """

        self.context = cl.create_some_context()
        self.cmd_queue = cl.CommandQueue(
            self.context,
            properties=cl.command_queue_properties.PROFILING_ENABLE)

    def kernel_from_file(self, src_path, kernel_name):
        """Creates an OpenCL kernel from a given source string.

        Args:
            src_path (str): Path to the source file.
            kernel_name (str): Name of the kernel function,
                as defined in the C source.
        """

        with open(src_path, 'r') as file:
            source = file.read()

        program = cl.Program(self.context, source).build()
        return getattr(program, kernel_name)

    def output_defs(self, expected_outputs):
        """Generates output definitions to be passed to the `run_kernel` method.

        Args:
            expected_outputs (list): List of `numpy.ndarray`s with
                expected outputs. The method does not read their contents,
                only shape and data type information.
        """

        return [(out.size, out.dtype.type) for out in expected_outputs]

    def run_kernel(self, kernel, inputs, output_defs, global_size, local_size):
        """Executes an OpenCL kernel with specified arguments, returning outputs in a list.

        Inputs and outputs are converted into OpenCL buffers and fed into the kernel
        as positional arguments — first inputs, then outputs. After execution,
        outputs are converted into numpy.ndarrays in the specified order.

        Args:
            kernel (pyopencl.Kernel): Target OpenCL kernel, which can be obtained from
                a pyopencl.Program instance by calling `program.kernel_name()`.
            inputs (list): List of kernel inputs (numpy.ndarrays),
                given in the order they are declared in the kernel.
            output_defs (list): List of tuples of (length, type) for each kernel output,
                where `length` is the length of output array, and `type`
                is an element type (e.g. `numpy.float32` for OpenCL's `float`).
            global_size (tuple): Global size for kernel execution.
            local_size (tuple | None): Local size for kernel execution.

        Returns:
            A tuple of (exec_event, outputs), where `exec_event` is an instance of pyopencl.Event
            returned by the `enqueue_nd_range_kernel` operation and `outputs` is a list
            of `numpy.ndarray`s.
        """

        input_buffers = [
            cl.Buffer(
                self.context,
                cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                hostbuf=inp) for inp in inputs
        ]
        output_buffers = [
            cl.Buffer(
                self.context, cl.mem_flags.WRITE_ONLY,
                dtype().nbytes * length) for (length, dtype) in output_defs
        ]
        exec_event = kernel(
            self.cmd_queue, global_size, local_size,
            *(input_buffers + output_buffers))
        outputs = self.copy_outputs(exec_event, output_defs, output_buffers)
        return (exec_event, outputs)

    def copy_outputs(self, exec_event, output_defs, output_buffers):
        """Copies outputs of a kernel execution to host, returning a list of `numpy.ndarray`s.

        You can obtain the first two arguments, `exec_event` and `output_buffers`,
        by calling the `run_kernel` method.

        Args:
            exec_event (pyopencl.Event): Kernel execution event
            output_defs (list): See documentation for `run_kernel`
            output_buffers (list): List of `pyopencl.Buffer`s containing kernel outputs.
        """

        output_arrays = [
            np.zeros(length, dtype=dtype) for (length, dtype) in output_defs
        ]
        copy_events = [
            cl.enqueue_copy(
                self.cmd_queue, host_buf, device_buf, wait_for=[exec_event])
            for (host_buf, device_buf) in zip(output_arrays, output_buffers)
        ]
        cl.wait_for_events(copy_events)
        return output_arrays
