"""Create a pixel-aligned model-over-paper overlay for Paek (2020), Fig. 4.

The paper is CC BY 4.0. `reference/paek_2020.pdf` is its open-access Figshare
copy. The fixed crop is the plot rectangle on PDF page 3 at 180 dpi; keeping
that coordinate system makes the comparison auditable and reproducible.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pymupdf
from PIL import Image, ImageOps

from recon_figure4.figure4 import LINE_STYLES
from recon_figure4.rgt import sample_figure_4

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "reference" / "paek_2020.pdf"
OUTPUT = ROOT / "outputs" / "figure4-overlay.png"
DPI = 180
# Plot-box coordinates in the 180 dpi raster of page 3 (PDF page index 2).
CROP = (365, 768, 1203, 1242)


def original_plot() -> Image.Image:
    document = pymupdf.open(PDF)
    try:
        pixmap = document[2].get_pixmap(dpi=DPI, alpha=False)
        page = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
    finally:
        document.close()
    # Grayscale keeps the original axes, legend, and curves visible beneath
    # the colour model curves rather than concealing one blue/green line with
    # another nearly identical line.
    return ImageOps.grayscale(page.crop(CROP)).convert("RGBA")


def model_layer(width: int, height: int) -> Image.Image:
    figure = plt.figure(figsize=(width / 100, height / 100), dpi=100)
    figure.patch.set_alpha(0)
    # The source plot's top spine is 33 pixels below the crop top; its bottom
    # spine is the crop bottom. Preserve that inset when mapping data values.
    axis = figure.add_axes((0, 0, 1, (height - 33) / height))
    axis.patch.set_alpha(0)
    inclination, curves = sample_figure_4()
    for ratio, altitude in curves.items():
        color, linestyle = LINE_STYLES[ratio]
        axis.plot(inclination, altitude, color=color, linestyle=linestyle, lw=1.2, alpha=0.75)
    axis.set(xlim=(0, 180), ylim=(300, 1000))
    axis.set_axis_off()
    figure.canvas.draw()
    layer = Image.frombuffer(
        "RGBA", figure.canvas.get_width_height(), figure.canvas.buffer_rgba(), "raw", "RGBA", 0, 1
    ).copy()
    plt.close(figure)
    return layer


def main() -> None:
    if not PDF.exists():
        raise FileNotFoundError(f"Missing reference paper: {PDF}")
    paper = original_plot()
    overlay = Image.alpha_composite(paper, model_layer(*paper.size))
    OUTPUT.parent.mkdir(exist_ok=True)
    overlay.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
