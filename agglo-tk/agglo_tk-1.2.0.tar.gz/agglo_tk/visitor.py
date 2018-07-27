
# TODO enrichir avec visitor injector et composite
# http://caron-yann.developpez.com/tutoriels/java/visitor-injector/
# https://github.com/IndexErrorCoders/python-patterns

import inspect

# TODO creer un accept_decorator(before, after) avec before et after qui sont des methodes (visitor, visitable, *args, **kwargs). Il se pose sur une classe heritant de visitable et surcharge la methode accept

class AtkVisitable(object):

    def accept(self, visitor, *args, **kwargs):
        visit_method = None

        # Iterate on self ancestors
        for cls in type(self).__mro__:
            # print cls
            visit_method_name = 'visit_' + cls.__name__
            visit_method = getattr(visitor, visit_method_name, None)
            if visit_method:
                break

        # If no visit method dedicated to visitable has been found
        if not visit_method:
            # Use generic visit method
            visit_method = visitor.visit
        
        # Call visit method dedicated to actual visitable class
        return visit_method(self, *args, **kwargs)
