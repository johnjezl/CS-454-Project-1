from buildDFA import buildDFA
from buildStates import failed_state
from countStrings import state_length

dfa = buildDFA()
n = 6

count = 0
for p in dfa.get_states():
    if p == failed_state:
        continue

    slen = state_length(p)
    if  slen != min(5, n // 2 - 1):
        continue

    q = dfa.transition(p, 'a')
    if q == failed_state:
        continue
    q = dfa.transition(q, 'a')
    if q == failed_state:
        continue

    count += 1

print(f"Number of times countPairStrings is called for n={n}: {count}")
