class Grammar:
    def __init__(self, VN, VT, P):
        self.VN = VN
        self.VT = VT
        self.P = P

    def generate_valid_strings(self, n=5):
        valid_strings = []
        for _ in range(n):
            valid_strings.append(self.generate_string('S'))
        return valid_strings

    def generate_string(self, symbol):
        import random

        if symbol not in self.P:
            return symbol

        productions = self.P[symbol]
        production = random.choice(productions)
        string = ''
        for s in production:
            if s in self.VT:
                string += s
            else:
                string += self.generate_string(s)
        return string    def __init__(self, VN, VT, P):
        self.VN = VN
        self.VT = VT
        self.P = P
    def generate_valid_strings(self, n=5):
        valid_strings = []
        for _ in range(n):
            valid_strings.append(self.generate_string('S'))
        return valid_strings
