from Delta import *

class DFAForInputPairs:

    def __init__(self, base_dfa, start_state, first_final_state):
        self.base_states = base_dfa.get_states()
        self.base_dfa = base_dfa
        self.base_accept_states = base_dfa.get_accept_states()
        self.base_alphabet = self.base_dfa.get_alphabet()
        self.base_transition_table = self.base_dfa.get_transition_table()
        self.accept_states = set()
        self.transition_cache = {}
        self.start_state = start_state
        self.first_final_state = first_final_state
        self.states = self.generate_states(self.base_states)
        self.accept_states = self.generate_accept_states()
        self.alphabet = self.gen_alphabet()
        self.alpha_to_idx = {sym: i for i, sym in enumerate(self.base_alphabet)}

    def get_alphabet(self):
        return self.alphabet       

    def get_states(self):
        return self.states

    def get_accept_states(self):
        return self.accept_states
    
    def generate_accept_states(self):
        # Valid accepting states are states where the
        # second element of the couplet match the target state
        # and both are accepting states of the base DFA
        accept_states = set()
        for s2 in self.base_accept_states:
            if (self.first_final_state, s2) in self.states:
                accept_states.add((self.first_final_state, s2))
        return accept_states

    def generate_states(self, states):
        state_pairs = []
        for s1 in states:
            if s1 != failed_state:
                for s2 in states:
                    if s2 != failed_state:
                        state_pairs.append((s1, s2))
        return sorted(state_pairs)

    def gen_alphabet(self):
        alpha = []
        for x1 in self.base_dfa.get_alphabet():
            for x2 in self.base_dfa.get_alphabet():
                alpha.append((x1, x2))
        return alpha

    def encode_key_to_int(self, state1, state2, sym1, sym2):
        return (state1 << 44) | (state2 << 24) | (self.alpha_to_idx[sym1] << 4) | self.alpha_to_idx[sym2]

    def pretty_print_alpha(self, alpha):
        return f"({alpha[0]},{alpha[1]})"

    def pretty_print_state(self, state):
        return f"({self.base_dfa.pretty_print_state(state[0])} : {self.base_dfa.pretty_print_state(state[1])})"
