import pytest
from storage import StorageEngine


@pytest.fixture
def engine():
    """Fresh StorageEngine for each test."""
    e = StorageEngine()
    yield e
    e.reset()


@pytest.fixture
def engine_with_data(engine):
    """StorageEngine with pre-written data."""
    for i in range(10):
        engine.write(f"/vol/data/file-{i:03d}", f"content-{i}" * 100)
    return engine