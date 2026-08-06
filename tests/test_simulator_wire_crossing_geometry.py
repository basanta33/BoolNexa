from digital_logic_lab.simulator_wire_geometry import add_crossing_bridges, crossing_points


def _wire(src, d):
    return {"src_key": src, "d": d}


def test_unrelated_horizontal_wire_jumps_over_continuous_vertical_wire():
    wires = [
        _wire("A", "M 100 20 L 100 140"),
        _wire("B", "M 40 80 L 180 80"),
    ]
    add_crossing_bridges(wires)
    assert wires[0]["display_d"] == wires[0]["d"]
    assert " C " in wires[1]["display_d"]
    assert "L 94 80" in wires[1]["display_d"]
    assert "106 80" in wires[1]["display_d"]


def test_same_source_fanout_does_not_create_false_bridge():
    wires = [
        _wire("A", "M 100 20 L 100 140"),
        _wire("A", "M 40 80 L 180 80"),
    ]
    add_crossing_bridges(wires)
    assert wires[1]["display_d"] == wires[1]["d"]


def test_endpoint_touch_is_not_treated_as_non_electrical_crossing():
    wires = [
        _wire("A", "M 100 20 L 100 80"),
        _wire("B", "M 100 80 L 180 80"),
    ]
    assert crossing_points(wires) == {}
