import sys

from anytree import Node, RenderTree, PreOrderIter

from transpiler.lexer import *

# grammar:
# program = statements
# statements = statement | statement statements
# statement = assignment_statement | function_statement | return_statement | while_statement |
# if_statement | print_statement | func_call |  NEWLINE
# statement_block = INDENT statements DEDENT
# assignment_statement = IDENTIFIER [COLON type] EQUALS expression
# function_statement = DEF IDENTIFIER LP[IDENTIFIER COLON type] {COMMA IDENTIFIER’ COLON
# type} RP RETURN_TYPE(type | NONE) COLON statement_block
# return_statement = RETURN expression
# while_statement = WHILE expression COLON statement_block
# if_statement = IF expression COLON statement_block [else_statement | elif_statement]
# elif_statement = ELIF expression COLON statement_block [else_statement | elif_statement]
# else_statement = ELSE COLON statement_block
# print_statement = PRINT LP[expression] {COMMA expression} RP
# expression = func_call | operation
# operation = [unary_logic_op] (value | IDENTIFIER) {(binary_op | binary_logic_op | comparison_op) (value | IDENTIFIER)}
# func_call = IDENTIFIER LP (value | IDENTIFIER) {COMMA (value | IDENTIFIER)} RP
# unary_logic_op = NOT
# binary_op = PLUS | MINUS | MULTIPLY | DIVIDE | MODULO
# binary_logic_op = AND | OR
# comparison_op = ISEQUAL | ISNOTEQUAL | ISLESS | ISEQUALLESS | ISMORE | ISEQUALMORE
# type = INT | FLOAT | BOOL
# value = VALUE_INT | VALUE_FLOAT | VALUE_BOOL


class ParserError(Exception):
    """ Contains unrecognized syntax token
    """

    def __init__(self, token):
        self.token = token


class Parser:
    def parse(self, tokens):
        ast = Node('Program')
        variables = {}
        scope = ''
        token = None
        while True:
            try:
                token = self.statement(tokens, ast, variables, scope, token)
                if token is not None and token.type == 'DEDENT':
                    raise ParserError(token)
            except StopIteration:
                break
        return variables, ast

    def statement(self, tokens, ast, variables, scope, token=None):
        if token is None:
            token = next(tokens)
        while token.type == 'NEWLINE':
            token = next(tokens)
        if token.type == 'IDENTIFIER':
            token2 = next(tokens)
            if token2.type == 'COLON':
                token2 = next(tokens)
                if not self.type(token2.type):
                    raise ParserError(token2)
                if scope not in variables:
                    variables[scope] = []
                for variable in variables[scope]:
                    if token.value == variable[0] and token2.type != variable[1]:
                        raise ParserError(token)
                variables[scope].append((token.value, token2.type))
                token2 = next(tokens)
                if token2.type != 'EQUALS':
                    return token2
            if token2.type == 'EQUALS':
                assign_ast = Node(token2, parent=ast)
                Node(token, parent=assign_ast)
                return self.expression_statement(tokens, assign_ast, variables, scope)
            if token2.type == 'LP':
                func_call_ast = Node(Token(token.line, 'RETURN_TYPE'), parent=ast)
                Node(token, parent=func_call_ast)
                return self.func_call_statement(tokens, func_call_ast, variables, scope)
            raise ParserError(token)
        if token.type == 'DEF':
            sub_ast = Node(token, parent=ast)
            new_scope = scope
            return self.function_statement(
                tokens, sub_ast, variables, new_scope)
        if token.type == 'WHILE':
            sub_ast = Node(token, parent=ast)
            return self.while_statement(
                tokens, sub_ast, variables, scope)
        if token.type == 'IF':
            sub_ast = Node(token, parent=ast)
            return self.if_statement(
                tokens, sub_ast, variables, scope)
        if token.type == 'PRINT':
            sub_ast = Node(token, parent=ast)
            return self.print_statement(
                tokens, sub_ast, variables, scope)
        if token.type == 'RETURN':
            sub_ast = Node(token, parent=ast)
            return self.expression_statement(
                tokens, sub_ast, variables, scope)
        if token.type == 'DEDENT':
            return token
        raise ParserError(token)

    def func_call_statement(self, tokens, ast, variables, scope):
        token = next(tokens)
        if token.type == 'RP':
            return next(tokens)
        if not self.value(token.type) and token.type != 'IDENTIFIER':
            raise ParserError(token)
        Node(token, parent=ast)
        token = next(tokens)
        while token.type != 'RP':
            if token.type != 'COMMA':
                raise ParserError(token)
            token = next(tokens)
            if not self.value(token.type) and token.type != 'IDENTIFIER':
                raise ParserError(token)
            Node(token, parent=ast)
            token = next(tokens)
        return next(tokens)

    def function_statement(self, tokens, def_ast, variables, scope):
        token = next(tokens)
        if token.type != 'IDENTIFIER':
            raise ParserError(token)
        scope = token.value
        func_ast = Node(token, parent=def_ast)
        token = next(tokens)
        if token.type != 'LP':
            raise ParserError(token)
        token = next(tokens)
        while token.type != 'RP':
            if token.type != 'IDENTIFIER':
                raise ParserError(token)
            arg_ast = Node(token, parent=func_ast)
            token = next(tokens)
            if token.type != 'COLON':
                raise ParserError(token)
            token = next(tokens)
            if not self.type(token.type):
                raise ParserError(token)
            Node(token, parent=arg_ast)
            token = next(tokens)
            if token.type != 'COMMA' and token.type != 'RP':
                raise ParserError(token)
            if token.type == 'COMMA':
                token = next(tokens)
                if token.type == 'RP':
                    raise ParserError(token)
        token = next(tokens)
        if token.type != 'RETURN_TYPE':
            raise ParserError(token)
        token = next(tokens)
        if token.type != 'NONE' and not self.type(token.type):
            raise ParserError(token)
        Node(token, parent=def_ast)
        token = next(tokens)
        if token.type != 'COLON':
            raise ParserError(token)
        block_ast = Node(token, parent=def_ast)
        return self.statement_block(tokens, block_ast, variables, scope)

    def while_statement(self, tokens, while_ast, variables, scope):
        token = self.expression_statement(tokens, while_ast, variables, scope)
        if token.type != 'COLON':
            raise ParserError(token)
        block_ast = Node(token, parent=while_ast)
        return self.statement_block(tokens, block_ast, variables, scope)

    def if_statement(self, tokens, if_ast, variables, scope):
        token = self.expression_statement(tokens, if_ast, variables, scope)
        if token.type != 'COLON':
            raise ParserError(token)
        block_ast = Node(token, parent=if_ast)
        self.statement_block(tokens, block_ast, variables, scope)
        token = next(tokens)
        if token.type == 'ELSE':
            return self.else_statement(tokens, if_ast, variables, scope)
        elif token.type == 'ELIF':
            elif_ast = Node(Token(token.line, 'IF'), parent=if_ast)
            return self.if_statement(tokens, elif_ast, variables, scope)
        return token

    def else_statement(self, tokens, else_ast, variables, scope):
        token = next(tokens)
        if token.type != 'COLON':
            raise ParserError(token)
        block_ast = Node(token, parent=else_ast)
        return self.statement_block(tokens, block_ast, variables, scope)

    def print_statement(self, tokens, print_ast, variables, scope):
        token = next(tokens)
        if token.type != 'LP':
            raise ParserError(token)
        while token.type != 'RP':
            token = self.expression_statement(
                tokens, print_ast, variables, scope)
            if token.type != 'COMMA' and token.type != 'RP':
                raise ParserError(token)
        return next(tokens)

    def statement_block(self, tokens, ast, variables, scope):
        token = next(tokens)
        if token.type != 'INDENT':
            raise ParserError(token)
        token = self.statement(tokens, ast, variables, scope)
        while token is None or token.type != 'DEDENT':
            token = self.statement(tokens, ast, variables, scope, token)
        return None

    def expression_statement(self, tokens, ast, variables, scope):
        token = next(tokens)
        if token.type != 'IDENTIFIER' and token.type != 'NOT' and not self.value(token.type):
            return token
        token2 = next(tokens)
        if token.type == 'IDENTIFIER' and token2.type == 'LP':
            func_call_ast = Node(Token(token.line, 'RETURN_TYPE'), parent=ast)
            Node(token, parent=func_call_ast)
            return self.func_call_statement(tokens, func_call_ast, variables, scope)
        operation_ast = Node(Token(token.line, type='COLON'), parent=ast)
        Node(token, parent=operation_ast)
        if token.type == 'NOT' and token2.type != 'IDENTIFIER' and not self.value(token2.type):
            raise ParserError(token2)
        elif token.type == 'NOT' and (token2.type == 'IDENTIFIER' or self.value(token2.type)):
            token = next(tokens)
            Node(token2, parent=operation_ast)
            if not self.binary_op(token.type) and not self.binary_logic_op(token.type) and not self.comparison_op(token.type):
                return token
            Node(token, parent=operation_ast)
        elif (token.type == 'IDENTIFIER' or self.value(token.type)) and not self.binary_op(token2.type) and not self.binary_logic_op(token2.type) and not self.comparison_op(token2.type):
            return token2
        else:
            Node(token2, parent=operation_ast)
        while True:
            token = next(tokens)
            if token.type != 'IDENTIFIER' and not self.value(token.type):
                raise ParserError(token)
            Node(token, parent=operation_ast)
            token = next(tokens)
            if not self.binary_op(token.type) and not self.binary_logic_op(token.type) and not self.comparison_op(token.type):
                return token
            Node(token, parent=operation_ast)

    def value(self, token_type):
        return (token_type == 'VALUE_INT' or token_type == 'VALUE_FLOAT' or token_type == 'VALUE_BOOL')

    def type(self, token_type):
        return (token_type == 'INT' or token_type == 'FLOAT' or token_type == 'BOOL')

    def comparison_op(self, token_type):
        return (token_type == 'ISEQUAL' or token_type == 'ISNOTEQUAL' or token_type == 'ISLESS' or token_type == 'ISEQUALLESS' or token_type == 'ISMORE' or token_type == 'ISEQUALMORE')

    def binary_logic_op(self, token_type):
        return (token_type == 'AND' or token_type == 'OR')

    def binary_op(self, token_type):
        return (token_type == 'PLUS' or token_type == 'MINUS' or token_type == 'MULTIPLY' or token_type == 'DIVIDE' or token_type == 'MODULO')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <input file path>')
        sys.exit(1)
    with open(sys.argv[1]) as f:
        data = f.read()
    parser = Parser()
    lexer = Lexer()
    lexer.input(data)
    try:
        variables, ast = parser.parse(lexer.tokens())
        print(variables)
        for pre, _, node in RenderTree(ast):
            print("%s%s" % (pre, node.name))
    except LexerError as le:
        print(f'lexical error: line {le.line}')
    except ParserError as pe:
        print(f'syntax error: token {pe.token}, line {pe.token.line}')
