"""Animation module for creating fractal videos and GIFs."""

import numpy as np
from typing import List, Tuple, Optional, Callable
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
import matplotlib.pyplot as plt


class FractalAnimator:
    """Create animations of fractals with various effects."""
    
    def __init__(self, generator, fps: int = 30, dpi: int = 100):
        self.generator = generator
        self.fps = fps
        self.dpi = dpi
    
    def create_zoom_animation(
        self,
        target: complex,
        num_frames: int = 100,
        zoom_factor: float = 1.05,
        start_L: float = 3.0,
        output_path: str = "zoom.mp4",
        cmap: str = "fractal_default"
    ):
        """Create smooth zoom animation into a point."""
        frames = []
        L = start_L
        
        for i in range(num_frames):
            self.generator.generate(centre=target, L=L)
            frames.append(self.generator.get_image())
            L /= zoom_factor
        
        self._save_animation(frames, output_path, cmap)
    
    def create_julia_morph(
        self,
        start_C: complex,
        end_C: complex,
        num_frames: int = 100,
        output_path: str = "julia_morph.mp4",
        cmap: str = "fractal_default"
    ):
        """Morph between two Julia set constants."""
        from ..core.generators import JuliaGenerator
        
        frames = []
        for i in range(num_frames):
            t = i / (num_frames - 1)
            # Linear interpolation
            C = start_C * (1 - t) + end_C * t
            
            self.generator.set_constant(C)
            self.generator.generate(centre=0+0j, L=3.0)
            frames.append(self.generator.get_image())
        
        self._save_animation(frames, output_path, cmap)
    
    def create_rotation_animation(
        self,
        centre: complex,
        L: float,
        num_frames: int = 100,
        output_path: str = "rotation.mp4",
        cmap: str = "fractal_default"
    ):
        """Rotate the complex plane around a point."""
        frames = []
        
        for i in range(num_frames):
            angle = 2 * np.pi * i / num_frames
            rotation = np.exp(1j * angle)
            
            # Rotate bounds
            self.generator.generate(centre=centre * rotation, L=L)
            frames.append(self.generator.get_image())
        
        self._save_animation(frames, output_path, cmap)
    
    def create_colormap_cycle(
        self,
        image: np.ndarray,
        colormaps: List[str],
        frames_per_cmap: int = 30,
        output_path: str = "colormap_cycle.gif"
    ):
        """Cycle through different colormaps."""
        # Implementation for cycling colormaps
        pass
    
    def create_max_iter_animation(
        self,
        centre: complex,
        L: float,
        max_iter_range: Tuple[int, int],
        num_frames: int = 100,
        output_path: str = "max_iter.mp4",
        cmap: str = "fractal_default"
    ):
        """Animate increasing max_iter to show detail emergence."""
        frames = []
        min_iter, max_iter = max_iter_range
        
        for i in range(num_frames):
            t = i / (num_frames - 1)
            current_iter = int(min_iter + (max_iter - min_iter) * t)
            
            self.generator.max_iter = current_iter
            self.generator.generate(centre=centre, L=L)
            frames.append(self.generator.get_image())
        
        self._save_animation(frames, output_path, cmap)
    
    def _save_animation(
        self,
        frames: List[np.ndarray],
        output_path: str,
        cmap: str
    ):
        """Save frames as video or GIF."""
        from ..visualization.colormaps import PREDEFINED_COLORMAPS
        
        fig, ax = plt.subplots(figsize=(10, 10))
        colormap = PREDEFINED_COLORMAPS.get(cmap, cmap)
        
        # Prepare first frame
        img_data = np.log1p(frames[0])
        im = ax.imshow(img_data, cmap=colormap, origin='lower')
        ax.axis('off')
        
        def update(frame_num):
            img_data = np.log1p(frames[frame_num])
            im.set_array(img_data)
            return [im]
        
        anim = FuncAnimation(
            fig, update, frames=len(frames),
            interval=1000//self.fps, blit=True
        )
        
        if output_path.endswith('.gif'):
            writer = PillowWriter(fps=self.fps)
        else:
            writer = FFMpegWriter(fps=self.fps, bitrate=5000)
        
        anim.save(output_path, writer=writer, dpi=self.dpi)
        plt.close(fig)
        print(f"Animation saved to {output_path}")


class FractalVideoExporter:
    """Export high-quality fractal videos."""
    
    @staticmethod
    def create_journey(
        waypoints: List[Tuple[complex, float]],
        generator,
        output_path: str = "journey.mp4",
        frames_between: int = 60,
        fps: int = 30,
        cmap: str = "fractal_default"
    ):
        """Create a journey through multiple interesting points."""
        frames = []
        
        for i in range(len(waypoints) - 1):
            start_centre, start_L = waypoints[i]
            end_centre, end_L = waypoints[i + 1]
            
            # Interpolate between waypoints
            for j in range(frames_between):
                t = j / frames_between
                
                # Smooth interpolation
                t_smooth = 3*t**2 - 2*t**3  # Smoothstep
                
                current_centre = start_centre * (1-t_smooth) + end_centre * t_smooth
                current_L = start_L * (1-t_smooth) + end_L * t_smooth
                
                generator.generate(centre=current_centre, L=current_L)
                frames.append(generator.get_image())
        
        animator = FractalAnimator(generator, fps=fps)
        animator._save_animation(frames, output_path, cmap)
