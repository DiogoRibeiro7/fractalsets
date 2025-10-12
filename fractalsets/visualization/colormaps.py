"""Custom colormaps for fractal visualization."""

import numpy as np
from matplotlib.colors import LinearSegmentedColormap


def create_custom_colormap(name: str = 'fractal_default'):
    if name == 'fractal_default':
        colors = ['#000033', '#000055', '#0000BB', '#0E4C92',
                  '#2E8BC0', '#19D3F3', '#FFF000', '#FF6600', '#C70039']
    elif name == 'fractal_fire':
        colors = ['#000000', '#1a0000', '#4d0000', '#800000',
                  '#cc0000', '#ff3300', '#ff6600', '#ff9933', '#ffcc00']
    elif name == 'fractal_ice':
        colors = ['#000033', '#000066', '#0033cc', '#0066ff',
                  '#3399ff', '#66ccff', '#99ffff', '#ccffff', '#ffffff']
    elif name == 'fractal_psychedelic':
        colors = ['#ff00ff', '#ff0080', '#ff0000', '#ff8000',
                  '#ffff00', '#80ff00', '#00ff00', '#00ff80', '#00ffff']
    else:
        colors = ['black', 'blue', 'cyan', 'yellow', 'red', 'white']
    return LinearSegmentedColormap.from_list(name, colors, N=256)


PREDEFINED_COLORMAPS = {
    'hot': 'hot',
    'viridis': 'viridis',
    'plasma': 'plasma',
    'twilight': 'twilight',
    'fractal_default': create_custom_colormap('fractal_default'),
    'fractal_fire': create_custom_colormap('fractal_fire'),
    'fractal_ice': create_custom_colormap('fractal_ice'),
    'fractal_psychedelic': create_custom_colormap('fractal_psychedelic')
}
