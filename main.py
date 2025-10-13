from numpy.f2py.auxfuncs import isinteger

from Alphabet import alphabet
from DFA import DFA
from build_states import build_states
from count_strings import *
import time
from getpass import getpass


states, accepting_states = build_states()
dfa = DFA(states, alphabet, Delta(), 0, accepting_states)

choice = "0"
while (choice != "3"):
    print("Choices:")
    print("(1) Count number of strings of length n in L")
    print("(2) Count number of strings of length n in L'")
    print("(3) Quit")
    choice = getpass("Choice: ")

    if (choice == "1"):
        n = (getpass(f"Value for n (1-300): "))    #n should be between 1-300
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
        n = getpass(f"Value for n (1-300): ")
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


"""
def test(input_string):
    result = dfa.process_input(input_string)
    print(f"Input: {input_string}, Accepted: {result}")

states, accepting_states = build_states()
dfa = DFA(states, alphabet, Delta(), 0, accepting_states)

test("a")
test("b")
test("ab")
test("abcd")
test("abacd")
test("adacd")
test("abaad")
test("ddddd")
test("abbcdd")
test("abacdd")

test("adacdd")
test("bdbcdc")
test("badacdd")
test("abdbcdc")


for n in (1, 5, 6, 7, 10, 100):
    print(f"\nCalculating number of valid strings of length {n}:")
    time1 = time.perf_counter()
    count = countValidStrings(dfa, n)
    time2 = time.perf_counter()
    print(f"Number of valid strings of length {n}: {count}")


print(f"\nSplit string counting:")
for n in (4, 6, 100, 300):
    time1 = time.perf_counter()
    count = countAASplitStrings(dfa, n)
    print(f"\tNumber of valid strings of length {n} that contain 'aa' in the first half: {count}")
    time2 = time.perf_counter()
    print(f"\t\tDuration: {time2 - time1:.6f} seconds")
"""