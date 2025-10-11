from DFA import DFA
from Alphabet import alphabet
from Delta import *
from buildStates import buildStates

def buildDFA():
    states, accepting_states = buildStates()
    return DFA(states, alphabet, Delta(), 0, accepting_states)
 
 