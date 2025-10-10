from Delta import *
from PerfTimer import *

class DFAForInputPairs:
    transition_table = None

    def __init__(self, base_dfa, start_state, first_dest):
        self.base_dfa = base_dfa
        self.start_state = start_state
        self.target_split_state = first_dest
        self.states = self.generate_states(base_dfa.get_states())
        self.accept_states = set()
        # Valid accepting states are states where the
        # second element of the couplet match the target state
        # and both are accepting states of the base DFA
        for s1 in base_dfa.get_accept_states():
                for s2 in base_dfa.get_accept_states():
                    if s1 == first_dest:
                        self.accept_states.add((s1, s2))
        self.alphabet = self.gen_alphabet()
        if self.transition_table == None:
            PerfTimer.cont("build_transition_table")
            self.transition_table = self.build_transition_table()
            PerfTimer.end("build_transition_table")

    def get_alphabet(self):
        return self.alphabet       

    def get_states(self):
        return self.states

    def get_accept_states(self):
        return self.accept_states
    
    def get_transition(self, state, input_pair):
        if (state, input_pair) in self.transition_table:
            return self.transition_table[(state, input_pair)]
        return (failed_state, failed_state)

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

    def get_next_state(self, state, input_symbol):
        return self.get_transition(state, input_symbol)

    def build_transition_table(self):
        transition_table = {}
        for state1 in self.base_dfa.get_states():
            for input1 in self.base_dfa.get_alphabet():
                new_state1 = self.base_dfa.transition(state1, input1)
                if new_state1 != failed_state:
                    for state2 in self.base_dfa.get_states():
                        for input2 in self.base_dfa.get_alphabet():
                            new_state2 = self.base_dfa.transition(state2, input2)
                            if new_state2 != failed_state:
                                transition_table[((state1, state2), (input1, input2))] = (new_state1, new_state2)
        return transition_table

    def pretty_print_alpha(self, alpha):
        return f"({alpha[0]},{alpha[1]})"

    def pretty_print_state(self, state):
        return f"({self.base_dfa.pretty_print_state(state[0])},{self.base_dfa.pretty_print_state(state[1])})"
