"""Tests for visualization, animation, and 3D rendering helpers."""

import matplotlib

matplotlib.use("Agg")

import numpy as np
from matplotlib.animation import FuncAnimation

from fractalsets.core.generators import JuliaGenerator, MandelbrotGenerator
from fractalsets.visualization.animator import FractalAnimator, FractalVideoExporter
from fractalsets.visualization.plotters import FractalVisualizer
from fractalsets.visualization.renderer_3d import (
    Fractal3DRenderer,
    StereoscopicRenderer,
)


class TestFractalVisualizer:
    """Test visualization helpers."""

    def test_plot_returns_figure(self):
        """Test plotting a single image returns a configured figure."""
        image = np.random.rand(16, 16) * 100
        visualizer = FractalVisualizer()

        fig = visualizer.plot(
            image,
            title="Test Plot",
            cmap="fractal_default",
            show_colorbar=False,
            show_axes=True,
            bounds=(-2.0, 1.0, -1.5, 1.5),
        )

        assert fig is not None
        assert visualizer.ax.get_title() == "Test Plot"
        assert visualizer.ax.get_xlabel() == "Real Axis"
        assert visualizer.ax.get_ylabel() == "Imaginary Axis"

    def test_plot_comparison_returns_figure(self):
        """Test comparison plotting creates the expected number of axes."""
        images = [np.random.rand(10, 10) for _ in range(4)]
        titles = [f"Image {idx}" for idx in range(4)]
        visualizer = FractalVisualizer()

        fig = visualizer.plot_comparison(images, titles, suptitle="Comparison")

        assert fig is not None
        assert fig._suptitle.get_text() == "Comparison"
        assert len(fig.axes) == 6

    def test_animate_zoom_returns_animation(self, monkeypatch):
        """Test animate_zoom returns a FuncAnimation without showing a window."""
        generator = MandelbrotGenerator(width=20, height=20, max_iter=32)
        visualizer = FractalVisualizer(figsize=(4, 4))

        monkeypatch.setattr("matplotlib.pyplot.show", lambda: None)

        animation = visualizer.animate_zoom(
            generator,
            centre=-0.5 + 0j,
            num_frames=3,
            zoom_factor=1.1,
        )

        assert isinstance(animation, FuncAnimation)


class TestFractalAnimator:
    """Test animation helpers."""

    def test_create_zoom_animation_collects_frames(self, monkeypatch):
        """Test zoom animation prepares the requested number of frames."""
        generator = MandelbrotGenerator(width=20, height=20, max_iter=32)
        animator = FractalAnimator(generator, fps=12)
        captured = {}

        def fake_save(frames, output_path, cmap):
            captured["frames"] = frames
            captured["output_path"] = output_path
            captured["cmap"] = cmap

        monkeypatch.setattr(animator, "_save_animation", fake_save)

        animator.create_zoom_animation(
            target=-0.5 + 0j,
            num_frames=4,
            output_path="zoom.gif",
        )

        assert len(captured["frames"]) == 4
        assert captured["output_path"] == "zoom.gif"
        assert captured["cmap"] == "fractal_default"

    def test_create_julia_morph_collects_frames(self, monkeypatch):
        """Test Julia morph builds the expected number of frames."""
        generator = JuliaGenerator(-0.4 + 0.6j, width=20, height=20, max_iter=32)
        animator = FractalAnimator(generator, fps=12)
        captured = {}

        monkeypatch.setattr(
            animator,
            "_save_animation",
            lambda frames, output_path, cmap: captured.update(
                {"frames": frames, "output_path": output_path, "cmap": cmap}
            ),
        )

        animator.create_julia_morph(
            start_C=-0.4 + 0.6j,
            end_C=-0.8 + 0.156j,
            num_frames=5,
            output_path="morph.gif",
        )

        assert len(captured["frames"]) == 5
        assert captured["output_path"] == "morph.gif"

    def test_create_max_iter_animation_collects_frames(self, monkeypatch):
        """Test max-iteration animation steps through the requested frame count."""
        generator = MandelbrotGenerator(width=20, height=20, max_iter=32)
        animator = FractalAnimator(generator, fps=12)
        captured = {}

        monkeypatch.setattr(
            animator,
            "_save_animation",
            lambda frames, output_path, cmap: captured.update(
                {"frames": frames, "output_path": output_path, "cmap": cmap}
            ),
        )

        animator.create_max_iter_animation(
            centre=-0.5 + 0j,
            L=3.0,
            max_iter_range=(10, 30),
            num_frames=4,
            output_path="iter.gif",
        )

        assert len(captured["frames"]) == 4
        assert generator.max_iter == 30

    def test_save_animation_gif_path(self, monkeypatch):
        """Test saving a GIF animation chooses the Pillow writer path."""
        generator = MandelbrotGenerator(width=20, height=20, max_iter=32)
        animator = FractalAnimator(generator, fps=12)
        frames = [np.random.rand(10, 10), np.random.rand(10, 10)]
        saved = {}

        def fake_save(self, output_path, writer=None, dpi=None):
            saved["output_path"] = output_path
            saved["writer"] = writer
            saved["dpi"] = dpi

        monkeypatch.setattr("matplotlib.animation.FuncAnimation.save", fake_save)

        animator._save_animation(frames, "test.gif", "fractal_default")

        assert saved["output_path"] == "test.gif"
        assert saved["dpi"] == animator.dpi

    def test_create_journey_collects_frames(self, monkeypatch):
        """Test video exporter journey delegates with generated frames."""
        generator = MandelbrotGenerator(width=20, height=20, max_iter=32)
        captured = {}

        def fake_save(self, frames, output_path, cmap):
            captured["frames"] = frames
            captured["output_path"] = output_path
            captured["cmap"] = cmap

        monkeypatch.setattr(FractalAnimator, "_save_animation", fake_save)

        FractalVideoExporter.create_journey(
            waypoints=[(-0.5 + 0j, 3.0), (-0.75 + 0.1j, 0.5)],
            generator=generator,
            output_path="journey.gif",
            frames_between=4,
            fps=10,
        )

        assert len(captured["frames"]) == 4
        assert captured["output_path"] == "journey.gif"


class Test3DRenderers:
    """Test 3D rendering helpers."""

    def test_render_height_map_returns_figure(self):
        """Test height map rendering returns a figure."""
        image = np.random.rand(12, 12) * 100
        renderer = Fractal3DRenderer(figsize=(4, 4))

        fig = renderer.render_height_map(image, show_wireframe=False)

        assert fig is not None
        assert fig.axes[0].get_title() == "3D Height Map of Fractal"

    def test_render_cross_sections_returns_figure(self):
        """Test cross-section rendering returns a figure."""
        image = np.random.rand(12, 12) * 100
        renderer = Fractal3DRenderer(figsize=(4, 4))

        fig = renderer.render_cross_sections(image, num_levels=4)

        assert fig is not None
        assert fig.axes[0].get_title() == "Cross-Section Stack View"

    def test_render_mandelbulb_returns_figure(self):
        """Test Mandelbulb rendering works at a small resolution."""
        renderer = Fractal3DRenderer(figsize=(4, 4))

        fig = renderer.render_mandelbulb(resolution=5, max_iter=4, power=3)

        assert fig is not None
        assert "Mandelbulb" in fig.axes[0].get_title()

    def test_stereoscopic_anaglyph_shape(self):
        """Test stereoscopic renderer returns an RGB image."""
        image = np.random.rand(16, 16) * 100

        anaglyph = StereoscopicRenderer.create_anaglyph(image)

        assert anaglyph.shape == (16, 16, 3)
        assert np.all(anaglyph >= 0)
