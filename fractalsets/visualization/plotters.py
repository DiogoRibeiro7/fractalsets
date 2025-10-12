"""Visualization tools for fractals."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Optional, Tuple
from .colormaps import PREDEFINED_COLORMAPS


class FractalVisualizer:
    """Comprehensive fractal visualization class."""
    def __init__(self, figsize: Tuple[int, int] = (12, 10)):
        self.figsize = figsize
        self.fig = None
        self.ax = None

    def plot(self, image: np.ndarray, title: str = "Fractal",
             cmap: str = 'fractal_default',
             show_colorbar: bool = True,
             show_axes: bool = False,
             log_scale: bool = True,
             bounds: Optional[Tuple[float, float, float, float]] = None) -> Figure:
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        plot_image = np.log1p(image) if log_scale else image
        colormap = PREDEFINED_COLORMAPS.get(cmap, cmap)
        extent = bounds if bounds else None
        im = self.ax.imshow(plot_image, cmap=colormap, origin='lower',
                            extent=extent, interpolation='bilinear')
        self.ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        if show_colorbar:
            cbar = plt.colorbar(im, ax=self.ax, fraction=0.46/10, pad=0.04)
            cbar.set_label('Iteration Count', rotation=270, labelpad=20)
        if show_axes and bounds:
            self.ax.set_xlabel('Real Axis', fontsize=12)
            self.ax.set_ylabel('Imaginary Axis', fontsize=12)
        else:
            self.ax.axis('off')
        plt.tight_layout()
        return self.fig

    def plot_comparison(self, images: list, titles: list,
                        cmap: str = 'fractal_default',
                        suptitle: str = "Fractal Comparison") -> Figure:
        n = len(images)
        cols = min(3, n)
        rows = (n + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 5*rows))
        axes = np.array(axes).flatten()
        colormap = PREDEFINED_COLORMAPS.get(cmap, cmap)
        for idx, (img, title) in enumerate(zip(images, titles)):
            plot_img = np.log1p(img)
            axes[idx].imshow(plot_img, cmap=colormap, origin='lower')
            axes[idx].set_title(title, fontsize=12)
            axes[idx].axis('off')
        for idx in range(len(images), len(axes)):
            axes[idx].axis('off')
        fig.suptitle(suptitle, fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig

    def animate_zoom(self, generator, centre: complex, 
                     num_frames: int = 50, zoom_factor: float = 1.1,
                     cmap: str = 'fractal_default', save_path: Optional[str] = None):
        from matplotlib.animation import FuncAnimation, PillowWriter
        fig, ax = plt.subplots(figsize=self.figsize)
        generator.generate()
        img_data = np.log1p(generator.get_image())
        colormap = PREDEFINED_COLORMAPS.get(cmap, cmap)
        im = ax.imshow(img_data, cmap=colormap, origin='lower')
        ax.axis('off')

        def update(frame):
            zoom = zoom_factor ** frame
            generator.zoom(centre, zoom)
            img_data = np.log1p(generator.get_image())
            im.set_array(img_data)
            ax.set_title(f"Zoom: {zoom:.2f}x", fontsize=14)
            return [im]

        anim = FuncAnimation(fig, update, frames=num_frames, interval=100, blit=True)
        if save_path:
            writer = PillowWriter(fps=10)
            anim.save(save_path, writer=writer)
            print(f"Animation saved to {save_path}")
        plt.show()
        return anim
