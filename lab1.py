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
        return string

    def to_finite_automaton(self):
        from collections import defaultdict

        transitions = defaultdict(dict)
        for symbol in self.VN | self.VT:
            transitions[symbol] = {}

        for symbol in self.P:
            for production in self.P[symbol]:
                if len(production) == 1 and production[0] in self.VT:
                    transitions[symbol][production[0]] = production[0]
                elif len(production) == 2:
                    transitions[symbol][production[1]] = production[0]

        return FiniteAutomaton(transitions)

class FiniteAutomaton:
    def __init__(self, transitions):
        self.transitions = transitions

    def accepts(self, input_string):
        current_state = 'S'
        for symbol in input_string:
            if symbol not in self.transitions[current_state]:
                return False
            current_state = self.transitions[current_state][symbol]
        return True

    def is_deterministic(self):
        for state in self.transitions:
            symbols = set(self.transitions[state].keys())
            if len(symbols) != len(self.transitions[state]):
                return False
        return True

# Define the grammar and Create a grammar object
VN = {'S', 'A', 'B'}
VT = {'a', 'b', 'c'}
P = {
    'S': ['aS', 'bS', 'cA'],
    'A': ['aB'],
    'B': ['aB', 'bB', 'c']
}

grammar = Grammar(VN, VT, P)

# Generate 5 valid strings
valid_strings = grammar.generate_valid_strings(5)
print("5 Valid Strings:")
for string in valid_strings:
    print(string)

# Convert the grammar to a finite automaton
finite_automaton = grammar.to_finite_automaton()

# Check if an input string can be obtained via state transition
input_string = "abbc"
if finite_automaton.accepts(input_string):
    print(f"The string '{input_string}' can be obtained via state transition.")
else:
    print(f"The string '{input_string}' cannot be obtained via state transition.")

# Check if the Finite Automaton is deterministic or non-deterministic
if finite_automaton.is_deterministic():
    print("The Finite Automaton is deterministic.")
else:
    print("The Finite Automaton is non-deterministic.")
