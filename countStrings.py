from Alphabet import alphabet
from Delta import Delta, failed_state



def countValidStrings(dfa, n):
    states = list(dfa.states)
    num_states = len(states)
    
    state_to_index = {}
    for idx in range(len(states)):
        state = states[idx]
        state_to_index[state] = idx    
    
    prev = [0] * num_states
    for idx in range(len(states)):
        state = states[idx]
        if state in dfa.accept_states:
            prev[idx] = 1
        else:
            prev[idx] = 0
    
    for k in range(1, n + 1):
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
    
    # Return N_0(n) - count for the starting state (state 0)
    start_state = dfa.start_state  # Should be 0 according to PDF
    if start_state in state_to_index:
        return prev[state_to_index[start_state]]
    else:
        return 0

