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
def is_deterministic(Q, Sigma, delta):
    for q in Q:
        for symbol in Sigma:
            transitions = [state for state, s in delta.items() if s == (q, symbol)]
            if len(transitions) > 1:
                return False
    return True

is_det = is_deterministic(Q, Sigma, delta)
print("The FA is Deterministic." if is_det else "The FA is Non-Deterministic.")

def powerset(states):
    result = []
    for i in range(1 << len(states)):
        subset = [states[j] for j in range(len(states)) if (i & (1 << j)) > 0]
        result.append(subset)
    return result

def epsilon_closure(state, delta):
    closure = set()
    stack = list(state)  # Convert the set to a list to iterate over its elements
    while stack:
        current_state = stack.pop()
        closure.add(current_state)  # Add the current state to the closure
        for (s, t) in delta:
            if s == current_state and t == '':
                next_state = delta[(s, t)]
                if next_state not in closure:
                    stack.append(next_state)  # Add the next state to the stack for processing
    return frozenset(closure)  # Convert the closure set to a frozenset for immutability and hashability


def move(states, symbol, delta):
    result = set()
    for state in states:
        if (state, symbol) in delta:
            result.add(delta[(state, symbol)])
    return frozenset(result)

def ndfa_to_dfa(Q, Sigma, delta, q0, F):
    dfa_states = []
    dfa_delta = {}
    q0_closure = epsilon_closure({q0}, delta)  # Ensure q0_closure is initialized properly
    worklist = [q0_closure]
    dfa_states.append(q0_closure)

    while worklist:
        current_state = worklist.pop(0)
        for symbol in Sigma:
            next_state = epsilon_closure(move(current_state, symbol, delta), delta)
            if next_state not in dfa_states:
                dfa_states.append(next_state)
                worklist.append(next_state)
            dfa_delta[(current_state, symbol)] = next_state

    dfa_final_states = [s for s in dfa_states if any(q in F for q in s)]
    return dfa_states, dfa_delta, dfa_final_states

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
q0 = 'q0'

dfa_states, dfa_delta, dfa_final_states = ndfa_to_dfa(Q, Sigma, delta, q0, F)
print("DFA States:", dfa_states)
print("DFA Delta:", dfa_delta)
print("DFA Final States:", dfa_final_states)

import matplotlib.pyplot as plt
import networkx as nx

def draw_finite_automaton(states, delta, final_states):
    G = nx.DiGraph()

    # Add nodes for states
    for state in states:
        G.add_node(str(state))

    # Add edges for transitions
    for (current_state, symbol), next_state in delta.items():
        G.add_edge(str(current_state), str(next_state), label=symbol)

    # Highlight final states
    final_node_colors = ['green' if state in final_states else 'white' for state in G.nodes()]
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=final_node_colors, node_size=1500, font_size=12)

    # Add labels for transitions
    edge_labels = {(str(current_state), str(next_state)): symbol for (current_state, symbol), next_state in delta.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.show()

# Example DFA states, delta, and final states
dfa_states = [frozenset({'q0'}), frozenset({'q1'}), frozenset(), frozenset({'q2'}), frozenset({'q3'})]
dfa_delta = {
    (frozenset({'q0'}), 'a'): frozenset({'q1'}),
    (frozenset({'q0'}), 'b'): frozenset(),
    (frozenset({'q0'}), 'c'): frozenset(),
    (frozenset({'q1'}), 'a'): frozenset(),
    (frozenset({'q1'}), 'b'): frozenset({'q2'}),
    (frozenset({'q1'}), 'c'): frozenset(),
    (frozenset(), 'a'): frozenset(),
    (frozenset(), 'b'): frozenset(),
    (frozenset(), 'c'): frozenset(),
    (frozenset({'q2'}), 'a'): frozenset({'q2'}),
    (frozenset({'q2'}), 'b'): frozenset({'q3'}),
    (frozenset({'q2'}), 'c'): frozenset({'q0'}),
    (frozenset({'q3'}), 'a'): frozenset(),
    (frozenset({'q3'}), 'b'): frozenset(),
    (frozenset({'q3'}), 'c'): frozenset()
}
dfa_final_states = [frozenset({'q3'})]

draw_finite_automaton(dfa_states, dfa_delta, dfa_final_states)

