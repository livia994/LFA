import re

# Define TokenType enum
class TokenType:
    INTEGER = 'INTEGER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'

# Define Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

# Define Lexer class
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())
            elif self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')
            elif self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')
            elif self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*')
            elif self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')
            elif self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')
            elif self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')
            else:
                self.error()
        return Token(None, None)

# Define AST nodes
class BinOp:
    def __init__(self, left, op, right=None):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f'({self.left} {self.op} {self.right})'

# Define Parser class
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == TokenType.INTEGER:
            value = token.value
            self.eat(TokenType.INTEGER)
            return value
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = self.expr()
            self.eat(TokenType.RPAREN)
            return result
        elif token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            return self.factor()
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return BinOp(0, '-', self.factor())
        else:
            self.error()

    def term(self):
        result = self.factor()
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
                result = BinOp('*', result, self.factor())
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
                result = BinOp('/', result, self.factor())
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result = BinOp(result, '+', self.term())
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result = BinOp(result, '-', self.term())
        return result

    def parse(self):
        result = self.expr()  # Start parsing expressions directly
        if self.current_token.type is not None:
            self.error()
        return result

# Main function
# Main function
def main():
    text = "(34 + 16) / 4"
    lexer = Lexer(text)

    # Print tokens
    tokens = []
    while True:
        token = lexer.get_next_token()
        if token.type is None:
            break
        tokens.append((token.type, token.value))
    print("Tokens:", tokens)

    parser = Parser(Lexer(text))
    ast = parser.parse()
    print(ast)


if __name__ == '__main__':
    main()

