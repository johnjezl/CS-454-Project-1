from Delta import Delta

class DFA:
    def __init__(self, states, alphabet, delta, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_table = Delta.build_transition_table()
        self.start_state = start_state
        self.accept_states = accept_states

    def get_states(self):
        return self.states

    def get_accept_states(self):
        return self.accept_states

    def get_delta(self):
        return self.delta
    
    def get_alphabet(self):
        return self.alphabet

    def transition(self, state, input_symbol):
        return self.transition_table.get_next_state(state, input_symbol)

    def process_input(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol '{symbol}' not in alphabet")
            current_state = self.transition_table.get_next_state(current_state, symbol)
        return current_state in self.accept_states
    