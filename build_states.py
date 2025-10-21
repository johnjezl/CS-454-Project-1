from DFA import *


"""
Input:
    letters_to_add - number of letters to add to state
    state - current state being build off of
Output:
    states - list of all possible states, including the failed state
    accepting_states - list of all possible accepting states
Example:
    input - buildStates(5) with alphabet of 4 chars
    output - list of 1366 states (includes failed_state) and list of 1365 accepting states
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
    # Recursively generate all combinations up to max_length
    if len(current) > 0:
        states.append(len(states))

    if len(current) < max_length:
        for letter in alphabet:
            generate_state_numbers(current + letter, max_length, states)
