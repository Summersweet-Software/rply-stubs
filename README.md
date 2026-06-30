[![PyPI - Downloads](https://img.shields.io/pypi/dm/rply-stubs?style=for-the-badge)](https://pypi.org/project/rply-stubs/)

# RPLY Stubs

A stubs library for [RPLY](https://pypi.org/project/rply/)

# Correctness

This is an independent static analysis of the types being used. This is not the easiest task in a codebase so unmaintained and old (not to say that RPLY doesn't set out to accomplish all that it needs to. It is a well written and complete library from the way I see it.).

This is all to say that the type annotations provided are not always correct but provide a firm guideline in an otherwise untyped library.

# Completeness

| symbol | meaning       |
| ------ | ------------- |
| ⚪     | partial       |
| ❌     | Not worked on |
| ✅     | completed     |

| Module          | Status |
| --------------- | :----: |
| errors          |   ✅   |
| grammar         |   ⚪   |
| lexer           |   ✅   |
| lexergenerator  |   ✅   |
| parser          |   ✅   |
| parsergenerator |   ⚪   |
| token           |   ✅   |
| utils           |   ✅   |

# Difficulties In Completion

This stubs library is made significantly more difficult to complete due to the fact that single-letter naming conventions are used in several places without explanation or comment in to what each variable means.
For example:

```python
# rply/parsergenerator.py
def traverse(x, N, stack, F, X, R, FP):
    ...
```

It is clear that `stack` is some kind of list but what are `x`, `N`, `F`, `X`, `R`, and `FP`?

FP could be a function pointer? But that is just an educated guess.

Many such examples exist in the codebase and are hard to descern. That is also not mentioning the large amount of compounding types with signatures such as `list[dict[tuple[int, str], list[dict[...]]]]`. This is extremely hard to annotate or understand the individual parts of.

Most of the examples come from the `parsergenerator` module which I will personally say is not very readable. I would love if the library author could provide some assistance.
