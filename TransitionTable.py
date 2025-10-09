from buildStates import failed_state

class TransitionTable:
    def __init__(self):
        self.table = {}

    def add_transition(self, state, input_symbol, next_state):
        if state not in self.table:
            self.table[state] = {}
        self.table[state][input_symbol] = next_state
    
    def get_next_state(self, state, input_symbol):
        if state in self.table and input_symbol in self.table[state]:
            return self.table[state][input_symbol]
        return failed_state
    
