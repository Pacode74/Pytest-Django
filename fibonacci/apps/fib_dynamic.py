import sys


def fibonacci_dynamic(n: int) -> int:
    """This implementation is not very space efficient as it takes the whole list.
    This operation cost us total runtime complexity O(n). Because we iterate n times the total space
    complexity runtime for this solution will be O(n^2)"""
    fib_list = [0, 1]
    for i in range(1, n + 1):
        fib_list.append(fib_list[i] + fib_list[i - 1])
        print(fib_list)
        print(f"mem suze of fib_list is: {sys.getsizeof(fib_list)}")
    return fib_list[n]


def fibonacci_dynamic_v2(n: int) -> int:
    """This implementation is very space efficient as it takes only the last two values of the list
    and not the whole list. This operation cost us total runtime complexity O(n). The total space
    complexity runtime for this solution will be O(1) because we're only holding of constant number of
    temporary variables"""
    fib_1, fib_2 = 0, 1
    for i in range(1, n + 1):
        fi = fib_1 + fib_2
        fib_1, fib_2 = fib_2, fi
    return fib_1
