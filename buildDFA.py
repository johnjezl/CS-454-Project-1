from DFA import DFA
from Alphabet import alphabet
from Delta import Delta
from Delta import failed_state

def buildDFA():
    states, accepting_states = buildStates()
    return DFA(states, set(alphabet), Delta(), 0, accepting_states)
 
def buildStates(letters_to_add = 5, state = 0, states = set({0,failed_state}), accepting_states = set({0})):
    if letters_to_add == 0:
        return states, accepting_states
    for i in range(len(alphabet)):
        state = (state << 4) + (i+1)
        states.add(state)
 #       if is_an_accept_state(state):
        accepting_states.add(state)
        states, accepting_states = buildStates(letters_to_add - 1, state, states, accepting_states)
        state = state >> 4
    return states, accepting_states

#def is_an_accept_state(state):
#    letter_count = 0
#    if state < 0x10000:
#        return True
#    for i in range(1,len(alphabet)+1):
#        if (state & 0xF ) == i or ( state >> 4 & 0xF ) == i or ( state >> 8 & 0xF ) == i or ( state >> 12 & 0xF ) == i or ( state >> 16 & 0xF ) == i:
#            letter_count += 1
#    if letter_count >= 3:
#        return True

buildDFA()
