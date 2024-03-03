def fa_to_rg(Q, Sigma, delta, F):
    grammar = {}
    for q in Q:
        grammar[q] = []
        for symbol in Sigma:
            transitions = [state for state, s in delta.items() if s == (q, symbol)]
            if transitions:
                if len(transitions) == 1:
                    grammar[q].append(symbol + transitions[0])
                else:
                    for t in transitions:
                        grammar[q].append(symbol + t)
        if q in F:
            grammar[q].append('')
    return grammar

Q = {'q0', 'q1', 'q2', 'q3'}
Sigma = {'a', 'b', 'c'}
F = {'q3'}
delta = {
    ('q0', 'a'): 'q0',
    ('q1', 'b'): 'q2',
    ('q0', 'a'): 'q1',
    ('q2', 'a'): 'q2',
    ('q2', 'b'): 'q3',
    ('q2', 'c'): 'q0'
}

regular_grammar = fa_to_rg(Q, Sigma, delta, F)
for state, productions in regular_grammar.items():
    print(state + " -> " + " | ".join(productions))
