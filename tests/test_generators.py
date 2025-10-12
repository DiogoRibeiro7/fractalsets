"""
Unit tests for generator classes.
"""

import pytest
import numpy as np
from fractalsets.core.generators import MandelbrotGenerator, JuliaGenerator


class TestMandelbrotGenerator:
    """Test MandelbrotGenerator class."""
    
    def test_initialization(self):
        """Test generator initialization."""
        gen = MandelbrotGenerator(width=400, height=400, max_iter=128)
        assert gen.width == 400
        assert gen.height == 400
        assert gen.max_iter == 128
        assert gen.image is None
    
    def test_generate_with_centre_L(self):
        """Test generation with centre and L parameters."""
        gen = MandelbrotGenerator(width=200, height=200)
        result = gen.generate(centre=-0.5+0j, L=3.0)
        
        assert result is not None
        assert result.shape == (200, 200)
        assert gen.image is not None
    
    def test_generate_with_bounds(self):
        """Test generation with explicit bounds."""
        gen = MandelbrotGenerator(width=200, height=200)
        result = gen.generate(xmin=-2, xmax=1, ymin=-1.5, ymax=1.5)
        
        assert result.shape == (200, 200)
        assert gen.bounds == (-2, 1, -1.5, 1.5)
    
    def test_zoom(self):
        """Test zoom functionality."""
        gen = MandelbrotGenerator(width=200, height=200)
        gen.generate(centre=-0.5+0j, L=3.0)
        
        initial_bounds = gen.bounds
        gen.zoom(centre=-0.5+0j, zoom_factor=2.0)
        
        # After zoom, bounds should be smaller
        new_width = gen.bounds[1] - gen.bounds[0]
        old_width = initial_bounds[1] - initial_bounds[0]
        assert new_width < old_width
    
    def test_normalize_image(self):
        """Test image normalization."""
        gen = MandelbrotGenerator(width=100, height=100)
        gen.generate(centre=-0.5+0j, L=3.0)
        
        normalized = gen.normalize_image(log_scale=True)
        assert np.max(normalized) <= 1.0
        assert np.min(normalized) >= 0.0


class TestJuliaGenerator:
    """Test JuliaGenerator class."""
    
    def test_initialization(self):
        """Test Julia generator initialization."""
        C = -0.4 + 0.6j
        gen = JuliaGenerator(C, width=400, height=400)
        assert gen.C == C
        assert gen.width == 400
    
    def test_generate(self):
        """Test Julia set generation."""
        C = -0.4 + 0.6j
        gen = JuliaGenerator(C, width=200, height=200)
        result = gen.generate(centre=0+0j, L=3.0)
        
        assert result.shape == (200, 200)
        assert gen.image is not None
    
    def test_set_constant(self):
        """Test changing Julia constant."""
        gen = JuliaGenerator(-0.4+0.6j, width=200, height=200)
        
        new_C = -0.8 + 0.156j
        gen.set_constant(new_C)
        assert gen.C == new_C
    
    def test_different_constants(self):
        """Test that different constants produce different images."""
        gen1 = JuliaGenerator(-0.4+0.6j, width=100, height=100)
        gen2 = JuliaGenerator(-0.8+0.156j, width=100, height=100)
        
        img1 = gen1.generate(centre=0+0j, L=3.0)
        img2 = gen2.generate(centre=0+0j, L=3.0)
        
        assert not np.array_equal(img1, img2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
