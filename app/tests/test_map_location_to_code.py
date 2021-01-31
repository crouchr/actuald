import pytest

import map_location_to_code


# ----------
@pytest.mark.parametrize(
    "location, expected",
    [
        ('Stockcross, UK', 'UKXX0097'),
        ('Portsmouth, UK', 'UKXX0115'),
        ('Random City', 'UNKNOWN')
    ]
)
def test_map_location_to_code(location, expected):
    location_code = map_location_to_code.map_location_to_code(location)
    assert location_code == expected
