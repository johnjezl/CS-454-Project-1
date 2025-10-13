from DFA import DFA
from Alphabet import alphabet
from Delta import *
from buildStates import buildStates



"""
Input:  
    None
Output: 
    A DFA containing states, an alphabet, delta function, start state of 0, and accepting states
Example:
    input - buildDFA()
    output - A DFA containing the above
Preconditions:
    buildStates(), Delta(), and alphabet must be defined
"""
def buildDFA():
    states, accepting_states = buildStates()
    return DFA(states, alphabet, Delta(), 0, accepting_states)
 
 