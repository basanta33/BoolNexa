
from digital_logic_lab.kmap_engine import build_kmap
from digital_logic_lab.kmap_renderer import GROUP_COLORS, serialize_kmap


def _cell(serialized, row, column):
    return serialized[0]["rows"][row][column]


def test_kmap_group_outlines_use_distinct_colours_without_fill_metadata():
    result = build_kmap("AB + AC'")
    serialized = serialize_kmap(result)

    colours = {group.index: GROUP_COLORS[group.index - 1] for group in result.groups}
    assert len(set(colours.values())) == len(colours)

    for facet in serialized:
        for row in facet["rows"]:
            for cell in row:
                for outline in cell["outlines"]:
                    assert outline["color"] in colours.values()
                    assert "background" not in outline
                    assert "fill" not in outline
                    assert "zebra" not in outline


def test_overlapping_kmap_groups_are_nested_outlines_not_hatching():
    # m6 is covered by both selected implicants for AB + AC'.
    result = build_kmap("AB + AC'")
    serialized = serialize_kmap(result)

    overlap = None
    for row in serialized[0]["rows"]:
        for cell in row:
            if cell["minterm"] == "m6":
                overlap = cell
                break

    assert overlap is not None
    assert len(overlap["outlines"]) == 2
    assert overlap["outlines"][0]["color"] != overlap["outlines"][1]["color"]
    assert overlap["outlines"][0]["inset"] != overlap["outlines"][1]["inset"]


def test_adjacent_cells_in_same_group_drop_internal_border():
    result = build_kmap("AB")
    serialized = serialize_kmap(result)
    # In a 2-variable map AB is the single m3 cell, so use a 3-variable
    # group with direct horizontal adjacency instead.
    result = build_kmap("AB") if False else build_kmap("AB + ABC'")
    # This expression simplifies to AB and should select the pair m6,m7.
    serialized = serialize_kmap(result)
    m6 = m7 = None
    for row in serialized[0]["rows"]:
        for cell in row:
            if cell["minterm"] == "m6":
                m6 = cell
            elif cell["minterm"] == "m7":
                m7 = cell
    assert m6 is not None and m7 is not None
    # Gray-code columns place m7 and m6 next to one another; their shared
    # edge is omitted from the same group outline.
    o6 = m6["outlines"][0]
    o7 = m7["outlines"][0]
    assert "transparent" in o6["left"] or "transparent" in o6["right"]
    assert "transparent" in o7["left"] or "transparent" in o7["right"]



def _outline_for_group(cell, group_index):
    return next(
        outline for outline in cell["outlines"]
        if outline["group"] == str(group_index)
    )


def test_horizontal_wrap_pair_opens_outward_at_left_and_right_map_edges():
    # AB + AC' selects AC' = {m4,m6}; in the 3-variable Gray-code map those
    # cells occupy the first and last columns of A=1 and wrap left/right.
    result = build_kmap("AB + AC'")
    serialized = serialize_kmap(result)
    wrap_group = next(group for group in result.groups if group.term == "AC'")

    m4 = m6 = None
    for row in serialized[0]["rows"]:
        for cell in row:
            if cell["minterm"] == "m4":
                m4 = cell
            elif cell["minterm"] == "m6":
                m6 = cell

    assert m4 is not None and m6 is not None
    o4 = _outline_for_group(m4, wrap_group.index)
    o6 = _outline_for_group(m6, wrap_group.index)

    # Mano-style wrap: the left fragment opens through the LEFT boundary and
    # the right fragment opens through the RIGHT boundary.
    assert "transparent" in o4["left"]
    assert "solid" in o4["right"]
    assert "solid" in o6["left"]
    assert "transparent" in o6["right"]
    assert o4["wrap_horizontal"] == "true"
    assert o6["wrap_horizontal"] == "true"


def test_vertical_wrap_group_opens_outward_at_top_and_bottom_map_edges():
    # In a 4-variable map B'D' occupies all four physical corners, giving
    # simultaneous top/bottom and left/right wrap adjacency.
    result = build_kmap("B'D' + AA' + CC'")
    serialized = serialize_kmap(result)
    group = result.groups[0]

    cells = {}
    for facet in serialized:
        for row in facet["rows"]:
            for cell in row:
                if cell["value"] == "1":
                    cells[cell["minterm"]] = cell

    assert set(cells) == {"m0", "m2", "m8", "m10"}
    for cell in cells.values():
        outline = _outline_for_group(cell, group.index)
        assert outline["wrap_horizontal"] == "true"
        assert outline["wrap_vertical"] == "true"

    # m0 is the physical top-left corner: open top + left, retain inner sides.
    o0 = _outline_for_group(cells["m0"], group.index)
    assert "transparent" in o0["top"]
    assert "transparent" in o0["left"]
    assert "solid" in o0["right"]
    assert "solid" in o0["bottom"]

    # m10 is the physical bottom-right corner: open bottom + right.
    o10 = _outline_for_group(cells["m10"], group.index)
    assert "transparent" in o10["bottom"]
    assert "transparent" in o10["right"]
    assert "solid" in o10["left"]
    assert "solid" in o10["top"]
