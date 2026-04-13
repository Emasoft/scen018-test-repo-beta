"""Failing test that exercises the divide() sign-flip bug."""
from src.buggy import divide

def test_divide_positive() -> None:
    assert divide(10, 2) == 5

def test_divide_negative_should_be_negative() -> None:
    assert divide(-10, 2) == -5

def test_divide_zero_denominator() -> None:
    import pytest
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
