"""Predefined fractal gallery and examples."""

import numpy as np
from ..core.generators import BurningShipGenerator, JuliaGenerator, MandelbrotGenerator
from ..visualization.plotters import FractalVisualizer


class FractalGallery:
    """Gallery of interesting fractal locations and parameters."""
    JULIA_CONSTANTS = {
        'dendrite': -0.4 + 0.6j,
        'siegel_disk': -0.391 - 0.587j,
        'douady_rabbit': -0.123 + 0.745j,
        'san_marco': -0.75 + 0.0j,
        'spiral': -0.7 + 0.27015j,
        'dragon': -0.8 + 0.156j,
        'bat': 0.285 + 0.01j,
        'seahorse_valley': -0.745 + 0.113j
    }

    MANDELBROT_LOCATIONS = {
        'full_set': {'centre': -0.5 + 0j, 'L': 3.0},
        'seahorse_valley': {'centre': -0.745 + 0.1j, 'L': 0.01},
        'mini_mandelbrot': {'centre': -0.743643887037151 + 0.131825890901124j, 'L': 0.000001},
        'spiral': {'centre': -0.761574 - 0.0847596j, 'L': 0.001},
        'elephant_valley': {'centre': 0.282 - 0.01j, 'L': 0.005},
    }

    BURNING_SHIP_LOCATIONS = {
        'full_set': {'centre': -0.5 - 0.5j, 'L': 4.0},
        'classic_ship': {'centre': -1.75 - 0.03j, 'L': 0.08},
        'harbor': {'centre': -1.8 - 0.01j, 'L': 0.03},
    }

    @classmethod
    def generate_julia_collection(cls, width: int = 600, height: int = 600) -> dict:
        collection = {}
        for name, C in cls.JULIA_CONSTANTS.items():
            gen = JuliaGenerator(C, width=width, height=height, max_iter=256)
            gen.generate(centre=0+0j, L=3.0)
            collection[name] = gen.get_image()
        return collection

    @classmethod
    def generate_mandelbrot_zoom_sequence(cls, location: str = 'seahorse_valley',
                                          num_zooms: int = 5) -> list:
        if location not in cls.MANDELBROT_LOCATIONS:
            raise ValueError(f"Unknown location: {location}")
        params = cls.MANDELBROT_LOCATIONS[location]
        gen = MandelbrotGenerator(width=800, height=800, max_iter=512)
        images = []
        current_L = 3.0
        zoom_factor = (3.0 / params['L']) ** (1.0 / num_zooms)
        for _ in range(num_zooms):
            gen.generate(centre=params['centre'], L=current_L)
            images.append(gen.get_image())
            current_L /= zoom_factor
        return images

    @classmethod
    def showcase(cls):
        """Display showcase of various fractals."""
        vis = FractalVisualizer(figsize=(15, 12))
        print("Generating Julia set collection...")
        julia_collection = cls.generate_julia_collection(width=400, height=400)
        images = list(julia_collection.values())
        titles = [name.replace('_', ' ').title() for name in julia_collection.keys()]
        vis.plot_comparison(images[:6], titles[:6], 
                            cmap='fractal_default',
                            suptitle="Famous Julia Sets")

        print("\nGenerating Mandelbrot exploration...")
        mandel_gen = MandelbrotGenerator(width=600, height=600, max_iter=256)
        mandel_images, mandel_titles = [], []
        for name, params in list(cls.MANDELBROT_LOCATIONS.items())[:4]:
            mandel_gen.generate(**params)
            mandel_images.append(mandel_gen.get_image())
            mandel_titles.append(name.replace('_', ' ').title())
        vis.plot_comparison(mandel_images, mandel_titles,
                            cmap='fractal_fire',
                            suptitle="Mandelbrot Set Exploration")

        print("\nGenerating Burning Ship exploration...")
        ship_gen = BurningShipGenerator(width=600, height=600, max_iter=256)
        ship_images, ship_titles = [], []
        for name, params in cls.BURNING_SHIP_LOCATIONS.items():
            ship_gen.generate(**params)
            ship_images.append(ship_gen.get_image())
            ship_titles.append(name.replace('_', ' ').title())
        vis.plot_comparison(ship_images, ship_titles,
                            cmap='fractal_fire',
                            suptitle="Burning Ship Exploration")
