"""
Sheldon is a module that will help you find the divisions in your python source
code.
"""
import ast

try:
    from visitors.divisitor import DivVisitor
except:
    from .visitors.divisitor import DivVisitor

# based on div tuple in divisitor module
LINENO = 0
NUMERATOR = 1
DENOMINATOR = 2

# Constant for readable output
TABSIZE = 4

class Sheldon:
    """This master class uses the DivVisitor class
    to analyses the source code.

    :param source: source code
    :type source: str

    """
    def __init__(self, source):
        self._source = source
        self._divs = DivVisitor()
        self._analyzed = False
        self._ast = None

    def analyze(self):
        """analyze the python source code"""
        # analyze once
        if not self._analyzed:
            self._ast = ast.parse(self._source)
            # visit AST
            self._divs.visit(self._ast)
            self._analyzed = True

    @property
    def divisions(self):
        """Returns the divisions"""
        self.analyze()
        return self._divs.divs

    def printdivs(self, filename, divs, readable):
        """print the divisions found in the source code"""
        if divs:
            if readable:
                print(f"{filename}")
            for div in divs:
                if not readable:
                    print(f"{filename}", end="")
                else: print(" " * TABSIZE, end="")
                print(f" {div[LINENO]} {div[NUMERATOR]:5} / {div[DENOMINATOR]}")

if __name__ == "__main__":
    print("Leonard always drives Sheldon around")
    print("execute the leonard driver instead")
