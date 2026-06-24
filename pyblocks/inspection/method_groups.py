from __future__ import annotations

def split_methods(methods: list[str]) -> dict[str, list[str]]:
    public, private, dunder = [], [], []
    for m in methods:
        if m.startswith("__") and m.endswith("__"):
            dunder.append(m)
        elif m.startswith("_"):
            private.append(m)
        else:
            public.append(m)
    return {"public": public, "private": private, "dunder": dunder}
