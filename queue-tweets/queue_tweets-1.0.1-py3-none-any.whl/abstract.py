"""Abstract base class definitions"""
import abc

class AbstractQueue(metaclass=abc.ABCMeta):
    """abstract base class for what defines a queue. Must have
    two methods: put and get.

    Methods
    -------
    put - enqueue
    get - dequeue
    """
    
    @abc.abstractclassmethod
    def put(self, data):
        """put data onto the queue"""

        raise NotImplementedError
    
    @abc.abstractclassmethod
    def get(self):
        """get data from the queue"""

        raise NotImplementedError
    
    @classmethod
    def __subclasshook__(cls, C):
        if cls is AbstractQueue:

            methods = [B.__dict__ for B in C.__mro__][0]
            get_true = 'get' in methods
            put_true = 'put' in methods

            if get_true and put_true:
                return True

        return NotImplemented