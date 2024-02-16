Ministerul Educaţiei și Cercetării al Republicii Moldova Universitatea Tehnică a Moldovei
Facultatea Calculatoare, Informatică și Microelectronică








Laboratory work 1:
Regular Grammars &
Finite Automata
                    Variant 15




Elaborated:
st. gr. FAF-221	Gîncu Olivia

Verified:
asist. Univ                                                  Crețu Dumitru





Topic: Intro to formal languages. Regular grammars. Finite Automata.
Task: Discover what a language is and what it needs to have in order to be considered a formal one;

Provide the initial setup for the evolving project that you will work on during this semester. You can deal with each laboratory work as a separate task or project to demonstrate your understanding of the given themes, but you also can deal with labs as stages of making your own big solution, your own project. Do the following:

a. Create GitHub repository to deal with storing and updating your project;

b. Choose a programming language. Pick one that will be easiest for dealing with your tasks, you need to learn how to solve the problem itself, not everything around the problem (like setting up the project, launching it correctly and etc.);

c. Store reports separately in a way to make verification of your work simpler (duh)

According to your variant number, get the grammar definition and do the following:

a. Implement a type/class for your grammar;

b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;

c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;

d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;

Problem condition
Variant 15:

VN={S, A, B},
VT={a, b, c},
P={
    S → aS
    S → bS
    S → cA
    A → aB
    B → aB
    B → bB
    B → c
}

Git repository link: https://github.com/livia994/LFA

Code with Comments:

# Define the Grammar class
class Grammar:
    # Constructor method
    def __init__(self, VN, VT, P):
        self.VN = VN  # Set of non-terminal symbols
        self.VT = VT  # Set of terminal symbols
        self.P = P    # Set of production rules

    # Method to generate valid strings from the grammar
    def generate_valid_strings(self, n=5):
        valid_strings = []
        # Generate n valid strings
        for _ in range(n):
            # Start with symbol 'S' and generate a string
            valid_strings.append(self.generate_string('S'))
        return valid_strings

    # Recursive method to generate a string based on a symbol
    def generate_string(self, symbol):
        import random

        # If the symbol is not in the production rules, return the symbol itself
        if symbol not in self.P:
            return symbol

        productions = self.P[symbol]  # Possible productions for the symbol
        production = random.choice(productions)  # Choose a random production
        string = ''
        # Iterate over each symbol in the production
        for s in production:
            # If the symbol is a terminal symbol, add it to the string
            if s in self.VT:
                string += s
            # If the symbol is a non-terminal symbol, recursively generate a string for it
            else:
                string += self.generate_string(s)
        return string

    # Method to convert the grammar to a finite automaton
    def to_finite_automaton(self):
        from collections import defaultdict

        transitions = defaultdict(dict)
        # Initialize transitions dictionary for each symbol
        for symbol in self.VN | self.VT:
            transitions[symbol] = {}

        # Construct transitions based on production rules
        for symbol in self.P:
            for production in self.P[symbol]:
                if len(production) == 1 and production[0] in self.VT:
                    transitions[symbol][production[0]] = production[0]
                elif len(production) == 2:
                    transitions[symbol][production[1]] = production[0]

        return FiniteAutomaton(transitions)

# Define the FiniteAutomaton class
class FiniteAutomaton:
    # Constructor method
    def __init__(self, transitions):
        self.transitions = transitions

    # Method to check if an input string can be obtained via state transition
    def accepts(self, input_string):
        current_state = 'S'  # Start with initial state 'S'
        # Iterate over each symbol in the input string
        for symbol in input_string:
            # If the current state does not have a transition for the symbol, return False
            if symbol not in self.transitions[current_state]:
                return False
            # Update current state based on the transition for the symbol
            current_state = self.transitions[current_state][symbol]
        return True  # If the input string is successfully processed, return True

# Define the grammar and Create a grammar object
VN = {'S', 'A', 'B'}  # Set of non-terminal symbols
VT = {'a', 'b', 'c'}  # Set of terminal symbols
P = {  # Production rules
    'S': ['aS', 'bS', 'cA'],
    'A': ['aB'],
    'B': ['aB', 'bB', 'c']
}

grammar = Grammar(VN, VT, P)  # Create the grammar object

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


Overview:

This code defines a context-free grammar (CFG) using a Grammar class, which consists of non-terminal symbols (VN), terminal symbols (VT), and production rules (P). The grammar is capable of generating valid strings following the rules defined by the grammar. The `generate_valid_strings` method of the Grammar class generates a specified number of valid strings based on the production rules, recursively applying the rules until terminal symbols are reached. Additionally, the code converts the grammar into a finite automaton (FA) representation using the `to_finite_automaton` method. This FA is capable of accepting or rejecting input strings based on whether the strings can be derived from the initial state following transitions defined by the grammar. Finally, the code demonstrates the functionality by generating valid strings and testing whether a given input string can be obtained via state transitions in the corresponding finite automaton.


 Conclusion:

In this laboratory work, I have explored the concepts of regular grammars and finite automata, fundamental in the field of theoretical computer science. Additionally, the code highlights the practical application of these concepts in programming tasks such as string generation and language recognition. By implementing and utilizing CFGs and FAs, I learned about an essential aspect of computational theory and its practical implications in software development and language processing. Overall, this laboratory work provided a hands-on opportunity to engage with abstract concepts and develop proficiency in formal language theory.
g
