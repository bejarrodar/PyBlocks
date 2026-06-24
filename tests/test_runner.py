import time
import pytest
from pathlib import Path
from pyblocks.runner import ProgramRunner


def test_runner_runs_script(tmp_path):
    script = tmp_path / "hello.py"
    script.write_text('print("hello from runner")\n')
    lines = []
    runner = ProgramRunner(on_stdout=lambda l, _: lines.append(l),
                           on_stderr=lambda l: None,
                           on_exit=lambda code: None)
    runner.start(script)
    time.sleep(0.5)
    runner.wait()
    assert any("hello from runner" in l for l in lines)


def test_runner_captures_stderr(tmp_path):
    script = tmp_path / "err.py"
    script.write_text('import sys\nsys.stderr.write("err line\\n")\n')
    errors = []
    runner = ProgramRunner(on_stdout=lambda l, _: None,
                           on_stderr=lambda l: errors.append(l),
                           on_exit=lambda code: None)
    runner.start(script)
    time.sleep(0.5)
    runner.wait()
    assert any("err line" in e for e in errors)


def test_runner_exit_code(tmp_path):
    script = tmp_path / "exit.py"
    script.write_text('raise ValueError("boom")\n')
    codes = []
    runner = ProgramRunner(on_stdout=lambda l, _: None,
                           on_stderr=lambda l: None,
                           on_exit=lambda code: codes.append(code))
    runner.start(script)
    runner.wait()
    assert codes and codes[0] != 0


def test_runner_stop(tmp_path):
    script = tmp_path / "loop.py"
    script.write_text('import time\nwhile True:\n    time.sleep(0.1)\n')
    runner = ProgramRunner(on_stdout=lambda l, _: None,
                           on_stderr=lambda l: None,
                           on_exit=lambda code: None)
    runner.start(script)
    time.sleep(0.2)
    runner.stop()
    time.sleep(0.2)
    assert not runner.is_running


def test_runner_not_running_initially():
    runner = ProgramRunner(on_stdout=lambda l, _: None,
                           on_stderr=lambda l: None,
                           on_exit=lambda code: None)
    assert not runner.is_running
