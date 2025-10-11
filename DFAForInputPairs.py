from Delta import *
from PerfTimer import *
import numpy as np

class DFAForInputPairs:
    transition_table = None

    def __init__(self, base_dfa, start_state, first_dest):
        self.base_states_to_index = {}
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
            self.build_transition_table()
            PerfTimer.end("build_transition_table")
            PerfTimer.cont("build_transition_table_test")
            self.build_transition_table_test()
            PerfTimer.end("build_transition_table_test")

    def get_alphabet(self):
        return self.alphabet       

    def get_states(self):
        return self.states

    def get_accept_states(self):
        return self.accept_states
    
    def get_transition_table(self):
        return self.transition_table
    
    def get_xlat_table(self):
        return self.xlat_table
    
    def get_transition(self, state, input):
        PerfTimer.cont("state-to-index conversions")
        s1 = self.base_states.index(state[0])
        PerfTimer.end("state-to-index conversions")
        PerfTimer.cont("state-to-index conversions")
        s2 = self.base_states.index(state[1])
        PerfTimer.end("state-to-index conversions")
        PerfTimer.cont("state-to-index conversions")
        PerfTimer.end("state-to-index conversions")
        PerfTimer.cont("alpha-to-index conversions")
        i1 = int(self.base_alphabet.index(input[0]))
        i2 = int(self.base_alphabet.index(input[1]))
        PerfTimer.end("alpha-to-index conversions")
        return self.xlat_table[s1][s2][i1][i2]

    def get_transition_old(self, state, input):
        next_state = self.transition_table.get((state, input))

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
        self.base_states = self.base_dfa.get_states()
        self.base_alphabet = self.base_dfa.get_alphabet()
        self.base_transition_table = self.base_dfa.get_transition_table()
        self.base_transitions = {}
        self.transition_table = {}
        c = 0
        for state in self.base_states:
            if state != failed_state:
                for sym in self.base_alphabet:
                    next_state = self.base_transition_table[(state,sym)]
                    if next_state != failed_state:
                        c += 1
                        self.base_transitions[(state, sym)] = next_state
        for state_input1, new_state1 in self.base_transitions.items():
            for state_input2, new_state2 in self.base_transitions.items():
                self.transition_table[((state_input1[0],state_input2[0]),(state_input1[1],state_input2[1]))] = (new_state1,new_state2)

    def build_transition_table_test(self):
        self.base_states = self.base_dfa.get_states()
        self.base_alphabet = self.base_dfa.get_alphabet()
        self.base_transition_table = self.base_dfa.get_transition_table()
        self.base_transitions_test = {}
        num_base_states = len(self.base_states)
        num_base_alpha = len(self.base_alphabet)
        self.xlat_table = np.empty((num_base_states, num_base_states, num_base_alpha, num_base_alpha), dtype=object)
        c = 0
        for idx, state in enumerate(self.base_states):
            c = c + 1
            self.base_states_to_index[state] = idx
        c = 0
        for idx, state in enumerate(self.base_states_to_index):
            if state != failed_state:
                for sym in self.base_alphabet:
                    next_state = self.base_transition_table[(state,sym)]
                    if next_state != failed_state:
                        self.base_transitions_test[(idx, sym)] = next_state
        for stateidx_input1, new_state1 in self.base_transitions_test.items():
            for stateidx_input2, new_state2 in self.base_transitions_test.items():
                s1 = stateidx_input1[0]
                s2 = stateidx_input2[0]
                i1 = int(self.base_alphabet.index(stateidx_input1[1]))
                i2 = int(self.base_alphabet.index(stateidx_input2[1]))
                self.xlat_table[s1][s2][i1][i2] = (new_state1, new_state2)
                c = c + 1

    def pretty_print_alpha(self, alpha):
        return f"({alpha[0]},{alpha[1]})"

    def pretty_print_state(self, state):
        return f"({self.base_dfa.pretty_print_state(state[0])} : {self.base_dfa.pretty_print_state(state[1])})"
