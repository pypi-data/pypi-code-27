class Base:

    def __repr__(self):
        return "<%s %s>" % (type(self).__name__, self)

    def __hash__(self):
        return hash(str(self))
