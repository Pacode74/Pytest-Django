from fibonacci.apps.fib_cached import fibonacci_cached, fibonacci_lru_cached
from fibonacci.apps.fib_recursive import fibonacci_naive
import pytest
from typing import Callable

def test_naive_simple() -> None:
    """Naive testing without parameterized. Without cached."""
    res = fibonacci_naive(n=0)
    assert res == 0

    res = fibonacci_naive(n=1)
    assert res == 1

    res = fibonacci_naive(n=2)
    assert res == 1

    res = fibonacci_naive(n=20)
    assert res == 6765

@pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (2, 1), (20, 6765)])
def test_naive(n: int, expected: int) -> None:
    """Simply testing naive fibonacci without cached using parameterized"""
    res = fibonacci_naive(n=n)
    assert res == expected

@pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (2, 1), (20, 6765)])
def test_fibonacci_cached(n:int, expected:int)-> None:
    """Simply testing fibonacci cached using parameterized"""
    res = fibonacci_cached(n=n)
    assert res == expected

@pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (2, 1), (20, 6765)])
def test_fibonacci_lru_cached(n:int, expected:int)-> None:
    """Simply testing fibonacci_lru_cached using parameterized"""
    res = fibonacci_lru_cached(n=n)
    assert res == expected

@pytest.mark.parametrize("fib_func", [fibonacci_naive, fibonacci_cached, fibonacci_lru_cached])
@pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (2, 1), (20, 6765)])
def test_fibonacci(fib_func: Callable[[int], int], n: int, expected: int)-> None:
    """To avoid duplicating above test codes of test_naive, test_fibonacci_cached and
    test_fibonacci_lru_cached we can test three functions at the same time with
    the same arguments.You can switch above order of @pytest.mark.parameterized then
    the visual result will be different."""
    res = fib_func(n)
    assert res == expected
