"""Examples C.12 and C.13 (Appendix C.4.2).  Enumerates the 236 hierarchies on X = {a, b, c, d, e}."""
from fractions import Fraction
from hierarchies import *

X = frozenset('abcde')
assert len(hierarchies(X)) == 236

# ---------------------------------------------------------------- Example C.12
s = similarity({'ab': 4, 'ad': 3, 'ae': 3, 'bc': 3, 'be': 3, 'cd': 1, 'ce': 1})
ab, abe, abcd = frozenset('ab'), frozenset('abe'), frozenset('abcd')
opt, opts, costs = optima(s, X)
assert opt == 62 and len(opts) == 1 and proper_nontrivial(opts[0], X) == ['ab', 'abe', 'abce']
assert robustly_mandatory(abe, X, s)
assert robustly_mandatory(ab, abe, s)
family = R_rob(s, X)
assert ab in family and abe in family
T = with_trivial(X, 'bc', 'ad', 'abcd')
assert is_binary(T, X) and costs[T] == 67
assert [A for A in compat(T, ab) if 2 <= len(A) < len(X)] == [abcd]
assert min(costs[T2] for T2 in hierarchies(X) if ab in T2 and abcd in T2) == 68
assert not robustly_mandatory(ab, X, s)
print("Example C.12: unique optimum of cost 62 with {a,b} < {a,b,e} < {a,b,c,e}; {a,b,e} is robustly")
print("  mandatory, {a,b} is robustly mandatory for s|_{a,b,e} but not for s; R_rob(s) has the proper")
print("  nontrivial members", proper_nontrivial(family, X))

# ---------------------------------------------------------------- Example C.13
s = similarity({'bd': 4, 'be': 3, 'ce': 3, 'ac': 2, 'ad': 2, 'de': 2})
opt, opts, costs = optima(s, X)
assert opt == 52 and len(opts) == 1 and proper_nontrivial(opts[0], X) == ['ac', 'bd', 'bde']
merges = average_linkage_merges(s, X)
assert [(value, ''.join(sorted(block))) for value, block, _ in merges[:3]] == [(4, 'bd'), (3, 'ce'), (Fraction(5, 4), 'bcde')]
assert all(runner_up is None or runner_up < value for value, _, runner_up in merges), "a tie in average linkage"
assert cut_density(s, 'a', 'bd') == cut_density(s, 'a', 'ce') == 1
al = frozenset([X] + [frozenset([x]) for x in X] + [block for _, block, _ in merges])
assert proper_nontrivial(al, X) == ['bd', 'ce', 'bcde'] and frozenset('ac') not in al
assert frozenset('ac') not in R_rob(s, X)          # as Theorem 3.4 implies
print("Example C.13: unique optimum of cost 52 with {a,c}, {b,d}, {b,d,e}; average linkage merges")
print("  b,d (4), then c,e (3), then {b,d},{c,e} (5/4, against 1 for a), without ties, and omits {a,c}")
print("Examples C.12 and C.13: all claims confirmed")
