"""Example 3.2 and its details in Appendix C.4.2: s(a,b) = s(b,c) = 3, s(c,d) = 2, all other
similarities zero, on X = {a, b, c, d}.  Enumerates the 26 hierarchies on X."""
from hierarchies import *

X = frozenset('abcd')
s = similarity({'ab': 3, 'bc': 3, 'cd': 2})
cd, bcd = frozenset('cd'), frozenset('bcd')

hs = hierarchies(X)
assert len(hs) == 26
opt, opts, costs = optima(s, X)
assert opt == 2 * 3 + 2 * 2 + 4 * 3 == 22
assert len(opts) == 1 and proper_nontrivial(opts[0], X) == ['ab', 'cd']
print("unique optimum of cost 22 with proper nontrivial clusters {a,b} and {c,d}, so {c,d} is mandatory")

# (2) fails for C = {c,d} with A = {c} and Z = {b}
A, Z = frozenset('c'), frozenset('b')
assert not cut_density(s, A, cd - A) > cut_density(s, A, Z)
assert not robustly_mandatory(cd, X, s)
print("(2) fails with A = {c}, Z = {b}, and {c,d} is not robustly mandatory")

# the only allowed change raises the cost of {b,c} < {b,c,d} from 24 to 25
T = with_trivial(X, 'bc', 'bcd')
assert costs[T] == 2 * 3 + 3 * 2 + 4 * 3 == 24
assert proper_nontrivial(compat(T, cd), X) == ['bcd']
changes = allowed_changes(T, cd, X)
assert len(changes) == 1 and costs[changes[0]] == 2 * 2 + 3 * 3 + 4 * 3 == 25
print("{b,c} < {b,c,d}: cost 24; its only allowed change for {c,d} costs 25")

# every hierarchy that contains {a,b} but not {c,d}
ab = frozenset('ab')
with_ab = [T for T in hs if ab in T and cd not in T]
assert sorted(proper_nontrivial(T, X) for T in with_ab) == [['ab'], ['ab', 'abc'], ['ab', 'abd']]
assert sorted(costs[T] for T in with_ab) == [23, 26, 26]
for T in with_ab:
    assert allowed_changes(T, cd, X) == [opts[0]]
print("the three hierarchies with {a,b} but not {c,d} cost 23, 26, 26; the allowed change gives the optimum")

# {c,d} is not in R_rob(s)
family = R_rob(s, X)
assert cd not in family
print("R_rob(s) has the proper nontrivial members", proper_nontrivial(family, X))
print("Example 3.2 and Appendix C.4.2: all claims confirmed")
