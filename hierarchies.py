"""Definitions used by the enumerations in the proofs of the paper
"Partial Optimality in Dasgupta Hierarchical Clustering".

Objects are one-letter strings. A cluster is a frozenset of objects. A hierarchy on a ground set L
is a laminar family of nonempty subsets of L that contains L and every singleton; it is stored as a
frozenset of clusters. A similarity is a dict that maps frozenset({x, y}) to a nonnegative integer;
pairs that are not listed have similarity zero. All arithmetic is exact (integers and Fractions).
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product


# ---------------------------------------------------------------- similarities

def similarity(values):
    """{'ab': 3, 'cd': 2} -> similarity dict."""
    return {frozenset(pair): v for pair, v in values.items()}


def sim(s, x, y):
    return s.get(frozenset((x, y)), 0)


def sim_sets(s, A, B):
    """s(A, B), the sum of s(x, y) over x in A and y in B."""
    return sum(sim(s, x, y) for x in A for y in B)


# ---------------------------------------------------------------- hierarchies

def set_partitions(items):
    """All partitions of the list `items` into nonempty blocks."""
    items = list(items)
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in set_partitions(rest):
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]
        yield [[first]] + part


@lru_cache(maxsize=None)
def hierarchies(L):
    """All hierarchies on the frozenset L."""
    L = frozenset(L)
    if len(L) == 1:
        return (frozenset([L]),)
    result = []
    for part in set_partitions(sorted(L)):
        if len(part) < 2:
            continue
        for combo in product(*(hierarchies(frozenset(block)) for block in part)):
            result.append(frozenset([L]).union(*combo))
    return tuple(result)


def is_binary(T, L):
    return len(T) == 2 * len(L) - 1


def binary_hierarchies(L):
    return [T for T in hierarchies(frozenset(L)) if is_binary(T, L)]


def lca(T, A):
    """The smallest cluster of T containing the set A."""
    return min((B for B in T if frozenset(A) <= B), key=len)


def cost(T, s, L):
    """Dasgupta cost of the hierarchy T on L: the sum of s(x,y) |lca_T(x,y)| over the pairs of L."""
    return sum(sim(s, x, y) * len(lca(T, (x, y))) for x, y in combinations(sorted(L), 2))


def restrict(T, A):
    """The hierarchy T|_A = {B cap A : B in T, B cap A nonempty} induced on A."""
    A = frozenset(A)
    return frozenset(B & A for B in T if B & A)


def proper_nontrivial(T, L):
    """The clusters A of T with 2 <= |A| < |L|, as sorted strings (for printing and comparisons)."""
    return sorted((''.join(sorted(A)) for A in T if 2 <= len(A) < len(L)), key=lambda t: (len(t), t))


def clusters(*names):
    return [frozenset(name) for name in names]


def with_trivial(L, *names):
    """The hierarchy on L whose proper nontrivial clusters are the given sets."""
    L = frozenset(L)
    return frozenset([L] + [frozenset([x]) for x in L] + clusters(*names))


def optima(s, L):
    hs = hierarchies(frozenset(L))
    costs = {T: cost(T, s, L) for T in hs}
    opt = min(costs.values())
    return opt, [T for T in hs if costs[T] == opt], costs


# ---------------------------------------------------------------- Definitions 3.1 and 3.3

def compatible(A, C):
    return A <= C or C <= A or not (A & C)


def compat(T, C):
    """compat_C(T), the clusters of T compatible with C."""
    return frozenset(A for A in T if compatible(A, C))


def allowed_changes(T, C, L):
    """The hierarchies on L that contain compat_C(T) and C (Definition 3.1)."""
    required = compat(T, C) | {frozenset(C)}
    return [T2 for T2 in hierarchies(frozenset(L)) if required <= T2]


def robustly_mandatory(C, L, s):
    """Definition 3.1 for C inside L, with the similarity s restricted to L."""
    C, L = frozenset(C), frozenset(L)
    for T in hierarchies(L):
        if C in T:
            continue
        if not min(cost(T2, s, L) for T2 in allowed_changes(T, C, L)) < cost(T, s, L):
            return False
    return True


def inductive_family(L, rule):
    """The family that contains the trivial clusters and every C with 2 <= |C|, C strictly inside a
    member P, and rule(C, P) true (Definitions 3.3 and 4.2, and the family R_K of Appendix C.1)."""
    L = frozenset(L)
    family = {L} | {frozenset([x]) for x in L}
    candidates = [frozenset(c) for k in range(2, len(L)) for c in combinations(sorted(L), k)]
    changed = True
    while changed:
        changed = False
        for P in sorted(family, key=len, reverse=True):
            for C in candidates:
                if C not in family and C < P and rule(C, P):
                    family.add(C)
                    changed = True
    return frozenset(family)


def R_rob(s, L):
    return inductive_family(L, lambda C, P: robustly_mandatory(C, P, s))


# ---------------------------------------------------------------- grafts, anchor grafts, margins (Section 4)

def graft_nodes(T, C, L):
    """The nodes V of the outer tree T|_{L - C} with V inside lca_T(C) - C such that no cluster of T
    disjoint from C strictly contains V (Section 4.1)."""
    C, L = frozenset(C), frozenset(L)
    H = lca(T, C)
    outer = restrict(T, L - C)
    return [V for V in outer if V <= H - C and not any(B > V and not (B & C) for B in T)]


def graft(T, C, V, L):
    """The graft T^V of formula (3)."""
    C, L = frozenset(C), frozenset(L)
    outer = restrict(T, L - C)
    return frozenset({B for B in outer if not B > V}
                     | {B | C for B in outer if B >= V}
                     | restrict(T, C))


def grafts(T, C, L):
    return {V: graft(T, C, V, L) for V in graft_nodes(T, C, L)}


def anchor_graft(T, C, r, L):
    """The anchor graft at the anchor r in C (Appendix B.3): A* is the smallest cluster of T that
    contains r and is not inside C, V_r = A* - C, and the anchor graft is T^{V_r}.  It is compared
    with formula (17)."""
    C = frozenset(C)
    A_star = min((A for A in T if r in A and not A <= C), key=len)
    V_r = A_star - C
    T_r = graft(T, C, V_r, L)
    formula = frozenset({A & C for A in T if A & C}
                        | {A | C for A in T if r in A}
                        | {A - C for A in T if r not in A and A - C})
    assert T_r == formula, "anchor graft differs from formula (17)"
    return V_r, T_r


def best_gain(T, C, L, s):
    """cost(T) - min over the grafts T^V of cost(T^V), all costs for s restricted to L."""
    return cost(T, s, L) - min(cost(G, s, L) for G in grafts(T, C, L).values())


def margin(C, P, s):
    """The margin of C inside P (Definition 4.2)."""
    C, P = frozenset(C), frozenset(P)
    return min(best_gain(T, C, P, s) for T in binary_hierarchies(P) if C not in T)


def R_gr(s, L):
    return inductive_family(L, lambda C, P: margin(C, P, s) > 0)


# ---------------------------------------------------------------- profile scores (Appendix C.1)

def ordered_partitions(C):
    """The ordered partitions of C with at least two blocks."""
    for part in set_partitions(sorted(C)):
        if len(part) >= 2:
            for order in permutations(part):
                yield [frozenset(block) for block in order]


def profile_score(s, C, P, z, pi):
    """The profile score (20) of the ordered partition pi of C for the outsider z, inside P."""
    m = len(C)
    ordered = sum(sim_sets(s, pi[i], pi[j]) - len(pi[j]) * sim_sets(s, pi[i], [z])
                  for i in range(len(pi)) for j in range(i + 1, len(pi)))
    deviation = max(sim_sets(s, frozenset().union(*pi[:k]), [z]) - Fraction(sum(len(B) for B in pi[:k]), m)
                    * sim_sets(s, C, [z]) for k in range(len(pi)))
    return ordered - (len(P) - m - 1) * deviation


def profile_margin(C, P, s):
    """xi(C, P) of (21): the minimum of the profile scores over the outsiders and the ordered
    partitions of C with at least two blocks."""
    C, P = frozenset(C), frozenset(P)
    return min(profile_score(s, C, P, z, pi) for z in P - C for pi in ordered_partitions(C))


def profile_minimizers(C, P, s):
    """The pairs (z, pi) that attain xi(C, P)."""
    C, P = frozenset(C), frozenset(P)
    xi = profile_margin(C, P, s)
    return [(z, pi) for z in sorted(P - C) for pi in ordered_partitions(C) if profile_score(s, C, P, z, pi) == xi]


def R_K(s, L):
    return inductive_family(L, lambda C, P: profile_margin(C, P, s) > 0)


# ---------------------------------------------------------------- average linkage and recursive sparsest cut

def average_linkage_merges(s, L):
    """The merges of average linkage, as (average, merged block, second-largest average); the caller
    checks that the second-largest average is smaller, so that the merge involves no tie."""
    blocks = [frozenset([x]) for x in sorted(L)]
    merges = []
    while len(blocks) > 1:
        averages = sorted(((Fraction(sim_sets(s, A, B), len(A) * len(B)), A, B)
                           for A, B in combinations(blocks, 2)), key=lambda t: t[0], reverse=True)
        best, A, B = averages[0]
        runner_up = averages[1][0] if len(averages) > 1 else None
        merges.append((best, A | B, runner_up))
        blocks = [D for D in blocks if D not in (A, B)] + [A | B]
    return merges


def cuts(V):
    """The cuts A | V - A of V, each listed once."""
    V = sorted(V)
    first, rest = V[0], V[1:]
    for k in range(len(rest)):
        for comb in combinations(rest, k):
            A = frozenset((first,) + comb)
            yield A, frozenset(V) - A


def cut_density(s, A, B):
    return Fraction(sim_sets(s, A, B), len(A) * len(B))
