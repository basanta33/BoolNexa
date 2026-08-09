from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "digital_logic_lab"
FEEDBACK_MAILTO = "mailto:boolnexa.sim@gmail.com?subject=BoolNexa%20Feedback"


def test_shared_public_header_exposes_feedback_mailto_link():
    source = (PACKAGE / "ui" / "components.py").read_text(encoding="utf-8")
    assert '"Feedback"' in source
    assert f'href="{FEEDBACK_MAILTO}"' in source


def test_simulator_sidebar_exposes_same_feedback_mailto_link():
    source = (PACKAGE / "digital_logic_lab.py").read_text(encoding="utf-8")
    assert '"Feedback"' in source
    assert f'href="{FEEDBACK_MAILTO}"' in source


def test_feedback_links_are_navigation_only_and_do_not_bind_state_events():
    shared = (PACKAGE / "ui" / "components.py").read_text(encoding="utf-8")
    simulator = (PACKAGE / "digital_logic_lab.py").read_text(encoding="utf-8")

    shared_feedback = shared[shared.index('rx.link(\n                rx.text(\n                    "Feedback"'):shared.index('            width="100%",', shared.index('rx.link(\n                rx.text(\n                    "Feedback"'))]
    simulator_feedback = simulator[simulator.index('rx.link(\n                          "Feedback"'):simulator.index('                      width="100%", spacing="0",', simulator.index('rx.link(\n                          "Feedback"'))]

    for block in (shared_feedback, simulator_feedback):
        assert "on_click=" not in block
        assert "State." not in block


def test_feedback_links_explicitly_stay_in_current_tab_for_mailto():
    shared = (PACKAGE / "ui" / "components.py").read_text(encoding="utf-8")
    simulator = (PACKAGE / "digital_logic_lab.py").read_text(encoding="utf-8")

    shared_start = shared.index('rx.link(\n                rx.text(\n                    "Feedback"')
    shared_block = shared[shared_start:shared.index('            width="100%",', shared_start)]
    simulator_start = simulator.index('rx.link(\n                          "Feedback"')
    simulator_block = simulator[simulator_start:simulator.index('                      width="100%", spacing="0",', simulator_start)]

    for block in (shared_block, simulator_block):
        assert 'target="_self"' in block
        assert 'target="_blank"' not in block
