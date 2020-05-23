import sys

from transpiler.lexer import *
from transpiler.parser import *


class CodeGen:
    def __init__(self):
        self.start = '#include <iostream>\n\n'
        self.main = '\nint main()\n{\n'
        self.end = self.indent('return 0;\n}\n', 1)

    def generate(self, variables, ast):
        code = self.start
        for node in ast.children:
            if node.name.type == 'DEF':
                code += self.function_code(variables, node)
        code += self.main
        if '' in variables:
            for variable in variables['']:
                code += self.indent(self.type(variable[1]) +
                                    ' ' + variable[0] + ';\n', 1)
        code += self.block(ast, 1)
        code += self.end
        return code

    def block(self, ast, indent):
        code = ''
        for node in ast.children:
            if node.name.type == 'EQUALS':
                code += self.assignment_code(node, indent)
            elif node.name.type == 'WHILE':
                code += self.while_code(node, indent)
            elif node.name.type == 'IF':
                code += self.if_code(node, indent)
            elif node.name.type == 'PRINT':
                code += self.print_code(node, indent)
            elif node.name.type == 'RETURN':
                code += self.return_code(node, indent)
            elif node.name.type == 'RETURN_TYPE':
                code += self.func_call_code(node,
                                            statement=True, indent=indent)
        return code

    def function_code(self, variables, ast):
        function_name = ast.children[0].name.value
        code = self.type(ast.children[1].name.type) + ' ' + function_name + '('
        code += (', '.join([self.type(arg.children[0].name.type) +
                            ' ' + arg.name.value for arg in ast.children[0].children]))
        code += ')\n{\n'
        indent = 1
        if function_name in variables:
            for variable in variables[function_name]:
                code += self.indent(self.type(variable[1]) +
                                    ' ' + variable[0] + ';\n', indent)
        code += self.block(ast.children[2], indent)
        code += '}\n'
        return code

    def assignment_code(self, ast, indent):
        return self.indent(ast.children[0].name.value + ' = ' + self.expression_code(ast.children[1]) + ';\n', indent)

    def return_code(self, ast, indent):
        return self.indent('return ' + self.expression_code(ast.children[0]) + ';\n', indent)

    def while_code(self, ast, indent):
        code = self.indent(
            'while(' + self.expression_code(ast.children[0]) + ')\n', indent) + self.indent('{\n', indent)
        indent += 1
        code += self.block(ast.children[1], indent)
        indent -= 1
        code += self.indent('}\n', indent)
        return code

    def if_code(self, ast, indent):
        code = self.indent(
            'if(' + self.expression_code(ast.children[0]) + ')\n', indent) + self.indent('{\n', indent)
        indent += 1
        code += self.block(ast.children[1], indent)
        indent -= 1
        code += self.indent('}\n', indent)
        if len(ast.children) >= 3:
            if ast.children[2].name.type == 'IF':
                code += self.if_code(ast.children[2], indent)
            else:
                code += self.else_code(ast.children[2], indent)
        return code

    def else_code(self, ast, indent):
        code = self.indent('else\n', indent)
        code += self.indent('{\n', indent)
        indent += 1
        code += self.block(ast, indent)
        indent -= 1
        code += self.indent('}\n', indent)
        return code

    def print_code(self, ast, indent):
        code = self.indent('std::cout << ', indent)
        for arg in ast.children:
            code += self.expression_code(arg)
            code += ' << '
        code += 'std::endl;\n'
        return code

    def func_call_code(self, ast, statement=False, indent=0):
        code = ''
        if statement:
            code += self.indent('', indent)
        code += ast.children[0].name.value + '('
        code += (', '.join([self.element_translator(arg.name)
                            for arg in ast.children[1:]]))
        code += ')'
        if statement:
            code += ';\n'
        return code

    def operation_code(self, ast):
        return (' '.join([self.element_translator(el.name) for el in ast.children]))

    def expression_code(self, ast):
        if ast.name.type != 'RETURN_TYPE':
            return self.operation_code(ast)
        else:
            return self.func_call_code(ast)

    def indent(self, code, indent):
        return indent * 4 * ' ' + code

    def element_translator(self, token):
        if token.type == 'IDENTIFIER':
            return token.value
        elif token.type == 'VALUE_INT' or token.type == 'VALUE_FLOAT' or token.type == 'VALUE_BOOL':
            return str(token.value)
        elif token.type == 'NOT':
            return '!'
        elif token.type == 'PLUS':
            return '+'
        elif token.type == 'MINUS':
            return '-'
        elif token.type == 'MULTIPLY':
            return '*'
        elif token.type == 'DIVIDE':
            return '/'
        elif token.type == 'MODULO':
            return '%'
        elif token.type == 'AND':
            return '&&'
        elif token.type == 'OR':
            return '||'
        elif token.type == 'ISEQUAL':
            return '=='
        elif token.type == 'ISNOTEQUAL':
            return '!='
        elif token.type == 'ISLESS':
            return '<'
        elif token.type == 'ISEQUALLESS':
            return '<='
        elif token.type == 'ISMORE':
            return '>'
        elif token.type == 'ISEQUALMORE':
            return '>='

    def type(self, type):
        if type == 'INT':
            return 'int'
        if type == 'FLOAT':
            return 'float'
        if type == 'BOOL':
            return 'bool'
        if type == 'NONE':
            return 'void'


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(
            f'Usage: python {sys.argv[0]} <input file path> <output file path>')
        sys.exit(1)
    with open(sys.argv[1]) as f:
        data = f.read()
    lexer = Lexer()
    parser = Parser()
    code_generator = CodeGen()
    lexer.input(data)
    try:
        output_code = code_generator.generate(*parser.parse(lexer.tokens()))
        print(output_code)
    except LexerError as le:
        print(f'lexical error: line {le.line}')
    except ParserError as pe:
        print(f'syntax error: token {pe.token}, line {pe.token.line}')
    with open(sys.argv[2], 'w') as f:
        f.write(output_code)
