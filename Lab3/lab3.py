
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Invalid character")

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
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token("INTEGER", self.integer())
            if self.current_char == "+":
                self.advance()
                return Token("PLUS", "+")
            if self.current_char == "-":
                self.advance()
                return Token("MINUS", "-")
            if self.current_char == "*":
                self.advance()
                return Token("MULTIPLY", "*")
            if self.current_char == "/":
                self.advance()
                return Token("DIVIDE", "/")
            if self.current_char == "(":
                self.advance()
                return Token("LEFT_PAREN", "(")
            if self.current_char == ")":
                self.advance()
                return Token("RIGHT_PAREN", ")")
            self.error()
        return Token("EOF", None)


if __name__ == "__main__":
    text = "122 - 10 + 3"
    lexer = Lexer(text)
    token = lexer.get_next_token()
    while token.type != "EOF":
        print(token)
        token = lexer.get_next_token()
