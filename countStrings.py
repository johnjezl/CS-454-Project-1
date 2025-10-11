from Alphabet import alphabet
from Delta import Delta
from buildStates import failed_state
from DFAForInputPairs import DFAForInputPairs
from PerfTimer import *



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
            for x in alphabet:
                # Get next state using delta transition
                next_state = Delta.delta(from_state, x)
                
                # Add contribution if transition is valid
                if next_state != failed_state and next_state in state_to_index:
                    next_state_idx = state_to_index[next_state]
                    sum_value += prev[next_state_idx]
            
            next[j] = sum_value
        
        prev = next.copy()
    
    start_state = dfa.start_state  # Should be 0 according to PDF
    if start_state in state_to_index:
        return prev[state_to_index[start_state]]
    else:
        return 0



def countAASplitStrings(dfa, n):
    if n % 2 != 0:
        return 0  # Must be even length

    total_count = 0
    total_count2 = 0
    
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

        # Build DFA for Input Pairs based on this state
        PerfTimer.cont("DFAForInputPairs")
        dfaForPairs = DFAForInputPairs(dfa, (0, q), p)
        PerfTimer.end("DFAForInputPairs")

        count = countPairStrings_old(dfaForPairs, n//2 - 1)
        total_count += count

    PerfTimer.print_timers()

    return total_count


def countPairStrings(dfaForPairs, n):
    states = list(dfaForPairs.get_states())
    num_states = len(states)
    # Avoid having to make a function call to do transition lookups
    transition_table = dfaForPairs.get_transition_table()

    state_to_index = {}
    for idx in range(len(states)):
        state = states[idx]
        state_to_index[state] = idx    

    PerfTimer.cont("build prev")
    prev = [0] * num_states 
    for idx in range(len(states)):
        state = states[idx]
        if state in dfaForPairs.get_accept_states():
            prev[idx] = 1
        else:
            prev[idx] = 0
    PerfTimer.end("build prev")

    for k in range(1, n + 1):
        next = [0] * num_states
        
        for j, from_state in enumerate(states):

            # Failed state always fails
            if from_state[0] == failed_state or from_state[1] == failed_state:
                next[j] = 0
                continue

            sum_value = 0
            for input in dfaForPairs.get_alphabet():
                # Get next state using delta transition
                PerfTimer.cont("get_transition")
                next_state = None
                next_state = dfaForPairs.get_transition(from_state, input)
                PerfTimer.end("get_transition")
                
                # Add if transition is valid
                if next_state != None:
                    if next_state[0] != failed_state and next_state[1] != failed_state:
                        if next_state in state_to_index:
                            next_state_idx = state_to_index[next_state]
                            sum_value += prev[next_state_idx]
            next[j] = sum_value

        prev = next.copy()       

    return prev[state_to_index[dfaForPairs.start_state]]


def countPairStrings_old(dfaForPairs, n):
    states = list(dfaForPairs.get_states())
    num_states = len(states)
    # Avoid having to make a function call to do transition lookups
    transition_table = dfaForPairs.get_transition_table()

    state_to_index = {}
    for idx in range(len(states)):
        state = states[idx]
        state_to_index[state] = idx    

    prev = [0] * num_states 
    for idx in range(len(states)):
        state = states[idx]
        if state in dfaForPairs.get_accept_states():
            prev[idx] = 1
        else:
            prev[idx] = 0

    for k in range(1, n + 1):
        next = [0] * num_states
        
        for j, from_state in enumerate(states):

            # Failed state always fails
            if from_state[0] == failed_state or from_state[1] == failed_state:
                next[j] = 0
                continue

            sum_value = 0
            for input in dfaForPairs.get_alphabet():
                # Get next state using delta transition
                PerfTimer.cont("transition_table lookup")
                next_state = transition_table.get((from_state, input))
                PerfTimer.end("transition_table lookup")
                
                # Add if transition is valid
                if next_state != None:
                    if next_state[0] != failed_state and next_state[1] != failed_state:
                        if next_state in state_to_index:
                            next_state_idx = state_to_index[next_state]
                            sum_value += prev[next_state_idx]
            next[j] = sum_value

        prev = next.copy()       

    return prev[state_to_index[dfaForPairs.start_state]]

def state_length(state):
    if state == failed_state:
        return -1
    length = 0
    while state > 0:
        length += 1
        state = state >> 4
    return length