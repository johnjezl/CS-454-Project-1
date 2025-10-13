from Delta import Delta
from build_states import *

class DFA:

    """
    Input:
        self - the dfa itself
        states - a list of the states of the dfa
        alphabet - the alphabet used by the dfa
        delta - the delta function of the dfa
        start_state - the start state of the dfa
        accept_states - a list of the accepting states of the dfa
    Output:
        None, a dfa is initialized with the above
    Example:
        Call - DFA(states, alphabet, delta, start_state, accept_states)
        Result - dfa is initialized with the above
    Preconditions:
        'delta' contains transitions for states in 'states' and on inputs from 'alphabet'
        All 'accepting_states' are also in 'states'
        'start_state' exists in 'states'
    """
    def __init__(self, states, alphabet, delta, start_state, accept_states):
        self.states = states.copy()
        self.alphabet = alphabet.copy()
        self.delta = delta
        self.transition_table = self.build_transition_table()
        self.start_state = start_state
        self.accept_states = accept_states.copy()



    """
    Input:
        self - the dfa itself
    Output:
        A list of the states in the dfa
    Example:
        Call - dfa.get_states()
        Output - The states in the dfa as a list
    Preconditions:
        None
    """
    def get_states(self):
        return self.states



    """
    Input:
        self - the dfa itself
    Output:
        A list of the accepting states of the dfa
    Example:
        Call - dfa.get_accept_states()
        Output - The accepting states of the dfa as a list
    Preconditions:
        None
    """
    def get_accept_states(self):
        return self.accept_states



    """
    Input:
        self - the dfa itself
    Output:
        The delta function of the dfa
    Example:
        Call - dfa.get_delta()
        Output - The delta function of the dfa
    Preconditions:
        None
    """
    def get_delta(self):
        return self.delta



    """
    Input:
        self - the dfa itself
    Output:
        The alphabet used by the dfa in list form
    Example:
        Call - dfa.get_alphabet()
        Output - The alphabet used by the dfa in list form (a, b, c, d)
    Preconditions:
        None
    """
    def get_alphabet(self):
        return self.alphabet



    """
    Input:
        self - the dfa itself
    Output:
        The transition table of the dfa in form of a dictionary
    Example:
        Call - dfa.get_transition_table()
        Output - The transition table of the dfa in dictionary form
    Preconditions:
        None
    """
    def get_transition_table(self):
        return self.transition_table



    """
    Input:  
        self - the DFA itself
        state - the current state to transition from
        input_symbol - the input symbol to transition on
    Output: 
        The state the DFA goes to on delta(state, input_symbol) or failed_state if there was no state to go to
    Example:
        Input - self.transition(1, a)
        Output - 9 (using base 8 encoding)
    Preconditions: 
        failed_state is defined
    """
    def transition(self, state, input_symbol):
        if (state, input_symbol) in self.transition_table:
            return self.transition_table[(state, input_symbol)]
        return failed_state



    """
    Input:  
        self - the DFA itself
        input_string - a string made from the alphabet
    Output: 
        true if the current_state is an accepting state, false if it is not
    Example:
        Input - self.process_input(abc)
        Output - true
    Preconditions:
        None
    """
    def process_input(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol '{symbol}' not in alphabet")
            current_state = self.transition(current_state, symbol)
        return current_state in self.accept_states



    """
    Input:  
        self - the DFA itself
    Output: 
        table - a transition table for the DFA in form of a dictionary
    Example:
        Input - self.build_transition_table()
        Output - a dictionary mapping delta(state, symbol) to the state it goes to for all states in the DFA
    Preconditions:
        Need the delta function from class Delta, need buildStates() to build all the states, alphabet is defined
    """
    def build_transition_table(self):
        table = {}

        # Generate all states
        states, accepting_states = build_states()

        # Build transition table using the delta passed to __init__
        for state in states:
            for symbol in self.alphabet:
                next_state = self.delta.delta(state, symbol)
                table[(state, symbol)] = next_state

        return table



    """
    Input:  
        self - the DFA itself
        state - the state to be converted to a string using the alphabet
    Output: 
        state_string - the state in the form of a string using the alphabet
        or "failed_state" if state == -1
        or "start" if state == 0
    Example:
        Input - self.pretty_print_state(1)
        Output - a
    Preconditions:
        alphabet is defined
    """
    def pretty_print_state(self, state):
        state_string = ""
        if state == -1:
            return "failed_state"
        if state == 0:
            return "start"
        while (state > 0):
            letter_idx = (state & 0xf) - 1
            state_string = state_string + self.alphabet[letter_idx]
            state = state >> 4
        return state_string

