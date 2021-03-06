from spi_lexer import *
from spi_parser import *

# Visitor Pattern
class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}

    def visit_BinOp(self, node):
        if node.op.type == 'PLUS':
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == 'MINUS':
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == 'MUL':
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == 'INTEGER_DIV':
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == 'FLOAT_DIV':
            return float(self.visit(node.left)) / float(self.visit(node.right))

    def visit_UnaryOp(self, node):
        if node.op.type == 'PLUS':
            return +self.visit(node.expr)
        elif node.op.type == 'MINUS':
            return -self.visit(node.expr)

    def visit_Num(self, node):
        return node.value

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def visit_Program(self, node):
        # Register the program name?
        self.visit(node.block)
    
    def visit_Block(self, node):
        for decl in node.declarations:
            self.visit(decl)
        
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        # Register in Symbol table for the variable
        node.var_node
        self.visit(node.var_type)

    def visit_Type(self, node):
        return node.value

    def interpret(self):
        root = self.parser.parse()
        self.visit(root)
