"""Render a faithful, reproducible version of Paek (2020), Figure 4."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from .rgt import sample_figure_4


LINE_STYLES = {
    14.0: ("blue", "-"),
    14.5: ("green", "--"),
    15.0: ("red", (0, (1, 3))),
    15.5: ("c", (0, (5, 3, 1, 3))),
}


def render(output: str | Path) -> Path:
    """Render and save Figure 4, returning the resulting path."""
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    inclination, curves = sample_figure_4()

    fig, axis = plt.subplots(figsize=(8.0, 4.75), constrained_layout=True)
    for ratio, altitude in curves.items():
        color, linestyle = LINE_STYLES[ratio]
        axis.plot(
            inclination,
            altitude,
            color=color,
            linestyle=linestyle,
            linewidth=1.5,
            label=f"RGT Ratio = {ratio:g}",
        )

    axis.set_xlim(0, 180)
    axis.set_ylim(300, 1000)
    axis.set_xticks(range(0, 181, 30))
    axis.set_yticks(range(300, 1001, 100))
    axis.set_xlabel("Inclination (deg)")
    axis.set_ylabel("Altitude (km)")
    axis.tick_params(direction="in", top=True, right=True)
    axis.legend(loc="upper left", frameon=True, fancybox=False, edgecolor="black")
    fig.savefig(output, dpi=300)
    plt.close(fig)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce Paek (2020) Figure 4")
    parser.add_argument("--output", default="outputs/figure4.png")
    args = parser.parse_args()
    print(render(args.output))


if __name__ == "__main__":
    main()
