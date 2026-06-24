from __future__ import annotations
from pyblocks.blocks.definition import register_block
from pyblocks.inspection.block_factory import BlockFactory
from pyblocks.inspection.package_cache import PackageCache
from pyblocks.inspection.package_scanner import CallableEntry


class PackageLoader:
    @staticmethod
    def load_enabled(enabled_packages: list[str]) -> None:
        for name in enabled_packages:
            data = PackageCache.get(name)
            if data is None:
                continue
            entries = [CallableEntry(**e) for e in data["entries"]]
            defns = BlockFactory.from_entries(entries, data["color"])
            for defn in defns:
                register_block(defn)
