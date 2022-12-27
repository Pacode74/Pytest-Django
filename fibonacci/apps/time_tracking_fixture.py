from datetime import datetime
import pytest


@pytest.fixture
def time_tracker():
    """In order to use the time tracker in our test we need to mark it as a fixture."""
    start = datetime.now()
    yield  # yield and pass the cpu to run the test
    end = datetime.now()
    diff = end - start
    print(f"\n runtime: {diff.total_seconds()}")
