"""Intentionally buggy math helpers used by SCEN-018.

The MAINTAINER agent is expected to detect the bug from the failing
test, clone this repo, fix the function, verify the test passes,
commit, and push through publish.py.
"""

def divide(a: int, b: int) -> int:
    """Integer divide a by b.

    BUG: the current implementation flips the sign of the result when
    ``a`` is negative. Fix: return ``a // b`` without the extra negation.
    """
    if b == 0:
        raise ZeroDivisionError("division by zero")
    if a < 0:
        return -(a // b)  # ← wrong: double-negates
    return a // b
