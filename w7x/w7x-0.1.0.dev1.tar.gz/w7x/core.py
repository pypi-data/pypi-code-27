"""
abstract classes to work with the webservice revolving around the osa package
"""
import six
import copy
from six import string_types
import osa
import timeout
import logging
import tfields
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import HTTPError


def compareErrorAttributes(error, errors=None, attributes=None, messageContent=None, **kwargs):
    """
    Annotation:
        if you want a content in the msg, use args attribute.
    Returns:
        True if error.attributes == errorList.attributes else False
    Examples:
        >>> from w7x import core
        >>> d = {'errors': [core.HTTPError(None, 500, None, None, None),
        ...                 core.HTTPError("ASDF", 600, None, None, None)],
        ...      'attributes': ['code'],
        ...      'messageContent': None}
        >>> core.compareErrorAttributes(core.HTTPError(None, 500, None, None, None), **d)
        [True, False]
        >>> e = {'errors': [RuntimeError("A special Message content"),
        ...                 core.HTTPError("ASDF", 600, None, None, None)],
        ...      'attributes': ['args']}
        >>> core.compareErrorAttributes(RuntimeError("This is A special Message content for you"), **e)
        [True, False]

    """
    errors = errors or []
    attributes = attributes or ['code']
    compareList = []
    for inst in errors:
        returnBool = True
        if type(error) is not type(inst):  # must be same type ...
            returnBool = False
        else:
            for attr in attributes:  # ... and contain the same requested attribute values
                if not hasattr(error, attr) or not hasattr(inst, attr):
                    returnBool = False
                    break
                if attr == 'args':
                    if len(error.args) == 0:
                        raise TypeError("Length of args is not suiting.")
                    if not inst.args[0] in error.args[0]:
                        returnBool = False
                        break
                elif not getattr(error, attr) == getattr(inst, attr):
                    returnBool = False
                    break
        compareList.append(returnBool)
    return compareList


def runService(fun, *args, **kwargs):
    """
    Run a service function with the arguments args. Check for HTTPError occurence and redo if you get it.
    Kwargs:
        maxTries (int): Maximum tries, Default is 1
        maxTime (int): Maximum time for the process [s]. Default is inf (<None> value)
        errorDicts (list of dicts describing errors): Each dict has the
            keywords:
                'errors' (list of Error instances)
                'attributes' (list of attributes)
                'action' (str): 'retry' / 'skip'
            Perform action if error.attributes == errorList.attributes for any
            error
    Returns:
        Result of service or function. None if Error from errorDict says skip
    """
    log = logging.getLogger()
    maxTries = kwargs.pop("maxTries", 1)
    if maxTries < 1:
        raise ValueError("maxTries needs to be 1 at minimum.")
    maxTime = kwargs.pop("maxTime", None)
    errorDictsDefault = [{'errors': [HTTPError(None, 500, None, None, None)],
                          'attributes': ['code'],
                          'action': 'retry'},
                         {'errors': [HTTPError(None, 404, None, None, None)],
                          'attributes': ['code'],
                          'action': 'retry'},
                         {'errors': [HTTPError(None, 413, None, None, None)],
                          'attributes': ['code'],
                          'action': 'retry'},
                         {'errors': [RuntimeError('Grid_CylLowendel')],
                          'attributes': ['args'],
                          'action': 'skip'},
                         {'errors': [RuntimeError('ThreadTracer failed.')],
                          'attributes': ['args'],
                          'action': 'skip'},
                         {'errors': [RuntimeError('zero field')],
                          'attributes': ['args'],
                          'action': 'skip'}]
    errorDicts = kwargs.pop('errorDicts', [])
    errorDicts.extend(errorDictsDefault)

    result = None
    tryCount = 1

    @timeout.timeout(maxTime)
    def run(fun, *args):
        return fun(*args)

    while result is None:
        try:
            result = run(fun, *args)  # run service with arguments
            if result is None:
                log.warning("Result is really None")
            break
        except timeout.TimeoutError as err:
            log.error("TimeoutError. Took more than %s seconds." % maxTime)
            if tryCount < maxTries:
                tryCount += 1
                log.info("Retry service %s." % fun)
            else:
                raise  # Also allows result being <None>
        except Exception as err:
            log.error(err)
            skip = False
            retry = False
            for eD in errorDicts:
                if any(compareErrorAttributes(err, **eD)):
                    if eD['action'] == 'retry':
                        retry = True
                    elif eD['action'] == 'skip':
                        skip = True
                    else:
                        raise TypeError("%s is no allowed Action" % eD['action'])
            if skip:
                log.info("Skip service %s." % fun)
                break
            elif retry:
                if tryCount < maxTries:
                    tryCount += 1
                    log.info("Retry service %s." % fun)
                    continue
            raise
    return result


serverCache = {}


def getServer(address):
    """
    Cached method to retrieve osa.Client from adress.
    Timeout is implemented.
    Examples:
        TODO: this example only works if the server can connect
        >>> import w7x
        >>> addr = w7x.Server.addrFieldLineServer
        >>> addr in str(w7x.getServer(addr))
        True

    """
    if address in serverCache:
        return serverCache[address]

    server = None
    log = logging.getLogger()
    try:
        server = runService(osa.Client, address, maxTries=1, maxTime=1)
    except Exception:
        log.error("Server at {0} could not connect.".format(address))
    serverCache[address] = server
    return server


def getWsClass(wsServer, wsClass):
    """
    Args:
        wsServer (str): address of webservice
        wsClass (str): name of webService type class
    Returns:
        server.types.wsClass
    """
    server = getServer(wsServer)
    return getattr(server.types, wsClass)


def is_w7x_instance(obj, tpe, convert=True):
    """
    Check, if an object is instance of a web server class
    Args:
        obj (object instance): instance to check the ...
        tpe (class or <webservice>.types.<class>): ... type for
        convert (bool): convert all obj and tpe to osa before checking
            you can provide conversion ability by defining the methods
            'as_input' for objs and 'getWsClass' for tpes
    Returns:
        bool
    Examples:
        >>> import w7x
        >>> p = w7x.Points3D([[5, 1, 0]])

        checking osa type directly
        >>> fieldLineServer = w7x.getServer(w7x.Server.addrFieldLineServer)
        >>> w7x.core.is_w7x_instance(p, fieldLineServer.types.Points3D)
        True
        >>> w7x.core.is_w7x_instance(p.as_input(), fieldLineServer.types.Points3D)
        True

        checking objects that provide getWsClass methods
        >>> w7x.core.is_w7x_instance(p, w7x.Points3D)
        True
        >>> w7x.core.is_w7x_instance(p.as_input(), w7x.Points3D)
        True

        checking only osa types
        >>> w7x.core.is_w7x_instance(p, w7x.Points3D, convert=False)
        True
        >>> w7x.core.is_w7x_instance(p.as_input(), w7x.Points3D, convert=False)
        False
        >>> w7x.core.is_w7x_instance(p, fieldLineServer.types.Points3D, convert=False)
        False
        >>> w7x.core.is_w7x_instance(p.as_input(), fieldLineServer.types.Points3D, convert=False)
        True

        test the same for Base derived instance
        >>> m = w7x.MagneticConfig.default()
        >>> w7x.core.is_w7x_instance(m.as_input(), w7x.MagneticConfig)
        True
        >>> w7x.core.is_w7x_instance(m, w7x.MagneticConfig)
        True
        >>> w7x.core.is_w7x_instance(m, w7x.MagneticConfig.getWsClass())
        True
        
    """
    # convert all Base derived objs and tpes to osa
    if convert:
        if issubclass(obj.__class__, Base) or hasattr(obj, 'as_input'):
            obj = obj.as_input()
        if issubclass(tpe, Base) or hasattr(tpe, 'getWsClass'):
            tpe = tpe.getWsClass()

    if isinstance(tpe, osa.xmltypes.ComplexTypeMeta):
        if convert or isinstance(obj.__class__, osa.xmltypes.ComplexTypeMeta):
            return obj.__class__.__name__ == tpe.__name__

    return isinstance(obj, tpe)


class Base(object):
    """
    set this to a dictionary with keys and defaults
    """
    propDefaults = None
    propOrder = None

    wsServer = None
    wsClass = None
    wsClassArgs = None
    wsClassKwargs = None

    def __init__(self, *args, **kwargs):

        self.propDefaults = self.propDefaults or {}
        self.propOrder = self.propOrder or []

        if len(args) == 1 and is_w7x_instance(args[0], self.__class__):
            # copy constructor from cls or related ws class
            other = args[0]
            if is_w7x_instance(other, self.getWsClass(), convert=False):
                for attr in self.getPropAttrs():
                    if hasattr(other, attr):
                        kwargs[attr] = getattr(other, attr)
            else:
                kwargs = other.getPropDict(kwargs)
            if len(args) > 1:
                raise ValueError("More than one argument given in copy "
                                 "constructor.")
        else:
            # update kwargs with arguments defined in args
            for attr, arg in zip(self.propOrder, args):
                if attr in kwargs:
                    raise AttributeError("Attribute {attr} specified in args "
                                         "and kwargs! I will use args!"
                                         .format())
                kwargs[attr] = arg

        # default properties
        props = self.getPropDict()
        props.update(self.propDefaults)
        # set attributes from kwargs or props
        for key, default in six.iteritems(props):
            val = kwargs.pop(key, default)
            setattr(self, key, val)

        if len(kwargs) > 0:
            raise AttributeError('kwargs have unused arguments %s' % kwargs.keys())

    def getPropAttrs(self):
        """
        Returns:
            list of str: properties that are occuring in the osa type input
        """
        try:
            attrs = dir(self.getWsClass())
        except:
            log = logging.getLogger()
            log.warning("could not connect to server and thus not dynamically "
                        "get the property defaults.")
            if self.propDefaults is not None:
                attrs = self.propDefaults.keys()

        propAttrs = []
        for attr in attrs:
            if attr.startswith('_'):
                continue
            if attr in ['from_file', 'from_xml', 'to_file', 'to_xml']:
                continue
            propAttrs.append(attr)
        return propAttrs

    def getPropDict(self, kwargs=None):
        kwargs = kwargs or {}
        for key in self.getPropAttrs():
            kwargs[key] = getattr(self, key, None)
        return kwargs

    def __deepcopy__(self, memo):
        """
        copy with the copy constructor
        """
        kwargs = copy.deepcopy(self.getPropDict(), memo)
        return self.__class__(**kwargs)

    def copy(self):
        """
        copy with deepcopy
        """
        return copy.deepcopy(self)

    @classmethod
    def getWsClass(cls):
        """
        Returns the osa class version of this class
        """
        wsClass = cls.wsClass or cls.__name__
        return getWsClass(cls.wsServer, wsClass)

    def to_file(self, path):
        """
        Forward to xml.to_file(self, path)
        """
        self.as_input().to_file(tfields.lib.in_out.resolve(path))

    def as_input(self):
        """
        return copy in getWsClass format. Chain this to the attributes.
        """
        cls = self.getWsClass()
        wsClassArgs = self.wsClassArgs or []
        wsClassKwargs = self.wsClassKwargs or {}
        instance = cls(*wsClassArgs, **wsClassKwargs)
        for (prop, default) in six.iteritems(self.propDefaults):
            value = self.__dict__.get(prop, default)
            if value is not None:
                if issubclass(value.__class__, Base) or hasattr(value, 'as_input'):
                    value = value.as_input()
                elif hasattr(value, '__iter__') and not isinstance(value,
                                                                   string_types):
                    value = [v.as_input() if hasattr(v, 'as_input')
                             else v for v in value]
                setattr(instance, prop, value)
        return instance


if __name__ == "__main__":
    import doctest
    doctest.testmod()
