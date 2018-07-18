class Scope(object):

    def __init__(self, scope, func):
        self.scope = scope
        self.func = func

    def get(self, attribute):
        return self.scope[attribute]

    def execute(self):
        return self.func(get=self.get)
