"""3D visualization and rendering of fractals."""

import numpy as np
from typing import Optional, Tuple
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Fractal3DRenderer:
    """Render fractals in 3D with various techniques."""
    
    def __init__(self, figsize: Tuple[int, int] = (12, 10)):
        self.figsize = figsize
    
    def render_height_map(
        self,
        image: np.ndarray,
        elevation_scale: float = 1.0,
        cmap: str = 'terrain',
        show_wireframe: bool = False
    ):
        """Render iteration count as 3D height map."""
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        # Create coordinate meshgrid
        h, w = image.shape
        x = np.linspace(0, w-1, w)
        y = np.linspace(0, h-1, h)
        X, Y = np.meshgrid(x, y)
        
        # Use iteration count as height
        Z = np.log1p(image) * elevation_scale
        
        if show_wireframe:
            ax.plot_wireframe(X, Y, Z, cmap=cmap, alpha=0.7)
        else:
            ax.plot_surface(X, Y, Z, cmap=cmap, 
                          linewidth=0, antialiased=True)
        
        ax.set_xlabel('Real Axis')
        ax.set_ylabel('Imaginary Axis')
        ax.set_zlabel('Iteration Count')
        ax.set_title('3D Height Map of Fractal')
        
        return fig
    
    def render_mandelbulb(
        self,
        resolution: int = 100,
        max_iter: int = 10,
        power: int = 8,
        output_path: Optional[str] = None
    ):
        """Render 3D Mandelbulb fractal."""
        # Generate 3D points
        x = np.linspace(-1.5, 1.5, resolution)
        y = np.linspace(-1.5, 1.5, resolution)
        z = np.linspace(-1.5, 1.5, resolution)
        
        # Create voxel grid
        voxels = np.zeros((resolution, resolution, resolution), dtype=bool)
        
        for i, xi in enumerate(x):
            for j, yj in enumerate(y):
                for k, zk in enumerate(z):
                    if self._mandelbulb_iterate(xi, yj, zk, max_iter, power):
                        voxels[i, j, k] = True
        
        # Plot voxels
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111, projection='3d')
        ax.voxels(voxels, facecolors='cyan', edgecolor='k', alpha=0.5)
        ax.set_title(f'Mandelbulb (power={power})')
        
        if output_path:
            plt.savefig(output_path, dpi=150)
        
        return fig
    
    @staticmethod
    def _mandelbulb_iterate(x: float, y: float, z: float, 
                           max_iter: int, power: int) -> bool:
        """Check if point is in Mandelbulb."""
        x0, y0, z0 = x, y, z
        
        for _ in range(max_iter):
            r = np.sqrt(x**2 + y**2 + z**2)
            if r > 2.0:
                return False
            
            theta = np.arctan2(np.sqrt(x**2 + y**2), z)
            phi = np.arctan2(y, x)
            
            r_pow = r ** power
            x = r_pow * np.sin(theta * power) * np.cos(phi * power) + x0
            y = r_pow * np.sin(theta * power) * np.sin(phi * power) + y0
            z = r_pow * np.cos(theta * power) + z0
        
        return True
    
    def render_cross_sections(
        self,
        image: np.ndarray,
        num_levels: int = 10,
        cmap: str = 'viridis'
    ):
        """Render fractal as stacked cross-sections."""
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        h, w = image.shape
        levels = np.linspace(0, np.max(image), num_levels)
        
        for i, level in enumerate(levels):
            # Create contour at this level
            mask = (image >= level)
            Z = np.ones_like(image) * i
            
            x = np.arange(w)
            y = np.arange(h)
            X, Y = np.meshgrid(x, y)
            
            ax.contour(X, Y, image, levels=[level], 
                      offset=i, cmap=cmap, alpha=0.7)
        
        ax.set_title('Cross-Section Stack View')
        return fig


class StereoscopicRenderer:
    """Create stereoscopic 3D images for VR/3D viewing."""
    
    @staticmethod
    def create_anaglyph(
        image: np.ndarray,
        depth_scale: float = 0.05,
        cmap: str = 'gray'
    ):
        """Create red-cyan anaglyph 3D image."""
        # Use iteration count as depth
        depth = np.log1p(image)
        
        # Shift for stereo pair
        shift = int(depth_scale * image.shape[1])
        
        left = np.roll(image, -shift, axis=1)
        right = np.roll(image, shift, axis=1)
        
        # Create anaglyph
        anaglyph = np.zeros((*image.shape, 3))
        anaglyph[:, :, 0] = left / np.max(left)  # Red channel
        anaglyph[:, :, 1] = right / np.max(right)  # Green/Cyan
        anaglyph[:, :, 2] = right / np.max(right)
        
        return anaglyph
