from .visual import create_viz
import collections


# plot_registries = []
#
# def regis_plot_attrs(plot_type, title, legend=None):
#     """
#     :param plot_type:
#             'line'
#             'scatter'
#     :param title: should be consistent with the key of plotters
#     :return:
#     """
#     def _regis_plot_type(func):
#         func.plot_type = plot_type
#         func.title = title
#         func.legend = legend
#         plot_registries.append(func.__name__)
#         return func
#
#     return _regis_plot_type
#
#
# class Plotter:
#     """
#         Plot the metrics such as train/val loss, accuracy, etc.
#
#         Usage:
#             If you want to plot something, just add @regis_plot_attrs.
#
#     """
#     def __init__(self, env, server='localhost', port=8097, type='visdom'):
#         """
#         Parameters:
#         ----------
#         type: str, choose which kind of plotter
#         """
#
#         self.type = type
#         self.env = env
#         self.server = server
#         self.port = port
#         if type == 'visdom':
#             self._plotter = create_viz('main', env, port, server, type)
#         elif type == 'tensorboard':
#             self._plotter = create_viz('main', env, type)
#         else:
#             raise ValueError("viz type is wrong. Neither visdom nor tensorboard")
#
#         # TODO: Add Matplotlib plotter to plot figures
#
#         self.register_logs()
#
#     def register_logs(self):
#         for entry in plot_registries:
#             func = getattr(self, entry)
#             # Add some attributes
#             if self.type == 'visdom':
#                 # It will be troublesome if we take env,server,etc. as the attributes of func
#                 self._plotter.regis_log(func, self.env, self.server, self.port)
#             else:
#                 raise NotImplementedError()
#
#
#     def _convert_input_to_multiple_plot(self, iters, vals):
#         """Check and convert the input for the multiple plot in one figure.
#            Supported input format:(e.g. iters, vals)
#            Case a. 1, [2,3]
#            Case b. [2,2], [2,3]
#         """
#         if not isinstance(iters, collections.Sequence):
#             iters = [iters for i in range(len(vals))]
#         assert len(iters) == len(vals)
#         return iters, vals
#
#
#
#
#     @regis_plot_attrs('line', title='train_loss')
#     def plot_train_loss(self, iter_i, loss):
#         self._plotter.plotters['train_loss'].log(iter_i, loss)
#
#     @regis_plot_attrs('line', title='train_test_loss', legend=['train', 'test'])
#     def plot_train_test_loss(self, iters, vals):
#         self.plot(iters, vals, 'train_test_loss')
#
#         # import pdb;pdb.set_trace()
#         iters, losses = self._convert_input_to_multiple_plot(iters, losses)
#         self._plotter.plotters['train_test_loss'].log(iters, losses)
#
#     @regis_plot_attrs('line', title='train_acc')
#     def plot_train_acc(self, iter_i, acc):
#         self._plotter.plotters['train_acc'].log(iter_i, acc)
#
#     @regis_plot_attrs('line', title='test_loss')
#     def plot_test_loss(self, iter_i, loss):
#         self._plotter.plotters['test_loss'].log(iter_i, loss)
#
#     @regis_plot_attrs('line', title='train_iou')
#     def plot_train_iou(self, iter_i, iou):
#         self._plotter.plotters['train_iou'].log(iter_i, iou)
#
#     @regis_plot_attrs('line', title='test_iou')
#     def plot_test_iou(self, iter_i, iou):
#         self._plotter.plotters['test_iou'].log(iter_i, iou)
#
#     def image(self, *args, **kwargs):
#         self._plotter.image(*args, **kwargs)
#
#     def images(self, *args, **kwargs):
#         self._plotter.images(*args, **kwargs)
#
#     def heatmap(self, *args, **kwargs):
#         self._plotter.heatmap(*args, **kwargs)



class Plotter(object):
    """
        The highest abstraction for plotter(visualization)

        0. Support different backends including visdom, tensorboard(not implemented)
        1. Plot the metrics such as train/val loss, accuracy, etc.
        2. support image, heatmap

        Usage:

    """
    ALLOWABLE_PLOT_TYPES = ['line', 'scatter']

    def __init__(self, name, env, server='localhost', port=8097, backend='visdom'):
        super(Plotter, self).__init__()

        self.name = name
        self.backend = backend
        self.env = env
        self.server = server
        self.port = port

        if backend == 'visdom':
            self._plotter = create_viz(name, env, port, server, backend)
        elif backend == 'tensorboard':
            self._plotter = create_viz(name, env, port, server, backend)
        else:
            raise ValueError("viz type is wrong. Neither visdom nor tensorboard")

    def _legalize_multiple_plot(self, iters, vals):
        """Check and convert the input for the multiple plot in one figure.
           Supported input format:(e.g. iters, vals)
           Case a. 1, [2,3]
           Case b. [2,2], [2,3]
        """
        #TODO: Legalize (Cuda) Tensor
        if not isinstance(iters, collections.Sequence):
            iters = [iters for i in range(len(vals))]
        assert len(iters) == len(vals)
        return iters, vals

    def register_plot_type(self, plot_type, opts={}):
        """
        Register plot such as line, scatter which needs to be updated.
        :param title:
        :param plot_type: the form you want to plot such as line, scatter, etc.
        :param opts: dict
            title: (must exist)
        :return:
        """
        assert 'title' in opts
        assert plot_type in self.ALLOWABLE_PLOT_TYPES
        if self.backend == 'visdom':
            self._plotter.regis_visdom_logger(plot_type, opts)
        else:
            raise NotImplementedError()

    def update_plot(self, plot_name, X, Y=None):
        """

        :param plot_name:
        :param x: (N*K) OR (N,)
         N is the number of points will be ploted in each plot
         K is the number of plots.
        :param y: Support tensor Shape: (N*K) Or (N,)
        :return:
        """
        # x, y = self._legalize_multiple_plot(x, y)
        self._plotter.update_plot(plot_name, X, Y)

    def image(self, *args, **kwargs):
        self._plotter.image(*args, **kwargs)

    def images(self, imgs, opts={'title':''}):
        self._plotter.images(imgs, opts)

    def heatmap(self, *args, **kwargs):
        self._plotter.heatmap(*args, **kwargs)


class PlotterManager(object):
    def __init__(self):
        self.plt_dict = {}

    def create_plotter(self, name, env, server, port, backend, plotter_cls=Plotter):
        plotter = plotter_cls(name, env, server, port, backend)
        assert name not in self.plt_dict, "Plotter Manager: the name in plt_dict already exist"
        self.plt_dict[name] = plotter
        return plotter

def get_plotter(name=None):
    name = name if name else 'root'
    return plt_manager.plt_dict[name]


def create_plotter(name, env, server='localhost', port=8097, backend='visdom', plotter_cls=Plotter):
    name = name if name else 'root'

    plotter = plt_manager.create_plotter(name, env, server, port, backend, plotter_cls)

    return plotter


plt_manager = PlotterManager()