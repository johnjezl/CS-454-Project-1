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
    from ProductDFA import ProductDFA

    if n % 2 != 0:
        return 0

    half_len = n // 2 - 1
    if half_len < 0:
        return 0

    # Create ProductDFA with lazy state generation
    # Both components start at start_state (0), first_final_state is unused now
    prod_dfa = ProductDFA(dfa, dfa.start_state, dfa.start_state)

    # Start state: both DFAs at start (0, 0)
    start_encoded = prod_dfa.encode_state_pair(0, 0)

    # Forward DP using ProductDFA
    # Track how many ways to reach each ProductDFA state from start
    # After half_len steps, both components will have processed their respective halves
    counts = {start_encoded: 1}

    for _ in range(half_len):
        next_counts = {}
        for state, count in counts.items():
            # Get all forward transitions (cached internally)
            for _, next_state in prod_dfa.get_forward_transitions(state):
                next_counts[next_state] = next_counts.get(next_state, 0) + count
        counts = next_counts

    # Count paths that end at accepting states
    # Accepting means both left_half and right_half are accepted by the base DFA
    total = 0
    for state, count in counts.items():
        if prod_dfa.is_accept_state(state):
            total += count

    return int(total)
