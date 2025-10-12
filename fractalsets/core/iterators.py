"""Core iteration functions for fractal computation."""

import numpy as np
from numba import jit, prange
from typing import Union, Tuple


@jit(nopython=True)
def mandel_iterate(z_0: complex, max_iter: int = 256, 
                   escape_radius: float = 2.0) -> int:
    """
    Compute iterations before escape for Mandelbrot set.
    """
    z = 0.0 + 0.0j
    for i in range(max_iter):
        z = z * z + z_0
        if z.real * z.real + z.imag * z.imag > escape_radius * escape_radius:
            return i
    return max_iter


@jit(nopython=True)
def julia_iterate(z: complex, C: complex, max_iter: int = 256,
                  escape_radius: float = 2.0) -> int:
    """
    Compute iterations before escape for Julia set.
    """
    for i in range(max_iter):
        z = z * z + C
        if z.real * z.real + z.imag * z.imag > escape_radius * escape_radius:
            return i
    return max_iter


@jit(nopython=True)
def smooth_mandel_iterate(z_0: complex, max_iter: int = 256,
                          escape_radius: float = 2.0) -> float:
    """
    Smooth iteration count for Mandelbrot (better coloring).
    """
    z = 0.0 + 0.0j
    for i in range(max_iter):
        z = z * z + z_0
        if z.real * z.real + z.imag * z.imag > escape_radius * escape_radius:
            log_zn = np.log(z.real * z.real + z.imag * z.imag) / 2
            nu = np.log(log_zn / np.log(2)) / np.log(2)
            return i + 1 - nu
    return float(max_iter)


@jit(nopython=True)
def smooth_julia_iterate(z: complex, C: complex, max_iter: int = 256,
                         escape_radius: float = 2.0) -> float:
    """
    Smooth iteration count for Julia set (better coloring).
    """
    for i in range(max_iter):
        z = z * z + C
        if z.real * z.real + z.imag * z.imag > escape_radius * escape_radius:
            log_zn = np.log(z.real * z.real + z.imag * z.imag) / 2
            nu = np.log(log_zn / np.log(2)) / np.log(2)
            return i + 1 - nu
    return float(max_iter)


@jit(nopython=True, parallel=True)
def compute_mandelbrot_array(width: int, height: int,
                             xmin: float, xmax: float,
                             ymin: float, ymax: float,
                             max_iter: int = 256,
                             smooth: bool = False) -> np.ndarray:
    """
    Compute Mandelbrot set for an image grid.
    """
    image = np.zeros((height, width), dtype=np.float64)
    for i in prange(height):
        y = ymin + (ymax - ymin) * i / (height - 1)
        for j in range(width):
            x = xmin + (xmax - xmin) * j / (width - 1)
            z_0 = complex(x, y)
            image[i, j] = (
                smooth_mandel_iterate(z_0, max_iter)
                if smooth else mandel_iterate(z_0, max_iter)
            )
    return image


@jit(nopython=True, parallel=True)
def compute_julia_array(width: int, height: int,
                        xmin: float, xmax: float,
                        ymin: float, ymax: float,
                        C: complex, max_iter: int = 256,
                        smooth: bool = False) -> np.ndarray:
    """
    Compute Julia set for an image grid.
    """
    image = np.zeros((height, width), dtype=np.float64)
    for i in prange(height):
        y = ymin + (ymax - ymin) * i / (height - 1)
        for j in range(width):
            x = xmin + (xmax - xmin) * j / (width - 1)
            z = complex(x, y)
            image[i, j] = (
                smooth_julia_iterate(z, C, max_iter)
                if smooth else julia_iterate(z, C, max_iter)
            )
    return image
