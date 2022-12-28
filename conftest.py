import pytest
from datetime import datetime, timedelta
from typing import Callable


@pytest.fixture
def time_tracker():
    """In order to use the time tracker in our test we need to mark it as a fixture."""
    start = datetime.now()
    yield  # yield and pass the cpu to run the test
    end = datetime.now()
    diff = end - start
    print(f"\n runtime: {diff.total_seconds()}")


class PerformanceException(Exception):
    """Implementation of exception with details of runtime"""

    def __init__(self, runtime: timedelta, limit: timedelta):
        self.runtime = runtime
        self.limit = limit

    def __str__(self) -> str:
        return f"Performance test failed, runtime: {self.runtime.total_seconds()}, limit: {self.limit.total_seconds()}"


def track_performance_decorator(method: Callable, runtime_limit=timedelta(seconds=2)):  # (1)
    """Decorator that check the time performance of a function and
    when runtime limit is exceeded it raises Performance Exception."""

    def run_function_and_validate_runtime(*args, **kwargs):
        start = datetime.now()
        result = method(*args, **kwargs)
        end = datetime.now()
        runtime = end - start
        print(f"\n runtime: {runtime.total_seconds()}")
        # db.add(runtime)  # (2)
        if runtime > runtime_limit:
            raise PerformanceException(runtime=runtime, limit=runtime_limit)
        return result

    return run_function_and_validate_runtime


"""
Notes:
(1) We can configure the runtime limit to be something dynamic so we can define 
dynamically a baseline that's going to be the average of all the runs of all the developers.
And that's going to be our baseline and that's going to be the runtime limit for our test.
That's a very simple example, but that's a very common use case that we can do with 
performance testing.

(2) option to monitor and save into a database the performance results of the tests.
So lets say we have a few developers in our team and we want that for each developer 
that is running our test. We want to save the result of the test in the database.
I mean, the runtime result. So we can just add this functionality in our decorator 
because we implemented it ourselves.

"""
