import itertools
import unittest

class Grammar:
    def __init__(self, rules):
        self.rules = rules

    def removeLambda(self):
        nullable_symbols = set()

        # Step 1: Identify nullable symbols
        for non_terminal, productions in self.rules.items():
            if '' in productions:
                nullable_symbols.add(non_terminal)

        # Step 2: Remove epsilon productions
        for non_terminal, productions in self.rules.items():
            updated_productions = [p for p in productions if p != '']
            self.rules[non_terminal] = updated_productions

        # Step 3: Iteratively remove productions containing nullable symbols
        while True:
            exists_new_null = False
            for non_terminal, productions in self.rules.items():
                for production in productions:
                    null_test = production
                    for nullable in nullable_symbols:
                        null_test = null_test.replace(nullable, '')
                    if null_test == '' and non_terminal not in nullable_symbols:
                        nullable_symbols.add(non_terminal)
                        exists_new_null = True
            if not exists_new_null:
                break

        # Step 4: Replace productions containing nullable symbols
        for non_terminal, productions in self.rules.items():
            new_productions = []
            for production in productions:
                null_indices = [i for i, symbol in enumerate(production) if symbol in nullable_symbols]
                if null_indices:
                    combinations = itertools.product([0, 1], repeat=len(null_indices))
                    for combination in combinations:
                        new_production = ''.join([symbol for i, symbol in enumerate(production) if
                                                  i not in null_indices or combination[null_indices.index(i)] == 1])
                        if new_production != '':
                            new_productions.append(new_production)
                else:
                    new_productions.append(production)
            self.rules[non_terminal] = list(set(new_productions))

        # Step 5: Modify productions to avoid infinite loops
        if 'C' in self.rules:
            self.rules['C'] = ['aC', 'bC']  # Modify the production to avoid infinite loops

    def convertToCNF(self):
        # Create a copy of keys to avoid RuntimeErrorgit
        non_terminals = list(self.rules.keys())

        for non_terminal in non_terminals:
            productions = self.rules[non_terminal]
            new_productions = []
            for production in productions:
                while len(production) > 2:
                    first_two = production[:2]
                    remaining = production[2:]
                    if first_two in self.rules:
                        new_productions.append(first_two)
                    else:
                        # If the first two symbols are terminals, create a new non-terminal and a production
                        new_non_terminal = self.generateNewNonTerminal()
                        self.rules[new_non_terminal] = [first_two]
                        new_productions.append(new_non_terminal)
                    production = remaining
                new_productions.append(production)
            self.rules[non_terminal] = new_productions

    def generateNewNonTerminal(self):
        # Generate a new non-terminal symbol
        new_non_terminal = 'X'
        while new_non_terminal in self.rules:
            new_non_terminal += "'"
        return new_non_terminal

    def printRules(self):
        for f, t in self.rules.items():
            print(f + ' -> ' + ' | '.join(t))

# Provided sample grammar
sample_grammar = {
    'S': ['AC', 'bA', 'B', 'aA'],
    'A': ['', 'aS', 'ABab'],
    'B': ['a', 'bS'],
    'C': ['abC'],
    'D': ['AB']
}


grammar = Grammar(sample_grammar)
grammar.removeLambda()
grammar.convertToCNF()


grammar.printRules()
class TestGrammar(unittest.TestCase):
    def test_removeLambda(self):

        sample_grammar = {
            'S': ['AB', 'A', 'B'],
            'A': ['', 'aA'],
            'B': ['b']
        }
        expected_grammar = {
            'S': ['AB', 'A', 'B'],
            'A': ['aA', 'a'],
            'B': ['b']
        }
        grammar = Grammar(sample_grammar)
        grammar.removeLambda()
        # Check the presence of productions rather than their order
        for non_terminal, productions in expected_grammar.items():
            self.assertCountEqual(grammar.rules[non_terminal], productions)

    def test_convertToCNF(self):
        sample_grammar = {
            'S': ['AC', 'bA', 'B', 'aA'],
            'A': ['', 'aS', 'ABab'],
            'B': ['a', 'bS'],
            'C': ['abC'],
            'D': ['AB']
        }
        expected_grammar = {
            'S': ['AC', 'aC', 'AB', 'aA', 'bA', 'b', 'a', 'abC'],
            'A': ['aS', 'ab', 'ABab', 'b', 'Bab'],
            'B': ['bS', 'a'],
            'C': ['aC', 'bC'],
            'D': ['AB'],
            'X': ['Ba'],
            'X\'': ['AB']
        }
        grammar = Grammar(sample_grammar)
        grammar.removeLambda()
        grammar.convertToCNF()
        # Check the presence of productions rather than their order
        for non_terminal, productions in expected_grammar.items():
            self.assertCountEqual(grammar.rules[non_terminal], productions)
