# FractalSets

FractalSets is a Python package for generating and visualizing Mandelbrot and Julia sets. The current codebase includes:

- core Mandelbrot and Julia generators
- plotting helpers and custom colormaps
- image export utilities
- animation helpers
- 3D rendering helpers
- a Tk GUI explorer
- optional advanced analysis tools

## Status

The package is usable, but some parts are still exploratory:

- the core generation, plotting, export, and gallery paths are the most stable
- `numba` acceleration is optional
- advanced analysis depends on extra scientific packages
- GUI, animation, and 3D helpers are available, but they have lighter test coverage than the core modules

## Installation

Base install:

```bash
pip install fractalsets
```

With optional performance acceleration:

```bash
pip install "fractalsets[performance]"
```

With advanced analysis dependencies:

```bash
pip install "fractalsets[analysis]"
```

For local development:

```bash
git clone https://github.com/DiogoRibeiro7/fractalsets.git
cd fractalsets
pip install -e ".[dev]"
```

If you want both acceleration and analysis locally:

```bash
pip install -e ".[dev,performance,analysis]"
```

## Quick Start

Generate and plot a Mandelbrot set:

```python
from fractalsets import MandelbrotGenerator, FractalVisualizer

gen = MandelbrotGenerator(width=800, height=800, max_iter=256)
image = gen.generate(centre=-0.5 + 0j, L=3.0)

vis = FractalVisualizer()
vis.plot(image, title="Mandelbrot Set", cmap="fractal_fire")
```

Generate a Julia set:

```python
from fractalsets import JuliaGenerator, FractalVisualizer

gen = JuliaGenerator(C=-0.4 + 0.6j, width=800, height=800, max_iter=256)
image = gen.generate(centre=0 + 0j, L=3.0)

vis = FractalVisualizer()
vis.plot(image, title="Julia Set", cmap="fractal_default")
```

Export an image:

```python
from fractalsets import MandelbrotGenerator, export_fractal

gen = MandelbrotGenerator(width=1920, height=1080, max_iter=512)
gen.generate(centre=-0.5 + 0j, L=3.0)

export_fractal(gen.get_image(), "mandelbrot.png", cmap="fractal_default", dpi=300)
```

Render from the command line:

```bash
fractalsets-render --fractal burning-ship --output burning_ship.png --width 1600 --height 1200 --max-iter 512 --centre-real -1.75 --centre-imag -0.03 --L 0.08 --cmap fractal_fire
```

List available presets:

```bash
fractalsets-render --fractal burning-ship --list-presets
```

Render a named preset:

```bash
fractalsets-render --fractal mandelbrot --preset seahorse_valley --output seahorse.png --width 1600 --height 1600 --max-iter 512 --cmap fractal_fire
```

Launch the GUI explorer:

```python
from fractalsets.gui import launch_gui

launch_gui()
```

Create an animation:

```python
from fractalsets import MandelbrotGenerator
from fractalsets.animation import FractalAnimator

gen = MandelbrotGenerator(width=600, height=600, max_iter=256)
animator = FractalAnimator(gen, fps=30)
animator.create_zoom_animation(
    target=-0.745 + 0.1j,
    num_frames=60,
    output_path="zoom.gif",
)
```

Run advanced analysis:

```python
from fractalsets.analysis import FractalAnalyzer

analyzer = FractalAnalyzer()
boundary = analyzer.detect_boundary(image)
dimension, details = analyzer.calculate_hausdorff_dimension(image)
```

## Public Modules

- `fractalsets`
  Core top-level exports such as `MandelbrotGenerator`, `JuliaGenerator`, `FractalVisualizer`, `FractalAnimator`, `Fractal3DRenderer`, `FractalGallery`, and `export_fractal`.
- `fractalsets.animation`
  Animation helpers like `FractalAnimator` and `FractalVideoExporter`.
- `fractalsets.analysis`
  Analysis helpers like `FractalAnalyzer`, `BifurcationAnalyzer`, and `OrbitAnalyzer`.
- `fractalsets.gui`
  Tk GUI entry points such as `launch_gui`.
- `fractalsets.visualization`
  Plotting, colormaps, animation, and 3D rendering exports.
- `fractalsets.cli`
  Command-line rendering entry point used by `fractalsets-render`.

## Package Layout

```text
fractalsets/
├── __init__.py
├── animation.py
├── analysis/
│   ├── __init__.py
│   └── advanced.py
├── core/
│   ├── generators.py
│   └── iterators.py
├── examples/
├── gui/
│   ├── __init__.py
│   └── interactive_explorer.py
├── utils/
│   ├── export.py
│   └── math_utils.py
└── visualization/
    ├── __init__.py
    ├── animator.py
    ├── colormaps.py
    ├── plotters.py
    └── renderer_3d.py
```

## Current Gaps

Known areas still worth improving:

- README examples are now aligned with the shipped API, but the broader docs set still needs cleanup
- the GUI and renderer modules need deeper behavioral tests
- advanced analysis works best when installed via the `analysis` extra
- additional fractal types beyond Mandelbrot, Julia, and Burning Ship are not implemented yet

## Development

Run tests:

```bash
pytest
```

Relevant repository files:

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CHANGELOG.md](CHANGELOG.md)
- [FEATURES_ROADMAP.md](FEATURES_ROADMAP.md)
- [REPO_REVIEW.md](REPO_REVIEW.md)
