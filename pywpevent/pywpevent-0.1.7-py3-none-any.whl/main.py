from pywpevent.events import EventCtrl


def initialize():
    ctrl = EventCtrl()
    ctrl.initialize_plugin()


def add_action(name, func, priority=0):
    ctrl = EventCtrl()
    ctrl.add_action(name, func, priority)


def add_filter(name, func, priority=0):
    ctrl = EventCtrl()
    ctrl.add_filter(name, func, priority)


def do_action(name, *args, **kwargs):
    ctrl = EventCtrl()
    ctrl.do_action(name, *args, **kwargs)


def apply_filter(name, value, *args, **kwargs):
    ctrl = EventCtrl()
    return ctrl.apply_filter(name, value, *args, **kwargs)


def list_event():
    ctrl = EventCtrl()
    ctrl.list_event()
