from star_builder import Type, validators


class A(Type):
    name = validators.String()

class Union(Type):
    field = (validators.Array(validators.String(default="")) | validators.String(
        default="")) << {"allow_null": True}
    print(field)
    print(field.allow_null)
    # name = validators.Proxy(A, allow_null=True)
a = Union()
a.format()
print(a)

