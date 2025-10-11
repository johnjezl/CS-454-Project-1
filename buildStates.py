from Alphabet import alphabet

failed_state = -1

def buildStates(letters_to_add = 5, state = 0):
    states, accepting_states = buildStatesHelper(letters_to_add, state, { 0, failed_state }, { 0 })
    return list(states), list(accepting_states)

def buildStatesHelper(letters_to_add, state, states, accepting_states):
    if letters_to_add == 0:
        return states, accepting_states
    for i in range(len(alphabet)):
        new_state = (state << 4) + (i+1)
        states.add(new_state)
        accepting_states.add(new_state)
        states, accepting_states = buildStatesHelper(letters_to_add - 1, new_state, states, accepting_states)
    return states, accepting_states
