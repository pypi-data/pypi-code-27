from modelx.core.cpydep import alter_freevars


def dummy():

    x = 3

    def foo():
        return x

    return foo



def foo():
    return x


naked = dummy().__code__
altfoo = alter_freevars(foo, x=3)
nested = altfoo.__code__


for attr in dir(nested):

    print(attr,
          getattr(nested, attr),
          getattr(naked, attr),
          getattr(nested, attr) == getattr(naked, attr))
