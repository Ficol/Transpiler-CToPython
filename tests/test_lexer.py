import unittest

from transpiler.lexer import *


class LexerTesting(unittest.TestCase):

    def setUp(self):
        self.lexer = Lexer()

    def test_empty(self):
        self.lexer.input('')
        self.assertIs(self.lexer.token(), None)

    def test_command(self):
        self.lexer.input('ifelif')
        self.assertEqual(self.lexer.token(), Token(1, 'IF'))
        self.assertEqual(self.lexer.token(), Token(1, 'ELIF'))

    def test_value(self):
        self.lexer.input('4 -4.5 True')
        self.assertEqual(self.lexer.token(), Token(1, 'VALUE_INT', 4))
        self.assertEqual(self.lexer.token(), Token(1, 'VALUE_FLOAT', -4.5))
        self.assertEqual(self.lexer.token(), Token(1, 'VALUE_BOOL', True))

    def test_operator(self):
        self.lexer.input('-> - > = == <=')
        self.assertEqual(self.lexer.token(), Token(1, 'RETURN_TYPE'))
        self.assertEqual(self.lexer.token(), Token(1, 'MINUS'))
        self.assertEqual(self.lexer.token(), Token(1, 'ISMORE'))
        self.assertEqual(self.lexer.token(), Token(1, 'EQUALS'))
        self.assertEqual(self.lexer.token(), Token(1, 'ISEQUAL'))
        self.assertEqual(self.lexer.token(), Token(1, 'ISEQUALLESS'))

    def test_identifier(self):
        self.lexer.input('variable variable2 variable3')
        self.assertEqual(self.lexer.token(), Token(
            1, 'IDENTIFIER', 'variable'))
        self.assertEqual(self.lexer.token(), Token(
            1, 'IDENTIFIER', 'variable2'))
        self.assertEqual(self.lexer.token(), Token(
            1, 'IDENTIFIER', 'variable3'))

    def test_new_line(self):
        self.lexer.input('\n\n\t\n')
        self.assertEqual(self.lexer.token(), Token(2, 'NEWLINE'))
        self.assertEqual(self.lexer.token(), Token(3, 'INDENT'))
        self.assertEqual(self.lexer.token(), Token(4, 'DEDENT'))

    def test_undefined(self):
        self.lexer.input('x &')
        self.lexer.token()
        with self.assertRaises(LexerError):
            self.lexer.token()


if __name__ == '__main__':
    unittest.main()
