from Delta import Delta
from build_states import failed_state


class DFAWrapper:
    """
    Wrapper around DFA that provides a delta function with symbol indices.
    """
    def __init__(self, dfa):
        self.dfa = dfa
        self.alphabet = dfa.get_alphabet()
        self.symbol_to_idx = {sym: i for i, sym in enumerate(self.alphabet)}

    def delta(self, state, symbol_idx):
        """
        Input:
            state - the current state number
            symbol_idx - the index of the symbol in the alphabet (0-3)
        Output:
            the new state after transition, or failed_state if invalid
        """
        if symbol_idx < 0 or symbol_idx >= len(self.alphabet):
            return failed_state
        symbol = self.alphabet[symbol_idx]
        return self.dfa.transition(state, symbol)


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
    states = list(dfa.get_states())
    num_states = len(states)

    # Forward DP: start from the start state
    # prev[i] = number of ways to reach states[i] in the current number of steps
    prev = [0] * num_states
    prev[dfa.start_state] = 1  # One way to be at start with 0 steps

    # For each step from 1 to n
    for _ in range(n):
        next_counts = [0] * num_states

        # For each state, compute how many ways to reach other states in one more step
        for from_idx in range(num_states):
            from_state = states[from_idx]

            # Skip if no ways to reach this state
            if prev[from_idx] == 0:
                continue

            # Skip failed state
            if from_state == failed_state:
                continue

            # Try all symbols
            for symbol in dfa.get_alphabet():
                next_state = dfa.transition(from_state, symbol)

                # Add paths through this transition
                if next_state != failed_state:
                    next_counts[next_state] += prev[from_idx]

        prev = next_counts

    # Sum up counts at all accepting states
    total = 0
    for idx in range(num_states):
        if states[idx] in dfa.get_accept_states():
            total += prev[idx]

    return int(total)



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

    states = list(dfa.get_states())
    num_states = len(states)
    accepting_states = set(dfa.get_accept_states())

    # PHASE 1: Forward DP through left_half
    # Count ways to reach each state after processing left_half
    left_counts = [0] * num_states
    left_counts[dfa.start_state] = 1

    for _ in range(half_len):
        next_counts = [0] * num_states
        for state_idx in range(num_states):
            if left_counts[state_idx] == 0:
                continue
            state = states[state_idx]
            if state == -1:
                continue

            for symbol in dfa.get_alphabet():
                next_state = dfa.transition(state, symbol)
                if next_state != -1:
                    next_counts[next_state] += left_counts[state_idx]

        left_counts = next_counts

    # PHASE 2: Transition on "aa"
    # From each state reached by left_half, transition on 'a' then 'a'
    middle_counts = [0] * num_states
    for state_idx in range(num_states):
        if left_counts[state_idx] == 0:
            continue
        state = states[state_idx]
        if state == -1:
            continue

        # Transition on 'a' twice
        mid_state = dfa.transition(state, 'a')
        if mid_state != -1:
            final_state = dfa.transition(mid_state, 'a')
            if final_state != -1:
                middle_counts[final_state] += left_counts[state_idx]

    # PHASE 3: Forward DP through right_half
    # Starting from middle states, count ways to reach accepting states
    right_counts = middle_counts

    for _ in range(half_len):
        next_counts = [0] * num_states
        for state_idx in range(num_states):
            if right_counts[state_idx] == 0:
                continue
            state = states[state_idx]
            if state == -1:
                continue

            for symbol in dfa.get_alphabet():
                next_state = dfa.transition(state, symbol)
                if next_state != -1:
                    next_counts[next_state] += right_counts[state_idx]

        right_counts = next_counts

    # PHASE 4: Count accepting states
    total = 0
    for state_idx in range(num_states):
        if states[state_idx] in accepting_states:
            total += right_counts[state_idx]

    return int(total)
