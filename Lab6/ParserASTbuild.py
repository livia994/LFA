import re

# Define token types using regular expressions
INTEGER = re.compile(r'\d+')
PLUS = re.compile(r'\+')
MINUS = re.compile(r'\-')
MULTIPLY = re.compile(r'\*')
DIVIDE = re.compile(r'\/')
LPAREN = re.compile(r'\(')
RPAREN = re.compile(r'\)')

# Tokenize input text
def tokenize(text):
    tokens = []
    patterns = [(name, pattern) for name, pattern in globals().items() if isinstance(pattern, re.Pattern)]

    while text:
        match = None
        for name, pattern in patterns:
            match = pattern.match(text)
            if match:
                token = (name, match.group(0))
                tokens.append(token)
                text = text[len(match.group(0)):]
                break
        if not match:
            if text[0].isspace():
                text = text[1:]  # Skip whitespace
            else:
                raise ValueError('Invalid input at: ' + text)

    return tokens

# Define AST nodes
class ASTNode:
    pass

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class NumNode(ASTNode):
    def __init__(self, value):
        self.value = value

# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = -1
        self.advance()

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None

    def parse(self):
        return self.expr()

    def expr(self):
        result = self.term()  # Start by parsing a term or factor

        while self.current_token and self.current_token[0] in (PLUS, MINUS):
            op = self.current_token
            self.advance()  # Advance past the operator
            right = self.term()  # Now parse the term or factor after the operator
            result = BinOpNode(result, op, right)

        return result

    def term(self):
        result = self.factor()  # Start by parsing a factor

        while self.current_token and self.current_token[0] in (MULTIPLY, DIVIDE):
            op = self.current_token
            self.advance()  # Advance past the operator
            right = self.factor()  # Now parse the factor after the operator
            result = BinOpNode(result, op, right)

        return result

    def factor(self):
        token = self.current_token
        print(f"Current token: {token}")

        if token[0] == 'INTEGER':
            value = int(token[1])  # Convert the token value to an integer
            self.advance()
            return NumNode(value)
        elif token[0] == 'LPAREN':
            self.advance()
            result = self.expr()  # Parse the expression within parentheses
            if self.current_token[0] != 'RPAREN':
                raise ValueError('Expected RPAREN')
            self.advance()
            return result
        elif token[0] == 'MINUS':  # Check for negative number
            self.advance()  # Advance past minus sign
            result = self.factor()  # Parse the factor after the minus sign
            return BinOpNode(NumNode('0'), MINUS, result)  # Negate the parsed factor
        else:
            raise ValueError('Invalid factor')


def print_ast(node, indent=""):
    if isinstance(node, BinOpNode):
        print(f"{indent}{node.op[1]}")
        print_ast(node.left, indent + "  ")
        print_ast(node.right, indent + "  ")
    elif isinstance(node, NumNode):
        print(f"{indent}{node.value}")

def main():
    text = "3 + 4 * (2 - 1)"
    tokens = tokenize(text)
    print("Tokens:", tokens)

    parser = Parser(tokens)
    ast = parser.parse()

    # Print AST using the helper function
    print("AST:")
    print_ast(ast)

if __name__ == "__main__":
    main()
