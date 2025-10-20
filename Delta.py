from DFA import *


class Delta:

    """
    Input:
        state - the state to start from (base-4 encoding representing a string of characters)
        input - the character to transition on
    Output:
        new_state - the new state a state of less than 5 chars will be in after transitioning on input
        or state - the state a state of 5+ chars will be in after transitioning on input
        or failed_state - a state of -1 representing there was no valid transition from (state, input)
    Example:
        Input - delta(1, 'a')  (state 1 = 'a')
        Output - 5 (state 5 = 'aa')
    Preconditions:
        failed_state and alphabet must be defined
        state must be a valid state representing a string in the alphabet or failed state
    """
    @staticmethod
    def delta(state, input):
        if state == failed_state:
            return failed_state
        if input not in alphabet:
            raise ValueError(f"Input '{input}' not in alphabet")

        # Get state length
        state_len = Delta._state_length(state)
        input_value = alphabet.index(input)

        # If state has less than 5 characters, append the new character
        if state_len < 5:
            new_state = state * 4 + input_value + 1
            return new_state
        else:
            # State has 5 characters, check if transition is valid
            if Delta._is_valid_transition(state, input):
                # Remove the oldest (leftmost) character and add the new one
                # Extract the 4 rightmost digits, shift left, add new symbol
                state_without_oldest = Delta._remove_oldest_char(state)
                new_state = state_without_oldest * 4 + input_value + 1
                return new_state
            else:
                return failed_state



    """
    Input:
        state - the state (encoded integer)
    Output:
        length of the state (number of characters it represents)
    Example:
        Input - 6
        Output - 2
    Preconditions:
        state must be a valid state or 0
    """
    @staticmethod
    def _state_length(state):
        if state == 0:
            return 0
        if state == failed_state:
            return -1

        state -= 1
        if state >= 4:
            if state >= 4 + 16:
                if state >= 4 + 16 + 64:
                    if state >= 4 + 16 + 64 + 256:
                        return 5
                    else:
                        return 4
                else:
                    return 3
            else:
                return 2
        return 1

    """
    Input:
        state - the state representing at least 1 character
    Output:
        list of character values (0-3) representing the state
    Example:
        Input - 6
        Output - 'aa'
    Preconditions:
        state must be valid
    """
    @staticmethod
    def _decode_state(state):
        if state == 0:
            return []

        state_len = Delta._state_length(state)

        chars = [0] * state_len
        tmp = state - 1
        for i in range(state_len-1):
            tmp -= 4 ** (i+1)
        for i in range(state_len):
            chars[state_len - i - 1] = (tmp % 4) 
            tmp = tmp // 4
        return chars

    """
    Input:
        state - the state to start from (representing a string of characters)
        input - the character to transition on
    Output:
        true if is valid transition (if adding input to state results in all characters in alphabet), false if not
    Example:
        Input - _is_valid_transition(1364, 'a')     (where 1364 = 'ddddd')
        Output - false (adding 'a' to 'ddddd' gives 'ddddda', last 6 chars don't have all alphabet letters)
    Preconditions:
        state must represent a string of at least 5 chars, input must be a letter that exists in alphabet
    """
    @staticmethod
    def _is_valid_transition(state, input):
        # Get the 5 characters of the current state (decoded as symbol indices 0-3)
        chars = Delta._decode_state(state)

        # All transition from states with less than 5 chars are valid
        if len(chars) < 5:
            return True

        input_value = alphabet.index(input)  # Symbol index: a=0, b=1, c=2, d=3

        # The 6 characters to check are: all 5 current chars + the new input
        char_set = set(chars[:5] + [input_value])

        # Check if we have all alphabet letters (0, 1, 2, 3 for a 4-letter alphabet)
        required_chars = set(range(len(alphabet)))

        return char_set == required_chars

    """
    Input:
        state - the state representing at least 1 character
    Output:
        new state with the first (oldest) character removed
    Example:
        Input - 'aa'
        Output - 'a'
    Preconditions:
        state must have at least 1 character
    """
    @staticmethod
    def _remove_oldest_char(state):
        sub = 0
        add = 0
        for i in range(Delta._state_length(state)):
            sub = sub + 4 ** (i)
            if i > 0:
                add = add + 4 ** (i - 1)
        new_state = state - sub
        mask = (0x3 << ((Delta._state_length(state)-1)*2))
        new_state = new_state - (new_state & mask)
        new_state = new_state + add
        return new_state
    