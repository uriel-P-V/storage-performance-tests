import pytest
from storage import StorageEngine


@pytest.fixture
def engine():
    e = StorageEngine()
    yield e
    e.reset()


def test_benchmark_write(benchmark, engine):
    """
    Benchmark write operation using pytest-benchmark.
    Runs the operation multiple times and reports statistics.
    """
    result = benchmark(engine.write, "/vol/bench", "data" * 100)
    assert result["duration_ms"] > 0


def test_benchmark_read(benchmark, engine):
    """Benchmark read operation."""
    engine.write("/vol/bench", "data" * 100)
    result = benchmark(engine.read, "/vol/bench")
    assert result["duration_ms"] > 0


def test_benchmark_write_large_payload(benchmark, engine):
    """Benchmark write with large payload — 1MB of data."""
    large_data = "x" * 1_000_000  # 1MB
    result = benchmark(engine.write, "/vol/large", large_data)
    assert result["duration_ms"] > 0