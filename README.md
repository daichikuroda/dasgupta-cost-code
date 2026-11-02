# dasgupta-cost-code

Enumerations used in the proofs of the paper

> **Partial Optimality in Dasgupta Hierarchical Clustering**
> Daichi Kuroda, Maximilien Dreveton, Matthias Grossglauser, Patrick Thiran

Some examples and constructions in the paper are verified by enumerating all hierarchies on four or
five objects (26 and 236 of them), all binary hierarchies omitting a given set, all grafts, all
ordered partitions, or all cuts. This repository contains these enumerations. Each script checks
every number and property that the paper states for its instance, with exact arithmetic.

## Usage

Python 3.9 or later, standard library only.

```bash
python3 run_all.py              # runs all scripts (a few seconds)
python3 appendix_D4.py          # a single script
```

Each script exits with an `AssertionError` if a claim fails.

## Contents

Numbers of results and equations refer to the version of the paper of 2 November 2026.

| Script | Instance in the paper |
|---|---|
| `example_3_2.py` | Example 3.2 and its details in Appendix C.4.2 |
| `examples_C12_C13.py` | Examples C.12 and C.13 |
| `appendix_D4.py` | The two instances in Appendix D.4 (strict inclusions) |
| `proposition_6_1_iii.py` | The instance in the proof of Proposition 6.1 (iii) in Appendix E |

`hierarchies.py` implements the definitions used by the scripts, as stated in the paper: the
Dasgupta cost, allowed changes and robust mandatoriness (Definition 3.1), the families R_rob(s)
(Definition 3.3), R_gr(s) (Definition 4.2), and R_K(s) (Appendix C.1), grafts (formula (3)) and
anchor grafts (formula (17)), margins (Definition 4.2), profile scores and margins ((20) and (21)),
average linkage, and cut densities for recursive sparsest cut.

## License

MIT, see `LICENSE`.
