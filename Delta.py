from Alphabet import alphabet
from buildStates import *

class Delta:



    """
    Input:  
        state - the state to start from (base 8 encoding representing a string of characters)
        input - the character to transition on
    Output: 
        new_state - the new state a state of less than 5 chars will be in after transitioning on input
        or state - the state a state of over 5 chars will be in after transitioning on input
        or failed_state - a state of -1 representing there was no valid transition from (state, input)
    Example:
        Input - delta(1, a)
        Output - 9 (using base 8 encoding)
    Preconditions: 
        failed_state and alphabet must be defined, state must be a valid state representing a string in the alphabet or failed state
    """
    @staticmethod
    def delta(state, input):
        if state == failed_state:
            return failed_state
        if input not in alphabet:
            raise ValueError(f"Input '{input}' not in alphabet")
        input_value = alphabet.index(input) + 1
        if state < 0x10000:
            new_state = (state << 4) + input_value
            return new_state
        else:
            if Delta._is_valid_transition(state, input):
                state = ((state & 0xFFFF) << 4) + input_value
                return state
            else:
                return failed_state



    """
    Input:  
        state - the state to start from (representing a string of characters)
        input - the character to transition on
    Output: 
        true if is valid transition (if adding input to state results in all characters in alphabet), false if not
    Example:
        Input - _is_valid_transition(115785, a)     (where 115785 = cdbaaa in base 8)
        Output - false
    Preconditions: 
        state must represent a string of at least 5 chars, input must be a letter that exists in alphabet
    """
    @staticmethod
    def _is_valid_transition(state, input):
        input_index = alphabet.index(input) + 1
        unique_char_count = 0 
        for i in range(1,len(alphabet)+1):
            if input_index == i or ( state & 0xF ) == i or ( state >> 4 & 0xF ) == i or ( state >> 8 & 0xF ) == i or ( state >> 12 & 0xF ) == i or ( state >> 16 & 0xF ) == i:
                unique_char_count += 1
        if unique_char_count == len(alphabet):
            return True
        return False
