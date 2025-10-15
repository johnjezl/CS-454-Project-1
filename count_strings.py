from Delta import Delta
from build_states import failed_state


"""
Input:
    dfa - the dfa that accepts pairs of strings having all letters of alphabet in each substring of length 6
    n - the length to count valid strings for
Output:
    the number of strings of length n accepted by dfa
Example:
    input - countValidStrings(dfa, 1)
    output - 4      (because alphabet has 4 letters)
Preconditions:
    n >= 0
    dfa must contain all states and accepting states and delta function
"""
def countValidStrings(dfa, n):
    states = dfa.get_states()
    alphabet = dfa.get_alphabet()
    num_states = len(states)
    num_symbols = len(alphabet)

    # Create state-to-index mapping
    max_state = max(s for s in states if s != failed_state)
    state_to_index = [-1] * (max_state + 1)

    for idx, state in enumerate(states):
        if state != failed_state:
            state_to_index[state] = idx

    # Build transition matrix as list of lists
    # transitions[from_idx][symbol_idx] = to_idx (-1 for failed)
    transitions = [[-1] * num_symbols for _ in range(num_states)]

    for from_idx, from_state in enumerate(states):
        if from_state == failed_state:
            continue

        for sym_idx, symbol in enumerate(alphabet):
            next_state = dfa.transition(from_state, symbol)
            if next_state != failed_state and next_state < len(state_to_index):
                next_idx = state_to_index[next_state]
                if next_idx != -1:
                    transitions[from_idx][sym_idx] = next_idx

    # Initialize with accepting states
    accept_set = set(dfa.get_accept_states())
    prev = [0] * num_states
    for idx, state in enumerate(states):
        if state in accept_set:
            prev[idx] = 1

    for _ in range(n):
        next_counts = [0] * num_states

        for from_idx in range(num_states):
            if states[from_idx] == failed_state:
                continue

            for sym_idx in range(num_symbols):
                to_idx = transitions[from_idx][sym_idx]
                if to_idx != -1:
                    next_counts[from_idx] += prev[to_idx]

        prev = next_counts

    # Return count from start state
    start_idx = state_to_index[dfa.start_state]
    return int(prev[start_idx])



"""
Input:
    dfa - the DFA that accepts strings having all letters of alphabet in each substring of length 6
    n - the length to count valid strings for
Output:
    the number of strings of even length n accepted with aa in the middle
    and having all letters of alphabet in each substring of length 6
Example:
    input - countAASplitStrings(dfa, 2) with alphabet of 4
    output - 1
Preconditions:
    n >= 0
    dfa must contain all states and accepting states and have a transition function
"""
def countAASplitStrings(dfa, n):
    if n % 2 != 0:
        return 0

    half_len = n // 2 - 1
    if half_len < 0:
        return 0

    states = dfa.get_states()
    alphabet = dfa.get_alphabet()
    num_states = len(states)

    # Build state index mapping
    max_state = max(s for s in states if s != failed_state)
    state_to_index = [-1] * (max_state + 1)
    for idx, state in enumerate(states):
        if state != failed_state:
            state_to_index[state] = idx

    # Build forward and backward transition 
    forward_trans = [[] for _ in range(num_states)]
    backward_trans = [[] for _ in range(num_states)]

    for from_idx, from_state in enumerate(states):
        if from_state == failed_state:
            continue
        for symbol in alphabet:
            next_state = dfa.transition(from_state, symbol)
            if next_state != failed_state and next_state < len(state_to_index):
                next_idx = state_to_index[next_state]
                if next_idx != -1:
                    forward_trans[from_idx].append(next_idx)
                    backward_trans[next_idx].append(from_idx)

    left_counts = {}
    left_counts[state_to_index[0]] = 1

    for _ in range(half_len):
        next_left = {}
        for from_idx, count in left_counts.items():
            for to_idx in forward_trans[from_idx]:
                next_left[to_idx] = next_left.get(to_idx, 0) + count
        left_counts = next_left

    accept_set = set(dfa.get_accept_states())
    right_counts = {}

    for idx, state in enumerate(states):
        if state in accept_set:
            right_counts[idx] = 1

    for _ in range(half_len):
        next_right = {}
        for to_idx, count in right_counts.items():
            for from_idx in backward_trans[to_idx]:
                next_right[from_idx] = next_right.get(from_idx, 0) + count
        right_counts = next_right

    # Combine... for each state p with left paths, check "aa" transition to q
    total = 0
    for p_idx, left_count in left_counts.items():
        p_state = states[p_idx]

        p_a = dfa.transition(p_state, 'a')
        if p_a == failed_state:
            continue

        q = dfa.transition(p_a, 'a')
        if q == failed_state:
            continue

        q_idx = state_to_index[q]
        if q_idx in right_counts:
            total += left_count * right_counts[q_idx]

    return int(total)
