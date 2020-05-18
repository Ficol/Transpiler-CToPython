import unittest

from transpiler.lexer import *
from transpiler.parser import *


class ParserTesting(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_empty(self):
        tokens = iter([])
        variables, ast = self.parser.parse(tokens)
        self.assertEqual(
            [node.name for node in PreOrderIter(ast)], ['Program'])
        self.assertEqual(variables, {})

    def test_if(self):
        tokens = iter([Token(1, 'IF'), Token(1, 'VALUE_BOOL', True), Token(
            1, 'COLON'), Token(1, 'INDENT'), Token(1, 'DEDENT')])
        variables, ast = self.parser.parse(tokens)
        self.assertEqual([str(node.name) for node in PreOrderIter(ast)], [
                         'Program', 'IF', 'COLON', 'VALUE_BOOL(True)', 'COLON'])
        self.assertEqual(variables, {})

    def test_assignment_initialization(self):
        tokens = iter([Token(1, 'IDENTIFIER', 'x'), Token(1, 'COLON'), Token(
            1, 'INT'), Token(1, 'EQUALS'), Token(1, 'VALUE_INT', 5), Token(1, 'NEWLINE')])
        variables, ast = self.parser.parse(tokens)
        self.assertEqual([str(node.name) for node in PreOrderIter(ast)], [
                         'Program', 'EQUALS', 'IDENTIFIER(x)', 'COLON', 'VALUE_INT(5)'])
        self.assertEqual(variables, {'': [('x', 'INT')]})

    def test_assignment(self):
        tokens = iter([Token(1, 'IDENTIFIER', 'x'), Token(
            1, 'EQUALS'), Token(1, 'VALUE_INT', 5), Token(1, 'NEWLINE')])
        variables, ast = self.parser.parse(tokens)
        self.assertEqual([str(node.name) for node in PreOrderIter(ast)], [
                         'Program', 'EQUALS', 'IDENTIFIER(x)', 'COLON', 'VALUE_INT(5)'])
        self.assertEqual(variables, {})

    def test_function(self):
        tokens = iter([Token(1, 'DEF'), Token(1, 'IDENTIFIER', 'x'), Token(1, 'LP'), Token(1, 'IDENTIFIER', 'y'), Token(1, 'COLON'), Token(
            1, 'BOOL'), Token(1, 'RP'), Token(1, 'RETURN_TYPE'), Token(1, 'NONE'), Token(1, 'COLON'), Token(1, 'INDENT'), Token(
            1, 'IDENTIFIER', 'z'), Token(1, 'COLON'), Token(1, 'INT'), Token(1, 'DEDENT')])
        variables, ast = self.parser.parse(tokens)
        self.assertEqual([str(node.name) for node in PreOrderIter(ast)], [
                         'Program', 'DEF', 'IDENTIFIER(x)', 'IDENTIFIER(y)', 'BOOL', 'NONE', 'COLON'])
        self.assertEqual(variables, {'x': [('z', 'INT')]})

    def test_return(self):
        tokens = iter([Token(1, 'RETURN'), Token(1, 'IDENTIFIER', 'x'), Token(
            1, 'PLUS'), Token(1, 'VALUE_INT', 2), Token(1, 'NEWLINE')])
        variables, ast = self.parser.parse(tokens)
        self.assertEqual([str(node.name) for node in PreOrderIter(ast)], [
                         'Program', 'RETURN', 'COLON', 'IDENTIFIER(x)', 'PLUS', 'VALUE_INT(2)'])
        self.assertEqual(variables, {})

    def test_print(self):
        tokens = iter([Token(1, 'PRINT'), Token(1, 'LP'), Token(1, 'IDENTIFIER', 'x'), Token(
            1, 'COMMA'), Token(1, 'VALUE_INT', 2), Token(1, 'RP'), Token(1, 'NEWLINE')])
        variables, ast = self.parser.parse(tokens)
        self.assertEqual([str(node.name) for node in PreOrderIter(ast)], [
                         'Program', 'PRINT', 'COLON', 'IDENTIFIER(x)', 'COLON', 'VALUE_INT(2)'])
        self.assertEqual(variables, {})

    def test_func_call(self):
        tokens = iter([Token(1, 'IDENTIFIER', 'x'), Token(1, 'LP'), Token(1, 'IDENTIFIER', 'y'), Token(
            1, 'COMMA'), Token(1, 'VALUE_INT', 2), Token(1, 'RP'), Token(1, 'NEWLINE')])
        variables, ast = self.parser.parse(tokens)
        for pre, _, node in RenderTree(ast):
            print("%s%s" % (pre, node.name))
        print([str(node.name) for node in PreOrderIter(ast)])
        self.assertEqual([str(node.name) for node in PreOrderIter(ast)], [
                         'Program', 'IDENTIFIER(x)', 'IDENTIFIER(y)', 'VALUE_INT(2)'])
        self.assertEqual(variables, {})

    def test_statement_error(self):
        tokens = iter([Token(1, 'IDENTIFIER', 'x'), Token(1, 'LP'), Token(1, 'IDENTIFIER', 'y'), Token(
            1, 'PLUS'), Token(1, 'RP'), Token(1, 'NEWLINE')])
        with self.assertRaises(ParserError):
            variables, ast = self.parser.parse(tokens)


if __name__ == '__main__':
    unittest.main()
