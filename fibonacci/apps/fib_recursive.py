def fibonacci_naive(n: int) -> int:
    """Recursive Fibonacci function"""
    if n == 0 or n == 1:
        return n
    return fibonacci_naive(n - 2) + fibonacci_naive(n - 1)
