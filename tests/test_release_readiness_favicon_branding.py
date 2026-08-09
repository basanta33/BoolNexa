import hashlib
from pathlib import Path
import struct


ROOT = Path(__file__).resolve().parents[1]
FAVICON = ROOT / "assets" / "favicon.ico"


def test_release_favicon_is_a_valid_multisize_branded_icon():
    """The public tab icon must be a real multi-size BoolNexa favicon."""
    payload = FAVICON.read_bytes()
    reserved, image_type, image_count = struct.unpack_from("<HHH", payload)
    assert (reserved, image_type, image_count) == (0, 1, 3)

    sizes = set()
    for index in range(image_count):
        width, height = struct.unpack_from("BB", payload, 6 + index * 16)
        sizes.add((width or 256, height or 256))
    assert sizes == {(16, 16), (32, 32), (48, 48)}

    # Pin the approved favicon so Reflex's purple default cannot silently
    # replace the existing BoolNexa BN-chip artwork in a future release.
    assert hashlib.sha256(payload).hexdigest() == (
        "be952e93c70957a16ea38bc9a13011e064162b390f0ae8506e32d725a5b853e2"
    )
