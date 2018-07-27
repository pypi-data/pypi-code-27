import logging
from inspect import iscoroutinefunction

from stateflow.refresher import logger

from stateflow import reactive
from stateflow.common import Observable
from stateflow.decorators import hide_nested_calls
from stateflow.errors import NotInitializedError
from stateflow.forwarders import ConstForwarders, MutatingForwarders
from stateflow.notifier import Notifier, ScopedName
from stateflow.var import Box, as_observable, obtain_call_line, updates_stack


class BoxOld(Observable):
    def __init__(self, value=None):
        self._notifier = Notifier(self._notify)
        self._exception = None  # type: Exception
        self._value = value

    def _notify(self):
        raise NotImplementedError()

    @property
    def __notifier__(self):
        return self._notifier

    def __eval__(self):
        if self._exception:
            raise self._exception
        return self._value

    def set(self, value):
        self._raw = value
        self._exception = None
        self._notifier.notify_observers()

    def set_exception(self, e):
        self._exception = e
        self._raw = None
        self._notifier.notify_observers()

    # def __str__(self):
    #     try:
    #         return '{}({})'.format(self.__class__.__name__, repr(self.__eval__))
    #     except Exception as e:
    #         return '{}(exception={})'.format(self.__class__.__name__, repr(e))


class VarOld(Box, ConstForwarders, MutatingForwarders):
    NOT_INITIALIZED = NotInitializedError()

    def __init__(self, value=NOT_INITIALIZED, name=None):
        with ScopedName(name):
            super().__init__()
            if value is self.NOT_INITIALIZED:
                self.set_exception(NotInitializedError())
            else:
                self.set(value)

    def set(self, value):
        self._raw = value
        self._exception = None
        self._notifier.notify_observers()

    def set_exception(self, e):
        self._exception = e
        self._raw = None
        self._notifier.notify_observers()

    def _notify(self):
        pass

    # noinspection PyMethodOverriding
    @Box.__eval__.setter
    def __eval__(self, value):
        return self.set(value)

    def __imatmul__(self, other):
        """
        A syntax sugar (at the expense of some inconsistency and inconvenience when we want to make @= on the inner)
        """
        self.set(other)
        return self

    # Not sure whether we should simply forward it
    def __getattr__(self, item):
        return getattr(self._target().__eval__, item)


class ProxyOld(Observable, ConstForwarders, MutatingForwarders):
    def __init__(self, other_var: Observable):
        assert other_var is not None
        super().__init__()
        self._notifier = Notifier()
        self._other_var = other_var
        self._other_var.__notifier__.add_observer(self._notifier)

    @property
    def __notifier__(self):
        return self._notifier

    def _target(self):
        return self._other_var

    @property
    def __eval__(self):
        return self._other_var.__eval__

    def __getattr__(self, item):
        return getattr(self._target().__eval__, item)


class SwitchableProxyOld(Observable, ConstForwarders):
    """
    A proxy to any observable object (possibly another proxy or some Wrapper like Var or Const). It tries to behave
    exactly like the object itself.

    It must implement WrapperInterface since it's possible that the object inside implements it. If the
    Proxy was given as a parameter to the @reactive function, it should be observed and unwrapped.
    """

    def __init__(self):
        super().__init__()
        self._ref = Box()
        self._notifier = Notifier()
        self._ref.__notifier__.add_observer(self._notifier)

    @property
    def __notifier__(self):
        return self._notifier

    def __eval__(self):
        ref = self._get_ref()
        if ref is not None:
            return ref.__eval__()

    def _get_ref(self):
        try:
            return self._ref.__eval__()
        except Exception:
            return None

    def _set_ref(self, ref):
        self._unobserve_value()
        self._ref @= as_observable(ref)
        self._observe_value()

    def _unobserve_value(self):
        ref = self._get_ref()
        if ref is not None and hasattr(ref, '__notifier__'):
            return ref.__notifier__.remove_observer(self._notifier)

    def _observe_value(self):
        ref = self._get_ref()
        if ref is not None and hasattr(ref, '__notifier__'):
            return ref.__notifier__.add_observer(self._notifier)

    @reactive
    def __getattr__(self, item):
        return getattr(self, item)


class LazySwitchableProxy(Observable, ConstForwarders):
    """
    A proxy to any observable object (possibly another proxy or some Wrapper like Var or Const). It tries to behave
    exactly like the object itself.

    It must implement WrapperInterface since it's possible that the object inside implements it. If the
    Proxy was given as a parameter to the @reactive function, it should be observed and unwrapped.
    """

    def __init__(self, async):
        super().__init__()
        self.async = async
        self._ref = None
        self._dirty = False
        if async:
            # I have no idea how to call do lazy updating if update is async (and getter isn't)
            self._notifier = Notifier(self._update_async)
        else:
            self._notifier = Notifier(self._args_changed)
            self._dirty = True
        self._exception = None
        self._notifier.line = obtain_call_line()

    @property
    def __notifier__(self):
        return self._notifier

    @property
    def __eval__(self):
        try:
            self._update_if_dirty()

            if self._exception is not None:
                raise self._exception
            #            if isinstance(self._exception, SilentError):
            #                raise self._exception
            # raise Exception() from self._exception
            if self._ref is not None and hasattr(self._ref, '__eval__'):
                return self._ref.__eval__
        except AttributeError as e:
            # AttributeError could be interpreted as 'no such method' on at some point of the call stack
            raise Exception("Disabling AttributeError") from e

    def _target(self):
        self._update_if_dirty()
        if self._ref is None:
            raise NotInitializedError()
        return self._ref

    def _get_ref(self):
        try:
            return self._ref
        except Exception:
            return None

    def _set_ref(self, ref):
        self._unobserve_value()
        self._ref = as_observable(ref)
        self._exception = None
        self._observe_value()

    def _unobserve_value(self):
        ref = self._get_ref()
        if ref is not None and hasattr(ref, '__notifier__'):
            return ref.__notifier__.remove_observer(self._notifier)

    def _observe_value(self):
        ref = self._get_ref()
        if ref is not None and hasattr(ref, '__notifier__'):
            return ref.__notifier__.add_observer(self._notifier)

    @reactive
    def __getattr__(self, item):
        return getattr(self, item)

    def _update_if_dirty(self):
        if self._dirty:
            # FIXME: doesn't work for async updates
            logger.debug('updating {}'.format(self._notifier.name))
            updates_stack.append(self._notifier.line)
            try:
                hide_nested_calls(self._update)()
            except Exception as e:
                # import traceback
                # print(traceback.print_stack())
                logging.exception('error when updating {}'.format(self._notifier.name))
                # logging.exception('error when updating {}'.format(
                #    '\n======\n'.join(['\n'.join(map(str, l)) for l in updates_stack])))
            updates_stack.pop()
            self._dirty = False

    def _args_changed(self):
        assert not iscoroutinefunction(self._update)
        self._dirty = True
        return True

    @hide_nested_calls
    async def _update_async(self):
        assert iscoroutinefunction(self._update)
        await self._update()
        return True
