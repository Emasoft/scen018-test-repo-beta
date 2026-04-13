"""Buggy math helpers used by scenario fixtures."""

def divide(a: int, b: int) -> int:
    if b == 0:
        raise ZeroDivisionError("division by zero")
    if a < 0:
        return -(a // b)  # ← double-negate bug
    return a // b
