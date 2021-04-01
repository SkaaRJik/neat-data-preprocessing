from abc import abstractmethod, ABCMeta


class AbstractMessageListener:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._queueName = ''

    @abstractmethod
    def action(self):
        """verify excel dataset format"""
        raise NotImplementedError("This method is abstract")
