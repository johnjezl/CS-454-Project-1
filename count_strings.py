from DFA import failed_state


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
    dfa must contain all states and accepting states and transition function
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
    Count strings in L' using 3-phase forward dynamic programming (DP).

    L' = {w | w is in L, |w| is even and the middle two characters are "aa"}

    The 3-phase approach:
    1. Forward DP through left_half: count ways to reach each state p
    2. Transition on "aa": from each state p, compute q = delta(p, "aa")
    3. Forward DP through right_half: count ways to reach accepting states from q

    This sums over all possible values of p, weighted by the number of paths that 
    reach each p in the left half.
    """
    if n % 2 != 0:
        return 0

    half_len = n // 2 - 1
    if half_len < 0:
        return 0

    states = list(dfa.get_states())
    num_states = len(states)

    # PHASE 1: Forward DP through left_half
    # prev[i] = number of ways to reach states[i]
    prev = [0] * num_states
    prev[dfa.start_state] = 1

    for _ in range(half_len):
        next = [0] * num_states
        for from_idx in range(num_states):
            if prev[from_idx] == 0:
                continue
            from_state = states[from_idx]
            if from_state == -1:
                continue

            for symbol in dfa.get_alphabet():
                next_state = dfa.transition(from_state, symbol)
                if next_state != -1:
                    next[next_state] += prev[from_idx]

        prev = next

    # PHASE 2: Transition on "aa"
    # next[i] = number of ways to reach states[i] after left_half + "aa"
    next = [0] * num_states
    for state_idx in range(num_states):
        if prev[state_idx] == 0:
            continue
        state = states[state_idx]
        if state == -1:
            continue

        # Transition on 'a' then 'a'
        mid_state = dfa.transition(state, 'a')
        if mid_state != -1:
            final_state = dfa.transition(mid_state, 'a')
            if final_state != -1:
                next[final_state] += prev[state_idx]

    # PHASE 3: Forward DP through right_half
    prev = next

    for _ in range(half_len):
        next = [0] * num_states
        for from_idx in range(num_states):
            if prev[from_idx] == 0:
                continue
            from_state = states[from_idx]
            if from_state == -1:
                continue

            for symbol in dfa.get_alphabet():
                next_state = dfa.transition(from_state, symbol)
                if next_state != -1:
                    next[next_state] += prev[from_idx]

        prev = next

    # Count accepting states
    total = 0
    for state_idx in range(num_states):
        if states[state_idx] in dfa.get_accept_states():
            total += prev[state_idx]

    return int(total)
