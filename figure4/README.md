# ReCon Figure 4 reproduction

A minimal, physics-based reproduction of Figure 4, *Repeating ground track
altitude as a function of inclinations*, from:

> S. W. Paek, “Reconfigurable Satellite Constellations for Geo-Spatially
> Adaptive Earth Observation Missions” (2020), Figure 4.
> [Open-access paper (Figshare)](https://doi.org/10.6084/m9.figshare.12234656.v1)

The curves are not digitized: each altitude is calculated by solving the
paper's circular-orbit, J2-perturbed repeating-ground-track equations (1) and
(2). Earth constants use km and seconds: `mu = 398600.4418 km³/s²`,
`R_E = 6378.137 km`, `J2 = 1.08262668e-3`, and
`omega_E = 7.292115e-5 rad/s`.

The source paper PDF itself is not included in this repository (copyright);
see the Figshare link above for the open-access original.

## Run

This project uses [uv](https://docs.astral.sh/uv/) for all environment and
dependency management.

```bash
uv sync --all-groups
uv run reproduce-figure4 --output outputs/figure4.png
uv run pytest
```

The output reproduces the original axes (0–180° inclination; 300–1000 km
altitude), four RGT ratios (14, 14.5, 15, 15.5), colours, line styles, and
legend labels.

## Validation

Tests are written first and prioritize orbital constraints over implementation
details. They check published plot anchors, solve Equation (1) back to the
requested RGT ratio, use Hypothesis to check the two physical monotonicities
visible in the figure, and verify render creation.
