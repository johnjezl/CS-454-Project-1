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
    def __init__(self, base_dfa, p, q):
        """
        Initialize ProductDFA Mp as specified in PDF.

        PDF spec: Mp = ⟨Q × Q, Σ × Σ, δ1, (0, p), F1⟩ where
        - δ1((q1, q2), (a1, a2)) = (δ(q1, a1), δ(q2, a2))
        - F1 = {(p, f) | f ∈ F}

        For AA-split problem:
        - p = 0 (start state) - this is what first component must equal to accept
        - q = δ(p, "aa") - this is where second component starts

        Args:
            p: The state that first component must equal for accepting (typically 0)
            q: The initial state for second component = δ(p, "aa")
        """
        self.base_dfa = base_dfa
        self.base_accept_states = set(base_dfa.get_accept_states())
        self.base_alphabet = self.base_dfa.get_alphabet()
        self.p = p  # First component must equal this to accept
        self.q = q  # Second component starts here

        # Base DFA uses sequential state numbering: 0, 1, 2, 3, ..., 1364
        # We can directly use state values as indices (no mapping needed)
        base_states = [s for s in base_dfa.get_states() if s != -1]
        self.num_base_states = len(base_states)  # 1365 states (0-1364)

        # PDF spec: alphabet is Σ × Σ, indexed 0-15 for 4-letter base alphabet
        # Symbol i represents pair (a1, a2) where:
        # a1 = i // 4, a2 = i % 4 (both 0-3)
        self.alphabet_size = len(self.base_alphabet) * len(self.base_alphabet)

        # PDF spec: Start state is (0, q) where q = δ(p, "aa")
        self.product_start_state = self.encode_state_pair(0, q)

        # Lazy state generation - no upfront state generation
        # States are created on-demand through delta transitions
        self.forward_trans_cache = {}  # Cache for forward transitions
        self.backward_trans_cache = {}  # Cache for backward transitions



    """
    Input:
        self - the product dfa itself
    Output:
        The alphabet size (Σ×Σ, so 16 for 4-letter base alphabet)
    Example:
        Call - productDFA.get_alphabet()
        Output - 16
    Preconditions:
        alphabet must be initialized
    """
    def get_alphabet(self):
        return self.alphabet_size



    """
    Input:
        self - the product dfa itself
        encoded_state - an encoded ProductDFA state
    Output:
        True if this is an accepting state
    Example:
        Call - productDFA.is_accept_state(encoded_state)
        Output - True if first component = first_final_state and second is accepting
    Preconditions:
        None
    """
    def is_accept_state(self, encoded_state):
        # PDF spec: F = {(p, f) | f ∈ F} where p = first component acceptance criterion
        # Accepting states are those where first component equals p
        # and second component is in base DFA's accepting states
        s1, s2 = self.decode_state_pair(encoded_state)
        return s1 == self.p and s2 in self.base_accept_states



    """
    Input:
        self - the product dfa itself
        s1 - first component (base DFA state value: 0, 1, 2, ..., 1365)
        s2 - second component (base DFA state value: 0, 1, 2, ..., 1365)
    Output:
        Sequential index from 0 to num_base_states² - 1
    Example:
        Call - productDFA.encode_state_pair(0, 0) with 1366 base states
        Output - 0 (0 * 1366 + 0 = 0)
        Call - productDFA.encode_state_pair(1, 0)
        Output - 1366 (1 * 1366 + 0 = 1366)
    Preconditions:
        s1 and s2 must be valid base DFA states (0-1365)
    """
    def encode_state_pair(self, s1, s2):
        # Since base DFA states are sequential (0, 1, 2, ..., 1365),
        # we can directly use them as indices
        # Sequential encoding: s1 * num_base_states + s2
        return s1 * self.num_base_states + s2

    """
    Input:
        self - the product dfa itself
        encoded_state - sequential index (0 to num_base_states² - 1)
    Output:
        tuple (s1, s2) representing base DFA state values (both 0-1365)
    Example:
        Call - productDFA.decode_state_pair(0)
        Output - (0, 0)
        Call - productDFA.decode_state_pair(1366)
        Output - (1, 0)
    Preconditions:
        encoded_state must be valid sequential index
    """
    def decode_state_pair(self, encoded_state):
        # Decode to base DFA state values (which are sequential 0-1365)
        s1 = encoded_state // self.num_base_states
        s2 = encoded_state % self.num_base_states
        return (s1, s2)

    """
    Input:
        self - the product dfa itself
        encoded_state - the current encoded state (single integer)
    Output:
        list of (symbol_idx, next_encoded_state) pairs for all valid transitions
    Example:
        Call - productDFA.get_forward_transitions(0)
        Output - [(0, 1366), (1, 2732), (2, 4098), (3, 5464)]
    Preconditions:
        None
    """
    def get_forward_transitions(self, encoded_state):
        if encoded_state in self.forward_trans_cache:
            return self.forward_trans_cache[encoded_state]

        transitions = []
        # Iterate over all symbols in Σ×Σ (0-15 for 4-letter alphabet)
        for sym_idx in range(self.alphabet_size):
            next_state = self.delta(encoded_state, sym_idx)
            if next_state != failed_state:
                transitions.append((sym_idx, next_state))

        self.forward_trans_cache[encoded_state] = transitions
        return transitions



    """
    Input:
        self - the product dfa itself
        encoded_state - the current encoded state
    Output:
        list of encoded states that can reach encoded_state in one transition
    Example:
        Call - productDFA.get_backward_transitions(1366)
        Output - [0]  # Only state (0,0) can reach state (1,1) via 'a'
    Preconditions:
        Must call get_forward_transitions first to build the reverse map
    """
    def get_backward_transitions(self, encoded_state):
        if encoded_state in self.backward_trans_cache:
            return self.backward_trans_cache[encoded_state]
        # This will be built lazily as forward transitions are discovered
        return []



    """
    Input:
        self - the product dfa itself
        from_state - the encoded state transitioning from
        to_state - the encoded state transitioning to
    Output:
        None (updates internal backward transition cache)
    Example:
        Call - productDFA.register_backward_transition(0, 1366)
        Result - backward_trans_cache[1366] will include 0
    Preconditions:
        None
    """
    def register_backward_transition(self, from_state, to_state):
        if to_state not in self.backward_trans_cache:
            self.backward_trans_cache[to_state] = []
        if from_state not in self.backward_trans_cache[to_state]:
            self.backward_trans_cache[to_state].append(from_state)



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



    """
    Input:
        self - the product dfa itself
        state - the current encoded state (single integer)
        symbol_idx - the index of the symbol in Σ×Σ alphabet (0-15)
    Output:
        the new encoded state after transition, or failed_state if invalid
    Example:
        Call - productDFA.delta(encoded_state, 0)  # transition on (a,a) = symbol 0
        Output - new encoded state after (q1,q2) -> (δ(q1,a), δ(q2,a))
    Preconditions:
        state must be a valid encoded state
        symbol_idx must be in range [0, alphabet_size-1]
    """
    def delta(self, state, symbol_idx):
        if symbol_idx < 0 or symbol_idx >= self.alphabet_size:
            return failed_state

        # Decode symbol_idx to get (a1, a2) pair
        # For 4-letter alphabet: symbol_idx = a1*4 + a2
        a1 = symbol_idx // len(self.base_alphabet)
        a2 = symbol_idx % len(self.base_alphabet)

        # Get the actual symbols from base alphabet
        symbol1 = self.base_alphabet[a1]
        symbol2 = self.base_alphabet[a2]

        # Decode product state to (s1, s2)
        s1, s2 = self.decode_state_pair(state)

        # Transition: δ1((s1,s2), (a1,a2)) = (δ(s1,a1), δ(s2,a2))
        next_s1 = self.base_dfa.transition(s1, symbol1)
        next_s2 = self.base_dfa.transition(s2, symbol2)

        if next_s1 == failed_state or next_s2 == failed_state:
            return failed_state

        next_state = self.encode_state_pair(next_s1, next_s2)

        # Note: Backward transition registration removed for performance
        # It was only needed for backward DP, which we no longer use

        return next_state



    """
    Input:
        self - the product dfa itself
    Output:
        generator yielding all encoded accepting states
    Example:
        Call - list(productDFA.get_accept_states())
        Output - [encoded states where both components are accepting]
    Preconditions:
        None
    """
    def get_accept_states(self):
        # For AA-split problem: BOTH components must be at accepting states
        # This represents that both left_half and right_half satisfy the DFA
        for s1 in self.base_accept_states:
            for s2 in self.base_accept_states:
                yield self.encode_state_pair(s1, s2)
