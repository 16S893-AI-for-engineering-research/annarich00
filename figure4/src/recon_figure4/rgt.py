"""Circular, J2-perturbed repeating-ground-track orbit calculations.

Equations (1) and (2) of Paek, *Reconfigurable Satellite Constellations
for Geo-Spatially Adaptive Earth Observation Missions* (2020) are used with
zero eccentricity.  Units are kilometres and seconds throughout.
"""

from __future__ import annotations

import math

import numpy as np

EARTH_RADIUS_KM = 6378.137
EARTH_MU_KM3_S2 = 398600.4418
EARTH_J2 = 1.08262668e-3
EARTH_ROTATION_RAD_S = 7.292115e-5
FIGURE_4_RATIOS = (14.0, 14.5, 15.0, 15.5)


def _validate(ratio: float, inclination_deg: float) -> None:
    if not math.isfinite(ratio) or ratio <= 0:
        raise ValueError("RGT ratio must be a finite positive number")
    if not math.isfinite(inclination_deg) or not 0.0 <= inclination_deg <= 180.0:
        raise ValueError("inclination must be finite and in [0, 180] degrees")


def rgt_ratio(semi_major_axis_km: float, inclination_deg: float) -> float:
    """Return the J2-perturbed RGT ratio for a circular orbit.

    The returned quantity is revolutions per Greenwich nodal day.
    """
    if not math.isfinite(semi_major_axis_km) or semi_major_axis_km <= EARTH_RADIUS_KM:
        raise ValueError("semi-major axis must be finite and outside Earth")
    _validate(1.0, inclination_deg)

    inclination = math.radians(inclination_deg)
    mean_motion = math.sqrt(EARTH_MU_KM3_S2 / semi_major_axis_km**3)
    xi = 3.0 * EARTH_RADIUS_KM**2 * EARTH_J2 / (4.0 * semi_major_axis_km**2)
    sin_squared = math.sin(inclination) ** 2

    delta_mean_motion = xi * mean_motion * (2.0 - 3.0 * sin_squared)
    apsidal_rate = xi * mean_motion * (4.0 - 5.0 * sin_squared)
    nodal_rate = -2.0 * xi * mean_motion * math.cos(inclination)
    return (mean_motion + delta_mean_motion + apsidal_rate) / (
        EARTH_ROTATION_RAD_S - nodal_rate
    )


def altitude_for_rgt(ratio: float, inclination_deg: float) -> float:
    """Solve for circular RGT altitude in km using bracketed bisection.

    The bracket (100--2000 km) deliberately covers every orbit displayed in
    Fig. 4 while excluding an Earth-intersecting numerical solution.
    """
    _validate(ratio, inclination_deg)
    lower = EARTH_RADIUS_KM + 100.0
    upper = EARTH_RADIUS_KM + 2000.0
    lower_ratio = rgt_ratio(lower, inclination_deg)
    upper_ratio = rgt_ratio(upper, inclination_deg)
    if not upper_ratio <= ratio <= lower_ratio:
        raise ValueError(
            "ratio has no solution in the supported 100--2000 km altitude range"
        )

    for _ in range(64):
        midpoint = (lower + upper) / 2.0
        if rgt_ratio(midpoint, inclination_deg) > ratio:
            lower = midpoint
        else:
            upper = midpoint
    return (lower + upper) / 2.0 - EARTH_RADIUS_KM


def sample_figure_4() -> tuple[np.ndarray, dict[float, np.ndarray]]:
    """Return Fig. 4's 0--180 degree sampling and its four RGT curves."""
    inclination = np.arange(0.0, 181.0, 1.0)
    curves = {
        ratio: np.array([altitude_for_rgt(ratio, degree) for degree in inclination])
        for ratio in FIGURE_4_RATIOS
    }
    return inclination, curves
