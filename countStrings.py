from Alphabet import alphabet
from Delta import Delta, failed_state


#def countValidStringsUsingRecurrenceFormula(dfa, max_length):


 #   states = dfa.states
  #  prev = states
   # for i in range(max_length-5):
     #   next = []
    #    for state in prev:
      #      for c in alphabet:
       #         new_state = dfa.get_delta(state, c)
        #        if new_state != -1:
         #           next.append(new_state)
#        prev = next
 #   return len(prev)


def N(dfa, n, j):
    if n == 0:
        if j in dfa.get_accept_states():
            return 1
        return 0
    sum = 0
    for x in alphabet:
        new_state = Delta.delta(j, x)
        if new_state != -1:
            sum += N(dfa, n-1, new_state)
    return sum

def N_recursive(dfa, n, j):
    # Create a memoization cache
    cache = {}
    
    def N_helper(n, j):
        # Check cache first
        if (n, j) in cache:
            return cache[(n, j)]
        
        # Base case
        if n == 0:
            # Check if current state is accepting
            if j in dfa.accept_states:
                result = 1
            else:
                result = 0
        else:
            # Recursive case
            result = 0
            for x in alphabet:
                new_state = Delta.delta(j, x)
                if new_state != failed_state:  # Only continue if not in failed state
                    result += N_helper(n-1, new_state)
        
        cache[(n, j)] = result
        return result
    
    return N_helper(n, j)

#def count_strings(dfa, n):
 #   states = list(dfa.get_states())
  #  m = len(states)
   # 
#    # Initialize: N_j(0)
 #   # prev = [1 if j in dfa.get_accept_states() else 0 for j in range(m)]
#    prev = []
##    for j in range(m):
 #       if j in dfa.get_accept_states():
 #           prev.append(1)
 ##       else:
  #          prev.append(0)

#    # Iterate for lengths 1 to n
##    for length in range(1, n+1):
 #       next = [0] * m
 #       for state_idx in range(m):
 #           for symbol in alphabet:
 #               state = states[state_idx]
 #               print(f"Current state: {state}, symbol: '{symbol}'")
 #               next_state = Delta.delta(state, symbol)
 ##               prev_idx = states.index(next_state)
  ##              next[state_idx] += prev[prev_idx]
   #     prev = next
    
   # return prev[0]


#def countValidStrings(dfa, max_length):
 #   count, scount = countValidStringsHelper(dfa, max_length, "")
  #  return count

#def countValidStringsHelper(dfa, max_length, input_string):
    #if max_length == 0:
   #     if dfa.process_input(input_string):
   #         return 1, 1
   #     else:
  #          return 0, 1
 #   count = 0
 #   scount = 0
 #   for c in alphabet:
 #       new_input_string = input_string + ''.join(c)
 #       c, sc = countValidStringsHelper(dfa, max_length-1, new_input_string)
#        count += c
#        scount += sc
#    return count, scount
