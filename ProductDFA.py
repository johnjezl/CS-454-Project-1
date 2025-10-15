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

        # Calculate max state value for contiguous indexing
        self.max_base_state = max(s for s in self.base_states if s != -1) + 1

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
            encoded_state = self.encode_state_pair(self.first_final_state, s2)
            if encoded_state in self.states:
                accept_states.add(encoded_state)
        return accept_states



    """
    Input:
        self - the product dfa itself
        s1 - first component of the state pair
        s2 - second component of the state pair
    Output:
        encoded state as a single integer using formula: s1 * max_base_state + s2
    Example:
        Call - productDFA.encode_state_pair(5, 3) with max_base_state=1365
        Output - 6828 (5 * 1365 + 3)
    Preconditions:
        max_base_state must be set
    """
    def encode_state_pair(self, s1, s2):
        return s1 * self.max_base_state + s2

    """
    Input:
        self - the product dfa itself
        encoded_state - the encoded state as a single integer
    Output:
        tuple (s1, s2) representing the state pair
    Example:
        Call - productDFA.decode_state_pair(6828) with max_base_state=1365
        Output - (5, 3)
    Preconditions:
        max_base_state must be set
    """
    def decode_state_pair(self, encoded_state):
        s1 = encoded_state // self.max_base_state
        s2 = encoded_state % self.max_base_state
        return (s1, s2)

    """
    Input:
        self - the product dfa itself
        states - the states that will be made into pairs for the product dfa
    Output:
        a sorted list of encoded state pairs (as single integers)
    Example:
        Call - productDFA.generate_states()
        Result - productDFA now has a sorted list of encoded state pairs
    Preconditions:
        failed_state is defined, max_base_state must be set
    """
    def generate_states(self, states):
        state_pairs = []
        for s1 in states:
            if s1 != failed_state:
                for s2 in states:
                    if s2 != failed_state:
                        encoded = self.encode_state_pair(s1, s2)
                        state_pairs.append(encoded)
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
        encoded_state - the encoded product state (s1 * max_base_state + s2)
        sym1 - the first input symbol in a pair
        sym2 - the second input symbol in a pair
    Output:
        the state and symbols encoded to a single int for caching
    Example:
        Call - productDFA.encode_key_to_int(encoded_state, sym1, sym2)
        Output - the inputs encoded into one int
    Preconditions:
        None
    """
    def encode_key_to_int(self, encoded_state, sym1, sym2):
        # Use bit shifting: encoded_state | (sym1_idx << some_bits) | sym2_idx
        return (encoded_state << 8) | (self.alpha_to_idx[sym1] << 4) | self.alpha_to_idx[sym2]



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
        state - an encoded state (single integer)
    Output:
        the pair of states printed in form (state1 : state2)
    Example:
        Call - productDFA.pretty_print_state(6828)
        Output - (5 : 3) or in pretty form using base DFA names
    Preconditions:
        state must be a valid encoded state
    """
    def pretty_print_state(self, state):
        s1, s2 = self.decode_state_pair(state)
        return f"({self.base_dfa.pretty_print_state(s1)} : {self.base_dfa.pretty_print_state(s2)})"
