"""Tests for the fractal rendering CLI."""

import pytest

from fractalsets.cli import build_parser, main
from fractalsets.core.generators import JuliaGenerator
from fractalsets.core.generators import BurningShipGenerator, JuliaGenerator, MandelbrotGenerator


def test_parser_defaults():
    """CLI parser should expose stable defaults."""
    args = build_parser().parse_args(["--output", "out.png"])

    assert args.fractal == "mandelbrot"
    assert args.width == 800
    assert args.height == 800
    assert args.max_iter == 256
    assert args.cmap == "fractal_default"
    assert args.output == "out.png"


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


def test_main_lists_presets(capsys):
    """CLI should list presets for the selected fractal type."""
    exit_code = main(["--fractal", "burning-ship", "--list-presets"])

    output = capsys.readouterr().out.strip().splitlines()
    assert exit_code == 0
    assert output == ["classic_ship", "full_set", "harbor"]


def test_main_renders_burning_ship_preset(monkeypatch):
    """CLI should render named presets for preset-aware fractals."""
    calls = {}

    original_generate = BurningShipGenerator.generate

    def tracking_generate(self, **kwargs):
        calls.update(kwargs)
        return original_generate(self, **kwargs)

    monkeypatch.setattr(BurningShipGenerator, "generate", tracking_generate)
    monkeypatch.setattr("fractalsets.cli.export_fractal", lambda *args, **kwargs: None)

    exit_code = main(
        [
            "--fractal",
            "burning-ship",
            "--preset",
            "classic_ship",
            "--output",
            "ship.png",
        ]
    )

    assert exit_code == 0
    assert calls["centre"] == -1.75 - 0.03j
    assert calls["L"] == 0.08


def test_main_renders_julia_preset(monkeypatch):
    """CLI should allow Julia presets instead of explicit constants."""
    created = {}

    original_init = JuliaGenerator.__init__

    def tracking_init(self, C, width=800, height=800, max_iter=256, smooth=True):
        created["C"] = C
        original_init(self, C, width=width, height=height, max_iter=max_iter, smooth=smooth)

    monkeypatch.setattr(JuliaGenerator, "__init__", tracking_init)
    monkeypatch.setattr("fractalsets.cli.export_fractal", lambda *args, **kwargs: None)

    exit_code = main(
        [
            "--fractal",
            "julia",
            "--preset",
            "dragon",
            "--output",
            "dragon.png",
        ]
    )

    assert exit_code == 0
    assert created["C"] == -0.8 + 0.156j


def test_main_rejects_unknown_preset():
    """CLI should reject presets that are not valid for the chosen fractal."""
    with pytest.raises(SystemExit):
        main(["--fractal", "mandelbrot", "--preset", "dragon", "--output", "out.png"])


def test_main_requires_output_for_rendering():
    """CLI should still require an output path for rendering commands."""
    with pytest.raises(SystemExit):
        main([])


def test_main_runs_zoom_animation(monkeypatch):
    """CLI should dispatch zoom animations to the animator."""
    calls = {}

    monkeypatch.setattr(
        "fractalsets.cli.FractalAnimator.create_zoom_animation",
        lambda self, target, num_frames, zoom_factor, start_L, output_path, cmap: calls.update(
            {
                "target": target,
                "num_frames": num_frames,
                "zoom_factor": zoom_factor,
                "start_L": start_L,
                "output_path": output_path,
                "cmap": cmap,
            }
        ),
    )

    exit_code = main(
        [
            "--animate",
            "zoom",
            "--output",
            "zoom.gif",
            "--frames",
            "12",
            "--zoom-factor",
            "1.2",
        ]
    )

    assert exit_code == 0
    assert calls["target"] == -0.5 + 0j
    assert calls["num_frames"] == 12
    assert calls["zoom_factor"] == 1.2
    assert calls["start_L"] == 3.0
    assert calls["output_path"] == "zoom.gif"


def test_main_runs_zoom_animation_for_preset(monkeypatch):
    """CLI zoom animation should use preset view parameters when present."""
    calls = {}

    monkeypatch.setattr(
        "fractalsets.cli.FractalAnimator.create_zoom_animation",
        lambda self, target, num_frames, zoom_factor, start_L, output_path, cmap: calls.update(
            {
                "target": target,
                "start_L": start_L,
                "output_path": output_path,
            }
        ),
    )

    exit_code = main(
        [
            "--fractal",
            "burning-ship",
            "--preset",
            "classic_ship",
            "--animate",
            "zoom",
            "--output",
            "ship_zoom.gif",
        ]
    )

    assert exit_code == 0
    assert calls["target"] == -1.75 - 0.03j
    assert calls["start_L"] == 0.08
    assert calls["output_path"] == "ship_zoom.gif"


def test_main_runs_julia_morph_animation(monkeypatch):
    """CLI should dispatch Julia morph animations with start and end constants."""
    calls = {}

    monkeypatch.setattr(
        "fractalsets.cli.FractalAnimator.create_julia_morph",
        lambda self, start_C, end_C, num_frames, output_path, cmap: calls.update(
            {
                "start_C": start_C,
                "end_C": end_C,
                "num_frames": num_frames,
                "output_path": output_path,
                "cmap": cmap,
            }
        ),
    )

    exit_code = main(
        [
            "--fractal",
            "julia",
            "--julia-real",
            "-0.4",
            "--julia-imag",
            "0.6",
            "--animate",
            "julia-morph",
            "--julia-end-real",
            "-0.8",
            "--julia-end-imag",
            "0.156",
            "--frames",
            "8",
            "--output",
            "morph.gif",
        ]
    )

    assert exit_code == 0
    assert calls["start_C"] == -0.4 + 0.6j
    assert calls["end_C"] == -0.8 + 0.156j
    assert calls["num_frames"] == 8
    assert calls["output_path"] == "morph.gif"


def test_main_rejects_julia_morph_without_end_constant():
    """CLI should reject incomplete Julia morph parameters."""
    with pytest.raises(SystemExit):
        main(
            [
                "--fractal",
                "julia",
                "--julia-real",
                "-0.4",
                "--julia-imag",
                "0.6",
                "--animate",
                "julia-morph",
                "--output",
                "morph.gif",
            ]
        )


def test_main_rejects_julia_morph_for_non_julia():
    """CLI should reject Julia morph requests for non-Julia fractals."""
    with pytest.raises(SystemExit):
        main(
            [
                "--fractal",
                "mandelbrot",
                "--animate",
                "julia-morph",
                "--julia-end-real",
                "-0.8",
                "--julia-end-imag",
                "0.156",
                "--output",
                "bad.gif",
            ]
        )


def test_main_rejects_zoom_with_explicit_bounds():
    """CLI should reject zoom animation requests with explicit bounds."""
    with pytest.raises(SystemExit):
        main(
            [
                "--animate",
                "zoom",
                "--xmin",
                "-2.0",
                "--xmax",
                "1.0",
                "--ymin",
                "-1.5",
                "--ymax",
                "1.5",
                "--output",
                "bad.gif",
            ]
        )
