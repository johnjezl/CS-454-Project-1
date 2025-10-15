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
def build_states(letters_to_add = 5, state = 0):
    states, accepting_states = buildStatesHelper(letters_to_add, state, { 0, failed_state }, { 0 }, 0)
    return list(states), list(accepting_states)



"""
Input:
    letters_to_add - number of letters to add to state
    state - current state being build off of
    states - a set of states in the DFA (initially only start state and failed state)
    accepting_states - a set of accepting states in the DFA (initially only start state)
    length - current length of the state string (0 for start state)
Output:
    states - set of all possible states, including failed state
    accepting_states - set of all possible accepting states
Example:
    input - buildStatesHelper(5, 0, {0, failed_state}, {0}, 0) with alphabet of 4 chars
    output - set of 1365 states (plus failed_state) and set of 1365 accepting_states
Preconditions:
    failed_state must be defined, letters_to_add must be a positive int
"""
def buildStatesHelper(letters_to_add, state, states, accepting_states, length):
    if letters_to_add == 0:
        return states, accepting_states
    for i in range(len(alphabet)):
        # New encoding: state + (i+1) * 4^length
        # For start state (0): a=1, b=2, c=3, d=4
        # For length 1: add (i+1) * 4
        # For length 2: add (i+1) * 16, etc.
        new_state = state + (i + 1) * (4 ** length)
        states.add(new_state)
        accepting_states.add(new_state)
        states, accepting_states = buildStatesHelper(letters_to_add - 1, new_state, states, accepting_states, length + 1)
    return states, accepting_states
