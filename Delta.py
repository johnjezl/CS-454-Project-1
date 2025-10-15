from build_states import *

alphabet = list(['a', 'b', 'c', 'd'])

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
        input_value = alphabet.index(input) + 1

        # If state has less than 5 characters, append the new character
        if state_len < 5:
            # New state = old_state + input_value * 4^state_len
            new_state = state + input_value * (4 ** state_len)
            return new_state
        else:
            # State has 5 characters, check if transition is valid
            if Delta._is_valid_transition(state, input):
                # Remove the oldest character and add the new one
                # This means we need to shift left by one position in base-4
                state_without_oldest = Delta._remove_oldest_char(state)
                new_state = state_without_oldest + input_value * (4 ** 4)  # Add at depth 4 (5th position)
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

        length = 0
        remaining = state
        while remaining > 0:
            contribution = remaining % 4
            if contribution == 0:
                contribution = 4
                remaining = (remaining // 4) - 1
            else:
                remaining = remaining // 4
            length += 1
        return length

    """
    Input:
        state - the state representing at least 1 character
    Output:
        list of character values (1-4) representing the state
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

        chars = []
        remaining = state
        while remaining > 0:
            contribution = remaining % 4
            if contribution == 0:
                contribution = 4
                remaining = (remaining // 4) - 1
            else:
                remaining = remaining // 4
            chars.append(contribution)
        return chars

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
        chars = Delta._decode_state(state)
        if len(chars) <= 1:
            return 0

        # Remove the first character and re-encode
        new_chars = chars[1:]
        new_state = 0
        for depth, char_val in enumerate(new_chars):
            new_state += char_val * (4 ** depth)
        return new_state

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
        # Get the last 5 characters of the state
        chars = Delta._decode_state(state)

        # We'll check the last 5 chars + the new input = 6 chars total
        # After sliding window, we keep chars[1:5] + new char
        if len(chars) < 5:
            return False

        # Get the last 5 characters (which will become positions 0-4 after removing oldest)
        last_5_chars = chars[:5]  # chars are stored in reverse order (first char is at index 0)

        # Actually, chars are in the order they were added, so chars[0] is the oldest
        # We want to check: chars[1], chars[2], chars[3], chars[4], and the new input
        # That's 6 characters total (the last 5 of current state + new input)

        # Wait, let me reconsider. If state has 5 chars, we want to check if
        # removing the oldest and adding the new one gives us all alphabet letters in the resulting 6 chars
        # But the state only has 5 chars, so after transition we'd have chars[1:5] + input = 5 chars
        # That's not 6 chars for validation

        # I think the logic is: when we have 5+ characters and try to add another,
        # we check if the last 5 characters plus the new character contain all alphabet letters
        input_value = alphabet.index(input) + 1

        # Collect the character values from the last 5 positions + the new input
        char_set = set(last_5_chars + [input_value])

        # Check if we have all alphabet letters (1, 2, 3, 4 for a 4-letter alphabet)
        required_chars = set(range(1, len(alphabet) + 1))

        return char_set == required_chars
