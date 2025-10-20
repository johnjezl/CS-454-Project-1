from Alphabet import alphabet

failed_state = -1





"""
Input:
    letters_to_add - number of letters to add to state
    state - current state being build off of
Output:
    states - list of all possible states, including the failed state
    accepting_states - list of all possible accepting states
Example:
    input - buildStates(5, 0) with alphabet of 4 chars
    output - list of 1365 states (plus failed_state) and list of 1365 accepting states
Preconditions:
    buildStatesHelper and failed_state must be defined, letters_to_add must be a positive int
"""
def build_states(max_length = 5):
    states = [0]
    accepting_states = [0]

    generate_state_numbers("", 5, accepting_states)
    states = accepting_states.copy()
    states.append(failed_state)
    return list(states), list(accepting_states)


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
