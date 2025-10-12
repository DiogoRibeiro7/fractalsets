"""Advanced usage examples and demonstrations."""

import numpy as np
from ..core.generators import MandelbrotGenerator, JuliaGenerator
from ..visualization.plotters import FractalVisualizer
from ..utils.export import export_fractal


def example_basic_mandelbrot():
    print("Example 1: Basic Mandelbrot Set")
    print("-" * 50)
    gen = MandelbrotGenerator(width=800, height=800, max_iter=256)
    gen.generate(centre=-0.5+0j, L=3.0)
    vis = FractalVisualizer()
    vis.plot(gen.get_image(), title="Mandelbrot Set", cmap='fractal_default')
    print("Mandelbrot set generated successfully!\n")


def example_julia_variations():
    print("Example 2: Julia Set Variations")
    print("-" * 50)
    constants = [
        (-0.4 + 0.6j, "Dendrite"),
        (-0.123 + 0.745j, "Douady Rabbit"),
        (-0.8 + 0.156j, "Dragon"),
        (0.285 + 0.01j, "Bat")
    ]
    images, titles = [], []
    for C, name in constants:
        gen = JuliaGenerator(C, width=500, height=500, max_iter=256)
        gen.generate(centre=0+0j, L=3.0)
        images.append(gen.get_image())
        titles.append(f"{name}\nC = {C:.3f}")
    vis = FractalVisualizer(figsize=(16, 8))
    vis.plot_comparison(images, titles, cmap='fractal_psychedelic',
                        suptitle="Julia Set Gallery")
    print("Julia set variations generated!\n")


def example_deep_zoom():
    print("Example 3: Deep Zoom Sequence")
    print("-" * 50)
    target = -0.743643887037151 + 0.131825890901124j
    gen = MandelbrotGenerator(width=600, height=600, max_iter=512)
    zoom_levels = [1, 10, 100, 1000, 10000, 100000]
    images, titles = [], []
    for zoom in zoom_levels:
        L = 3.0 / zoom
        gen.generate(centre=target, L=L)
        images.append(gen.get_image())
        titles.append(f"Zoom: {zoom}x")
    vis = FractalVisualizer(figsize=(18, 12))
    vis.plot_comparison(images, titles, cmap='fractal_fire',
                        suptitle="Mandelbrot Deep Zoom")
    print("Deep zoom sequence generated!\n")


def example_custom_colormap():
    print("Example 4: Custom Colormaps")
    print("-" * 50)
    gen = MandelbrotGenerator(width=700, height=700, max_iter=256)
    gen.generate(centre=-0.5+0j, L=3.0)
    colormaps = ['hot', 'viridis', 'fractal_fire', 'fractal_ice']
    images = [gen.get_image()] * 4
    titles = [f"Colormap: {cmap}" for cmap in colormaps]
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(16, 16))
    axes = axes.flatten()
    from ..visualization.colormaps import PREDEFINED_COLORMAPS
    for idx, (img, title, cmap) in enumerate(zip(images, titles, colormaps)):
        plot_img = np.log1p(img)
        colormap = PREDEFINED_COLORMAPS.get(cmap, cmap)
        axes[idx].imshow(plot_img, cmap=colormap, origin='lower')
        axes[idx].set_title(title, fontsize=14)
        axes[idx].axis('off')
    plt.suptitle("Colormap Comparison", fontsize=16, fontweight='bold')
    plt.tight_layout()
    print("Colormap comparison generated!\n")


def example_high_resolution_export():
    print("Example 5: High-Resolution Export")
    print("-" * 50)
    gen = MandelbrotGenerator(width=2400, height=2400, max_iter=512, smooth=True)
    gen.generate(centre=-0.5+0j, L=3.0)
    export_fractal(gen.get_image(),
                   "mandelbrot_highres.png",
                   cmap='fractal_default',
                   dpi=300)
    print("High-resolution image exported!\n")


def example_julia_animation():
    print("Example 6: Julia Set Animation")
    print("-" * 50)
    print("Generating Julia set animation frames...")
    num_frames = 30
    images, titles = [], []
    for i in range(num_frames):
        angle = 2 * np.pi * i / num_frames
        C = 0.7885 * np.exp(1j * angle)
        gen = JuliaGenerator(C, width=400, height=400, max_iter=256)
        gen.generate(centre=0+0j, L=3.0)
        images.append(gen.get_image())
        titles.append(f"C = {C:.3f}")
    vis = FractalVisualizer(figsize=(18, 12))
    vis.plot_comparison(images[::5], titles[::5], cmap='fractal_default',
                        suptitle="Julia Set Parameter Evolution")
    print("Animation frames generated!\n")


def example_mandelbrot_regions():
    print("Example 7: Mandelbrot Interesting Regions")
    print("-" * 50)
    regions = [
        {'centre': -0.5+0j, 'L': 3.0, 'name': 'Full Set'},
        {'centre': -0.745+0.1j, 'L': 0.01, 'name': 'Seahorse Valley'},
        {'centre': 0.282-0.01j, 'L': 0.005, 'name': 'Elephant Valley'},
        {'centre': -0.761574-0.0847596j, 'L': 0.001, 'name': 'Spiral'},
        {'centre': -1.25+0j, 'L': 0.02, 'name': 'Antenna'},
        {'centre': -0.16+1.04j, 'L': 0.02, 'name': 'Triple Spiral'}
    ]
    gen = MandelbrotGenerator(width=500, height=500, max_iter=512)
    images, titles = [], []
    for region in regions:
        gen.generate(**{k: v for k, v in region.items() if k != 'name'})
        images.append(gen.get_image())
        titles.append(region['name'])
    vis = FractalVisualizer(figsize=(18, 12))
    vis.plot_comparison(images, titles, cmap='fractal_fire',
                        suptitle="Mandelbrot Set: Interesting Regions")
    print("Interesting regions explored!\n")


def run_all_examples():
    print("=" * 60)
    print("FRACTALSETS PACKAGE - EXAMPLES SHOWCASE")
    print("=" * 60)
    print()
    try:
        example_basic_mandelbrot()
        example_julia_variations()
        example_deep_zoom()
        example_custom_colormap()
        example_high_resolution_export()
        example_julia_animation()
        example_mandelbrot_regions()
        print("=" * 60)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
    except Exception as e:
        print(f"Error during examples: {e}")
        import traceback
        traceback.print_exc()
