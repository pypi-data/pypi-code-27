"""
Control flow graph builder.
"""
# Aurelien Coet, 2018.

import ast
from .model import Block, Link, CFG


def invert(node):
    """
    Invert the operation in an ast node object (get its negation).

    Args:
        node: An ast node object.

    Returns:
        An ast node object containing the inverse (negation) of the input node.
    """
    inverse = {ast.Eq: ast.NotEq,
               ast.NotEq: ast.Eq,
               ast.Lt: ast.GtE,
               ast.LtE: ast.Gt,
               ast.Gt: ast.LtE,
               ast.GtE: ast.Lt,
               ast.Is: ast.IsNot,
               ast.IsNot: ast.Is,
               ast.In: ast.NotIn,
               ast.NotIn: ast.In}

    if type(node) == ast.Compare:
        op = type(node.ops[0])
        inverse_node = ast.Compare(left=node.left, ops=[inverse[op]()],
                                   comparators=node.comparators)
    elif type(node) == ast.NameConstant and node.value in [True, False]:
        inverse_node = ast.NameConstant(value=not node.value)
    else:
        inverse_node = ast.UnaryOp(op=ast.Not(), operand=node)

    return inverse_node


def merge_exitcases(exit1, exit2):
    """
    Merge the exitcases of two Links.

    Args:
        exit1: The exitcase of a Link object.
        exit2: Another exitcase to merge with exit1.

    Returns:
        The merged exitcases.
    """
    if exit1:
        if exit2:
            return ast.BoolOp(ast.And(), values=[exit1, exit2])
        return exit1
    return exit2


class CFGBuilder(ast.NodeVisitor):
    """
    Control flow graph builder.

    A control flow graph builder is an ast.NodeVisitor that can walk through
    a program's AST and iteratively build the corresponding CFG.
    """

    # ---------- CFG building methods ---------- #
    def build(self, name, tree, async=False, entry_id=0):
        """
        Build a CFG from an AST.

        Args:
            name: The name of the CFG being built.
            tree: The root of the AST from which the CFG must be built.
            async: Boolean indicating whether the CFG being built represents an
                   asynchronous function or not. When the CFG of a Python
                   program is being built, it is considered like a synchronous
                   'main' function.
            entry_id: Value for the id of the entry block of the CFG.

        Returns:
            The CFG produced from the AST.
        """
        self.cfg = CFG(name, async=async)
        # Tracking of the current block while building the CFG.
        self.current_id = entry_id
        self.current_block = self.new_block()
        self.cfg.entryblock = self.current_block
        # Actual building of the CFG is done here.
        self.visit(tree)
        self.clean_cfg(self.cfg.entryblock)
        return self.cfg

    def build_from_src(self, name, src):
        """
        Build a CFG from some Python source code.

        Args:
            name: The name of the CFG being built.
            src: A string containing the source code to build the CFG from.

        Returns:
            The CFG produced from the source code.
        """
        tree = ast.parse(src, mode='exec')
        return self.build(name, tree)

    def build_from_file(self, name, filepath):
        """
        Build a CFG from some Python source file.

        Args:
            name: The name of the CFG being built.
            filepath: The path to the file containing the Python source code
                      to build the CFG from.

        Returns:
            The CFG produced from the source file.
        """
        with open(filepath, 'r') as src_file:
            src = src_file.read()
            return self.build_from_src(name, src)

    # ---------- Graph management methods ---------- #
    def new_block(self):
        """
        Create a new block with a new id.

        Returns:
            A Block object with a new unique id.
        """
        self.current_id += 1
        return Block(self.current_id)

    def add_statement(self, block, statement):
        """
        Add a statement to a block.

        Args:
            block: A Block object to which a statement must be added.
            statement: An AST node representing the statement that must be
                       added to the current block.
        """
        block.statements.append(statement)

    def add_exit(self, block, nextblock, exitcase=None):
        """
        Add a new exit to a block.

        Args:
            block: A block to which an exit must be added.
            nextblock: The block to which control jumps from the new exit.
            exitcase: An AST node representing the 'case' (or condition)
                      leading to the exit from the block in the program.
        """
        newlink = Link(block, nextblock, exitcase)
        block.exits.append(newlink)
        nextblock.predecessors.append(newlink)

    def new_loopguard(self):
        """
        Create a new block for a loop's guard if the current block is not
        empty. Links the current block to the new loop guard.

        Returns:
            The block to be used as new loop guard.
        """
        if self.current_block.is_empty() and\
           len(self.current_block.exits) == 0:
            # If the current block is empty and has no exits, it is used as
            # entry block (condition test) for the loop.
            loopguard = self.current_block
        else:
            # Jump to a new block for the loop's guard if the current block
            # isn't empty or has exits.
            loopguard = self.new_block()
            self.add_exit(self.current_block, loopguard)

        return loopguard

    def new_functionCFG(self, node, async=False):
        """
        Create a new sub-CFG for a function definition and add it to the
        function CFGs of the CFG being built.

        Args:
            node: The AST node containing the function definition.
            async: Boolean indicating whether the function for which the CFG is
                   being built is asynchronous or not.
        """
        self.current_id += 1
        # A new sub-CFG is created for the body of the function definition and
        # added to the function CFGs of the current CFG.
        func_body = ast.Module(body=node.body)
        func_builder = CFGBuilder()
        self.cfg.functioncfgs[node.name] = func_builder.build(node.name,
                                                              func_body,
                                                              async,
                                                              self.current_id)
        self.current_id = func_builder.current_id + 1

    def clean_cfg(self, block, visited=[]):
        """
        Remove the useless (empty) blocks from a CFG.

        Args:
            block: The block from which to start traversing the CFG to clean
                   it.
            visited: A list of blocks that already have been visited by
                     clean_cfg (recursive function).
        """
        # Don't visit blocks twice.
        if block in visited:
            return
        visited.append(block)

        # Empty blocks are removed from the CFG.
        if block.is_empty():
            to_visit = []
            for pred in block.predecessors:
                for exit in block.exits:
                    self.add_exit(pred.source, exit.target,
                                  merge_exitcases(pred.exitcase,
                                                  exit.exitcase))
                    exit.target.predecessors.remove(exit)
                pred.source.exits.remove(pred)

            block.predecessors = []
            for exit in block.exits:
                self.clean_cfg(exit.target, visited)
            block.exits = []
        else:
            for exit in block.exits:
                self.clean_cfg(exit.target, visited)

    # ---------- AST Node visitor methods ---------- #
    def visit_Expr(self, node):
        self.add_statement(self.current_block, node)
        self.generic_visit(node)

    def visit_Call(self, node):
        func = node.func
        if type(func) == ast.Attribute:
            func_name = "{}.{}".format(func.value.id, func.attr)
        else:
            func_name = func.id
        self.current_block.func_calls.append(func_name)

    def visit_Assign(self, node):
        self.add_statement(self.current_block, node)
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        self.add_statement(self.current_block, node)
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        self.add_statement(self.current_block, node)
        self.generic_visit(node)

    def visit_Raise(self, node):
        # TODO
        pass

    def visit_Assert(self, node):
        self.add_statement(self.current_block, node)
        # New block for the case in which the assertion 'fails'.
        failblock = self.new_block
        self.add_exit(self.current_block, failblock, invert(node.test))
        # If the assertion fails, the current flow ends, so the fail block is a
        # final block of the CFG.
        self.cfg.final_blocks.append(failblock)
        # If the assertion is True, continue the flow of the program.
        successblock = self.new_block()
        self.add_exit(self.current_block, successblock, node.test)
        self.current_block = successblock
        self.generic_visit(node)

    def visit_If(self, node):
        # Add the If statement at the end of the current block.
        self.add_statement(self.current_block, node)

        # Create a new block for the body of the if.
        if_block = self.new_block()
        self.add_exit(self.current_block, if_block, node.test)

        # Create a block for the code after the if-else.
        afterif_block = self.new_block()

        # New block for the body of the else if there is an else clause.
        if len(node.orelse) != 0:
            else_block = self.new_block()
            self.add_exit(self.current_block, else_block, invert(node.test))
            else_label = ""
            self.current_block = else_block
            # Visit the children in the body of the else to populate the block.
            for child in node.orelse:
                self.visit(child)
            self.add_exit(self.current_block, afterif_block)
        else:
            self.add_exit(self.current_block, afterif_block, invert(node.test))

        # Visit children to populate the if block.
        self.current_block = if_block
        for child in node.body:
            self.visit(child)
        self.add_exit(self.current_block, afterif_block)

        # Continue building the CFG in the after-if block.
        self.current_block = afterif_block

    def visit_While(self, node):
        loop_guard = self.new_loopguard()
        self.current_block = loop_guard
        self.add_statement(self.current_block, node)

        # New block for the case where the test in the while is True.
        while_block = self.new_block()
        self.add_exit(self.current_block, while_block, node.test)

        # New block for the case where the test in the while is False.
        afterwhile_block = self.new_block()
        self.add_exit(self.current_block, afterwhile_block, invert(node.test))

        # Populate the while block.
        self.current_block = while_block
        for child in node.body:
            self.visit(child)
        self.add_exit(self.current_block, loop_guard)

        # Continue building the CFG in the after-while block.
        self.current_block = afterwhile_block

    def visit_For(self, node):
        loop_guard = self.new_loopguard()
        self.current_block = loop_guard
        self.add_statement(self.current_block, node)

        # New block for the body of the for-loop.
        for_block = self.new_block()
        self.add_exit(self.current_block, for_block, node.iter)

        # Block of code after the for loop.
        afterfor_block = self.new_block()
        self.add_exit(self.current_block, afterfor_block)
        self.current_block = for_block

        # Populate the body of the for loop.
        for child in node.body:
            self.visit(child)
        self.add_exit(self.current_block, loop_guard)

        # Continue building the CFG in the after-for block.
        self.current_block = afterfor_block

    def visit_Break(self, node):
        # TODO
        pass

    def visit_Continue(self, node):
        # TODO
        pass

    def visit_Import(self, node):
        self.add_statement(self.current_block, node)

    def visit_ImportFrom(self, node):
        self.add_statement(self.current_block, node)

    def visit_FunctionDef(self, node):
        self.add_statement(self.current_block, node)
        self.new_functionCFG(node, async=False)

    def visit_AsyncFunctionDef(self, node):
        self.add_statement(self.current_block, node)
        self.new_functionCFG(node, async=True)

    def visit_Await(self, node):
        afterawait_block = self.new_block()
        self.add_exit(self.current_block, afterawait_block)
        self.generic_visit(node)
        self.current_block = afterawait_block

    def visit_Return(self, node):
        self.add_statement(self.current_block, node)
        self.cfg.finalblocks.append(self.current_block)
        # Continue in a new block but without any jump to it -> all code after
        # the return statement will not be included in the CFG.
        self.current_block = self.new_block()

    def visit_Yield(self, node):
        self.cfg.async = True
        afteryield_block = self.new_block()
        self.add_exit(self.current_block, afteryield_block)
        self.current_block = afteryield_block
