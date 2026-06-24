from __future__ import annotations
import re

_ID_MARKER = "# __pyblocks_id__:"
_FILE_LINE_RE = re.compile(r'File ".*?", line (\d+)')

class ErrorMapper:

    @staticmethod
    def extract_error_line(stderr: str) -> int | None:
        matches = _FILE_LINE_RE.findall(stderr)
        if not matches:
            return None
        return int(matches[-1])

    @staticmethod
    def find_block_id(source: str, line_no: int) -> str | None:
        lines = source.splitlines()
        # Search from error line upward for nearest __pyblocks_id__
        for i in range(min(line_no - 1, len(lines) - 1), -1, -1):
            line = lines[i]
            idx = line.find(_ID_MARKER)
            if idx != -1:
                return line[idx + len(_ID_MARKER):].strip()
        return None

    @staticmethod
    def map(stderr: str, source: str) -> str | None:
        line_no = ErrorMapper.extract_error_line(stderr)
        if line_no is None:
            return None
        return ErrorMapper.find_block_id(source, line_no)
