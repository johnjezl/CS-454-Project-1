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

    def transition(self, state, input_symbol):
        if (state, input_symbol) in self.transition_table:
            return self.transition_table[(state, input_symbol)]
        return failed_state

    def process_input(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol '{symbol}' not in alphabet")
            current_state = self.transition(current_state, symbol)
        return current_state in self.accept_states
    
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

