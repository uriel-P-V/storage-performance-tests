"""
storage_engine.py
-----------------
Simulates storage I/O operations with realistic timing.
This is the System Under Test (SUT) for performance tests.
"""

import time
import random
import hashlib


class StorageEngine:
    """
    Simulates a block storage engine with read/write operations.
    Includes realistic I/O delays to simulate disk behavior.
    """

    # Simulated I/O delays 
    WRITE_DELAY = 0.005   # 5ms base write latency
    READ_DELAY  = 0.002   # 2ms base read latency

    def __init__(self):
        self._store = {}   
        self._stats = {
            "writes": 0,
            "reads":  0,
            "deletes": 0,
        }

    def write(self, path: str, data: str) -> dict:
        """
        Write data to storage path.
        Returns metadata including write duration.
        """
        if not path or not data:
            raise ValueError("path and data are required")

        start = time.perf_counter()

        # Simulate I/O delay
        time.sleep(self.WRITE_DELAY + random.uniform(0, 0.002))

        # Store data with checksum
        checksum = hashlib.md5(data.encode()).hexdigest()
        self._store[path] = {"data": data, "checksum": checksum}
        self._stats["writes"] += 1

        duration_ms = (time.perf_counter() - start) * 1000

        return {
            "path":        path,
            "size_bytes":  len(data.encode()),
            "checksum":    checksum,
            "duration_ms": round(duration_ms, 3),
        }

    def read(self, path: str) -> dict:
        """
        Read data from storage path.
        Returns data with read duration.
        """
        if path not in self._store:
            raise FileNotFoundError(f"Path not found: {path}")

        start = time.perf_counter()

        # Simulate I/O delay
        time.sleep(self.READ_DELAY + random.uniform(0, 0.001))

        entry = self._store[path]
        self._stats["reads"] += 1

        duration_ms = (time.perf_counter() - start) * 1000

        return {
            "path":        path,
            "data":        entry["data"],
            "checksum":    entry["checksum"],
            "duration_ms": round(duration_ms, 3),
        }

    def delete(self, path: str) -> dict:
        """Delete data from storage path."""
        if path not in self._store:
            raise FileNotFoundError(f"Path not found: {path}")

        start = time.perf_counter()
        del self._store[path]
        self._stats["deletes"] += 1
        duration_ms = (time.perf_counter() - start) * 1000

        return {
            "path":        path,
            "duration_ms": round(duration_ms, 3),
        }

    def get_stats(self) -> dict:
        """Return operation counters."""
        return self._stats.copy()

    def reset(self):
        """Reset storage state."""
        self._store.clear()
        self._stats = {"writes": 0, "reads": 0, "deletes": 0}