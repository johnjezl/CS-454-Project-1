from Alphabet import alphabet
from DFA import DFA
from build_states import build_states
from count_strings import *


states, accepting_states = build_states()
dfa = DFA(states, alphabet, Delta(), 0, accepting_states)

choice = "0"
while (choice != "3"):
    print("Choices:")
    print("(1) Count number of strings of length n in L")
    print("(2) Count number of strings of length n in L'")
    print("(3) Quit")
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
        print("Quitting...")

    else:
        print("Invalid choice.\n")