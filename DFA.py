
alphabet = list(['a', 'b', 'c', 'd'])
failed_state = -1

class DFA:

    """
    Input:
        self - the dfa itself
        states - a list of the states of the dfa
        alphabet - the alphabet used by the dfa
        delta - the delta function of the dfa
        start_state - the start state of the dfa
        accept_states - a list of the accepting states of the dfa
    Output:
        None, a dfa is initialized with the above
    Example:
        Call - DFA(states, alphabet, delta, start_state, accept_states)
        Result - dfa is initialized with the above
    Preconditions:
        'delta' contains transitions for states in 'states' and on inputs from 'alphabet'
        All 'accepting_states' are also in 'states'
        'start_state' exists in 'states'
    """
    def __init__(self, states, alphabet, delta, start_state, accept_states):
        self.states = states.copy()
        self.alphabet = alphabet.copy()
        self.delta = delta
        self.transition_table = self.build_transition_table()
        self.start_state = start_state
        self.accept_states = accept_states.copy()

        # Pre-compute symbol-to-index mapping for O(1) lookup
        self.symbol_to_idx = {symbol: idx for idx, symbol in enumerate(alphabet)}



    """
    Input:
        self - the dfa itself
    Output:
        A list of the states in the dfa
    Example:
        Call - dfa.get_states()
        Output - The states in the dfa as a list
    Preconditions:
        None
    """
    def get_states(self):
        return self.states



    """
    Input:
        self - the dfa itself
    Output:
        A list of the accepting states of the dfa
    Example:
        Call - dfa.get_accept_states()
        Output - The accepting states of the dfa as a list
    Preconditions:
        None
    """
    def get_accept_states(self):
        return self.accept_states



    """
    Input:
        self - the dfa itself
    Output:
        The delta function of the dfa
    Example:
        Call - dfa.get_delta()
        Output - The delta function of the dfa
    Preconditions:
        None
    """
    def get_delta(self):
        return self.delta



    """
    Input:
        self - the dfa itself
    Output:
        The alphabet used by the dfa in list form
    Example:
        Call - dfa.get_alphabet()
        Output - The alphabet used by the dfa in list form (a, b, c, d)
    Preconditions:
        None
    """
    def get_alphabet(self):
        return self.alphabet



    """
    Input:
        self - the dfa itself
    Output:
        The transition table of the dfa in form of a dictionary
    Example:
        Call - dfa.get_transition_table()
        Output - The transition table of the dfa in dictionary form
    Preconditions:
        None
    """
    def get_transition_table(self):
        return self.transition_table



    """
    Input:  
        self - the DFA itself
        state - the current state to transition from
        input_symbol - the input symbol to transition on
    Output: 
        The state the DFA goes to on delta(state, input_symbol) or failed_state if there was no state to go to
    Example:
        Input - self.transition(1, a)
        Output - 6
    Preconditions: 
        failed_state is defined
    """
    def transition(self, state, input_symbol):
        # Use pre-computed mapping instead of linear search
        return self.transition_table[state][self.symbol_to_idx[input_symbol]]



    """
    Input:  
        self - the DFA itself
    Output: 
        table - a transition table for the DFA in form of a dictionary
    Example:
        Input - self.build_transition_table()
        Output - a dictionary mapping delta(state, symbol) to the state it goes to for all states in the DFA
    Preconditions:
        Need the delta function from class Delta, need buildStates() to build all the states, alphabet is defined
    """
    def build_transition_table(self):
        table = [[-1 for _ in range(len(self.alphabet))] for _ in range(len(self.states))]

        # Build transition table using the delta passed to __init__
        for state_idx, state in enumerate(self.states):
            for sym_idx, symbol in enumerate(self.alphabet):
                next_state = self.delta.delta(state, symbol)
                table[state_idx][sym_idx] = next_state

        return table



    """
    Input:
        self - the DFA itself
        state - the state to be converted to a string using the alphabet
    Output:
        state_string - the state in the form of a string using the alphabet
        or "failed_state" if state == -1
        or "start" if state == 0
    Example:
        Input - self.pretty_print_state(1)
        Output - a
    Preconditions:
        alphabet is defined
    """
    def pretty_print_state(self, state):
        if state == -1:
            return "failed_state"
        if state == 0:
            return "start"

        # Decode using (symbol + 1) encoding
        state_string = ""
        remaining = state
        while remaining > 0:
            digit = remaining % 4
            if digit == 0:  # d (index 3) is encoded as 4, which is 0 mod 4
                state_string = self.alphabet[3] + state_string
                remaining = (remaining // 4) - 1
            else:
                state_string = self.alphabet[digit - 1] + state_string
                remaining = remaining // 4

        return state_string

