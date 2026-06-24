from __future__ import annotations
import re as _re
import platform as _platform
import tkinter as tk
from tkinter import font as tkfont
from pyblocks.canvas.model import Block, CanvasModel, MAX_NESTING_DEPTH
from pyblocks.canvas.drag import DragState, DRAG_THRESHOLD

BLOCK_H = 36          # height of a non-container block row
CONTAINER_FOOTER = 8  # height of the closing bar on a container block
H_PAD = 8             # horizontal padding inside block label
INDENT_W = 20         # pixels of indentation per nesting level
BLOCK_W = 300         # default block width (excluding indent)
SEL_OUTLINE = "#f5c2e7"
SEL_WIDTH = 2
_LABEL_FONT = ("Segoe UI", 10, "bold")
_INPUT_FONT = ("Segoe UI", 9)

if _platform.system() != "Windows":
    _LABEL_FONT = ("Helvetica", 10, "bold")
    _INPUT_FONT = ("Helvetica", 9)


def _darken(hex_color: str, amount: int = 40) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r, g, b = max(0, r - amount), max(0, g - amount), max(0, b - amount)
    return f"#{r:02x}{g:02x}{b:02x}"


def _draw_rounded_rect(canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, r: int, **kw) -> int:
    pts = [
        x1+r, y1,   x2-r, y1,
        x2,   y1,   x2,   y1+r,
        x2,   y2-r, x2,   y2,
        x2-r, y2,   x1+r, y2,
        x1,   y2,   x1,   y2-r,
        x1,   y1+r, x1,   y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kw)


def parse_label(label: str) -> list[str | tuple[str, ...]]:
    raw = _re.split(r'\{(\w+)\}', label)
    result = []
    for i, seg in enumerate(raw):
        result.append(seg if i % 2 == 0 else (seg,))
    return result


class CanvasRenderer(tk.Canvas):

    def __init__(self, parent, canvas_model: CanvasModel,
                      on_change=None, on_block_deleted=None, on_select=None, **kwargs):
        kwargs.setdefault("bg", "#1e1e2e")
        kwargs.setdefault("highlightthickness", 0)
        super().__init__(parent, **kwargs)
        self._model = canvas_model
        self.selected_id: str | None = None
        self.block_rects: dict[str, tuple[int, int, int, int]] = {}
        # Maps container_id → (x1, body_top, x2, body_bottom) — the area between
        # the header's bottom edge and the footer's top edge.
        self.container_body_bounds: dict[str, tuple[int, int, int, int]] = {}
        self.bind("<Button-1>", self._on_click)
        self.bind("<Delete>", self._on_delete)
        self.bind("<BackSpace>", self._on_delete)
        self.focus_set()
        self._on_change = on_change
        self._on_block_deleted = on_block_deleted
        self._on_select = on_select
        self._drag: DragState | None = None
        self._lbl_font_obj: tkfont.Font | None = None
        self._inp_font_obj: tkfont.Font | None = None
        self._field_rects: dict[tuple[str, str], tuple[int, int, int, int]] = {}
        self._active_editor: dict | None = None  # {entry, block, field_key, window_id}
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)

    def set_model(self, canvas_model: CanvasModel) -> None:
        self._model = canvas_model
        self.redraw()

    def redraw(self) -> None:
        self.delete("all")
        self.block_rects.clear()
        self.container_body_bounds.clear()
        self._field_rects.clear()
        y = 12
        for block in self._model.blocks:
            y = self._draw_block(block, x=12, y=y, depth=0)
            y += 6

    def _draw_block(self, block: Block, x: int, y: int, depth: int) -> int:
        x_offset = x + depth * INDENT_W
        w = BLOCK_W - depth * INDENT_W
        color = block.color

        if not block.indent:
            x1, y1, x2, y2 = x_offset, y, x_offset + w, y + BLOCK_H
            is_sel = block.id == self.selected_id
            border = _darken(color, 40)
            _draw_rounded_rect(self, x1, y1, x2, y2, r=6,
                               fill=color, outline=border, width=1,
                               tags=("block", block.id))
            if is_sel:
                _draw_rounded_rect(self, x1-1, y1-1, x2+1, y2+1, r=7,
                                   fill="", outline=SEL_OUTLINE, width=SEL_WIDTH,
                                   tags=("block", block.id))
            self._draw_label(block, x1, y1, x2, y2)
            self.block_rects[block.id] = (x1, y1, x2, y2)
            # Render visual-only children (expression sub-blocks for display)
            if block.children:
                bar_x = x_offset + INDENT_W // 2
                child_y = y2 + 2
                for child in block.children:
                    child_y = self._draw_block(child, x=x, y=child_y,
                                               depth=depth + 1) + 2
                self.create_line(bar_x, y2, bar_x, child_y - 2,
                                 fill=color, width=2)
                return child_y - 2
            return y2
        else:
            # Container: header + body + footer
            hx1, hy1, hx2, hy2 = x_offset, y, x_offset + w, y + BLOCK_H
            is_sel = block.id == self.selected_id
            border = _darken(color, 40)
            _draw_rounded_rect(self, hx1, hy1, hx2, hy2, r=6,
                               fill=color, outline=border, width=1,
                               tags=("block", block.id))
            if is_sel:
                _draw_rounded_rect(self, hx1-1, hy1-1, hx2+1, hy2+1, r=7,
                                   fill="", outline=SEL_OUTLINE, width=SEL_WIDTH,
                                   tags=("block", block.id))
            self._draw_label(block, hx1, hy1, hx2, hy2)
            self.block_rects[block.id] = (hx1, hy1, hx2, hy2)
            body_y = hy2

            if depth >= MAX_NESTING_DEPTH - 1:
                # Max depth indicator — no children rendered
                self.create_text(x_offset + INDENT_W + H_PAD, body_y + 10,
                                  text="⛔ max depth", anchor="w",
                                  fill="#f38ba8", font=("Consolas", 9))
                body_y += 24
            else:
                bar_x = x_offset + INDENT_W // 2
                child_y = body_y + 4
                if block.children:
                    for child in block.children:
                        child_y = self._draw_block(child, x=x, y=child_y,
                                                    depth=depth + 1) + 4
                else:
                    # Empty body placeholder
                    _draw_rounded_rect(self, x_offset + INDENT_W, child_y,
                                       x_offset + w - 4, child_y + 20, r=3,
                                       fill="#313244", outline="#45475a",
                                       tags=("drop_target", block.id))
                    child_y += 24
                # Left accent bar
                self.create_line(bar_x, body_y, bar_x, child_y,
                                  fill=color, width=3)
                body_y = child_y

            # Record the body area (between header bottom and footer top) for
            # drop-zone detection — the cursor being here means "insert inside".
            self.container_body_bounds[block.id] = (hx1, hy2, hx2, body_y)

            # Footer bar
            _draw_rounded_rect(self, x_offset, body_y, x_offset + w,
                               body_y + CONTAINER_FOOTER, r=4,
                               fill=color, outline=color)
            return body_y + CONTAINER_FOOTER

    def _draw_label(self, block: Block, x1: int, y1: int, x2: int, y2: int) -> None:
        segments = parse_label(block.label_template)
        cx = x1 + H_PAD
        cy = (y1 + y2) // 2
        pad_x = 4

        if self._lbl_font_obj is None:
            self._lbl_font_obj = tkfont.Font(
                family=_LABEL_FONT[0], size=_LABEL_FONT[1],
                weight=_LABEL_FONT[2] if len(_LABEL_FONT) > 2 else "normal"
            )
        if self._inp_font_obj is None:
            self._inp_font_obj = tkfont.Font(
                family=_INPUT_FONT[0], size=_INPUT_FONT[1]
            )

        for seg in segments:
            if isinstance(seg, str):
                if not seg:
                    continue
                self.create_text(cx, cy, text=seg, fill="white",
                                 font=self._lbl_font_obj, anchor="w",
                                 tags=("block_label", block.id))
                cx += self._lbl_font_obj.measure(seg)
            else:
                field_key = seg[0]
                val = block.inputs.get(field_key, "")
                display = val if val else field_key
                fill_col = "white" if val else "#6c7086"

                text_w = self._inp_font_obj.measure(display)
                pill_w = text_w + pad_x * 2
                pill_h = BLOCK_H - 10
                fx1 = cx
                fy1 = cy - pill_h // 2
                fx2 = cx + pill_w
                fy2 = cy + pill_h // 2
                _draw_rounded_rect(self, fx1, fy1, fx2, fy2, r=3,
                                   fill=_darken(block.color, 30),
                                   outline=_darken(block.color, 50), width=1,
                                   tags=("field_bg", block.id))
                self.create_text(fx1 + pad_x, cy, text=display,
                                 fill=fill_col, font=self._inp_font_obj, anchor="w",
                                 tags=("field_text", block.id, field_key))
                self._field_rects[(block.id, field_key)] = (fx1, fy1, fx2, fy2)
                cx = fx2 + 4

    def _on_click(self, event):
        cx, cy = self.canvasx(event.x), self.canvasy(event.y)
        for block_id, (x1, y1, x2, y2) in reversed(self.block_rects.items()):
            if x1 <= cx <= x2 and y1 <= cy <= y2:
                self._begin_drag(block_id, event.x, event.y)
                return
        self.deselect()

    def _begin_drag(self, block_id: str, cursor_x: int, cursor_y: int) -> None:
        rect = self.block_rects.get(block_id)
        if rect is None:
            return
        self.focus_set()
        x1, y1, _, _ = rect
        self._drag = DragState(
            block_id=block_id,
            start_x=cursor_x,
            start_y=cursor_y,
            offset_x=cursor_x - x1,
            offset_y=cursor_y - y1,
        )
        self.select(block_id)

    @property
    def _drag_state(self):
        # backward-compat alias: old tests read _drag_state["id"]
        if self._drag is None:
            return None
        return {"id": self._drag.block_id, "start_x": self._drag.start_x,
                "start_y": self._drag.start_y}

    def _on_drag(self, event) -> None:
        if self._drag is None:
            return
        dx = abs(event.x - self._drag.start_x)
        dy = abs(event.y - self._drag.start_y)
        if dx < DRAG_THRESHOLD and dy < DRAG_THRESHOLD:
            return
        self._drag.is_dragging = True
        self._draw_drop_indicators(self.canvasx(event.x), self.canvasy(event.y))

    def _draw_drop_indicators(self, cx: int, cy: int) -> None:
        self.delete("drop_indicator")
        zone = self._compute_drop_zone(cx, cy)
        if zone:
            y = zone["y"]
            self.create_line(zone["x1"], y, zone["x2"], y, fill="#f5c2e7",
                             width=2, tags=("drop_indicator",))

    def _compute_drop_zone(self, cx: int, cy: int) -> dict | None:
        """Return the best drop position for the cursor at (cx, cy).

        Strategy: if the cursor is inside any container's body area (between
        its header and its footer), find the nearest child slot in that container.
        Otherwise find the nearest slot among top-level blocks only.
        Innermost container wins when they are nested.
        """
        if self._drag is None:
            return None
        drag_id = self._drag.block_id

        # Find the innermost container body the cursor is inside.
        target_container: str | None = None
        target_depth = -1
        for cid, (bx1, by1, bx2, by2) in self.container_body_bounds.items():
            if cid == drag_id:
                continue
            if bx1 <= cx <= bx2 and by1 <= cy <= by2:
                depth = (bx1 - 12) // INDENT_W
                if depth > target_depth:
                    target_depth = depth
                    target_container = cid

        if target_container is not None:
            return self._zone_in_container(target_container, drag_id, cy)

        return self._zone_top_level(drag_id, cy)

    def _zone_in_container(self, container_id: str, drag_id: str, cy: int) -> dict | None:
        """Nearest insertion slot among direct children of container_id."""
        container, _, _ = self._model.find_block(container_id)
        if container is None:
            return None
        best: dict | None = None
        best_dist = float("inf")
        for child in container.children:
            if child.id == drag_id:
                continue
            rect = self.block_rects.get(child.id)
            if rect is None:
                continue
            x1, y1, x2, y2 = rect
            mid_y = (y1 + y2) // 2
            dist = abs(cy - mid_y)
            if dist < best_dist:
                best_dist = dist
                above = cy < mid_y
                best = {"block_id": child.id, "above": above,
                        "y": y1 if above else y2, "x1": x1, "x2": x2}
        if best is not None:
            return best
        # No eligible children (empty container or only the drag block is inside).
        crect = self.block_rects.get(container_id)
        if crect:
            x1, y1, x2, y2 = crect
            return {"block_id": container_id, "above": False,
                    "y": y2 + 4, "x1": x1 + INDENT_W, "x2": x2,
                    "_into_container": container_id}
        return None

    def _zone_top_level(self, drag_id: str, cy: int) -> dict | None:
        """Nearest insertion slot among top-level blocks (depth 0 only)."""
        best: dict | None = None
        best_dist = float("inf")
        for block_id, (x1, y1, x2, y2) in self.block_rects.items():
            if block_id == drag_id:
                continue
            if (x1 - 12) // INDENT_W != 0:
                continue  # only consider top-level blocks
            mid_y = (y1 + y2) // 2
            dist = abs(cy - mid_y)
            if dist < best_dist:
                best_dist = dist
                above = cy < mid_y
                best = {"block_id": block_id, "y": y1 if above else y2,
                        "above": above, "x1": x1, "x2": x2}
        return best

    def _on_release(self, event) -> None:
        if self._drag is None:
            return
        drag = self._drag
        self.delete("drop_indicator")

        cx, cy = self.canvasx(event.x), self.canvasy(event.y)

        if not drag.is_dragging:
            self._drag = None
            # It was a click — open inline editor if a field was clicked
            if hasattr(self, "_try_open_field_editor"):
                self._try_open_field_editor(cx, cy)
            return

        drag_id = drag.block_id
        zone = self._compute_drop_zone(cx, cy)
        self._drag = None
        if zone is None:
            self.redraw()
            return

        if "_into_container" in zone:
            container_id = zone["_into_container"]
            moved = self._model.move_block(drag_id, container_id, 0)
            self.selected_id = drag_id if moved else None
            self.redraw()
            if moved and self._on_change:
                self._on_change()
            return

        ref_id = zone["block_id"]
        ref_block, ref_parent, ref_idx = self._model.find_block(ref_id)
        target_idx = ref_idx if zone["above"] else ref_idx + 1
        target_parent_id = ref_parent.id if ref_parent else None
        moved = self._model.move_block(drag_id, target_parent_id, target_idx)
        self.selected_id = drag_id if moved else None
        self.redraw()
        if moved and self._on_change:
            self._on_change()

    def _commit_drag(self, drop_parent_id: str | None, drop_index: int) -> None:
        """Programmatic drop — for testing."""
        if self._drag is None:
            return
        block_id = self._drag.block_id
        self._drag = None
        moved = self._model.move_block(block_id, drop_parent_id, drop_index)
        self.selected_id = block_id if moved else None
        self.redraw()
        if moved and self._on_change:
            self._on_change()

    def select(self, block_id: str) -> None:
        self.selected_id = block_id
        self.redraw()
        if self._on_select:
            self._on_select(block_id)

    def deselect(self) -> None:
        self.selected_id = None
        self.redraw()

    def _on_delete(self, _event):
        if self.selected_id:
            self._model.remove_block(self.selected_id)
            self.selected_id = None
            self.redraw()
            if self._on_change:
                self._on_change()

    def _try_open_field_editor(self, cx: int, cy: int) -> None:
        if self._active_editor is not None:
            self._commit_edit()

        for (block_id, field_key), (fx1, fy1, fx2, fy2) in self._field_rects.items():
            if fx1 <= cx <= fx2 and fy1 <= cy <= fy2:
                block, _, _ = self._model.find_block(block_id)
                if block is None:
                    return
                field_cx = (fx1 + fx2) // 2
                field_cy = (fy1 + fy2) // 2
                field_w = max(fx2 - fx1, 60)

                entry = tk.Entry(self, font=_INPUT_FONT,
                                 bg=_darken(block.color, 30),
                                 fg="white", insertbackground="white",
                                 relief="flat", bd=0)
                entry.insert(0, block.inputs.get(field_key, ""))
                entry.select_range(0, "end")

                window_id = self.create_window(field_cx, field_cy,
                                               window=entry, width=field_w)
                entry.focus_set()

                self._active_editor = {
                    "entry": entry,
                    "block": block,
                    "field_key": field_key,
                    "window_id": window_id,
                }

                entry.bind("<Return>", lambda _: self._commit_edit())
                entry.bind("<Escape>", lambda _: self._cancel_edit())
                entry.bind("<FocusOut>", lambda _: self._commit_edit())
                return

    def _commit_edit(self) -> None:
        if self._active_editor is None:
            return
        ed = self._active_editor
        self._active_editor = None
        val = ed["entry"].get()
        ed["entry"].destroy()
        self.delete(ed["window_id"])
        ed["block"].inputs[ed["field_key"]] = val
        self.redraw()
        if self._on_change:
            self._on_change()

    def _cancel_edit(self) -> None:
        if self._active_editor is None:
            return
        ed = self._active_editor
        self._active_editor = None
        ed["entry"].destroy()
        self.delete(ed["window_id"])
        self.redraw()

