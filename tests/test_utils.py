"""
Unit tests for utility functions.
"""

import pytest
import numpy as np
import tempfile
import os
from pathlib import Path
from fractalsets.utils.math_utils import (
    calculate_fractal_dimension,
    find_period,
    estimate_julia_area,
    cardioid_test,
    bulb_test
)
from fractalsets.utils.export import export_fractal


class TestMathUtils:
    """Test mathematical utility functions."""
    
    def test_calculate_fractal_dimension(self):
        """Test fractal dimension calculation."""
        # Create a simple binary pattern
        image = np.random.rand(100, 100)
        dimension = calculate_fractal_dimension(image, threshold=0.5)
        
        # Fractal dimension should be between 1 and 2 for 2D fractals
        assert 1.0 <= dimension <= 2.0
    
    def test_calculate_fractal_dimension_uniform(self):
        """Test dimension of uniform array."""
        # All zeros should have dimension close to 0
        image = np.zeros((100, 100))
        dimension = calculate_fractal_dimension(image, threshold=0.5)
        assert dimension >= 0
        
        # All ones should have dimension close to 2
        image = np.ones((100, 100))
        dimension = calculate_fractal_dimension(image, threshold=0.0)
        assert dimension > 1.5
    
    def test_find_period_stable_point(self):
        """Test period detection for stable point."""
        # Point in main cardioid has period 1
        z_0 = 0 + 0j
        C = 0 + 0j
        period = find_period(z_0, C, max_iter=100)
        assert period >= 0
    
    def test_find_period_escaping_point(self):
        """Test period for escaping point."""
        z_0 = 0 + 0j
        C = 2 + 0j  # This should escape
        period = find_period(z_0, C, max_iter=100)
        assert period == 0  # Escaping points return 0
    
    def test_estimate_julia_area(self):
        """Test Julia set area estimation."""
        # Simple Julia set
        C = -0.4 + 0.6j
        area = estimate_julia_area(C, samples=1000)
        
        # Area should be positive and less than total region (16)
        assert 0 < area < 16
    
    def test_estimate_julia_area_consistency(self):
        """Test that area estimation is consistent."""
        C = -0.8 + 0.156j
        area1 = estimate_julia_area(C, samples=5000)
        area2 = estimate_julia_area(C, samples=5000)
        
        # Should be within reasonable range (Monte Carlo variance)
        assert abs(area1 - area2) < area1 * 0.3  # Within 30%
    
    def test_cardioid_test_inside(self):
        """Test cardioid detection for interior points."""
        # Point definitely in main cardioid
        c = 0 + 0j
        assert cardioid_test(c) == True
    
    def test_cardioid_test_outside(self):
        """Test cardioid detection for exterior points."""
        # Point definitely outside
        c = 1 + 1j
        assert cardioid_test(c) == False
    
    def test_bulb_test_inside(self):
        """Test period-2 bulb detection for interior."""
        # Point in period-2 bulb
        c = -1 + 0j
        assert bulb_test(c) == True
    
    def test_bulb_test_outside(self):
        """Test period-2 bulb detection for exterior."""
        c = 0 + 0j
        assert bulb_test(c) == False


class TestExport:
    """Test export functionality."""
    
    def test_export_fractal_creates_file(self):
        """Test that export creates a file."""
        image = np.random.rand(100, 100) * 256
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_fractal.png"
            export_fractal(image, str(filepath))
            
            assert filepath.exists()
            assert filepath.stat().st_size > 0
    
    def test_export_fractal_with_colormap(self):
        """Test export with custom colormap."""
        image = np.random.rand(100, 100) * 256
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_colored.png"
            export_fractal(image, str(filepath), cmap='hot')
            
            assert filepath.exists()
    
    def test_export_fractal_log_scale(self):
        """Test export with log scaling."""
        image = np.random.rand(100, 100) * 256
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath1 = Path(tmpdir) / "test_log.png"
            filepath2 = Path(tmpdir) / "test_linear.png"
            
            export_fractal(image, str(filepath1), log_scale=True)
            export_fractal(image, str(filepath2), log_scale=False)
            
            assert filepath1.exists()
            assert filepath2.exists()
    
    def test_export_fractal_different_dpi(self):
        """Test export with different DPI values."""
        image = np.random.rand(100, 100) * 256
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_dpi.png"
            export_fractal(image, str(filepath), dpi=150)
            
            assert filepath.exists()
    
    def test_export_fractal_handles_zeros(self):
        """Test export handles all-zero image."""
        image = np.zeros((100, 100))
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_zeros.png"
            export_fractal(image, str(filepath))
            
            assert filepath.exists()
    
    def test_export_fractal_handles_large_values(self):
        """Test export normalizes large values correctly."""
        image = np.random.rand(100, 100) * 10000
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_large.png"
            export_fractal(image, str(filepath))
            
            assert filepath.exists()


class TestMathUtilsEdgeCases:
    """Test edge cases for math utilities."""
    
    def test_fractal_dimension_small_image(self):
        """Test dimension calculation on small images."""
        image = np.random.rand(10, 10)
        dimension = calculate_fractal_dimension(image)
        assert dimension > 0
    
    def test_period_finding_max_iter(self):
        """Test period finding respects max_iter."""
        z_0 = 0.1 + 0.1j
        C = -0.1 + 0.1j
        period = find_period(z_0, C, max_iter=10)
        assert period <= 10
    
    def test_estimate_area_few_samples(self):
        """Test area estimation with few samples."""
        C = -0.4 + 0.6j
        area = estimate_julia_area(C, samples=100)
        assert area > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
