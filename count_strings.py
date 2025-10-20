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
    """
    Count strings in L' using 3-phase forward DP.

    L' = {w | w is in L, |w| is even and the middle two characters are "aa"}

    PDF spec relationship: This algorithm is mathematically equivalent to building
    ProductDFA Mp for each p ∈ Q and summing L(M0) ∪ L(M1) ∪ ⋯, but uses a more
    efficient implementation that avoids building 1365 separate ProductDFAs.

    The 3-phase approach:
    1. Forward DP through left_half: count ways to reach each state p
    2. Transition on "aa": from each state p, compute q = δ(p, "aa")
    3. Forward DP through right_half: count ways to reach accepting states from q

    This implicitly sums over all possible values of p (as required by PDF),
    weighted by the number of paths that reach each p in the left half.
    """
    if n % 2 != 0:
        return 0

    half_len = n // 2 - 1
    if half_len < 0:
        return 0

    states = list(dfa.get_states())
    num_states = len(states)

    # PHASE 1: Forward DP through left_half
    # left_counts[i] = number of ways to reach states[i] after half_len steps
    left_counts = [0] * num_states
    left_counts[dfa.start_state] = 1

    for _ in range(half_len):
        next_counts = [0] * num_states
        for from_idx in range(num_states):
            if left_counts[from_idx] == 0:
                continue
            from_state = states[from_idx]
            if from_state == -1:
                continue

            for symbol in dfa.get_alphabet():
                next_state = dfa.transition(from_state, symbol)
                if next_state != -1:
                    next_counts[next_state] += left_counts[from_idx]

        left_counts = next_counts

    # PHASE 2: Transition on "aa"
    # middle_counts[i] = number of ways to reach states[i] after left_half + "aa"
    middle_counts = [0] * num_states
    for state_idx in range(num_states):
        if left_counts[state_idx] == 0:
            continue
        state = states[state_idx]
        if state == -1:
            continue

        # Transition on 'a' then 'a'
        mid_state = dfa.transition(state, 'a')
        if mid_state != -1:
            final_state = dfa.transition(mid_state, 'a')
            if final_state != -1:
                middle_counts[final_state] += left_counts[state_idx]

    # PHASE 3: Forward DP through right_half
    # right_counts[i] = number of ways to reach states[i] after full string
    right_counts = middle_counts.copy()

    for _ in range(half_len):
        next_counts = [0] * num_states
        for from_idx in range(num_states):
            if right_counts[from_idx] == 0:
                continue
            from_state = states[from_idx]
            if from_state == -1:
                continue

            for symbol in dfa.get_alphabet():
                next_state = dfa.transition(from_state, symbol)
                if next_state != -1:
                    next_counts[next_state] += right_counts[from_idx]

        right_counts = next_counts

    # Count accepting states
    total = 0
    for state_idx in range(num_states):
        if states[state_idx] in dfa.get_accept_states():
            total += right_counts[state_idx]

    return int(total)
