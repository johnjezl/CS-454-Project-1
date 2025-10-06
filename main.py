from buildDFA import buildDFA
# from countStrings import countValidStrings, countValidStringsUsingRecurrenceFormula, N, count_strings
from countStrings import N, N_recursive

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

#count = countValidStrings(dfa, 6)
#print(f"Number of valid strings of length 6: {count}")

#count = countValidStrings(dfa, 7)
#print(f"Number of valid strings of length 7: {count}")

# count = countValidStringsUsingRecurrenceFormula(dfa, 6)
#print(f"Number of valid strings of length 6: {count}")

#count = countValidStringsUsingRecurrenceFormula(dfa, 7)
#print(f"Number of valid strings of length 7: {count}")

count = N(dfa, 6, 0)
print(f"Number of valid strings of length 6: {count}")

count = N(dfa, 7, 0)
print(f"Number of valid strings of length 7: {count}")

count = N_recursive(dfa, 6, 0)
print(f"Number of valid strings of length 6: {count}")

count = N_recursive(dfa, 7, 0)
print(f"Number of valid strings of length 7: {count}")

#count = count_strings(dfa, 6)
#print(f"Number of valid strings of length 6: {count}")

#count = count_strings(dfa, 7)
#print(f"Number of valid strings of length 7: {count}")