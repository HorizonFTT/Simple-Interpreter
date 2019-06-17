import logging
from visitor import NodeVisitor
import symbol


class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.scopes = {}
        self.current_scope = None

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Program(self, node):
        logging.debug(' ENTER scope: global')
        global_scope = symbol.ScopedSymbolTable(
            scope_name='global',
            scope_level=1,
            enclosing_scope=self.current_scope,  # None
        )
        global_scope._init_builtins()
        self.scopes['_global'] = global_scope
        self.current_scope = global_scope

        # visit subtree
        self.visit(node.block)

        logging.debug(global_scope)

        self.current_scope = self.current_scope.enclosing_scope
        logging.debug(' LEAVE scope: global')

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_IfElse(self, node):
        pass

    def visit_While(self, node):
        pass

    def visit_For(self, node):
        pass

    def visit_ProcedureDecl(self, node):
        proc_name = node.proc_name
        proc_symbol = symbol.ProcedureSymbol(proc_name)
        self.current_scope.insert(proc_symbol)

        logging.debug(' ENTER scope: %s' % proc_name)
        # Scope for parameters and local variables
        procedure_scope = symbol.ScopedSymbolTable(
            scope_name=proc_name,
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        self.scopes[proc_name] = procedure_scope
        self.current_scope = procedure_scope

        # Insert parameters into the procedure scope
        for param in node.params:
            param_type = self.current_scope.lookup(param.type_node.value)
            param_name = param.var_node.value
            var_symbol = symbol.VarSymbol(param_name, param_type)
            self.current_scope.insert(var_symbol)
            proc_symbol.params.append(var_symbol)

        self.visit(node.block_node)

        logging.debug(procedure_scope)

        self.current_scope = self.current_scope.enclosing_scope
        logging.debug(' LEAVE scope: %s' % proc_name)

    def visit_FunctionDecl(self, node):
        self.visit_ProcedureDecl(node)

    def visit_VarDecl(self, node):
        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)

        # We have all the information we need to create a variable symbol.
        # Create the symbol and insert it into the symbol table.
        var_name = node.var_node.value
        var_symbol = symbol.VarSymbol(var_name, type_symbol)

        # Signal an error if the table alrady has a symbol
        # with the same name
        if self.current_scope.lookup(var_name, current_scope_only=True):
            raise Exception(
                f'Error: Duplicate identifier \'{var_name}\' found'
            )

        self.current_scope.insert(var_symbol)

    def visit_Assign(self, node):
        # self.visit(node.right)
        # self.visit(node.left)
        # right-hand side
        value_type = self.visit(node.right).type
        # left-hand side
        var_type = self.visit(node.left).type
        if value_type.replace('_CONST', '') != var_type:
            raise Exception(
                f'Error: Can\'t assign {value_type} to {var_type}'
            )

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            raise Exception(
                "Error: Symbol(identifier) not found '%s'" % var_name
            )
        return var_symbol

    def visit_Num(self, node):
        return node.token

    def visit_String(self, node):
        return node.token

    def visit_UnaryOp(self, node):
        pass

    def visit_Call(self, node):
        call_name = node.procedure
        var_symbol = self.current_scope.lookup(call_name)
        if var_symbol is None:
            raise Exception(
                "Error: Symbol(identifier) not found '%s'" % call_name
            )
        params = node.params
        scope = self.current_scope.lookup(call_name)

    def analyze(self, tree):
        try:
            self.visit(tree)
        except Exception as e:
            print(e)
        return self.scopes
