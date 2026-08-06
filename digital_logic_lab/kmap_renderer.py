"""Presentation helpers for Mano-style Karnaugh maps.

The renderer keeps cells unfilled. Selected implicants are serialized as
*group-level overlay segments* instead of decorating individual cells. This
is important for textbook K-map geometry: ordinary adjacent groups become one
continuous loop, while wrap-around groups are represented by matching open
segments at opposite map boundaries.
"""

from __future__ import annotations

from .kmap_engine import KMapGroup, KMapResult

GROUP_COLORS: tuple[str, ...] = (
    "#2563EB", "#DC2626", "#D946EF", "#16A34A",
    "#EA580C", "#7C3AED", "#0891B2", "#A16207",
)

CELL_W_REM = 4.9
CELL_H_REM = 4.4
GROUP_INSET_PX = 7
GROUP_LANE_PX = 4
WRAP_EXTEND_PX = 9


def group_color(index: int) -> str:
    return GROUP_COLORS[(index - 1) % len(GROUP_COLORS)]


def _physical_runs(indices: list[int]) -> list[tuple[int, int]]:
    """Return inclusive contiguous runs in physical screen order."""
    if not indices:
        return []
    values = sorted(set(indices))
    runs: list[tuple[int, int]] = []
    start = prev = values[0]
    for value in values[1:]:
        if value == prev + 1:
            prev = value
            continue
        runs.append((start, prev))
        start = prev = value
    runs.append((start, prev))
    return runs


def _facet_group_segments(
    result: KMapResult, group: KMapGroup, facet: int
) -> list[dict[str, str]]:
    cells = [(r, c) for f, r, c in group.cells if f == facet]
    if not cells:
        return []

    rows = sorted({r for r, _ in cells})
    cols = sorted({c for _, c in cells})
    row_runs = _physical_runs(rows)
    col_runs = _physical_runs(cols)

    wraps_h = (
        len(col_runs) > 1 and 0 in cols and (result.columns - 1) in cols
    )
    wraps_v = (
        len(row_runs) > 1 and 0 in rows and (result.rows - 1) in rows
    )

    color = group_color(group.index)
    stroke = f"3px solid {color}"
    none = "0 solid transparent"
    # Give each implicant its own visual lane so overlapping pairing lines
    # remain separately visible instead of sitting on the same pixels.
    lane_inset = GROUP_INSET_PX + ((group.index - 1) % 4) * GROUP_LANE_PX
    segments: list[dict[str, str]] = []

    # A valid implicant is a Cartesian rectangle on the toroidal K-map. Each
    # physical run combination is one visible overlay segment.
    for r0, r1 in row_runs:
        for c0, c1 in col_runs:
            segment_cells = {
                (r, c)
                for r in range(r0, r1 + 1)
                for c in range(c0, c1 + 1)
            }
            if not segment_cells.issubset(set(cells)):
                continue

            open_left = wraps_h and c0 == 0
            open_right = wraps_h and c1 == result.columns - 1
            open_top = wraps_v and r0 == 0
            open_bottom = wraps_v and r1 == result.rows - 1

            # Keep ordinary loops slightly inside the grid. At a wrap edge,
            # extend the horizontal/vertical strokes just beyond the map and
            # omit the outer closing edge. This is the Mano-style visual cue.
            left_px = -WRAP_EXTEND_PX if open_left else lane_inset
            right_px = -WRAP_EXTEND_PX if open_right else lane_inset
            top_px = -WRAP_EXTEND_PX if open_top else lane_inset
            bottom_px = -WRAP_EXTEND_PX if open_bottom else lane_inset

            left = f"calc({c0 * CELL_W_REM}rem + {left_px}px)"
            top = f"calc({r0 * CELL_H_REM}rem + {top_px}px)"
            width = (
                f"calc({(c1 - c0 + 1) * CELL_W_REM}rem"
                f" - {left_px + right_px}px)"
            )
            height = (
                f"calc({(r1 - r0 + 1) * CELL_H_REM}rem"
                f" - {top_px + bottom_px}px)"
            )

            segments.append(
                {
                    "group": str(group.index),
                    "color": color,
                    "left": left,
                    "top": top,
                    "width": width,
                    "height": height,
                    "border_top": none if open_top else stroke,
                    "border_right": none if open_right else stroke,
                    "border_bottom": none if open_bottom else stroke,
                    "border_left": none if open_left else stroke,
                    # Open wrap edges must be square/open at the physical map
                    # boundary. Only inward ends of the bracket are rounded.
                    "radius_top_left": "0px" if (open_left or open_top) else "13px",
                    "radius_top_right": "0px" if (open_right or open_top) else "13px",
                    "radius_bottom_right": "0px" if (open_right or open_bottom) else "13px",
                    "radius_bottom_left": "0px" if (open_left or open_bottom) else "13px",
                    "open_left": "true" if open_left else "false",
                    "open_right": "true" if open_right else "false",
                    "open_top": "true" if open_top else "false",
                    "open_bottom": "true" if open_bottom else "false",
                }
            )
    return segments



def _compat_cell_outline(
    result: KMapResult, group: KMapGroup, facet: int, row: int, column: int, layer: int
) -> dict[str, str]:
    """Legacy per-cell metadata retained for regression/API compatibility.

    The UI no longer draws these fragments; real rendering uses group-level
    ``segments``.
    """
    color = group_color(group.index)
    inset_px = 4 + layer * 5
    stroke = f"3px solid {color}"
    none = "0 solid transparent"
    cells = set(group.cells)
    left_joined = column > 0 and (facet, row, column - 1) in cells
    right_joined = column + 1 < result.columns and (facet, row, column + 1) in cells
    top_joined = row > 0 and (facet, row - 1, column) in cells
    bottom_joined = row + 1 < result.rows and (facet, row + 1, column) in cells
    wraps_h = (facet, row, 0) in cells and (facet, row, result.columns - 1) in cells
    wraps_v = (facet, 0, column) in cells and (facet, result.rows - 1, column) in cells
    return {
        "group": str(group.index), "color": color, "inset": f"{inset_px}px",
        "top_offset": f"{-3 if (row == 0 and wraps_v) else inset_px}px",
        "right_offset": f"{-3 if (column == result.columns - 1 and wraps_h) else inset_px}px",
        "bottom_offset": f"{-3 if (row == result.rows - 1 and wraps_v) else inset_px}px",
        "left_offset": f"{-3 if (column == 0 and wraps_h) else inset_px}px",
        "top": none if top_joined or (row == 0 and wraps_v) else stroke,
        "right": none if right_joined or (column == result.columns - 1 and wraps_h) else stroke,
        "bottom": none if bottom_joined or (row == result.rows - 1 and wraps_v) else stroke,
        "left": none if left_joined or (column == 0 and wraps_h) else stroke,
        # Legacy metadata retained for existing regression tests/API users.
        # Actual UI grouping is drawn by the group-level overlay renderer.
        "radius_top_left": "0px" if ((row == 0 and wraps_v) or (column == 0 and wraps_h) or top_joined or left_joined) else "9px",
        "radius_top_right": "0px" if ((row == 0 and wraps_v) or (column == result.columns - 1 and wraps_h) or top_joined or right_joined) else "9px",
        "radius_bottom_right": "0px" if ((row == result.rows - 1 and wraps_v) or (column == result.columns - 1 and wraps_h) or bottom_joined or right_joined) else "9px",
        "radius_bottom_left": "0px" if ((row == result.rows - 1 and wraps_v) or (column == 0 and wraps_h) or bottom_joined or left_joined) else "9px",
        "wrap_horizontal": "true" if wraps_h else "false",
        "wrap_vertical": "true" if wraps_v else "false",
    }

def cell_matrix(result: KMapResult, facet: int) -> list[list[dict[str, object]]]:
    lookup = {(cell.facet, cell.row, cell.column): cell for cell in result.cells}
    matrix: list[list[dict[str, object]]] = []
    for row in range(result.rows):
        rendered_row: list[dict[str, object]] = []
        for column in range(result.columns):
            cell = lookup[(facet, row, column)]
            memberships = [
                group for group in result.groups
                if (facet, row, column) in group.cells
            ]
            rendered_row.append(
                {
                    "value": cell.value,
                    "minterm": f"m{cell.minterm}",
                    "groups": ", ".join(str(group.index) for group in memberships),
                    # Retained for compatibility with older tests/API consumers.
                    # The UI itself renders facet-level group segments below.
                    "outlines": [
                        _compat_cell_outline(
                            result, group, facet, row, column,
                            next(i for i, g in enumerate(result.groups) if g.index == group.index),
                        )
                        for group in memberships
                    ],
                }
            )
        matrix.append(rendered_row)
    return matrix


def serialize_kmap(result: KMapResult) -> list[dict[str, object]]:
    facets: list[dict[str, object]] = []
    for index, code in enumerate(result.facet_codes):
        segments: list[dict[str, str]] = []
        for group in result.groups:
            segments.extend(_facet_group_segments(result, group, index))
        facets.append(
            {
                "index": index,
                "code": code,
                "rows": cell_matrix(result, index),
                "segments": segments,
            }
        )
    return facets
