# FractalSets

A comprehensive, high-performance Python package for generating and visualizing Mandelbrot and Julia set fractals.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Monthly Reminder](https://github.com/DiogoRibeiro7/fractalsets/actions/workflows/monthly-reminder.yml/badge.svg)](https://github.com/DiogoRibeiro7/fractalsets/actions/workflows/monthly-reminder.yml)


## Features

✨ **High Performance**

- Numba JIT compilation for 100x+ speedup
- Parallel processing support
- Optimized iteration algorithms

🎨 **Beautiful Visualizations**

- Multiple built-in colormaps
- Custom colormap support
- Smooth gradient rendering
- High-resolution export

🔬 **Scientific Tools**

- Fractal dimension estimation
- Period detection
- Area calculation
- Mathematical utilities

📚 **Extensive Gallery**

- Pre-configured famous fractals
- Interactive exploration
- Zoom sequences
- Parameter animations

## Installation

### Basic Installation

```bash
pip install fractalsets
```

### With Performance Optimization (Recommended)

```bash
pip install fractalsets[performance]
```

### Development Installation

```bash
git clone https://github.com/DiogoRibeiro7/fractalsets.git
cd fractalsets
pip install -e .[dev]
```

## Quick Start

### Generate Mandelbrot Set

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

### Generate Julia Set

```python
from fractalsets import JuliaGenerator

# Create generator with specific constant
gen = JuliaGenerator(C=-0.4+0.6j, width=800, height=800)

# Generate and visualize
gen.generate(centre=0+0j, L=3.0)
vis.plot(gen.get_image(), title="Dendrite Julia Set")
```

### Explore the Gallery

```python
from fractalsets import FractalGallery

# Show pre-configured fractals
FractalGallery.showcase()

# Generate specific Julia set
julia_collection = FractalGallery.generate_julia_collection()
```

## Advanced Usage

### Deep Zoom

```python
# Zoom into interesting region
target = -0.743643887037151 + 0.131825890901124j
gen = MandelbrotGenerator(width=1200, height=1200, max_iter=512)

# Progressive zoom
for zoom_level in [1, 10, 100, 1000, 10000]:
    L = 3.0 / zoom_level
    gen.generate(centre=target, L=L)
    vis.plot(gen.get_image(), title=f"Zoom: {zoom_level}x")
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

# Generate high-res fractal
gen = MandelbrotGenerator(width=4000, height=4000, max_iter=1000)
gen.generate(centre=-0.5+0j, L=3.0)

# Export
export_fractal(gen.get_image(), 
              "mandelbrot_4k.png",
              cmap='fractal_default',
              dpi=300)
```

### Animate Zoom Sequence

```python
# Create zoom animation
vis = FractalVisualizer()
target = -0.745 + 0.1j

vis.animate_zoom(gen, 
                centre=target,
                num_frames=100,
                zoom_factor=1.05,
                save_path="zoom_animation.gif")
```

## Package Structure

```
fractalsets/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── iterators.py          # Core iteration algorithms
│   └── generators.py         # High-level generator classes
├── visualization/
│   ├── __init__.py
│   ├── plotters.py          # Visualization tools
│   └── colormaps.py         # Custom colormaps
├── utils/
│   ├── __init__.py
│   ├── math_utils.py        # Mathematical utilities
│   └── export.py            # Export functions
└── examples/
    ├── __init__.py
    ├── gallery.py           # Pre-configured fractals
    ├── interactive.py       # Interactive exploration
    └── advanced_examples.py # Advanced usage examples
```

## API Reference

### MandelbrotGenerator

```python
MandelbrotGenerator(width=800, height=800, max_iter=256, smooth=True)
```

**Methods:**

- `generate(centre, L)` - Generate fractal in square region
- `generate(xmin, xmax, ymin, ymax)` - Generate with explicit bounds
- `zoom(centre, zoom_factor)` - Zoom into specific point
- `get_image()` - Return image array
- `normalize_image(log_scale=True)` - Get normalized image

### JuliaGenerator

```python
JuliaGenerator(C, width=800, height=800, max_iter=256, smooth=True)
```

**Parameters:**

- `C` (complex) - Julia set constant parameter

**Methods:**

- Same as MandelbrotGenerator
- `set_constant(C)` - Update Julia constant

### FractalVisualizer

```python
FractalVisualizer(figsize=(12, 10))
```

**Methods:**

- `plot(image, title, cmap, ...)` - Plot single fractal
- `plot_comparison(images, titles, ...)` - Compare multiple fractals
- `animate_zoom(generator, ...)` - Create zoom animation

## Famous Julia Set Constants

The package includes several famous Julia set configurations:

- **Dendrite**: `C = -0.4 + 0.6j`
- **Douady Rabbit**: `C = -0.123 + 0.745j`
- **Siegel Disk**: `C = -0.391 - 0.587j`
- **Dragon**: `C = -0.8 + 0.156j`
- **San Marco**: `C = -0.75 + 0.0j`
- **Bat**: `C = 0.285 + 0.01j`

## Mandelbrot Interesting Regions

Explore these fascinating areas:

- **Seahorse Valley**: `centre=-0.745+0.1j, L=0.01`
- **Elephant Valley**: `centre=0.282-0.01j, L=0.005`
- **Spiral**: `centre=-0.761574-0.0847596j, L=0.001`
- **Mini Mandelbrot**: `centre=-0.743643887037151+0.131825890901124j, L=0.000001`

## Performance Tips

1. **Install Numba** for 100x+ speedup:

  ```bash
  pip install numba
  ```

2. **Use appropriate max_iter**:

  - Low detail (preview): 128
  - Standard: 256
  - High detail: 512-1000
  - Deep zoom: 2000+

3. **Leverage parallel processing** (automatic with Numba)

4. **Start with lower resolution** for exploration, then increase for final render

## Mathematical Background

### Mandelbrot Set

The Mandelbrot set consists of all complex numbers `c` for which the iteration:

```
z₀ = 0
z_{n+1} = z_n² + c
```

remains bounded (does not escape to infinity).

### Julia Set

For a given complex constant `C`, the Julia set consists of all complex numbers `z₀` for which:

```
z_{n+1} = z_n² + C
```

remains bounded.

### Escape Time Algorithm

Both sets use the escape time algorithm:

1. Iterate the function up to `max_iter` times
2. If |z| > 2 (escape radius), the point escapes
3. Color based on iteration count when escape occurs
4. Points that don't escape are in the set

### Smooth Coloring

For continuous color gradients, we use normalized iteration count:

```
smooth_iter = n + 1 - log(log|z_n|) / log(2)
```

## Examples Gallery

### Example 1: Basic Generation

```python
from fractalsets import MandelbrotGenerator, FractalVisualizer

gen = MandelbrotGenerator(width=800, height=800)
gen.generate(centre=-0.5+0j, L=3.0)

vis = FractalVisualizer()
vis.plot(gen.get_image(), title="The Mandelbrot Set")
```

### Example 2: Julia Set Collection

```python
from fractalsets import JuliaGenerator, FractalVisualizer

julia_constants = [
    (-0.4 + 0.6j, "Dendrite"),
    (-0.123 + 0.745j, "Douady Rabbit"),
    (-0.8 + 0.156j, "Dragon"),
    (0.285 + 0.01j, "Bat")
]

images = []
titles = []

for C, name in julia_constants:
    gen = JuliaGenerator(C, width=600, height=600)
    gen.generate(centre=0+0j, L=3.0)
    images.append(gen.get_image())
    titles.append(name)

vis = FractalVisualizer()
vis.plot_comparison(images, titles, suptitle="Julia Set Gallery")
```

### Example 3: Deep Zoom Animation

```python
from fractalsets import MandelbrotGenerator, FractalVisualizer

target = -0.743643887037151 + 0.131825890901124j
gen = MandelbrotGenerator(width=800, height=800, max_iter=512)
vis = FractalVisualizer()

vis.animate_zoom(gen, 
                centre=target,
                num_frames=50,
                zoom_factor=1.1,
                cmap='fractal_fire',
                save_path='deep_zoom.gif')
```

### Example 4: Comparison with Different Parameters

```python
from fractalsets import MandelbrotGenerator, FractalVisualizer

gen = MandelbrotGenerator(width=600, height=600)
images = []
titles = []

for max_iter in [64, 128, 256, 512]:
    gen.max_iter = max_iter
    gen.generate(centre=-0.5+0j, L=3.0)
    images.append(gen.get_image())
    titles.append(f"max_iter = {max_iter}")

vis = FractalVisualizer()
vis.plot_comparison(images, titles, 
                   suptitle="Effect of max_iter Parameter")
```

### Example 5: Explore Mandelbrot Regions

```python
from fractalsets import FractalGallery

# Generate zoom sequence into seahorse valley
zoom_sequence = FractalGallery.generate_mandelbrot_zoom_sequence(
    location='seahorse_valley',
    num_zooms=6
)

# Visualize
vis = FractalVisualizer()
titles = [f"Zoom Level {i+1}" for i in range(len(zoom_sequence))]
vis.plot_comparison(zoom_sequence, titles,
                   suptitle="Seahorse Valley Zoom Sequence")
```

### Example 6: Mathematical Analysis

```python
from fractalsets import JuliaGenerator
from fractalsets.utils.math_utils import (
    calculate_fractal_dimension,
    estimate_julia_area
)

# Generate Julia set
C = -0.4 + 0.6j
gen = JuliaGenerator(C, width=1000, height=1000, max_iter=256)
gen.generate(centre=0+0j, L=3.0)

# Calculate properties
dimension = calculate_fractal_dimension(gen.get_image())
area = estimate_julia_area(C)

print(f"Fractal Dimension: {dimension:.3f}")
print(f"Estimated Area: {area:.3f}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
git clone https://github.com/yourusername/fractalsets.git
cd fractalsets
pip install -e .[dev]
```

### Running Tests

```bash
pytest tests/ -v --cov=fractalsets
```

### Code Style

We use Black for code formatting:

```bash
black fractalsets/
flake8 fractalsets/
```

## Roadmap

- [x] Core Mandelbrot and Julia set generators
- [x] High-performance Numba optimization
- [x] Multiple colormap support
- [x] Export functionality
- [x] Gallery of famous fractals
- [ ] Interactive click-to-zoom GUI
- [ ] Burning Ship fractal
- [ ] Newton fractals
- [ ] 3D fractal rendering
- [ ] GPU acceleration (CUDA/OpenCL)
- [ ] Real-time parameter animation
- [ ] Web-based interactive explorer

## License

This project is licensed under the MIT License - see the <LICENSE> file for details.

## Acknowledgments

- Original R implementation by [Original Author]
- Inspired by the mathematical beauty of Benoit Mandelbrot and Gaston Julia
- Colormap designs influenced by fractal art community

## Citation

If you use FractalSets in your research, please cite:

```bibtex
@software{fractalsets2024,
  title = {FractalSets: A Python Package for Fractal Generation},
  author = {FractalSets Development Team},
  year = {2024},
  url = {https://github.com/yourusername/fractalsets}
}
```

## References

1. Mandelbrot, B. B. (1980). _Fractal aspects of the iteration of z → λz(1-z) for complex λ and z_. Annals of the New York Academy of Sciences, 357(1), 249-259.

2. Julia, G. (1918). _Mémoire sur l'itération des fonctions rationnelles_. Journal de Mathématiques Pures et Appliquées, 8, 47-245.

3. Peitgen, H. O., & Saupe, D. (Eds.). (1988). _The science of fractal images_. Springer Science & Business Media.

## Contact

- GitHub: <https://github.com/DiogoRibeiro7/fractalsets>
- Issues: <https://github.com/DiogoRibeiro7/fractalsets/issues>
- Email: <dfr@esmad.ipp.pt>

## Gallery Showcase

### Mandelbrot Set - Full View

![Mandelbrot Full](docs/images/mandelbrot_full.png)

### Seahorse Valley Detail

![Seahorse Valley](docs/images/seahorse_valley.png)

### Julia Set - Dendrite

![Julia Dendrite](docs/images/julia_dendrite.png)

### Deep Zoom Sequence

![Deep Zoom](docs/images/deep_zoom_sequence.png)

--------------------------------------------------------------------------------

**Happy Fractal Exploring! 🌀** """
