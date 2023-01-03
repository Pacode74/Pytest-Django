import pytest
from fibonacci.apps.fib_dynamic import fibonacci_dynamic_v2

## Option 1: Result is the same as option 2. I separated decorator and fixture:
# from fibonacci.apps.track_performance_decorator import track_performance_decorator

## Option 2: Result is the same as option 1. Teacher didn't separate decorator and fixture:
from conftest import track_performance_decorator


@pytest.mark.performance
@track_performance_decorator
def test_performance():
    """1) mark it with performance marker that is registered in pytest.ini.
    2) decorate it track_performance_decorator"""
    # sleep(3)
    fibonacci_dynamic_v2(1000)
