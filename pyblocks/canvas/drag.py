from dataclasses import dataclass

DRAG_THRESHOLD = 5  # pixels before motion becomes a drag


@dataclass
class DragState:
    block_id: str
    start_x: float
    start_y: float
    offset_x: float
    offset_y: float
    is_dragging: bool = False
