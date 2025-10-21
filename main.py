from Delta import Delta
from DFA import *
from build_states import build_states
from count_strings import *
from ProductDFA import ProductDFA


states, accepting_states = build_states()
dfa = DFA(states, alphabet, Delta(), 0, accepting_states)

# Create ProductDFA for option 3 with correct parameters
# p = 0 (acceptance criterion for first component)
# q = delta(delta(0, 'a'), 'a') = delta(0, "aa") (start state for second component)
q_after_aa = dfa.transition(dfa.transition(0, 'a'), 'a')
prod_dfa = ProductDFA(dfa, 0, q_after_aa)

choice = "0"
while (choice != "4"):
    print("Choices:")
    print("(1) Count number of strings of length n in L")
    print("(2) Count number of strings of length n in L'")
    print("(3) Query L' DFA's delta function")
    print("(4) Quit")
    choice = input("Choice: ")

    if (choice == "1"):
        n = (input(f"Value for n (1-300): "))    #n should be between 1-300
        if n.isnumeric():
            n = int(n)
        else:
            print("n must be between 1 and 300.\n")
            continue

        if (n >= 1 and n <= 300):
            print(f"Number of valid strings in L for {n}:  {countValidStrings(dfa, n)}\n")
        else:
            print("n must be between 1 and 300.\n")


    elif (choice == "2"):
        n = input(f"Value for n (1-300): ")
        if n.isnumeric():
            n = int(n)
        else:
            print("n must be between 1 and 300.\n")
            continue

        if (n >= 1 and n <= 300):
            print(f"Number of valid strings in L' for {n}:  {countAASplitStrings(dfa, n)}\n")
        else:
            print("n must be between 1 and 300.\n")

    elif (choice == "3"):
        # Query ProductDFA delta function
        q_input = input(f"Enter state q (0 to {prod_dfa.num_base_states ** 2 - 1}): ")
        if not q_input.isnumeric():
            print("q must be a valid integer.\n")
            continue

        q = int(q_input)
        max_state = prod_dfa.num_base_states ** 2 - 1

        if q < 0 or q > max_state:
            print(f"q must be between 0 and {max_state}.\n")
            continue

        j_input = input("Enter symbol j (0-15 for pairs (a,a)=0 to (d,d)=15): ")
        if not j_input.isnumeric():
            print("j must be 0-15.\n")
            continue

        j = int(j_input)

        if j < 0 or j > 15:
            print("j must be 0-15.\n")
            continue

        # Compute delta(q, j)
        result = prod_dfa.delta(q, j)

        # Decode states and symbol for pretty printing
        q1, q2 = prod_dfa.decode_state_pair(q)
        # j represents pair (a1, a2) where j = a1*4 + a2
        a1 = j // 4
        a2 = j % 4
        symbol1_name = alphabet[a1]
        symbol2_name = alphabet[a2]

        if result == -1:
            print(f"delta({q}, {j}) = {result} (failed state)")
            print(f"  State {q} = ({dfa.pretty_print_state(q1)}, {dfa.pretty_print_state(q2)})")
            print(f"  Symbol {j} = ({symbol1_name}, {symbol2_name})\n")
        else:
            r1, r2 = prod_dfa.decode_state_pair(result)
            print(f"delta({q}, {j}) = {result}")
            print(f"  State {q} = ({dfa.pretty_print_state(q1)}, {dfa.pretty_print_state(q2)})")
            print(f"  Symbol {j} = ({symbol1_name}, {symbol2_name})")
            print(f"  Result {result} = ({dfa.pretty_print_state(r1)}, {dfa.pretty_print_state(r2)})\n")

    elif (choice == "4"):
        print("Quitting...")

    else:
        print("Invalid choice.\n")