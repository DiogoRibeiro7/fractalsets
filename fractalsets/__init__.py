"""FractalSets package initialization."""

__version__ = "1.0.0"
__author__ = "FractalSets Team"
__all__ = [
    'MandelbrotGenerator',
    'JuliaGenerator',
    'FractalVisualizer',
    'mandel_iterate',
    'julia_iterate',
    'export_fractal',
    'FractalGallery'
]

from .core.generators import MandelbrotGenerator, JuliaGenerator
from .core.iterators import mandel_iterate, julia_iterate
from .visualization.plotters import FractalVisualizer
from .utils.export import export_fractal
from .examples.gallery import FractalGallery
