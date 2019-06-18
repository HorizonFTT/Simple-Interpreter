from Lexer.lexer import Lexer
from Lexer.token_types import *
from Parser.visitor import NodeVisitor
from Parser.myparser import Parser
from Semantic.semantic import SemanticAnalyzer
from Semantic.symbol import ScopedSymbolTable
from .frame import Frame
import logging
import sys


class Interpreter(NodeVisitor):

    def __init__(self, text=None):
        self.call_stack = []
        self.current_frame = None

        if text is None:
            text = open(f'{sys.path[0]}/{sys.argv[1]}', 'r').read()

        lexer = Lexer(text)
        parser = Parser(lexer)
        self.tree = parser.parse()

        semantic_analyzer = SemanticAnalyzer()
        self.scopes = semantic_analyzer.analyze(self.tree)

    def visit_Program(self, node):
        frame = Frame(self.scopes['_global'])
        self.current_frame = frame
        self.call_stack.append(frame)
        self.visit(node.block)
        self.call_stack.pop()
        self.current_frame = frame.enclosing_frame

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        # Do nothing
        pass

    def visit_Type(self, node):
        # Do nothing
        pass

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))

    def visit_Condition(self, node):
        if node.op_type == LESS_THAN:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op_type == GREATER_THAN:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op_type == EQUAL:
            return self.visit(node.left) == self.visit(node.right)

    def visit_IfElse(self, node):
        if self.visit(node.result):
            self.visit(node.true_statement)
        else:
            self.visit(node.false_statement)

    def visit_While(self, node):
        while self.visit(node.result):
            self.visit(node.statement)

    def visit_For(self, node):
        self.visit(node.beg)
        loop_var = node.beg.left
        beg = self.visit(loop_var)
        end = self.visit(node.end)
        while beg <= end:
            self.visit(node.statement)
            beg = self.visit(loop_var) + 1
            self.current_frame.set(loop_var.value, beg)

    def visit_Num(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        var_name = node.left.value
        var_value = self.visit(node.right)
        self.current_frame.set(var_name, var_value)

    def visit_Var(self, node):
        var_name = node.value
        var_value = self.current_frame.get(var_name)
        return var_value

    def visit_NoOp(self, node):
        pass

    def visit_ProcedureDecl(self, node):
        proc_name = node.proc_name
        self.current_frame.set(proc_name, node.block_node)

    def visit_FunctionDecl(self, node):
        self.visit_ProcedureDecl(node)

    def call_bulidin(self, node):
        call_name = node.procedure
        if call_name == 'WRITELN':
            for p in node.params:
                r = self.visit(p)
                print(r)
        elif call_name == 'READLN':
            for p in node.params:
                t = input()
                p_type = self.current_frame.scope.lookup(p.value).type.name
                if p_type == INTEGER:
                    t = int(t)
                elif p_type == REAL:
                    t = float(t)
                self.current_frame.set(p.value, t)

    def visit_Call(self, node):
        call_name = node.procedure
        call_node = self.current_frame.get(call_name)
        level = self.current_frame.scope.scope_level + 1
        scope = self.scopes.get(call_name)
        if scope is None:
            scope = ScopedSymbolTable(
                call_name, level, self.current_frame.scope)
        frame = Frame(scope, self.current_frame)
        self.call_stack.append(frame)
        if call_node is None:
            self.current_frame = frame
            self.call_bulidin(node)
        else:
            symbol = self.current_frame.scope.lookup(call_name)
            formal_params = symbol.params
            actual_params = node.params
            for f, a in zip(formal_params, actual_params):
                name = f.name
                value = self.visit(a)
                frame.set(name, value)
            self.current_frame = frame
            self.visit(call_node)
        self.call_stack.pop()
        return_value = self.current_frame.return_value
        self.current_frame = frame.enclosing_frame
        return return_value

    def interpret(self):
        tree = self.tree
        if tree is None:
            return ''
        return self.visit(tree)
