from __future__ import annotations
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

_LOG_DIR = Path.home() / ".pyblocks" / "logs"
_LOG_FILE = _LOG_DIR / "pyblocks.log"

_FMT = logging.Formatter(
    "%(asctime)s  %(levelname)-8s  %(name)-28s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_logger(name: str) -> logging.Logger:
    """Return a child logger under the 'pyblocks' hierarchy."""
    return logging.getLogger(f"pyblocks.{name}")


def _setup_root() -> None:
    root = logging.getLogger("pyblocks")
    if root.handlers:
        return
    root.setLevel(logging.DEBUG)

    _LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Rotate at midnight, keep 7 days of backups then delete automatically
    handler = TimedRotatingFileHandler(
        _LOG_FILE,
        when="midnight",
        backupCount=7,
        encoding="utf-8",
        delay=False,
    )
    handler.setFormatter(_FMT)
    root.addHandler(handler)

    root.info("=" * 60)
    root.info("PyBlocks started — log file: %s", _LOG_FILE)


_setup_root()
