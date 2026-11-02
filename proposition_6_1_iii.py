"""The instance in the proof of Proposition 6.1 (iii) (Appendix E): exact recursive sparsest cut
omits a member of R_gr(s), although the optimum and the exact RSC hierarchy are both unique."""
from fractions import Fraction
from hierarchies import *

X = frozenset('abcde')
s = similarity({'ab': 3, 'de': 3, 'ac': 2, 'ae': 2, 'ce': 2, 'ad': 1, 'cd': 1})
C = frozenset('ab')


def check_cuts(V, best_side, best_density, next_density):
    """The cut best_side | V - best_side has density best_density, and every other cut of V has
    density at least next_density."""
    V = frozenset(V)
    densities = {frozenset([A, B]): cut_density(s, A, B) for A, B in cuts(V)}
    best = frozenset([frozenset(best_side), V - frozenset(best_side)])
    assert densities[best] == best_density
    assert min(d for cut, d in densities.items() if cut != best) == next_density


check_cuts(X, 'b', Fraction(3, 4), Fraction(5, 6))
check_cuts('acde', 'ac', Fraction(3, 2), Fraction(5, 3))


def exact_rsc(V):
    """Exact recursive sparsest cut on V; asserts that every minimum-density cut is unique."""
    V = frozenset(V)
    if len(V) == 1:
        return {V}
    ranked = sorted(cuts(V), key=lambda cut: cut_density(s, *cut))
    if len(ranked) > 1:
        assert cut_density(s, *ranked[0]) < cut_density(s, *ranked[1]), "a tie between sparsest cuts"
    A, B = ranked[0]
    return {V} | exact_rsc(A) | exact_rsc(B)


rsc = frozenset(exact_rsc(X))
assert proper_nontrivial(rsc, X) == ['ac', 'de', 'acde'] and C not in rsc
print("exact RSC: cuts of densities 3/4 (next 5/6) and 3/2 (next 5/3), unique hierarchy with")
print("  {a,c}, {d,e}, {a,c,d,e}, which omits C = {a,b}")

assert len(hierarchies(X)) == 236
opt, opts, costs = optima(s, X)
assert opt == 46 and len(opts) == 1 and proper_nontrivial(opts[0], X) == ['ab', 'de', 'cde']
print("unique optimum of cost 46 with {a,b}, {d,e}, {c,d,e}")

omitting = [T for T in binary_hierarchies(X) if C not in T]
assert len(omitting) == 90
for T in omitting:
    assert max(cost(T, s, X) - cost(anchor_graft(T, C, r, X)[1], s, X) for r in C) >= 1
assert margin(C, X, s) >= 1 and C in R_gr(s, X)
print("each of the 90 binary hierarchies omitting C has an anchor graft of gain at least 1,")
print("  so mu(C, X) >= 1 and C lies in R_gr(s)")
print("Proposition 6.1 (iii): all claims confirmed")
