import unittest

from transpiler.lexer import *
from transpiler.parser import *
from transpiler.codegen import *


class CodeGenTesting(unittest.TestCase):

    def setUp(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.codegen = CodeGen()

    def test_empty(self):
        with open('tests/testfiles/empty.py') as f:
            self.lexer.input(f.read())
        with open('tests/testfiles/empty.cpp') as f:
            self.assertEqual(f.read(), self.codegen.generate(
                *self.parser.parse(self.lexer.tokens())))

    def test_if_elif_else(self):
        with open('tests/testfiles/if_elif_else.py') as f:
            self.lexer.input(f.read())
        with open('tests/testfiles/if_elif_else.cpp') as f:
            self.assertEqual(f.read(), self.codegen.generate(
                *self.parser.parse(self.lexer.tokens())))

    def test_assignment(self):
        with open('tests/testfiles/assignment.py') as f:
            self.lexer.input(f.read())
        with open('tests/testfiles/assignment.cpp') as f:
            self.assertEqual(f.read(), self.codegen.generate(
                *self.parser.parse(self.lexer.tokens())))

    def test_function(self):
        with open('tests/testfiles/function.py') as f:
            self.lexer.input(f.read())
        with open('tests/testfiles/function.cpp') as f:
            self.assertEqual(f.read(), self.codegen.generate(
                *self.parser.parse(self.lexer.tokens())))

    def test_function_assignment(self):
        with open('tests/testfiles/function_assignment.py') as f:
            self.lexer.input(f.read())
        with open('tests/testfiles/function_assignment.cpp') as f:
            self.assertEqual(f.read(), self.codegen.generate(
                *self.parser.parse(self.lexer.tokens())))

    def test_indents(self):
        with open('tests/testfiles/indents.py') as f:
            self.lexer.input(f.read())
        with open('tests/testfiles/indents.cpp') as f:
            self.assertEqual(f.read(), self.codegen.generate(
                *self.parser.parse(self.lexer.tokens())))

    def test_operators(self):
        with open('tests/testfiles/operators.py') as f:
            self.lexer.input(f.read())
        with open('tests/testfiles/operators.cpp') as f:
            self.assertEqual(f.read(), self.codegen.generate(
                *self.parser.parse(self.lexer.tokens())))

    def test_print(self):
        with open('tests/testfiles/print.py') as f:
            self.lexer.input(f.read())
        with open('tests/testfiles/print.cpp') as f:
            self.assertEqual(f.read(), self.codegen.generate(
                *self.parser.parse(self.lexer.tokens())))

    def test_variables(self):
        with open('tests/testfiles/variables.py') as f:
            self.lexer.input(f.read())
        with open('tests/testfiles/variables.cpp') as f:
            self.assertEqual(f.read(), self.codegen.generate(
                *self.parser.parse(self.lexer.tokens())))

    def test_while(self):
        with open('tests/testfiles/while.py') as f:
            self.lexer.input(f.read())
        with open('tests/testfiles/while.cpp') as f:
            self.assertEqual(f.read(), self.codegen.generate(
                *self.parser.parse(self.lexer.tokens())))

    def test_complex1(self):
        with open('tests/testfiles/complex1.py') as f:
            self.lexer.input(f.read())
        with open('tests/testfiles/complex1.cpp') as f:
            self.assertEqual(f.read(), self.codegen.generate(
                *self.parser.parse(self.lexer.tokens())))

    def test_complex2(self):
        with open('tests/testfiles/complex2.py') as f:
            self.lexer.input(f.read())
        with open('tests/testfiles/complex2.cpp') as f:
            self.assertEqual(f.read(), self.codegen.generate(
                *self.parser.parse(self.lexer.tokens())))

    def test_complex3(self):
        with open('tests/testfiles/complex3.py') as f:
            self.lexer.input(f.read())
        with open('tests/testfiles/complex3.cpp') as f:
            self.assertEqual(f.read(), self.codegen.generate(
                *self.parser.parse(self.lexer.tokens())))


if __name__ == '__main__':
    unittest.main()
