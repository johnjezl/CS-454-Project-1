from Alphabet import alphabet

failed_state = -1

class Delta:

    @staticmethod
    def delta(state, input):
        if state == failed_state:
            return failed_state
        if input not in alphabet:
            raise ValueError(f"Input '{input}' not in alphabet")
        if state < 0x10000:
            new_state = (state << 4) + (alphabet.index(input) + 1)
            return new_state
        else:
            if Delta._is_valid_transition(state, input):
                state = ((state & 0xFFFF) << 4) + (alphabet.index(input) + 1)
                return state
            else:
                return failed_state

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
