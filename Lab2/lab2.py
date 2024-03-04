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

def powerset(states):
    result = []
    for i in range(1 << len(states)):
        subset = [states[j] for j in range(len(states)) if (i & (1 << j)) > 0]
        result.append(subset)
    return result

def epsilon_closure(state, delta):
    closure = set()
    stack = list(state)
    while stack:
        current_state = stack.pop()
        closure.add(current_state)
        for (s, t) in delta:
            if s == current_state and t == '':
                next_state = delta[(s, t)]
                if next_state not in closure:
                    stack.append(next_state)
    return tuple(sorted(closure))

def move(states, symbol, delta):
    result = set()
    for state in states:
        if (state, symbol) in delta:
            result.add(delta[(state, symbol)])
    return tuple(sorted(result))


def ndfa_to_dfa(Q, Sigma, delta, q0, F):
    dfa_states = []
    dfa_delta = {}
    q0_closure = epsilon_closure({q0}, delta)
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

    # Convert the resulting states from sets to strings
    dfa_states = [','.join(sorted(state)) for state in dfa_states]
    dfa_final_states = [state for state in dfa_states if any(q in F for q in state.split(','))]

    # Convert the transition states from sets to strings
    dfa_delta = {(','.join(sorted(current_state)), symbol): ','.join(sorted(next_state))
                 for (current_state, symbol), next_state in dfa_delta.items()}

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

print("DFA Transitions:")
for (current_state, symbol), next_state in dfa_delta.items():
    current_state_str = ', '.join(current_state) if current_state else '∅'
    next_state_str = ', '.join(next_state) if next_state else '∅'
    print(f"({current_state_str}) --({symbol})--> ({next_state_str})")

print("\nDFA States:")
for state in dfa_states:
    print(state)

print("\nDFA Delta:")
for (current_state, symbol), next_state in dfa_delta.items():
    current_state_str = ', '.join(current_state) if current_state else '∅'
    next_state_str = ', '.join(next_state) if next_state else '∅'
    print(f"({current_state_str}) -> ({next_state_str}) with symbol {symbol}")

print("\nDFA Final States:", dfa_final_states)

def is_deterministic(Q, Sigma, delta):
    for q in Q:
        for symbol in Sigma:
            transitions = [state for state, s in delta.items() if s == (q, symbol)]
            if len(transitions) > 1:  # If there are multiple transitions for a state and symbol pair
                return False  # It's an NFA
    return True  # It's a DFA

is_det = is_deterministic(Q, Sigma, delta)
print("The FA is Deterministic." if is_det else "The FA is Non-Deterministic.")
