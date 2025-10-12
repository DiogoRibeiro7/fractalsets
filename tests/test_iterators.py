"""
Unit tests for core iteration functions.
"""

import pytest
import numpy as np
from fractalsets.core.iterators import (
    mandel_iterate,
    julia_iterate,
    smooth_mandel_iterate,
    smooth_julia_iterate,
    compute_mandelbrot_array,
    compute_julia_array
)


class TestMandelbrotIteration:
    """Test Mandelbrot iteration functions."""
    
    def test_mandel_iterate_origin(self):
        """Test that origin is in Mandelbrot set."""
        result = mandel_iterate(0+0j, max_iter=100)
        assert result == 100, "Origin should be in Mandelbrot set"
    
    def test_mandel_iterate_escape(self):
        """Test that point outside escapes."""
        result = mandel_iterate(2+2j, max_iter=100)
        assert result < 100, "Point at 2+2i should escape"
    
    def test_mandel_iterate_max_iter(self):
        """Test different max_iter values."""
        z = -0.5 + 0.5j
        result1 = mandel_iterate(z, max_iter=50)
        result2 = mandel_iterate(z, max_iter=100)
        assert result1 <= 50
        assert result2 <= 100
    
    def test_smooth_mandel_iterate(self):
        """Test smooth iteration returns float."""
        result = smooth_mandel_iterate(1+1j, max_iter=100)
        assert isinstance(result, float)
        assert result > 0


class TestJuliaIteration:
    """Test Julia iteration functions."""
    
    def test_julia_iterate_simple(self):
        """Test Julia iteration with simple constant."""
        C = -0.4 + 0.6j
        result = julia_iterate(0+0j, C, max_iter=100)
        assert isinstance(result, int)
        assert 0 <= result <= 100
    
    def test_julia_iterate_escape(self):
        """Test point that escapes quickly."""
        C = -0.4 + 0.6j
        result = julia_iterate(2+2j, C, max_iter=100)
        assert result < 10, "Point far from origin should escape quickly"
    
    def test_smooth_julia_iterate(self):
        """Test smooth Julia iteration."""
        C = -0.4 + 0.6j
        result = smooth_julia_iterate(0+0j, C, max_iter=100)
        assert isinstance(result, float)


class TestArrayComputation:
    """Test array computation functions."""
    
    def test_compute_mandelbrot_array_shape(self):
        """Test output array has correct shape."""
        width, height = 100, 100
        result = compute_mandelbrot_array(
            width, height, -2, 1, -1.5, 1.5, max_iter=50
        )
        assert result.shape == (height, width)
    
    def test_compute_mandelbrot_array_values(self):
        """Test output values are in valid range."""
        result = compute_mandelbrot_array(
            50, 50, -2, 1, -1.5, 1.5, max_iter=100
        )
        assert np.all(result >= 0)
        assert np.all(result <= 100)
    
    def test_compute_julia_array_shape(self):
        """Test Julia array has correct shape."""
        width, height = 100, 100
        C = -0.4 + 0.6j
        result = compute_julia_array(
            width, height, -2, 2, -2, 2, C, max_iter=50
        )
        assert result.shape == (height, width)
    
    def test_compute_julia_array_smooth(self):
        """Test smooth Julia array computation."""
        C = -0.4 + 0.6j
        result = compute_julia_array(
            50, 50, -2, 2, -2, 2, C, max_iter=100, smooth=True
        )
        assert result.dtype == np.float64
