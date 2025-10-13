from Delta import *

class ProductDFA:



    """
    Input:
        self - the product dfa itself
        base_dfa - the dfa that accepts strings where substrings of length 6 contain all letters from 'alphabet'
        start_state - the start state of product dfa
        first_final_state - the first final state of the product dfa
    Output:
        None, a product dfa is initialized with the above and more
    Example:
        Call - ProductDFA(base_dfa, start_state, first_final_state)
        Result - product dfa is initialized with the above and more
    Preconditions:
        base_dfa must be initialized with states, accepting states, transition table, and alphabet
    """
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



    """
    Input:
        self - the product dfa itself
    Output:
        The alphabet the product dfa uses in list form
    Example:
        Call - productDFA.get_alphabet()
        Output - the alphabet of productDFA (a, b, c, d)
    Preconditions:
        alphabet must be initialized
    """
    def get_alphabet(self):
        return self.alphabet



    """
    Input:
        self - the product dfa itself
    Output:
        The states in the product dfa
    Example:
        Call - productDFA.get_states()
        Output - a list of states in productDFA
    Preconditions:
        None
    """
    def get_states(self):
        return self.states



    """
    Input:
        self - the product dfa itself
    Output:
        The accept states in the product dfa
    Example:
        Call - productDFA.get_accept_states()
        Output - a list of accepting states in productDFA
    Preconditions:
        None
    """
    def get_accept_states(self):
        return self.accept_states



    """
    Input:
        self - the product dfa itself
    Output:
        accept_states - set of accepting states for the product dfa
    Example:
        Call - productDFA.generate_accept_states()
        Result - productDFA now has a set of accepting states
    Preconditions:
        self must have states, base_accept_states, and first_final_states
    """
    def generate_accept_states(self):
        # Valid accepting states are states where the
        # second element of the couplet match the target state
        # and both are accepting states of the base DFA
        accept_states = set()
        for s2 in self.base_accept_states:
            if (self.first_final_state, s2) in self.states:
                accept_states.add((self.first_final_state, s2))
        return accept_states



    """
    Input:
        self - the product dfa itself
        states - the states that will be made into pairs for the product dfa
    Output:
        a sorted list of state pairs
    Example:
        Call - productDFA.generate_states()
        Result - productDFA now has a sorted list of state pairs
    Preconditions:
        failed_state is defined
    """
    def generate_states(self, states):
        state_pairs = []
        for s1 in states:
            if s1 != failed_state:
                for s2 in states:
                    if s2 != failed_state:
                        state_pairs.append((s1, s2))
        return sorted(state_pairs)



    """
    Input:
        self - the product dfa itself
    Output:
        a list of pairs of letters in 'alphabet'
    Example:
        Call - productDFA.gen_alphabet()
        Result - productDFA now has a sorted list of alphabet symbol pairs
    Preconditions:
        alphabet must be defined
    """
    def gen_alphabet(self):
        alpha = []
        for x1 in self.base_dfa.get_alphabet():
            for x2 in self.base_dfa.get_alphabet():
                alpha.append((x1, x2))
        return alpha



    """
    Input:
        self - the product dfa itself
        state1 - the first state in a pair
        state2 - the second state in a pair
        sym1 - the first input symbol in a pair
        sym2 - the second input symbol in a pair
    Output:
        the pairs of states and symbols encoded to a single int
    Example:
        Call - productDFA.encode_key_to_int(state1, state2, sym1, sym2)
        Output - the inputs encoded into one int
    Preconditions:
        None
    """
    def encode_key_to_int(self, state1, state2, sym1, sym2):
        return (state1 << 44) | (state2 << 24) | (self.alpha_to_idx[sym1] << 4) | self.alpha_to_idx[sym2]



    """
    Input:
        self - the product dfa itself
        alpha - a set of a pair of symbols from the alphabet
    Output:
        the pair of symbols printed in form (alpha[0], alpha[1])
    Example:
        Call - productDFA.pretty_print_alpha({0, 1}) 
        Output - (0, 1)
    Preconditions:
        alpha must contain elements at indexes 0 and 1
    """
    def pretty_print_alpha(self, alpha):
        return f"({alpha[0]},{alpha[1]})"



    """
    Input:
        self - the product dfa itself
        state - a set of a pair of states
    Output:
        the pair of states printed in form (state[0] : state[1])
    Example:
        Call - productDFA.pretty_print_state({0, 1}) 
        Output - (0 : 1)
    Preconditions:
        state must contain elements at indexes 0 and 1
    """
    def pretty_print_state(self, state):
        return f"({self.base_dfa.pretty_print_state(state[0])} : {self.base_dfa.pretty_print_state(state[1])})"
