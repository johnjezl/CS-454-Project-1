from Delta import Delta

class DFAForInputPairs:
    def __init__(self, base_dfa, start_state_couplet, target_split_state):
        self.base_dfa = base_dfa
        self.start_state = start_state_couplet
        self.target_split_state = target_split_state
        self.states = self.generate_states(base_dfa, base_dfa.get_states())
        self.accept_states = set()
        for s1 in base_dfa.get_states():
            for s2 in base_dfa.get_states():
                if s2 == target_split_state and s1 in base_dfa.get_accept_states():
                    self.accept_states.add((s1, s2))
        self.alphabet = self.gen_alphabet()
        
    def get_alphabet(self):
        return self.alphabet       

    def get_states(self):
        return self.states

    def get_accept_states(self):
        return self.accept_states

    def process_input_pair(self, state_pair, input_pair):
        new_state1 = self.base_dfa.transition(state_pair[0], input_pair[0])
        new_state2 = self.base_dfa.transition(state_pair[1], input_pair[1])
        return (new_state1, new_state2)
    
    
    def generate_states(self, dfa, states):
        state_pairs = set()
        for s1 in states:
            for s2 in states:
                state_pairs.add((s1, s2))
        return list(state_pairs)

    def gen_alphabet(self):
        alpha = []
        for x1 in self.base_dfa.get_alphabet():
            for x2 in self.base_dfa.get_alphabet():
                alpha.append((x1, x2))
        return alpha

