from buildDFA import buildDFA
# from countStrings import countValidStrings, countValidStringsUsingRecurrenceFormula, N, count_strings
from countStrings import *
import time
"""
dfa = buildDFA()

choice = "0"
while (choice != "3"):
    print("Choices:")
    print("(1) Count number of strings of length n in L")
    print("(2) Count number of strings of length n in L'")
    print("(3) Quit")
    choice = input("Choice: ")  #choice should be between 1-300

    if (choice == "1"):
        n = int(input(f"Value for n: "))
        print(f"Number of valid strings in L for {n}:  {countValidStrings(dfa, n)}\n")

    elif (choice == "2"):
        n = int(input(f"Value for n: "))
        print(f"Number of valid strings in L' for {n}:  {countAASplitStrings(dfa, n)}\n")

    elif (choice == "3"):
        print("Quitting...")

    else:
        print("Invalid choice.\n")
"""


def test(input_string):
    result = dfa.process_input(input_string)
    print(f"Input: {input_string}, Accepted: {result}")

dfa = buildDFA()

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
    print(f"Time taken by countValidStrings (dynamic programming): {time2 - time1:.6f} seconds")


time1 = time.perf_counter()
n = 4
print(f"\nCalculating number of valid strings of length {n} that contain 'aa' in the first half:")
count = countAASplitStrings(dfa, n)
print(f"Number of valid strings of length {n} that contain 'aa' in the first half: {count}")
time2 = time.perf_counter()
print(f"Time taken by countAASplitStrings: {time2 - time1:.6f} seconds")
