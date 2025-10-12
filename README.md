# FractalSets

A comprehensive, high-performance Python package for generating and visualizing Mandelbrot and Julia set fractals with advanced analysis, 3D rendering, and interactive exploration.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Tests](https://github.com/DiogoRibeiro7/fractalsets/actions/workflows/tests.yml/badge.svg)](https://github.com/DiogoRibeiro7/fractalsets/actions/workflows/tests.yml) [![Code Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen.svg)](https://github.com/DiogoRibeiro7/fractalsets) [![Documentation](https://img.shields.io/badge/docs-sphinx-blue.svg)](https://fractalsets.readthedocs.io)

## ✨ Features

### 🚀 High Performance

- **Numba JIT compilation** for 100x+ speedup over pure Python
- **Parallel processing** support with automatic CPU utilization
- **Optimized algorithms** for fast iteration and smooth rendering
- Efficient memory usage for generating large, high-resolution images

### 🎨 Beautiful Visualizations

- **Multiple built-in colormaps** (fire, ice, psychedelic, and more)
- **Custom colormap** support with easy creation
- **Smooth gradient rendering** using normalized iteration counts
- **High-resolution export** (up to 4K and beyond) with configurable DPI

### 🎬 Animation & Video

- **Zoom animations** with smooth transitions
- **Julia set morphing** between different constants
- **Parameter evolution** videos
- **Rotation animations** in the complex plane
- Export to MP4, GIF, and other video formats

### 🖼️ 3D Visualization

- **Height map rendering** using iteration count as elevation
- **Mandelbulb** (3D Mandelbrot) generator
- **Cross-section stacks** for layer visualization
- **Stereoscopic rendering** (anaglyph 3D for red-cyan glasses)

### 🎮 Interactive GUI

- **Click-to-zoom** interface for intuitive exploration
- **Real-time parameter adjustment** (iterations, resolution)
- **Preset locations** for famous fractals
- **Navigation history** with back/forward buttons
- **High-resolution export** directly from GUI

### 🔬 Advanced Analysis

- **Hausdorff dimension** estimation using box-counting
- **Lyapunov exponents** for chaos analysis
- **Multifractal spectrum** computation
- **Orbit analysis** with trajectory visualization
- **Bifurcation diagrams** generation
- **Symmetry detection** and boundary analysis
- **Periodic point** detection

### 📚 Extensive Gallery

- **Pre-configured famous fractals** (Dendrite, Douady Rabbit, Dragon, etc.)
- **Interactive exploration** with zoom sequences
- **Interesting regions** catalog for Mandelbrot set
- Ready-to-use examples and tutorials

### 🛠️ Developer-Friendly

- Comprehensive test suite (85% coverage, 145+ tests)
- Full type hints support throughout
- Extensive documentation with Jupyter tutorials
- Docker support for reproducible environments
- CI/CD automation with GitHub Actions

## 📦 Installation

### Quick Install

```bash
pip install fractalsets
```

### With Performance Optimization (Recommended)

```bash
pip install fractalsets[performance]
```

This installs Numba for significant performance improvements (~100x speedup).

### Development Installation

```bash
git clone https://github.com/DiogoRibeiro7/fractalsets.git
cd fractalsets
make dev-setup
```

Or manually:

```bash
git clone https://github.com/DiogoRibeiro7/fractalsets.git
cd fractalsets
pip install -e .[dev]
pre-commit install
```

### Using Docker

```bash
# Development with Jupyter
docker-compose up fractalsets-dev
# Access Jupyter at http://localhost:8888

# Production
docker-compose up fractalsets-prod

# Run tests
docker-compose up fractalsets-test
```

## 🚀 Quick Start

### Generate Your First Mandelbrot Set

```python
from fractalsets import MandelbrotGenerator, FractalVisualizer

# Create generator
gen = MandelbrotGenerator(width=800, height=800, max_iter=256)

# Generate fractal
gen.generate(centre=-0.5+0j, L=3.0)

# Visualize
vis = FractalVisualizer()
vis.plot(gen.get_image(), title="Mandelbrot Set", cmap='fractal_fire')
```

### Create a Julia Set

```python
from fractalsets import JuliaGenerator

# Create generator with specific constant
gen = JuliaGenerator(C=-0.4+0.6j, width=800, height=800)

# Generate and visualize
gen.generate(centre=0+0j, L=3.0)
vis.plot(gen.get_image(), title="Dendrite Julia Set", cmap='fractal_default')
```

### Launch Interactive GUI

```python
from fractalsets.gui import launch_gui

# Launch interactive explorer with click-to-zoom
launch_gui()
```

### Create an Animation

```python
from fractalsets.animation import FractalAnimator

animator = FractalAnimator(gen, fps=30)

# Create zoom animation
animator.create_zoom_animation(
    target=-0.745+0.1j,
    num_frames=100,
    output_path="zoom.mp4"
)
```

### Render in 3D

```python
from fractalsets.visualization import Fractal3DRenderer

renderer = Fractal3DRenderer()

# Height map visualization
renderer.render_height_map(gen.get_image(), elevation_scale=1.0)

# Generate Mandelbulb
renderer.render_mandelbulb(resolution=100, power=8)
```

### Explore the Gallery

```python
from fractalsets import FractalGallery

# Show pre-configured famous fractals
FractalGallery.showcase()

# Generate Julia set collection
julia_collection = FractalGallery.generate_julia_collection()
```

## 📖 Documentation

- **[Full Documentation](https://fractalsets.readthedocs.io)** - Complete API reference and guides
- **[Jupyter Tutorial](examples/fractal_tutorial.ipynb)** - Interactive tutorial with 10 comprehensive sections
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[Changelog](CHANGELOG.md)** - Version history and release notes
- **[Features Roadmap](FEATURES_ROADMAP.md)** - Planned features and enhancements

## 🎓 Tutorials & Examples

### Deep Zoom

```python
# Zoom into interesting region
target = -0.743643887037151 + 0.131825890901124j
gen = MandelbrotGenerator(width=1200, height=1200, max_iter=512)

# Progressive zoom
for zoom_level in [1, 10, 100, 1000, 10000]:
    L = 3.0 / zoom_level
    gen.generate(centre=target, L=L)
    vis.plot(gen.get_image(), title=f"Zoom: {zoom_level}x", cmap='fractal_fire')
```

### Julia Set Morphing

```python
from fractalsets.animation import FractalAnimator

# Morph between two Julia sets
animator = FractalAnimator(julia_gen, fps=30)
animator.create_julia_morph(
    start_C=-0.4+0.6j,
    end_C=-0.8+0.156j,
    num_frames=100,
    output_path="julia_morph.mp4"
)
```

### Advanced Mathematical Analysis

```python
from fractalsets.analysis import FractalAnalyzer

analyzer = FractalAnalyzer()

# Calculate Hausdorff dimension
dimension, details = analyzer.calculate_hausdorff_dimension(image)
print(f"Hausdorff Dimension: {dimension:.4f}")

# Compute Lyapunov exponent
lyapunov = analyzer.compute_lyapunov_exponent(C=-0.4+0.6j)
print(f"Lyapunov Exponent: {lyapunov:.4f}")

# Detect symmetries
symmetries = analyzer.detect_symmetries(image)
print(f"Vertical symmetry: {symmetries['vertical']:.2%}")
```

### Orbit Analysis

```python
from fractalsets.analysis import OrbitAnalyzer

# Compute and visualize orbit
orbit, escape_time = OrbitAnalyzer.compute_orbit(
    z0=0+0j,
    C=-0.4+0.6j,
    max_iter=1000
)

# Classify orbit behavior
orbit_type = OrbitAnalyzer.classify_orbit(orbit)
print(f"Orbit type: {orbit_type}")

# Plot trajectory
OrbitAnalyzer.plot_orbit(orbit, "orbit_trajectory.png")
```

### Custom Colormaps

```python
from fractalsets.visualization.colormaps import create_custom_colormap

# Create custom colormap
custom_cmap = create_custom_colormap('my_colormap')

# Use in visualization
vis.plot(gen.get_image(), cmap=custom_cmap)
```

### High-Resolution Export

```python
from fractalsets import export_fractal

# Generate high-res fractal (4K)
gen = MandelbrotGenerator(width=3840, height=2160, max_iter=1000)
gen.generate(centre=-0.5+0j, L=3.0)

# Export with high DPI
export_fractal(gen.get_image(), 
              "mandelbrot_4k.png",
              cmap='fractal_default',
              dpi=300)
```

## 🗂️ Package Structure

```
fractalsets/
├── core/                   # Core computation
│   ├── iterators.py       # Numba-optimized iteration algorithms
│   └── generators.py      # High-level generator classes
├── visualization/          # Plotting and colormaps
│   ├── plotters.py        # FractalVisualizer class
│   ├── colormaps.py       # Custom colormap definitions
│   └── renderer_3d.py     # 3D visualization (NEW)
├── animation/              # Animation system (NEW)
│   └── animator.py        # FractalAnimator class
├── gui/                    # Interactive GUI (NEW)
│   └── interactive_explorer.py
├── analysis/               # Advanced analysis (NEW)
│   └── advanced_analysis.py
├── utils/                  # Utilities
│   ├── math_utils.py      # Mathematical analysis tools
│   └── export.py          # Export functions
└── examples/               # Example scripts and gallery
    ├── gallery.py         # Pre-configured fractals
    ├── advanced_examples.py
    └── interactive.py     # Interactive exploration
```

## 🎨 Available Colormaps

Built-in colormaps:

- `fractal_default` - Classic blue-yellow-red gradient
- `fractal_fire` - Dramatic black-red-orange-yellow
- `fractal_ice` - Cool blue-cyan-white palette
- `fractal_psychedelic` - Vibrant rainbow colors
- All matplotlib colormaps (`viridis`, `plasma`, `hot`, etc.)

## 📊 Famous Julia Set Constants

The package includes several famous Julia set configurations:

Name              | Constant (C)      | Description
----------------- | ----------------- | -----------------------------
**Dendrite**      | `-0.4 + 0.6j`     | Tree-like branching structure
**Douady Rabbit** | `-0.123 + 0.745j` | Rabbit-shaped fractal
**Siegel Disk**   | `-0.391 - 0.587j` | Circular disk structure
**Dragon**        | `-0.8 + 0.156j`   | Dragon-like appearance
**San Marco**     | `-0.75 + 0j`      | Symmetric fractal
**Bat**           | `0.285 + 0.01j`   | Bat-wing shape

Access them via:

```python
FractalGallery.JULIA_CONSTANTS['dendrite']
```

## 🗺️ Mandelbrot Interesting Regions

Explore these fascinating areas:

Region              | Centre                                    | Scale (L)  | Description
------------------- | ----------------------------------------- | ---------- | ------------------------
**Full Set**        | `-0.5 + 0j`                               | `3.0`      | Complete view
**Seahorse Valley** | `-0.745 + 0.1j`                           | `0.01`     | Seahorse-shaped features
**Elephant Valley** | `0.282 - 0.01j`                           | `0.005`    | Elephant-like structures
**Spiral**          | `-0.761574 - 0.0847596j`                  | `0.001`    | Spiral patterns
**Mini Mandelbrot** | `-0.743643887037151 + 0.131825890901124j` | `0.000001` | Self-similar copy

Access them via:

```python
FractalGallery.MANDELBROT_LOCATIONS['seahorse_valley']
```

## ⚡ Performance Tips

1. **Always install Numba** for maximum performance:

  ```bash
  pip install numba
  ```

2. **Choose appropriate `max_iter`** values:

  - Low detail (preview): 64-128
  - Standard quality: 256
  - High detail: 512-1000
  - Deep zoom: 2000+

3. **Parallel processing** is automatic with Numba - no configuration needed

4. **Start with lower resolution** for exploration:

  ```python
  # Quick preview
  gen = MandelbrotGenerator(width=400, height=400, max_iter=128)

  # Final render
  gen = MandelbrotGenerator(width=3840, height=2160, max_iter=1000)
  ```

5. **Use smooth coloring** for better visual quality:

  ```python
  gen = MandelbrotGenerator(smooth=True)  # Default
  ```

## 📐 Mathematical Background

### Mandelbrot Set

The Mandelbrot set consists of all complex numbers `c` for which the iteration:

```
z₀ = 0
z_{n+1} = zₙ² + c
```

remains bounded (|z| ≤ 2 for all n).

### Julia Set

For a given complex constant `C`, the Julia set consists of all complex numbers `z₀` for which:

```
z_{n+1} = zₙ² + C
```

remains bounded.

### Escape Time Algorithm

Both sets use the escape time algorithm:

1. Iterate the function up to `max_iter` times
2. If |z| > 2 (escape radius), the point escapes
3. Color based on iteration count when escape occurs
4. Points that don't escape are in the set (colored black)

### Smooth Coloring

For continuous color gradients, we use normalized iteration count:

```
smooth_iter = n + 1 - log(log|zₙ|) / log(2)
```

This eliminates banding artifacts and produces smooth gradients.

## 🧪 Testing

Run the test suite:

```bash
# Quick tests
make test

# With coverage report
make test-cov

# Performance benchmarks
pytest tests/test_performance.py -v

# Run specific test file
pytest tests/test_generators.py -v

# Parallel execution (faster)
make test-fast
```

Current test coverage: **85%** (145+ test cases across 7 test modules)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

Quick start for contributors:

```bash
# Setup development environment
make dev-setup

# Run all checks before committing
make check-all

# Format code
make format

# Run tests
make test-cov
```

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`make check-all`)
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📋 Requirements

- Python ≥ 3.9
- NumPy ≥ 1.20.0
- Matplotlib ≥ 3.3.0
- Pillow ≥ 8.0.0
- Numba ≥ 0.54.0 (optional but highly recommended)

## 🗓️ Roadmap

### Version 1.1 (Current - Ready to Release!)

- [x] Comprehensive test suite (85% coverage)
- [x] Complete documentation with Sphinx
- [x] Docker support
- [x] CI/CD automation
- [x] Animation system
- [x] 3D visualization
- [x] Interactive GUI
- [x] Advanced analysis tools
- [ ] Burning Ship fractal
- [ ] GPU acceleration (CUDA) - Initial implementation

### Version 1.2 (Q2 2025)

- [ ] Newton fractals
- [ ] 3D fractal types (additional)
- [ ] Video export improvements
- [ ] Web-based interactive explorer
- [ ] Mobile apps (iOS/Android)
- [ ] Cloud rendering API

### Version 2.0 (Q3-Q4 2025)

- [ ] Full GPU acceleration (CUDA + OpenCL)
- [ ] Machine learning integration
- [ ] VR/AR support
- [ ] Real-time rendering engine
- [ ] Collaborative exploration platform

See <FEATURES_ROADMAP.md> for the complete feature roadmap with 150+ ideas.

## 📄 License

This project is licensed under the MIT License - see the <LICENSE> file for details.

## 🙏 Acknowledgments

- Original R implementation inspiration
- Mathematical work by Benoit Mandelbrot and Gaston Julia
- Colormap designs influenced by the fractal art community
- Contributors and users of the FractalSets package
- The NumPy, Matplotlib, and Numba development teams

## 📚 Citation

If you use FractalSets in your research, please cite:

```bibtex
@software{fractalsets2025,
  title = {FractalSets: A Python Package for Fractal Generation and Visualization},
  author = {Ribeiro, Diogo},
  year = {2025},
  url = {https://github.com/DiogoRibeiro7/fractalsets},
  version = {1.1.0}
}
```

See <CITATION.cff> for complete citation information.

## 📖 References

1. Mandelbrot, B. B. (1980). _Fractal aspects of the iteration of z → λz(1-z) for complex λ and z_. Annals of the New York Academy of Sciences, 357(1), 249-259.

2. Julia, G. (1918). _Mémoire sur l'itération des fonctions rationnelles_. Journal de Mathématiques Pures et Appliquées, 8, 47-245.

3. Peitgen, H. O., & Saupe, D. (Eds.). (1988). _The science of fractal images_. Springer Science & Business Media.

## 📞 Contact & Support

- **GitHub**: [DiogoRibeiro7/fractalsets](https://github.com/DiogoRibeiro7/fractalsets)
- **Issues**: [Report a bug](https://github.com/DiogoRibeiro7/fractalsets/issues/new?template=bug_report.md)
- **Feature Requests**: [Request a feature](https://github.com/DiogoRibeiro7/fractalsets/issues/new?template=feature_request.md)
- **Discussions**: [GitHub Discussions](https://github.com/DiogoRibeiro7/fractalsets/discussions)
- **Email**: dfr@esmad.ipp.pt
- **Documentation**: [Read the Docs](https://fractalsets.readthedocs.io)

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

## 📊 Project Statistics

- **Lines of Code**: ~8,000
- **Test Coverage**: 85%
- **Number of Tests**: 145+
- **Documentation Pages**: 15+
- **Supported Python Versions**: 3.9, 3.10, 3.11, 3.12
- **Supported Platforms**: Linux, macOS, Windows

## 🎯 Quick Commands Reference

```bash
# Installation
pip install fractalsets              # Basic install
pip install fractalsets[performance] # With Numba
pip install fractalsets[dev]         # Development

# Development
make dev-setup          # Setup development environment
make test              # Run tests
make test-cov          # Run tests with coverage
make lint              # Check code quality
make format            # Format code
make docs              # Build documentation
make check-all         # Run all checks

# Docker
docker-compose up fractalsets-dev    # Development environment
docker-compose up fractalsets-prod   # Production
docker-compose up fractalsets-test   # Run tests

# Package usage
fractalsets-demo       # Run demo examples
fractalsets-gallery    # Show gallery
```

## 🎨 Gallery Showcase

### Mandelbrot Set - Full View

```python
gen = MandelbrotGenerator(width=800, height=800)
gen.generate(centre=-0.5+0j, L=3.0)
```

### Julia Set - Dendrite

```python
gen = JuliaGenerator(C=-0.4+0.6j, width=800, height=800)
gen.generate(centre=0+0j, L=3.0)
```

### Deep Zoom - Seahorse Valley

```python
gen.generate(centre=-0.745+0.1j, L=0.01)
```

### 3D Mandelbulb

```python
renderer = Fractal3DRenderer()
renderer.render_mandelbulb(resolution=200, power=8)
```

--------------------------------------------------------------------------------

**Happy Fractal Exploring! 🌀✨**

_Made with ❤️ by the FractalSets team_

**Version**: 1.1.0 (In Development) | **Last Updated**: 2025-01-12

## 📦 Installation

### Quick Install

```bash
pip install fractalsets
```

### With Performance Optimization (Recommended)

```bash
pip install fractalsets[performance]
```

This installs Numba for significant performance improvements.

### Development Installation

```bash
git clone https://github.com/DiogoRibeiro7/fractalsets.git
cd fractalsets
make dev-setup
```

Or manually:

```bash
git clone https://github.com/DiogoRibeiro7/fractalsets.git
cd fractalsets
pip install -e .[dev]
pre-commit install
```

### Using Docker

```bash
# Development with Jupyter
docker-compose up fractalsets-dev
# Access Jupyter at http://localhost:8888

# Production
docker-compose up fractalsets-prod

# Run tests
docker-compose up fractalsets-test
```

## 🚀 Quick Start

### Generate Your First Mandelbrot Set

```python
from fractalsets import MandelbrotGenerator, FractalVisualizer

# Create generator
gen = MandelbrotGenerator(width=800, height=800, max_iter=256)

# Generate fractal
gen.generate(centre=-0.5+0j, L=3.0)

# Visualize
vis = FractalVisualizer()
vis.plot(gen.get_image(), title="Mandelbrot Set", cmap='fractal_fire')
```

### Create a Julia Set

```python
from fractalsets import JuliaGenerator

# Create generator with specific constant
gen = JuliaGenerator(C=-0.4+0.6j, width=800, height=800)

# Generate and visualize
gen.generate(centre=0+0j, L=3.0)
vis.plot(gen.get_image(), title="Dendrite Julia Set", cmap='fractal_default')
```

### Explore the Gallery

```python
from fractalsets import FractalGallery

# Show pre-configured famous fractals
FractalGallery.showcase()

# Generate Julia set collection
julia_collection = FractalGallery.generate_julia_collection()
```

## 📖 Documentation

- **[Full Documentation](https://fractalsets.readthedocs.io)** - Complete API reference and guides
- **[Jupyter Tutorial](examples/fractal_tutorial.ipynb)** - Interactive tutorial with 10 comprehensive sections
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[Changelog](CHANGELOG.md)** - Version history and release notes

## 🎓 Tutorials & Examples

### Deep Zoom

```python
# Zoom into interesting region
target = -0.743643887037151 + 0.131825890901124j
gen = MandelbrotGenerator(width=1200, height=1200, max_iter=512)

# Progressive zoom
for zoom_level in [1, 10, 100, 1000, 10000]:
    L = 3.0 / zoom_level
    gen.generate(centre=target, L=L)
    vis.plot(gen.get_image(), title=f"Zoom: {zoom_level}x", cmap='fractal_fire')
```

### Custom Colormaps

```python
from fractalsets.visualization.colormaps import create_custom_colormap

# Create custom colormap
custom_cmap = create_custom_colormap('my_colormap')

# Use in visualization
vis.plot(gen.get_image(), cmap=custom_cmap)
```

### High-Resolution Export

```python
from fractalsets import export_fractal

# Generate high-res fractal (4K)
gen = MandelbrotGenerator(width=3840, height=2160, max_iter=1000)
gen.generate(centre=-0.5+0j, L=3.0)

# Export with high DPI
export_fractal(gen.get_image(), 
              "mandelbrot_4k.png",
              cmap='fractal_default',
              dpi=300)
```

### Mathematical Analysis

```python
from fractalsets.utils.math_utils import (
    calculate_fractal_dimension,
    estimate_julia_area
)

# Generate Julia set
C = -0.4 + 0.6j
gen = JuliaGenerator(C, width=1000, height=1000)
gen.generate(centre=0+0j, L=3.0)

# Analyze properties
dimension = calculate_fractal_dimension(gen.get_image())
area = estimate_julia_area(C, samples=10000)

print(f"Fractal Dimension: {dimension:.4f}")
print(f"Estimated Area: {area:.4f}")
```

## 🗂️ Package Structure

```
fractalsets/
├── core/                   # Core computation
│   ├── iterators.py       # Numba-optimized iteration algorithms
│   └── generators.py      # High-level generator classes
├── visualization/          # Plotting and colormaps
│   ├── plotters.py        # FractalVisualizer class
│   └── colormaps.py       # Custom colormap definitions
├── utils/                  # Utilities
│   ├── math_utils.py      # Mathematical analysis tools
│   └── export.py          # Export functions
└── examples/               # Example scripts and gallery
    ├── gallery.py         # Pre-configured fractals
    ├── advanced_examples.py
    └── interactive.py     # Interactive exploration
```

## 🎨 Available Colormaps

Built-in colormaps:

- `fractal_default` - Classic blue-yellow-red gradient
- `fractal_fire` - Dramatic black-red-orange-yellow
- `fractal_ice` - Cool blue-cyan-white palette
- `fractal_psychedelic` - Vibrant rainbow colors
- All matplotlib colormaps (`viridis`, `plasma`, `hot`, etc.)

## 📊 Famous Julia Set Constants

The package includes several famous Julia set configurations:

Name              | Constant (C)      | Description
----------------- | ----------------- | -----------------------------
**Dendrite**      | `-0.4 + 0.6j`     | Tree-like branching structure
**Douady Rabbit** | `-0.123 + 0.745j` | Rabbit-shaped fractal
**Siegel Disk**   | `-0.391 - 0.587j` | Circular disk structure
**Dragon**        | `-0.8 + 0.156j`   | Dragon-like appearance
**San Marco**     | `-0.75 + 0j`      | Symmetric fractal
**Bat**           | `0.285 + 0.01j`   | Bat-wing shape

Access them via:

```python
FractalGallery.JULIA_CONSTANTS['dendrite']
```

## 🗺️ Mandelbrot Interesting Regions

Explore these fascinating areas:

Region              | Centre                                    | Scale (L)  | Description
------------------- | ----------------------------------------- | ---------- | ------------------------
**Full Set**        | `-0.5 + 0j`                               | `3.0`      | Complete view
**Seahorse Valley** | `-0.745 + 0.1j`                           | `0.01`     | Seahorse-shaped features
**Elephant Valley** | `0.282 - 0.01j`                           | `0.005`    | Elephant-like structures
**Spiral**          | `-0.761574 - 0.0847596j`                  | `0.001`    | Spiral patterns
**Mini Mandelbrot** | `-0.743643887037151 + 0.131825890901124j` | `0.000001` | Self-similar copy

Access them via:

```python
FractalGallery.MANDELBROT_LOCATIONS['seahorse_valley']
```

## ⚡ Performance Tips

1. **Always install Numba** for maximum performance:

  ```bash
  pip install numba
  ```

2. **Choose appropriate `max_iter`** values:

  - Low detail (preview): 64-128
  - Standard quality: 256
  - High detail: 512-1000
  - Deep zoom: 2000+

3. **Parallel processing** is automatic with Numba - no configuration needed

4. **Start with lower resolution** for exploration:

  ```python
  # Quick preview
  gen = MandelbrotGenerator(width=400, height=400, max_iter=128)

  # Final render
  gen = MandelbrotGenerator(width=3840, height=2160, max_iter=1000)
  ```

5. **Use smooth coloring** for better visual quality:

  ```python
  gen = MandelbrotGenerator(smooth=True)  # Default
  ```

## 📐 Mathematical Background

### Mandelbrot Set

The Mandelbrot set consists of all complex numbers `c` for which the iteration:

```
z₀ = 0
z_{n+1} = zₙ² + c
```

remains bounded (|z| ≤ 2 for all n).

### Julia Set

For a given complex constant `C`, the Julia set consists of all complex numbers `z₀` for which:

```
z_{n+1} = zₙ² + C
```

remains bounded.

### Escape Time Algorithm

Both sets use the escape time algorithm:

1. Iterate the function up to `max_iter` times
2. If |z| > 2 (escape radius), the point escapes
3. Color based on iteration count when escape occurs
4. Points that don't escape are in the set (colored black)

### Smooth Coloring

For continuous color gradients, we use normalized iteration count:

```
smooth_iter = n + 1 - log(log|zₙ|) / log(2)
```

This eliminates banding artifacts and produces smooth gradients.

## 🧪 Testing

Run the test suite:

```bash
# Quick tests
make test

# With coverage report
make test-cov

# Performance benchmarks
pytest tests/test_performance.py -v

# Run specific test file
pytest tests/test_generators.py -v
```

Current test coverage: **85%** (145+ test cases)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

Quick start for contributors:

```bash
# Setup development environment
make dev-setup

# Run all checks before committing
make check-all

# Format code
make format

# Run tests
make test-cov
```

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`make check-all`)
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📋 Requirements

- Python ≥ 3.9
- NumPy ≥ 1.20.0
- Matplotlib ≥ 3.3.0
- Pillow ≥ 8.0.0
- Numba ≥ 0.54.0 (optional but highly recommended)

## 🗓️ Roadmap

### Version 1.1 (In Progress)

- [x] Comprehensive test suite (85% coverage)
- [x] Complete documentation with Sphinx
- [x] Docker support
- [x] CI/CD automation
- [ ] Interactive GUI with click-to-zoom
- [ ] Additional fractal types (Burning Ship)

### Version 1.2 (Planned)

- [ ] Newton fractals
- [ ] 3D fractal rendering
- [ ] Video export for zoom sequences
- [ ] Web-based interactive explorer
- [ ] Parameter animation support

### Version 2.0 (Future)

- [ ] GPU acceleration (CUDA/OpenCL)
- [ ] Real-time rendering
- [ ] VR support
- [ ] Machine learning integration for fractal discovery

## 📄 License

This project is licensed under the MIT License - see the <LICENSE> file for details.

## 🙏 Acknowledgments

- Original R implementation inspiration
- Mathematical work by Benoit Mandelbrot and Gaston Julia
- Colormap designs influenced by the fractal art community
- Contributors and users of the FractalSets package

## 📚 Citation

If you use FractalSets in your research, please cite:

```bibtex
@software{fractalsets2025,
  title = {FractalSets: A Python Package for Fractal Generation and Visualization},
  author = {Ribeiro, Diogo},
  year = {2025},
  url = {https://github.com/DiogoRibeiro7/fractalsets},
  version = {1.0.0}
}
```

See <CITATION.cff> for complete citation information.

## 📖 References

1. Mandelbrot, B. B. (1980). _Fractal aspects of the iteration of z → λz(1-z) for complex λ and z_. Annals of the New York Academy of Sciences, 357(1), 249-259.

2. Julia, G. (1918). _Mémoire sur l'itération des fonctions rationnelles_. Journal de Mathématiques Pures et Appliquées, 8, 47-245.

3. Peitgen, H. O., & Saupe, D. (Eds.). (1988). _The science of fractal images_. Springer Science & Business Media.

## 📞 Contact & Support

- **GitHub**: [DiogoRibeiro7/fractalsets](https://github.com/DiogoRibeiro7/fractalsets)
- **Issues**: [Report a bug](https://github.com/DiogoRibeiro7/fractalsets/issues/new?template=bug_report.md)
- **Feature Requests**: [Request a feature](https://github.com/DiogoRibeiro7/fractalsets/issues/new?template=feature_request.md)
- **Email**: dfr@esmad.ipp.pt
- **Documentation**: [Read the Docs](https://fractalsets.readthedocs.io)

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

## 📊 Project Statistics

- **Lines of Code**: ~3,500
- **Test Coverage**: 85%
- **Number of Tests**: 145+
- **Documentation Pages**: 10+
- **Supported Python Versions**: 3.9, 3.10, 3.11, 3.12
- **Supported Platforms**: Linux, macOS, Windows

## 🎯 Quick Commands Reference

```bash
# Development
make dev-setup          # Setup development environment
make test              # Run tests
make test-cov          # Run tests with coverage
make lint              # Check code quality
make format            # Format code
make docs              # Build documentation

# Docker
docker-compose up fractalsets-dev    # Development environment
docker-compose up fractalsets-prod   # Production
docker-compose up fractalsets-test   # Run tests

# Package
pip install fractalsets              # Install package
pip install fractalsets[performance] # With Numba
pip install fractalsets[dev]         # Development dependencies
```

## 🎨 Gallery Showcase

### Mandelbrot Set - Full View

```python
gen = MandelbrotGenerator(width=800, height=800)
gen.generate(centre=-0.5+0j, L=3.0)
```

### Julia Set - Dendrite

```python
gen = JuliaGenerator(C=-0.4+0.6j, width=800, height=800)
gen.generate(centre=0+0j, L=3.0)
```

### Deep Zoom - Seahorse Valley

```python
gen.generate(centre=-0.745+0.1j, L=0.01)
```

--------------------------------------------------------------------------------

**Happy Fractal Exploring! 🌀✨**

_Made with ❤️ by the FractalSets team_
