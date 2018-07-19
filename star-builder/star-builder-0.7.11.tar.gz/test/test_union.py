from star_builder import Type, validators


class Union(Type):
    field = (validators.Array(validators.String(default="")) | validators.String(
        default="")) << {"allow_null": True}

a = Union()
a.format()
print(a)

