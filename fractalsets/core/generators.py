"""High-level generator classes for fractals."""

import numpy as np
from typing import Optional
from .iterators import (
    compute_burning_ship_array,
    compute_julia_array,
    compute_mandelbrot_array,
)


class BaseFractalGenerator:
    """Base class for fractal generators."""
    def __init__(self, width: int = 800, height: int = 800,
                 max_iter: int = 256, smooth: bool = True):
        self.width = width
        self.height = height
        self.max_iter = max_iter
        self.smooth = smooth
        self.image = None
        self.bounds = None

    def get_image(self) -> Optional[np.ndarray]:
        return self.image

    def normalize_image(self, log_scale: bool = True) -> np.ndarray:
        if self.image is None:
            raise ValueError("No image generated yet")
        img = self.image.copy()
        if log_scale:
            img = np.log1p(img)
        img = img / np.max(img) if np.max(img) > 0 else img
        return img


class MandelbrotGenerator(BaseFractalGenerator):
    """Generator for Mandelbrot set fractals."""
    def __init__(self, width: int = 800, height: int = 800,
                 max_iter: int = 256, smooth: bool = True):
        super().__init__(width, height, max_iter, smooth)
        self.default_bounds = (-2.5, 1.0, -1.25, 1.25)

    def generate(self, centre: Optional[complex] = None,
                 L: Optional[float] = None,
                 xmin: Optional[float] = None, xmax: Optional[float] = None,
                 ymin: Optional[float] = None, ymax: Optional[float] = None) -> np.ndarray:
        if xmin is not None and xmax is not None and ymin is not None and ymax is not None:
            self.bounds = (xmin, xmax, ymin, ymax)
        elif centre is not None and L is not None:
            half_L = L / 2.0
            self.bounds = (centre.real - half_L, centre.real + half_L,
                           centre.imag - half_L, centre.imag + half_L)
        else:
            self.bounds = self.default_bounds

        self.image = compute_mandelbrot_array(
            self.width, self.height,
            self.bounds[0], self.bounds[1],
            self.bounds[2], self.bounds[3],
            self.max_iter, self.smooth
        )
        return self.image

    def zoom(self, centre: complex, zoom_factor: float = 2.0) -> np.ndarray:
        if self.bounds is None:
            self.bounds = self.default_bounds
        current_width = self.bounds[1] - self.bounds[0]
        current_height = self.bounds[3] - self.bounds[2]
        new_width = current_width / zoom_factor
        new_height = current_height / zoom_factor
        return self.generate(
            xmin=centre.real - new_width / 2,
            xmax=centre.real + new_width / 2,
            ymin=centre.imag - new_height / 2,
            ymax=centre.imag + new_height / 2
        )


class JuliaGenerator(BaseFractalGenerator):
    """Generator for Julia set fractals."""
    def __init__(self, C: complex, width: int = 800, height: int = 800,
                 max_iter: int = 256, smooth: bool = True):
        super().__init__(width, height, max_iter, smooth)
        self.C = C
        self.default_bounds = (-2.0, 2.0, -2.0, 2.0)

    def generate(self, centre: Optional[complex] = None,
                 L: Optional[float] = None,
                 xmin: Optional[float] = None, xmax: Optional[float] = None,
                 ymin: Optional[float] = None, ymax: Optional[float] = None) -> np.ndarray:
        if xmin is not None and xmax is not None and ymin is not None and ymax is not None:
            self.bounds = (xmin, xmax, ymin, ymax)
        elif centre is not None and L is not None:
            half_L = L / 2.0
            self.bounds = (centre.real - half_L, centre.real + half_L,
                           centre.imag - half_L, centre.imag + half_L)
        else:
            self.bounds = self.default_bounds

        self.image = compute_julia_array(
            self.width, self.height,
            self.bounds[0], self.bounds[1],
            self.bounds[2], self.bounds[3],
            self.C, self.max_iter, self.smooth
        )
        return self.image

    def set_constant(self, C: complex):
        self.C = C

    def zoom(self, centre: complex, zoom_factor: float = 2.0) -> np.ndarray:
        if self.bounds is None:
            self.bounds = self.default_bounds
        current_width = self.bounds[1] - self.bounds[0]
        current_height = self.bounds[3] - self.bounds[2]
        new_width = current_width / zoom_factor
        new_height = current_height / zoom_factor
        return self.generate(
            xmin=centre.real - new_width / 2,
            xmax=centre.real + new_width / 2,
            ymin=centre.imag - new_height / 2,
            ymax=centre.imag + new_height / 2
        )


class BurningShipGenerator(BaseFractalGenerator):
    """Generator for Burning Ship fractals."""

    def __init__(self, width: int = 800, height: int = 800,
                 max_iter: int = 256, smooth: bool = True):
        super().__init__(width, height, max_iter, smooth)
        self.default_bounds = (-2.2, 1.2, -2.5, 1.5)

    def generate(self, centre: Optional[complex] = None,
                 L: Optional[float] = None,
                 xmin: Optional[float] = None, xmax: Optional[float] = None,
                 ymin: Optional[float] = None, ymax: Optional[float] = None) -> np.ndarray:
        if xmin is not None and xmax is not None and ymin is not None and ymax is not None:
            self.bounds = (xmin, xmax, ymin, ymax)
        elif centre is not None and L is not None:
            half_L = L / 2.0
            self.bounds = (centre.real - half_L, centre.real + half_L,
                           centre.imag - half_L, centre.imag + half_L)
        else:
            self.bounds = self.default_bounds

        self.image = compute_burning_ship_array(
            self.width, self.height,
            self.bounds[0], self.bounds[1],
            self.bounds[2], self.bounds[3],
            self.max_iter, self.smooth
        )
        return self.image

    def zoom(self, centre: complex, zoom_factor: float = 2.0) -> np.ndarray:
        if self.bounds is None:
            self.bounds = self.default_bounds
        current_width = self.bounds[1] - self.bounds[0]
        current_height = self.bounds[3] - self.bounds[2]
        new_width = current_width / zoom_factor
        new_height = current_height / zoom_factor
        return self.generate(
            xmin=centre.real - new_width / 2,
            xmax=centre.real + new_width / 2,
            ymin=centre.imag - new_height / 2,
            ymax=centre.imag + new_height / 2
        )
