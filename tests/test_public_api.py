"""Smoke tests for the documented public API."""

import tempfile
from pathlib import Path

import numpy as np


def test_top_level_package_imports():
    import fractalsets

    assert fractalsets.MandelbrotGenerator is not None
    assert fractalsets.JuliaGenerator is not None
    assert fractalsets.BurningShipGenerator is not None
    assert fractalsets.FractalVisualizer is not None
    assert fractalsets.FractalAnimator is not None
    assert fractalsets.Fractal3DRenderer is not None
    assert fractalsets.launch_gui is not None


def test_documented_submodule_imports():
    from fractalsets.analysis import FractalAnalyzer, OrbitAnalyzer
    from fractalsets.animation import FractalAnimator
    from fractalsets.core.generators import BurningShipGenerator
    from fractalsets.gui import FractalExplorerGUI, launch_gui
    from fractalsets.visualization import Fractal3DRenderer, FractalVisualizer

    assert FractalAnalyzer is not None
    assert OrbitAnalyzer is not None
    assert FractalAnimator is not None
    assert BurningShipGenerator is not None
    assert FractalExplorerGUI is not None
    assert launch_gui is not None
    assert Fractal3DRenderer is not None
    assert FractalVisualizer is not None


def test_export_fractal_accepts_custom_colormap():
    from fractalsets.utils.export import export_fractal

    image = np.random.rand(32, 32) * 256
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "custom_colormap.png"
        export_fractal(image, str(filepath), cmap="fractal_default")
        assert filepath.exists()
        assert filepath.stat().st_size > 0
