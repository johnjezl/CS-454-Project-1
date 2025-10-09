from Alphabet import alphabet

failed_state = -1

def buildStates(letters_to_add = 5, state = 0, states = set({0,failed_state}), accepting_states = set({0})):
    if letters_to_add == 0:
        return states, accepting_states
    for i in range(len(alphabet)):
        state = (state << 4) + (i+1)
        states.add(state)
        accepting_states.add(state)
        states, accepting_states = buildStates(letters_to_add - 1, state, states, accepting_states)
        state = state >> 4
    return states, accepting_states
