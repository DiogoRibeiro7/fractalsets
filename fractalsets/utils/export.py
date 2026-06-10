"""Export utilities for fractals."""

import numpy as np
from PIL import Image
from typing import Optional
from ..visualization.colormaps import PREDEFINED_COLORMAPS


def export_fractal(image: np.ndarray, filename: str,
                   cmap: Optional[str] = None,
                   log_scale: bool = True,
                   dpi: int = 300):
    """
    Export fractal image to file.
    """
    img = np.log1p(image) if log_scale else image
    img = img / np.max(img) if np.max(img) > 0 else img
    img_8bit = (img * 255).astype(np.uint8)

    if cmap:
        import matplotlib.pyplot as plt
        colormap = PREDEFINED_COLORMAPS.get(cmap)
        if isinstance(colormap, str):
            colormap = plt.get_cmap(colormap)
        elif colormap is None:
            colormap = plt.get_cmap(cmap)
        img_colored = colormap(img_8bit)
        img_colored = (img_colored[:, :, :3] * 255).astype(np.uint8)
        pil_img = Image.fromarray(img_colored)
    else:
        pil_img = Image.fromarray(img_8bit)

    pil_img.save(filename, dpi=(dpi, dpi))
    print(f"Fractal saved to {filename}")
