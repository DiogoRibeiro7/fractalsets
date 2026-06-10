"""Tests for the fractal rendering CLI."""

import pytest

from fractalsets.cli import build_parser, main
from fractalsets.core.generators import BurningShipGenerator, JuliaGenerator, MandelbrotGenerator


def test_parser_defaults():
    """CLI parser should expose stable defaults."""
    args = build_parser().parse_args(["--output", "out.png"])

    assert args.fractal == "mandelbrot"
    assert args.width == 800
    assert args.height == 800
    assert args.max_iter == 256
    assert args.cmap == "fractal_default"


def test_main_renders_mandelbrot(monkeypatch):
    """CLI should render and export a Mandelbrot image."""
    exported = {}

    monkeypatch.setattr(
        "fractalsets.cli.export_fractal",
        lambda image, filename, cmap=None, log_scale=None, dpi=None: exported.update(
            {
                "image": image,
                "filename": filename,
                "cmap": cmap,
                "log_scale": log_scale,
                "dpi": dpi,
            }
        ),
    )

    exit_code = main(["--output", "mandelbrot.png"])

    assert exit_code == 0
    assert exported["filename"] == "mandelbrot.png"
    assert exported["cmap"] == "fractal_default"
    assert exported["log_scale"] is True
    assert exported["dpi"] == 300


def test_main_renders_julia(monkeypatch):
    """CLI should require and use a Julia constant for Julia renders."""
    created = {}

    original_init = JuliaGenerator.__init__

    def tracking_init(self, C, width=800, height=800, max_iter=256, smooth=True):
        created["C"] = C
        original_init(self, C, width=width, height=height, max_iter=max_iter, smooth=smooth)

    monkeypatch.setattr(JuliaGenerator, "__init__", tracking_init)
    monkeypatch.setattr(
        "fractalsets.cli.export_fractal",
        lambda *args, **kwargs: None,
    )

    exit_code = main(
        [
            "--fractal",
            "julia",
            "--julia-real",
            "-0.4",
            "--julia-imag",
            "0.6",
            "--output",
            "julia.png",
        ]
    )

    assert exit_code == 0
    assert created["C"] == complex(-0.4, 0.6)


def test_main_renders_burning_ship(monkeypatch):
    """CLI should construct a Burning Ship generator when requested."""
    created = {}

    original_init = BurningShipGenerator.__init__

    def tracking_init(self, width=800, height=800, max_iter=256, smooth=True):
        created["called"] = True
        original_init(self, width=width, height=height, max_iter=max_iter, smooth=smooth)

    monkeypatch.setattr(BurningShipGenerator, "__init__", tracking_init)
    monkeypatch.setattr(
        "fractalsets.cli.export_fractal",
        lambda *args, **kwargs: None,
    )

    exit_code = main(["--fractal", "burning-ship", "--output", "ship.png"])

    assert exit_code == 0
    assert created["called"] is True


def test_main_supports_explicit_bounds(monkeypatch):
    """CLI should support explicit bounds rendering."""
    calls = {}

    original_generate = MandelbrotGenerator.generate

    def tracking_generate(self, **kwargs):
        calls.update(kwargs)
        return original_generate(self, **kwargs)

    monkeypatch.setattr(MandelbrotGenerator, "generate", tracking_generate)
    monkeypatch.setattr(
        "fractalsets.cli.export_fractal",
        lambda *args, **kwargs: None,
    )

    exit_code = main(
        [
            "--output",
            "bounded.png",
            "--xmin",
            "-2.0",
            "--xmax",
            "1.0",
            "--ymin",
            "-1.5",
            "--ymax",
            "1.5",
        ]
    )

    assert exit_code == 0
    assert calls == {"xmin": -2.0, "xmax": 1.0, "ymin": -1.5, "ymax": 1.5}


def test_main_rejects_partial_bounds():
    """CLI should reject incomplete explicit bounds."""
    with pytest.raises(SystemExit):
        main(["--output", "bad.png", "--xmin", "-2.0"])


def test_main_rejects_missing_julia_constant():
    """CLI should reject Julia renders without a constant."""
    with pytest.raises(SystemExit):
        main(["--fractal", "julia", "--output", "julia.png"])
