import pytest
import time
import statistics

def test_write_performance(engine_with_data):
    
    result = engine_with_data.write("/vol/data/newfile", "new content" * 100)
    assert result["duration_ms"] < 50

def test_read_performance(engine_with_data):
    """Test that reading a file is performant."""
    result = engine_with_data.read("/vol/data/file-005")
    assert result["duration_ms"] < 30

def test_delete_performance(engine_with_data):
    result = engine_with_data.delete("/vol/data/file-003")
    assert result["duration_ms"] < 10

def test_write_returns_duration(engine_with_data):
    result = engine_with_data.write("/vol/data/newfile2", "new content" * 100)
    assert "duration_ms" in result

def test_read_nonexistent_raises_error(engine_with_data):
    with pytest.raises(FileNotFoundError):
        engine_with_data.read("/vol/data/nonexistent")



def test_throughput_writes(engine):
    """Verifica que el sistema puede hacer al menos 50 escrituras en 1 segundo."""
    start = time.perf_counter()
    count = 0

    while (time.perf_counter() - start) < 1.0:  # corre por 1 segundo
        engine.write(f"/vol/file-{count}", f"data-{count}")
        count += 1

    assert count >= 50, f"Solo completó {count} escrituras en 1 segundo"


def test_latency_consistency(engine):
    """
    Verifica que la latencia es consistente — sin picos extremos.
    El percentil 95 debe estar bajo 50ms.
    """
    durations = []

    for i in range(20):
        result = engine.write(f"/vol/file-{i}", f"data-{i}" * 50)
        durations.append(result["duration_ms"])

    avg    = statistics.mean(durations)
    median = statistics.median(durations)
    p95    = sorted(durations)[int(len(durations) * 0.95)]

    print(f"\n  Avg: {avg:.2f}ms | Median: {median:.2f}ms | P95: {p95:.2f}ms")

    assert avg < 20,  f"Promedio muy alto: {avg:.2f}ms"
    assert p95 < 50,  f"P95 muy alto: {p95:.2f}ms"


@pytest.mark.load
def test_load_mixed_operations(engine):
    """
    Simula carga mixta — escrituras y lecturas simultáneas.
    Verifica que el sistema no degrada bajo carga.
    """
    # Escribir datos iniciales
    for i in range(20):
        engine.write(f"/vol/load-{i}", f"payload-{i}" * 100)

    # Medir tiempo de operaciones mixtas
    start = time.perf_counter()

    for i in range(20):
        engine.read(f"/vol/load-{i}")
        engine.write(f"/vol/new-{i}", f"new-data-{i}")

    total_ms = (time.perf_counter() - start) * 1000

    # 40 operaciones mixtas deben completar en menos de 2 segundos
    assert total_ms < 2000, f"Carga mixta tardó {total_ms:.2f}ms"