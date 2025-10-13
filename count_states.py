from buildDFA import buildDFA

dfa = buildDFA()

states = dfa.get_states()
print(f"Number of DFA states: {len(states)}")
print(f"Number of state pairs (excl failed): {(len([s for s in states if s != -1]))**2}")
print(f"Alphabet size: {len(dfa.get_alphabet())}")
print(f"Number of input pairs: {len(dfa.get_alphabet())**2}")
print(f"\nTransition table entries to compute: {len(states)**2 * len(dfa.get_alphabet())**2}")
