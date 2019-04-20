from token_types import *


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    RESERVED_KEYWORDS = {
        'PROGRAM': Token(PROGRAM, 'PROGRAM'),
        'VAR': Token(VAR, 'VAR'),
        'DIV': Token(INTEGER_DIV, 'DIV'),
        'INTEGER': Token(INTEGER, 'INTEGER'),
        'REAL': Token(REAL, 'REAL'),
        'STRING': Token(STRING, 'STRING'),
        'BEGIN': Token(BEGIN, 'BEGIN'),
        'END': Token(END, 'END'),
        'PROCEDURE': Token(PROCEDURE, 'PROCEDURE'),
        'FUNCTION': Token(FUNCTION, 'FUNCTION'),
        'IF': Token(IF, 'IF'),
        'THEN': Token(THEN, 'THEN'),
        'ELSE': Token(ELSE, 'ELSE'),
        'WHILE': Token(WHILE, 'WHILE'),
        'DO': Token(DO, 'DO'),
        'FOR': Token(FOR, 'FOR'),
        'TO': Token(TO, 'TO')
    }

    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.is_declaration = False

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != '}':
            self.advance()
        self.advance()  # the closing curly brace

    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while (
                self.current_char is not None and
                self.current_char.isdigit()
            ):
                result += self.current_char
                self.advance()

            token = Token(REAL_CONST, float(result))
        else:
            token = Token(INTEGER_CONST, int(result))

        return token

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        if self.current_char == '(' and self.is_declaration is False:
            self.advance()
            token = self.RESERVED_KEYWORDS.get(
                result.upper(), Token(CALL, result))
        else:
            token = self.RESERVED_KEYWORDS.get(
                result.upper(), Token(ID, result))
            self.is_declaration = False
        if token.type in (PROCEDURE, FUNCTION):
            self.is_declaration = True
        return token

    def _string(self):
        self.advance()
        result = ''
        while self.current_char is not None and self.current_char != '\'':
            result += self.current_char
            self.advance()
        self.advance()
        token = Token(STRING_CONST, result)
        return token

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '\'':
                return self._string()

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(FLOAT_DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')

            if self.current_char == '<':
                self.advance()
                return Token(LESS_THAN, '<')

            if self.current_char == '>':
                self.advance()
                return Token(GREATER_THAN, '>')

            if self.current_char == '=':
                self.advance()
                return Token(EQUAL, '=')

            self.error()

        return Token(EOF, None)
