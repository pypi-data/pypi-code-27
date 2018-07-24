class Version:
    latest = False
    version = None

    def __init__(self, svr):
        if svr == "latest":
            self.latest = True
            return
        if svr.find('..') != -1 or svr.startswith('.') or svr.endswith('.'):
            raise ValueError("{} is not a valid version".format(svr))
        version = svr.strip().split('.')
        version_list = []
        for ver in version:
            try:
                ver = int(ver)
            except ValueError:
                raise ValueError("{} is not an integer".format(ver))
            if ver < 0:
                raise ValueError("version can't have negative integers")
            version_list.append(ver)

        if not version_list:
            raise ValueError("invalid version {}".format(svr))
        self.version = version_list

    def __lt__(self, other):
        if other.latest:
            if self.latest:
                return False
            return True
        if self.latest:
            return False
        x = self.version.copy()
        y = other.version.copy()
        length = max(len(x), len(y))
        x += [0] * (length - len(x))
        y += [0] * (length - len(y))

        for a, b in zip(x, y):
            if a < b:
                return True
            if a > b:
                return False

    def __eq__(self, other):
        if other.latest != self.latest:
            return False
        if self.latest:
            return True
        x = self.version.copy()
        y = other.version.copy()
        length = max(len(x), len(y))
        x += [0] * (length - len(x))
        y += [0] * (length - len(y))

        return x == y

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return other.__lt__(self)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)
