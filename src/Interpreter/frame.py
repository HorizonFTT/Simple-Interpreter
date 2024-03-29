from Semantic.symbol import *
import logging


class Frame(object):
    def __init__(self, scope, enclosing_frame=None):
        self.scope = scope
        self.data = {}
        self.enclosing_frame = enclosing_frame
        self.return_value = None

    def set(self, name, value):
        if name == self.scope.scope_name:
            self.return_value = value
            return
        symbol = self.scope.lookup(name, True)
        if symbol is None:
            self.enclosing_frame.set(name, value)
        else:
            logging.debug(f' set {symbol} to {value}')
            self.data[name] = value

    def get(self, name):
        symbol = self.scope.lookup(name, True)
        if symbol is None:
            return self.enclosing_frame.get(name)
        return self.data.get(name)
