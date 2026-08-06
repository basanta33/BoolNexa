from digital_logic_lab.academy.models import LAB_PREVIEWS, LEARNING_PATHS


def test_academy_v2_has_learning_paths():
    assert len(LEARNING_PATHS) == 12


def test_academy_v2_has_laboratory_previews():
    # Academy now exposes all seven completed learning-path laboratories
    # through the real autonomous BoolNexa tools.
    assert len(LAB_PREVIEWS) == 7
    assert all(lab.status == "live" for lab in LAB_PREVIEWS)


def test_academy_labs_link_to_real_tools():
    hrefs = {lab.href for lab in LAB_PREVIEWS}
    assert "/" in hrefs
    assert "/tools/boolean" in hrefs
    assert "/tools/circuit" in hrefs
    assert "/tools/number-systems" in hrefs
