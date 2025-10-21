from Alphabet import alphabet

failed_state = -1





"""
Input:
    max_length - the max length of a state
Output:
    states - list of all possible states, including the failed state
    accepting_states - list of all possible accepting states
Example:
    input - buildStates(5)
    output - list of 1365 states (plus failed_state) and list of 1365 accepting states
Preconditions:
    failed_state must be defined
"""
def build_states(max_length = 5):
    states = [0]
    accepting_states = [0]

    generate_state_numbers("", 5, accepting_states)
    states = accepting_states.copy()
    states.append(failed_state)
    return list(states), list(accepting_states)



"""
Input:
    current - the current state being built up
    max_length - The max length of a state (5)
    states - the place to store the built states
Output:
    None
Example:
    call - generate_state_numbers("", 5, states)
    result - All combinations of states up to length 5 have been generated and stores in 'states'
Preconditions:
    max_length >= 1
"""
def generate_state_numbers(current, max_length, states):
    """Recursively generate all combinations up to max_length"""
    if len(current) > 0:
        states.append(len(states))
    
    if len(current) < max_length:
        for letter in alphabet:
            generate_state_numbers(current + letter, max_length, states)




"""
    for level in range(max_length):
        next_level = []
        for state in current_level:
            for i in range(len(alphabet)):
                # Formula: state * 4 + (i + 1)
                # This gives (symbol_index + 1) at the rightmost position
                new_state = state * 4 + (i + 1)
                states.append(new_state + 1)
                accepting_states.append(new_state + 1)
                next_level.append(new_state)
        current_level = next_level
"""
