from buildDFA import buildDFA
# from countStrings import countValidStrings, countValidStringsUsingRecurrenceFormula, N, count_strings
from countStrings import *
import time

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


for n in range(100, 1001, 100):
    print(f"\nCalculating number of valid strings of length {n}:")
    time1 = time.perf_counter()
    count3 = countValidStrings(dfa, n)
    time2 = time.perf_counter()
    print(f"Number of valid strings of length {n}: {count3}")
    print(f"Time taken by countValidStrings (dynamic programming): {time2 - time1:.6f} seconds")
