# tests/codegen/test_debounce.py
import time
import pytest
from pyblocks.codegen.debounce import DebouncedWriter


def test_debounced_writer_fires_after_delay():
    calls = []
    writer = DebouncedWriter(delay=0.05, callback=lambda: calls.append(1))
    writer.schedule()
    time.sleep(0.1)
    assert calls == [1]


def test_debounced_writer_coalesces_rapid_calls():
    calls = []
    writer = DebouncedWriter(delay=0.1, callback=lambda: calls.append(1))
    writer.schedule()
    writer.schedule()
    writer.schedule()
    time.sleep(0.25)
    assert len(calls) == 1


def test_debounced_writer_cancel():
    calls = []
    writer = DebouncedWriter(delay=0.1, callback=lambda: calls.append(1))
    writer.schedule()
    writer.cancel()
    time.sleep(0.2)
    assert calls == []
