import re
import sys


class Token:
    """ Token containing position in file,
        type and value of token if needed
    """

    def __init__(self, pos, type, value=None):
        self.pos = pos
        self.type = type
        self.value = value

    def __str__(self):
        return f'pos={self.pos}, type={self.type}, value={self.value}'


class LexerError(Exception):
    """ Contains position in buffer and line of unrecognized token
    """

    def __init__(self, line, pos):
        self.line = line
        self.pos = pos


class Lexer:
    def __init__(self):
        tokens = [
            (r'def', 'DEF'),
            (r'if', 'IF'),
            (r'elif', 'ELIF'),
            (r'else', 'ELSE'),
            (r'while', 'WHILE'),
            (r'None', 'NONE'),
            (r'int', 'INT'),
            (r'float', 'FLOAT'),
            (r'bool', 'BOOL'),
            (r'return', 'RETURN'),
            (r'print', 'PRINT'),
            (r':', 'COLON'),
            (r',', 'COMMA'),
            (r'->', 'RETURN_TYPE'),
            (r'\+', 'PLUS'),
            (r'-', 'MINUS'),
            (r'\*', 'MULTIPLY'),
            (r'\/', 'DIVIDE'),
            (r'\(', 'LP'),
            (r'\)', 'RP'),
            (r'%', 'MODULO'),
            (r'==', 'ISEQUAL'),
            (r'!=', 'ISNOTEQUAL'),
            (r'<=', 'ISEQUALLESS'),
            (r'<', 'ISLESS'),
            (r'>=', 'ISEQUALLESS'),
            (r'>', 'ISMORE'),
            (r'=', 'EQUALS'),
            (r'and', 'AND'),
            (r'or', 'OR'),
            (r'not', 'NOT'),
            (r'\d+\.\d+', 'VALUE_FLOAT'),
            (r'\d+', 'VALUE_INT'),
            (r'True|False', 'VALUE_BOOL'),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER')
        ]
        self.buffer = None
        self.patterns = []
        for pattern, type in tokens:
            self.patterns.append((re.compile(pattern), type))
        self.whitespace = re.compile(r'\s+')
        self.newline = re.compile(r'\n\t*')

    def input(self, buffer):
        """ Initialize buffer as lexer input
        """
        self.buffer = buffer
        self.pos = 0
        self.line = 1
        self.indend = 0

    def token(self):
        """ Return next token in the buffer. If no matching token is found,
            LexerError is raised. Returns None if end of buffer is reached.
        """
        if self.buffer is None or self.pos >= len(self.buffer):
            return None
        newline = self.newline.match(self.buffer, self.pos)
        if newline:
            self.line += 1
            self.pos = newline.end()
            prev_indend = self.indend
            self.indend = newline.end() - newline.start() - 1
            if self.indend < prev_indend:
                return Token(self.pos, 'DEDEND')
            elif self.indend > prev_indend:
                return Token(self.pos, 'INDEND')
            else:
                return Token(self.pos, 'NEWLINE')
        whitespace = self.whitespace.match(self.buffer, self.pos)
        if whitespace:
            self.pos = whitespace.end()
            if self.pos >= len(self.buffer):
                return None
        for pattern, type in self.patterns:
            matched = pattern.match(self.buffer, self.pos)
            if matched:
                self.pos = matched.end()
                if type == 'VALUE_INT':
                    return Token(self.pos, type, int(matched.group(0)))
                if type == 'VALUE_FLOAT':
                    return Token(self.pos, type, float(matched.group(0)))
                if type == 'VALUE_BOOL':
                    return Token(self.pos, type, matched.group(0) == 'True')
                return Token(self.pos, type)
        raise LexerError(self.line, self.pos)

    def tokens(self):
        """ Returs iterator to tokens in the input buffer
        """
        token = self.token()
        while token is not None:
            yield token
            token = self.token()


if __name__ == '__main__':
    lexer = Lexer()
    with open(sys.argv[1]) as f:
        data = f.read()
    lexer.input(data)
    try:
        for token in lexer.tokens():
            print(token)
    except LexerError as le:
        print(f'lexical error: line {le.line}, position {le.pos}')
