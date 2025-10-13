from Delta import Delta
from buildStates import failed_state
from DFAForInputPairs import DFAForInputPairs
import numpy as np


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



def countAASplitStrings(dfa, n):
    if n % 2 != 0:
        return 0  # Must be even length

    # Build DFA for Input Pairs once - we'll reuse it
    dfaForPairs = DFAForInputPairs(dfa, (0, 0), 0)

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

    counts = countPairStrings(dfaForPairs, n//2 - 1, pairs_to_compute)
    total_count = sum(counts)

    return total_count


def countPairStrings(dfaForPairs, n, pairs_list):
    states = dfaForPairs.get_states()
    num_states = len(states)
    num_pairs = len(pairs_list)

    # Build state index map if not cached
    if not hasattr(dfaForPairs, '_state_to_index_cache'):
        state_to_index = {}
        for idx, state in enumerate(states):
            state_to_index[state] = idx
        dfaForPairs._state_to_index_cache = state_to_index

        # Pre-compute transitions as a sparse structure using lists of lists
        transitions = [[] for _ in range(num_states)]
        base_transition_table = dfaForPairs.base_transition_table

        for j, from_state in enumerate(states):
            if from_state[0] == failed_state or from_state[1] == failed_state:
                continue

            state1, state2 = from_state
            for input1, input2 in dfaForPairs.get_alphabet():
                next_state1 = base_transition_table[(state1, input1)]
                next_state2 = base_transition_table[(state2, input2)]

                if (next_state1 != failed_state and
                    next_state2 != failed_state):
                    next_state = (next_state1, next_state2)
                    next_idx = state_to_index.get(next_state)
                    if next_idx is not None:
                        transitions[j].append(next_idx)

        dfaForPairs._transitions_cache = transitions

    state_to_index = dfaForPairs._state_to_index_cache
    transitions = dfaForPairs._transitions_cache

    # Set up accept states for all pairs
    prev = np.zeros((num_pairs, num_states), dtype=np.int64)
    base_accept_states = dfaForPairs.base_accept_states

    for pair_idx, (start_state, first_final_state) in enumerate(pairs_list):
        for s2 in base_accept_states:
            state_pair = (first_final_state, s2)
            if state_pair in state_to_index:
                prev[pair_idx, state_to_index[state_pair]] = 1

    # Process all pairs simultaneously
    next = np.zeros((num_pairs, num_states), dtype=np.int64)
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


def state_length(state):
    if state == failed_state:
        return -1
    length = 0
    while state > 0:
        length += 1
        state = state >> 4
    return length
