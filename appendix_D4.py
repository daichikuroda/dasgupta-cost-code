"""Appendix D.4 (strict inclusions): the instances for R_gr(s) strictly inside R_rob(s) and for
R_sp(s) strictly inside R_gr(s)."""
from fractions import Fraction
from itertools import combinations
from hierarchies import *

# ---------------------------------------------------------------- R_gr(s) strictly inside R_rob(s)
X = frozenset('abcde')
s = similarity({'ae': 4, 'ac': 3, 'be': 3, 'de': 3, 'ce': 2, 'ab': 1, 'bc': 1, 'cd': 1})
C = frozenset('ae')
assert len(hierarchies(X)) == 236
opt, opts, costs = optima(s, X)
assert opt == 63 and len(opts) == 1 and proper_nontrivial(opts[0], X) == ['ae', 'ace', 'abce']
assert robustly_mandatory(C, X, s)
assert not robustly_mandatory(frozenset('ace'), X, s) and not robustly_mandatory(frozenset('abce'), X, s)
assert proper_nontrivial(R_rob(s, X), X) == ['ae']
T = with_trivial(X, 'ac', 'de', 'bde')
assert is_binary(T, X) and costs[T] == 66
outer = restrict(T, X - C)
for G in grafts(T, C, X).values():
    assert C in G and restrict(G, X - C) == outer
same_shape = [G for G in hierarchies(X) if C in G and restrict(G, X - C) == outer]
assert len(same_shape) == 7 and min(costs[G] for G in same_shape) >= 67
assert margin(C, X, s) <= 0
assert proper_nontrivial(R_gr(s, X), X) == []
print("R_gr(s) < R_rob(s): unique optimum of cost 63 with {a,e} < {a,c,e} < {a,b,c,e}; R_rob(s) has the")
print("  proper nontrivial member {a,e}; {a,c},{d,e},{b,d,e} costs 66, the seven hierarchies that contain")
print("  {a,e} and induce its outer tree cost at least 67, and R_gr(s) has no proper nontrivial member")

# ---------------------------------------------------------------- R_sp(s) strictly inside R_gr(s)
X = frozenset('abcd')
s = similarity({'ab': 2, 'bc': 4, 'cd': 3})
C = frozenset('bc')
candidates = [frozenset(c) for k in (2, 3) for c in combinations(sorted(X), k)]
assert len(candidates) == 10
xi = {A: profile_margin(A, X, s) for A in candidates}
assert all(v <= 0 for v in xi.values())
assert xi[C] == Fraction(-1, 2) and ('d', [frozenset('c'), frozenset('b')]) in profile_minimizers(C, X, s)
bcd = frozenset('bcd')
assert xi[bcd] == 0 and ('a', [frozenset('b'), frozenset('cd')]) in profile_minimizers(bcd, X, s)
assert [A for A in candidates if xi[A] == max(xi.values())] == [bcd]
assert proper_nontrivial(R_K(s, X), X) == []
omitting = [T for T in binary_hierarchies(X) if C not in T]
assert len(omitting) == 12
for T in omitting:
    assert min(cost(anchor_graft(T, C, r, X)[1], s, X) for r in C) < cost(T, s, X)
assert min(best_gain(T, C, X, s) for T in omitting) == 1
T = with_trivial(X, 'ab', 'cd')
assert cost(T, s, X) == 26 and best_gain(T, C, X, s) == 1
assert sorted(cost(G, s, X) for G in grafts(T, C, X).values()) == [25, 26, 28]
assert margin(C, X, s) == 1 and C in R_gr(s, X)
print("R_sp(s) < R_gr(s): no proper nontrivial cluster is profile-certified (xi({b,c}) = -1/2,")
print("  xi({b,c,d}) = 0 is the largest), so R_K(s) is trivial; the 12 binary hierarchies omitting {b,c}")
print("  each have a strictly cheaper anchor graft, mu({b,c}, X) = 1, and {b,c} lies in R_gr(s)")
print("Appendix D.4: all claims confirmed")
