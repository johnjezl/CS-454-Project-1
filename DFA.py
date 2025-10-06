from Delta import Delta

class DFA:
    def __init__(self, states, alphabet, delta, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.delta = delta
        self.start_state = start_state
        self.accept_states = accept_states

    def get_states(self):
        return self.states

    def get_accept_states(self):
        return self.accept_states

    def get_delta(self):
        return self.delta

    def process_input(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol '{symbol}' not in alphabet")
            current_state = Delta.delta(current_state, symbol)
        return current_state in self.accept_states
    