import math

import numpy as np
import pytest
from hypothesis import given, strategies as st

from recon_figure4.rgt import (
    EARTH_RADIUS_KM,
    altitude_for_rgt,
    rgt_ratio,
    sample_figure_4,
)


@pytest.mark.parametrize(
    ("ratio", "inclination_deg", "expected_altitude_km"),
    [
        (14.0, 0.0, 812.4),
        (14.0, 90.0, 874.5),
        (14.0, 180.0, 980.6),
        (14.5, 0.0, 639.6),
        (15.0, 90.0, 547.9),
        (15.5, 180.0, 520.0),
    ],
)
def test_figure_4_anchor_points(ratio, inclination_deg, expected_altitude_km):
    """Digitizable anchors from Paek (2020), Fig. 4 agree within plot precision."""
    assert altitude_for_rgt(ratio, inclination_deg) == pytest.approx(
        expected_altitude_km, abs=1.0
    )


@given(
    ratio=st.floats(min_value=14.0, max_value=15.5, allow_nan=False),
    inclination_deg=st.floats(min_value=0.0, max_value=180.0, allow_nan=False),
)
def test_solved_orbit_satisfies_the_repeating_ground_track_constraint(
    ratio, inclination_deg
):
    altitude = altitude_for_rgt(ratio, inclination_deg)
    achieved = rgt_ratio(EARTH_RADIUS_KM + altitude, inclination_deg)
    assert achieved == pytest.approx(ratio, abs=1e-10)


@given(
    ratio=st.floats(min_value=14.0, max_value=15.5, allow_nan=False),
    low=st.floats(min_value=0.0, max_value=179.0, allow_nan=False),
    delta=st.floats(min_value=0.01, max_value=1.0, allow_nan=False),
)
def test_altitude_increases_with_inclination(ratio, low, delta):
    high = min(180.0, low + delta)
    assert altitude_for_rgt(ratio, high) > altitude_for_rgt(ratio, low)


@given(
    inclination_deg=st.floats(min_value=0.0, max_value=180.0, allow_nan=False),
    low_ratio=st.floats(min_value=14.0, max_value=15.49, allow_nan=False),
    delta=st.floats(min_value=0.01, max_value=0.01, allow_nan=False),
)
def test_altitude_decreases_with_rgt_ratio(inclination_deg, low_ratio, delta):
    assert altitude_for_rgt(low_ratio, inclination_deg) > altitude_for_rgt(
        low_ratio + delta, inclination_deg
    )


def test_figure_data_has_the_paper_series_and_domain():
    inclination, curves = sample_figure_4()
    assert np.array_equal(inclination, np.arange(0.0, 181.0, 1.0))
    assert tuple(curves) == (14.0, 14.5, 15.0, 15.5)
    assert all(values.shape == inclination.shape for values in curves.values())


@pytest.mark.parametrize("bad_ratio", [0.0, -1.0, math.inf, math.nan])
def test_invalid_ratios_are_rejected(bad_ratio):
    with pytest.raises(ValueError):
        altitude_for_rgt(bad_ratio, 45.0)
