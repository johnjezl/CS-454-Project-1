from Delta import Delta
from build_states import failed_state
from ProductDFA import ProductDFA
import numpy as np


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
    failed state must be defined
"""
def countValidStrings(dfa, n):
    states = list(dfa.get_states())
    num_states = len(states)
    
    state_to_index = {}
    for idx in range(len(states)):
        state = states[idx]
        state_to_index[state] = idx    

    prev = [0] * num_states
    for idx in range(len(states)):
        state = states[idx]
        if state in dfa.get_accept_states():
            prev[idx] = 1
        else:
            prev[idx] = 0

    for _ in range(1, n + 1):
        next = [0] * num_states

        for j in range(len(states)):
            from_state = states[j]

            # Failed state always fails
            if from_state == failed_state:
                next[j] = 0
                continue

            sum_value = 0
            for x in dfa.get_alphabet():
                # Get next state using delta transition
                next_state = Delta.delta(from_state, x)

                # Add contribution if transition is valid
                if next_state != failed_state and next_state in state_to_index:
                    next_state_idx = state_to_index[next_state]
                    sum_value += prev[next_state_idx]

            next[j] = sum_value

        prev = next
    
    start_state = dfa.start_state  # Should be 0 according to PDF
    if start_state in state_to_index:
        return prev[state_to_index[start_state]]
    else:
        return 0



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
    productDFA class must exist
    failed state must be defined
"""
def countAASplitStrings(dfa, n):
    if n % 2 != 0:
        return 0  # Must be even length

    # Build DFA for Input Pairs once - we'll reuse it
    productDFA = ProductDFA(dfa, (0, 0), 0)

    # Collect start_state and first_final_state pairs to compute simultaneously
    pairs_to_compute = []
    for p in dfa.get_states():
        if p == failed_state:
            continue

        # We only care about states of the lesser of
        # length n/2 - 1 and length of the longest state (5)
        slen = state_length(p)
        if  slen != min(5, n // 2 - 1):
            continue

        # Get the state we would be at after we see 'aa' from this state
        q = dfa.transition(p, 'a')
        if q == failed_state:
            continue
        q = dfa.transition(q, 'a')
        if q == failed_state:
            continue

        pairs_to_compute.append(((0, q), p))

    counts = countPairStrings(productDFA, n//2 - 1, pairs_to_compute)
    total_count = sum(counts)

    return total_count




"""
Input:  
    productDFA - the DFA that accepts pairs of strings having all letters of alphabet in each substring of length 6
    n - the length of one half of the string without the a  (original string length / 2 - 1)
    pairs_list - pairs of start states and first final states
Output: 
    the number of strings of length n accepted by productDFA
Example:
    input - countPairStrings(productDFA, 1)    (original string length would be 4)
    output - 4      (because alphabet has 4 letters)
Preconditions:
    n >= 0, must be half the original string length - 1
    productDFA must contain all states and accepting states and have a transition table
    failed state must be defined
    pairs_list must contain valid pairs
"""
def countPairStrings(productDFA, n, pairs_list):
    states = productDFA.get_states()
    num_states = len(states)
    num_pairs = len(pairs_list)

    # Build state index map if not cached
    if not hasattr(productDFA, '_state_to_index_cache'):
        state_to_index = {}
        for idx, state in enumerate(states):
            state_to_index[state] = idx
        productDFA._state_to_index_cache = state_to_index

        # Pre-compute transitions as a sparse structure using lists of lists
        transitions = [[] for _ in range(num_states)]
        base_transition_table = productDFA.base_transition_table

        for j, from_state in enumerate(states):
            if from_state[0] == failed_state or from_state[1] == failed_state:
                continue

            state1, state2 = from_state
            for input1, input2 in productDFA.get_alphabet():
                next_state1 = base_transition_table[(state1, input1)]
                next_state2 = base_transition_table[(state2, input2)]

                if (next_state1 != failed_state and
                    next_state2 != failed_state):
                    next_state = (next_state1, next_state2)
                    next_idx = state_to_index.get(next_state)
                    if next_idx is not None:
                        transitions[j].append(next_idx)

        productDFA._transitions_cache = transitions

    state_to_index = productDFA._state_to_index_cache
    transitions = productDFA._transitions_cache

    # Set up accept states for all pairs
    prev = np.zeros((num_pairs, num_states), dtype=object)
    base_accept_states = productDFA.base_accept_states

    for pair_idx, (start_state, first_final_state) in enumerate(pairs_list):
        for s2 in base_accept_states:
            state_pair = (first_final_state, s2)
            if state_pair in state_to_index:
                prev[pair_idx, state_to_index[state_pair]] = 1

    # Process all pairs simultaneously
    next = np.zeros((num_pairs, num_states), dtype=object)
    for _ in range(1, n + 1):
        next.fill(0)

        for j in range(num_states):
            # For each state, sum found transition counds
            for next_state_idx in transitions[j]:
                # Update all pairs
                next[:, j] += prev[:, next_state_idx]

        prev, next = next, prev

    # Get final counts for each pair
    results = []
    for pair_idx, (start_state, first_final_state) in enumerate(pairs_list):
        results.append(int(prev[pair_idx, state_to_index[start_state]]))

    return results



"""
Input:  
    state - the state to check the length of (encoded in base 8)
Output: 
    length - the length of the state
Example:
    input - state_length(115785)    (where 115785 = cdbaaa in base 8)
    output - 6
Preconditions:
    state must be a valid state or the failed state
"""
def state_length(state):
    if state == failed_state:
        return -1
    length = 0
    while state > 0:
        length += 1
        state = state >> 4
    return length
