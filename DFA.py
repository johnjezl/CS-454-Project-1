from Delta import Delta
from buildStates import *

class DFA:
    def __init__(self, states, alphabet, delta, start_state, accept_states):
        self.states = states.copy()
        self.alphabet = alphabet.copy()
        self.transition_table = self.build_transition_table()
        self.start_state = start_state
        self.accept_states = accept_states.copy()

    def get_states(self):
        return self.states.copy()

    def get_accept_states(self):
        return self.accept_states.copy()

    def get_delta(self):
        return self.delta
    
    def get_alphabet(self):
        return self.alphabet.copy()
    
    def get_transition_table(self):
        return self.transition_table.copy()



    """
    Input:  
        self - the DFA itself
        state - the current state to transition from
        input_symbol - the input symbol to transition on
    Output: 
        the state the DFA goes to on delta(state, input_symbol) or failed_state if there was no state to go to
    Example:
        Input - self.transition(0, a)
        Output - 1
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
        from Delta import Delta
        table = {}
        
        # Generate all states
        states, accepting_states = buildStates()
        
        # Build transition table
        for state in states:
            for symbol in self.alphabet:
                next_state = Delta.delta(state, symbol)
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

