from __future__ import annotations
import subprocess
import threading
import sys
from pathlib import Path
from typing import Callable

class ProgramRunner:

    def __init__(
        self,
        on_stdout: Callable[[str], None],
        on_stderr: Callable[[str], None],
        on_exit: Callable[[int], None],
    ):
        self._on_stdout = on_stdout
        self._on_stderr = on_stderr
        self._on_exit = on_exit
        self._proc: subprocess.Popen | None = None
        self._threads: list[threading.Thread] = []
        self.is_running = False

    def start(self, script: Path) -> None:
        if self.is_running:
            self.stop()
        self._proc = subprocess.Popen(
            [sys.executable, "-u", str(script)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            bufsize=0,
        )
        self.is_running = True
        t_out = threading.Thread(target=self._drain_stdout, daemon=True)
        t_err = threading.Thread(target=self._drain_stderr, daemon=True)
        t_wait = threading.Thread(target=self._wait_exit, daemon=True)
        self._threads = [t_out, t_err, t_wait]
        for t in self._threads:
            t.start()

    def send_input(self, text: str) -> None:
        if self._proc and self._proc.stdin and self.is_running:
            try:
                self._proc.stdin.write((text + "\n").encode())
                self._proc.stdin.flush()
            except (BrokenPipeError, OSError):
                pass

    def stop(self) -> None:
        if self._proc and self.is_running:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._proc.kill()
        self.is_running = False

    def wait(self, timeout: float = 5.0) -> None:
        if self._proc:
            try:
                self._proc.wait(timeout=timeout)
                import time
                for _ in range(20):
                    if not self.is_running:
                        break
                    time.sleep(0.05)
            except subprocess.TimeoutExpired:
                pass

    def _drain_stdout(self) -> None:
        while True:
            chunk = self._proc.stdout.read(4096)
            if not chunk:
                break
            self._on_stdout(chunk.decode("utf-8", errors="replace"))
        self._proc.stdout.close()

    def _drain_stderr(self) -> None:
        while True:
            line = self._proc.stderr.readline()
            if not line:
                break
            self._on_stderr(line.decode("utf-8", errors="replace").rstrip("\n"))
        self._proc.stderr.close()

    def _wait_exit(self) -> None:
        code = self._proc.wait()
        self.is_running = False
        self._on_exit(code)

import collections

class ConsoleBatcher:
    """
    Collects stdout/stderr lines from background threads and flushes them
    to a tkinter callback in batches, at most once per FLUSH_INTERVAL_MS.
    Prevents flooding the tkinter event loop when a subprocess is verbose.
    """
    FLUSH_INTERVAL_MS = 50

    def __init__(self, tk_widget, on_flush_stdout, on_flush_stderr):
        self._widget = tk_widget          # any tk widget with .after()
        self._on_stdout = on_flush_stdout  # callable(lines: list[tuple[str, int]])
        self._on_stderr = on_flush_stderr  # callable(lines: list[str])
        self._lock = threading.Lock()
        self._stdout_buf: list[tuple[str, int]] = []
        self._stderr_buf: list[str] = []
        self._scheduled = False

    def push_stdout(self, line: str, line_no: int) -> None:
        with self._lock:
            self._stdout_buf.append((line, line_no))
            self._schedule()

    def push_stderr(self, line: str) -> None:
        with self._lock:
            self._stderr_buf.append(line)
            self._schedule()

    def _schedule(self) -> None:
        if not self._scheduled:
            self._scheduled = True
            self._widget.after(self.FLUSH_INTERVAL_MS, self._flush)

    def _flush(self) -> None:
        with self._lock:
            stdout_lines = list(self._stdout_buf)
            stderr_lines = list(self._stderr_buf)
            self._stdout_buf.clear()
            self._stderr_buf.clear()
            self._scheduled = False
        if stdout_lines:
            self._on_stdout(stdout_lines)
        if stderr_lines:
            self._on_stderr(stderr_lines)
