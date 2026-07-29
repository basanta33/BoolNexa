from digital_logic_lab.logic_core import get_input_pin_position


def test_mux_2_to_1_select_pin_is_top():
    assert get_input_pin_position("MUX_2_1", 3, 3) == ("top", 60, 0)


def test_demux_1_to_2_select_pin_is_top():
    assert get_input_pin_position("DEMUX_1_2", 2, 2) == ("top", 60, 0)
