"""FractalSets package initialization."""

__version__ = "1.0.0"
__author__ = "Diogo Ribeiro"
__all__ = [
    "MandelbrotGenerator",
    "JuliaGenerator",
    "BurningShipGenerator",
    "FractalVisualizer",
    "FractalAnimator",
    "Fractal3DRenderer",
    "StereoscopicRenderer",
    "launch_gui",
    "mandel_iterate",
    "julia_iterate",
    "burning_ship_iterate",
    "export_fractal",
    "FractalGallery",
]

from .core.generators import BurningShipGenerator, JuliaGenerator, MandelbrotGenerator
from .core.iterators import burning_ship_iterate, julia_iterate, mandel_iterate
from .visualization import (
    Fractal3DRenderer,
    FractalAnimator,
    FractalVisualizer,
    StereoscopicRenderer,
)
from .utils.export import export_fractal
from .examples.gallery import FractalGallery


def launch_gui():
    """Launch the GUI without importing tkinter during package import."""
    from .gui import launch_gui as _launch_gui

    return _launch_gui()
