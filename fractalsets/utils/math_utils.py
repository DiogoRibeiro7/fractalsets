"""Mathematical utilities for fractal analysis."""

import numpy as np
from typing import Tuple


def calculate_fractal_dimension(image: np.ndarray, threshold: float = 0.5) -> float:
    """
    Estimate fractal dimension using box-counting.
    """
    max_value = np.max(image)
    if max_value <= 0:
        return 0.0

    binary = (image > threshold * max_value).astype(int)
    if not np.any(binary):
        return 0.0
    if np.all(binary):
        return 2.0

    max_power = int(np.floor(np.log2(min(binary.shape))))
    if max_power <= 1:
        return float(np.ndim(binary))

    sizes = 2 ** np.arange(1, max_power)
    counts = []
    for size in sizes:
        count = 0
        for i in range(0, binary.shape[0], size):
            for j in range(0, binary.shape[1], size):
                box = binary[i:i+size, j:j+size]
                if np.sum(box) > 0:
                    count += 1
        counts.append(count)

    valid_sizes = []
    valid_counts = []
    for size, count in zip(sizes, counts):
        if count > 0:
            valid_sizes.append(size)
            valid_counts.append(count)

    if len(valid_counts) < 2:
        return 0.0

    coeffs = np.polyfit(np.log(valid_sizes), np.log(valid_counts), 1)
    return float(abs(coeffs[0]))


def find_period(z_0: complex, C: complex, max_iter: int = 1000) -> int:
    """
    Find the period of a point in Julia/Mandelbrot set.
    """
    z = z_0
    trajectory = [z]
    tolerance = 1e-6
    for i in range(max_iter):
        z = z * z + C
        if abs(z) > 2.0:
            return 0
        for period in range(1, min(i + 1, 100)):
            if i >= period and abs(z - trajectory[i - period]) < tolerance:
                return period
        trajectory.append(z)
    return 0


def estimate_julia_area(C: complex, samples: int = 10000) -> float:
    """
    Estimate the area of a Julia set via Monte Carlo.
    """
    from ..core.iterators import julia_iterate
    real_parts = np.random.uniform(-2, 2, samples)
    imag_parts = np.random.uniform(-2, 2, samples)
    in_set = 0
    for re, im in zip(real_parts, imag_parts):
        z = complex(re, im)
        if julia_iterate(z, C, max_iter=100) == 100:
            in_set += 1
    return 16.0 * in_set / samples


def cardioid_test(c: complex) -> bool:
    """
    Test if point is in the main cardioid of Mandelbrot.
    """
    x, y = c.real, c.imag
    p = np.sqrt((x - 0.25)**2 + y**2)
    return x < p - 2*p**2 + 0.25


def bulb_test(c: complex) -> bool:
    """
    Test if point is in the period-2 bulb of Mandelbrot.
    """
    x, y = c.real, c.imag
    return (x + 1)**2 + y**2 < 0.0625
