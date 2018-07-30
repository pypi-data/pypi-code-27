__all__ = ['Scope']


class Scope:
    '''
        This class represents a Scope object.

        Responsibilities on enter:

        - Set the enable flags.
        - Bind the framebuffer.
        - Assing textures to texture locations.
        - Assing buffers to uniform buffers.
        - Assing buffers to shader storage buffers.

        Responsibilities on exit:

        - Restore the enable flags.
        - Restore the framebuffer.
    '''

    __slots__ = ['mglo', 'ctx', 'extra']

    def __init__(self):
        self.mglo = None
        self.ctx = None
        self.extra = None
        raise TypeError()

    def __repr__(self):
        return '<Scope>'

    def __enter__(self):
        self.mglo.begin()
        return self

    def __exit__(self, *args):
        self.mglo.end()
