
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
                new_production = ''
                for symbol in production:
                    if symbol in self.rules or symbol == '':
                        if new_production:
                            new_productions.append(new_production)
                            new_production = ''
                        new_productions.append(symbol)
                    else:
                        new_production += symbol
                if new_production:
                    new_productions.append(new_production)
            self.rules[non_terminal] = new_productions

        # Step 5: Modify productions to avoid infinite loops;
        if 'C' in self.rules:
            self.rules['C'] = ['aC', 'bC']

    def convertToCNF(self):
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
                        new_non_terminal = self.generateNewNonTerminal()
                        self.rules[new_non_terminal] = [first_two]
                        new_productions.append(new_non_terminal)
                    production = remaining
                new_productions.append(production)
            self.rules[non_terminal] = new_productions

    def generateNewNonTerminal(self):
        new_non_terminal = 'X'
        while new_non_terminal in self.rules:
            new_non_terminal += "'"
        return new_non_terminal

    def printRules(self):
        for f, t in self.rules.items():
            print(f + ' -> ' + ' | '.join(t))

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

