class CNFConverter:
    def __init__(self, grammar):
        self.grammar = grammar

    def eliminate_epsilon(self):
        epsilon_productions = {lhs for lhs, rhs in self.grammar.items() if "" in rhs}
        while epsilon_productions:
            for lhs in epsilon_productions:
                self.grammar[lhs].remove("")
                if not self.grammar[lhs]:
                    del self.grammar[lhs]
                for prod_lhs, prod_rhs in self.grammar.items():
                    self.grammar[prod_lhs] = [rhs.replace(lhs, "") for rhs in prod_rhs]
            epsilon_productions = {lhs for lhs, rhs in self.grammar.items() if "" in rhs}

    def eliminate_renaming(self):
        renaming_productions = {lhs for lhs, rhs in self.grammar.items() if len(rhs) == 1 and rhs[0] in self.grammar}
        for lhs in renaming_productions:
            rhs = self.grammar[lhs][0]
            self.grammar[lhs] = self.grammar[rhs]

    def eliminate_inaccessible(self):
        accessible = set()
        to_process = {'S'}  # Start symbol
        while to_process:
            symbol = to_process.pop()
            if symbol in accessible:
                continue
            accessible.add(symbol)
            for rhs in self.grammar.get(symbol, []):
                to_process.update(set(rhs))
        inaccessible = set(self.grammar.keys()) - accessible
        for symbol in inaccessible:
            del self.grammar[symbol]

    def eliminate_non_productive(self):
        productive = set()
        to_process = {lhs for lhs, rhs in self.grammar.items() if
                      all(sym in productive or sym in {'a', 'b'} for sym in rhs)}
        while to_process:
            symbol = to_process.pop()
            if symbol in productive:
                continue
            productive.add(symbol)
            for lhs, rhs_list in list(self.grammar.items()):
                for rhs in rhs_list:
                    if all(sym in productive or sym in {'a', 'b'} for sym in rhs):
                        continue
                    if symbol in rhs:
                        self.grammar[lhs].remove(rhs)
                        if not self.grammar[lhs]:
                            del self.grammar[lhs]
                        to_process.add(lhs)

        non_productive = set(self.grammar.keys()) - productive
        for symbol in non_productive:
            if symbol != 'S':
                del self.grammar[symbol]

        if 'S' not in productive:
            self.grammar = {'S': []}

    def to_chomsky_normal_form(self):
        self.eliminate_epsilon()
        self.eliminate_renaming()
        self.eliminate_inaccessible()
        self.eliminate_non_productive()

        cnf_grammar = {}
        for lhs, prods in self.grammar.items():
            cnf_prods = []
            for prod in prods:
                if not prod:
                    cnf_prods.append('ε')
                elif len(prod) == 1 and prod.isupper():
                    cnf_prods.append(prod)
                else:
                    cnf_prods.extend(prod)
            cnf_grammar[lhs] = cnf_prods

        cnf_prods = {key: value for key, value in cnf_grammar.items() if key in {'A', 'B', 'C', 'D'}}
        print("Grammar in Chomsky Normal form:")
        for lhs, prods in cnf_prods.items():
            print(f'{lhs} → {" | ".join(prods)}')

    def print_grammar(self, message):
        print(message)
        for key, value in self.grammar.items():
            if value:
                for prod in value:
                    print(f'{key} -> {prod}')
            else:
                print(f'{key} -> ε')
        print()

    def normalize_grammar(self):
        self.to_chomsky_normal_form()
        return self.grammar


# Grammar
grammar = {
    'S': ['AC', 'bA', 'B', 'aA'],
    'A': ['', 'aS', 'ABab'],
    'B': ['a', 'bS'],
    'C': ['abC'],
    'D': ['AB']
}

# Unit tests
import unittest


class TestCNFConverter(unittest.TestCase):
    def setUp(self):
        self.converter = CNFConverter(grammar)

    def test_eliminate_epsilon(self):
        print("\nBefore eliminating epsilon productions:")
        print(self.converter.grammar)
        self.converter.eliminate_epsilon()
        print("\nAfter eliminating epsilon productions:")
        print(self.converter.grammar)
        self.assertNotIn('', self.converter.grammar['A'])

    def test_eliminate_renaming(self):
        print("\nBefore eliminating renaming productions:")
        print(self.converter.grammar)
        self.converter.eliminate_renaming()
        print("\nAfter eliminating renaming productions:")
        print(self.converter.grammar)
        self.assertNotIn('A', self.converter.grammar)

    def test_eliminate_inaccessible(self):
        print("\nBefore eliminating inaccessible symbols:")
        print(self.converter.grammar)
        self.converter.eliminate_inaccessible()
        print("\nAfter eliminating inaccessible symbols:")
        print(self.converter.grammar)
        self.assertIn('C', self.converter.grammar)

    def test_eliminate_non_productive(self):
        print("\nBefore eliminating non-productive symbols:")
        print(self.converter.grammar)
        self.converter.eliminate_non_productive()
        print("\nAfter eliminating non-productive symbols:")
        print(self.converter.grammar)
        self.assertNotIn('B', self.converter.grammar['S'])

    def test_to_chomsky_normal_form(self):
        print("\nBefore converting to Chomsky Normal Form:")
        print(self.converter.grammar)
        self.converter.to_chomsky_normal_form()
        print("\nAfter converting to Chomsky Normal Form:")
        print(self.converter.grammar)
        self.assertTrue(all(len(prod) <= 2 for prods in self.converter.grammar.values() for prod in prods))


if __name__ == '__main__':
    unittest.main()
