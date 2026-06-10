"""Interactive GUI for fractal exploration."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from typing import Optional


class FractalExplorerGUI:
    """
    Interactive GUI application for exploring fractals.
    
    Features:
    - Click to zoom in/out
    - Real-time parameter adjustment
    - Save high-resolution images
    - Preset locations
    - History navigation
    """
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("FractalSets Explorer")
        self.root.geometry("1200x800")

        self.generator = None

        self.history = []
        self.history_index = -1
        
        self.setup_ui()
        self.generate_and_display()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Controls
        control_frame = ttk.Frame(main_frame, width=300)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Fractal type selection
        ttk.Label(control_frame, text="Fractal Type:").pack()
        self.fractal_type = ttk.Combobox(
            control_frame,
            values=["Mandelbrot", "Julia"],
            state="readonly"
        )
        self.fractal_type.set("Mandelbrot")
        self.fractal_type.pack()
        self.fractal_type.bind("<<ComboboxSelected>>", self.on_fractal_change)
        
        # Julia constant (only for Julia sets)
        self.julia_frame = ttk.LabelFrame(control_frame, text="Julia Constant")
        self.julia_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.julia_frame, text="Real:").grid(row=0, column=0)
        self.julia_real = ttk.Entry(self.julia_frame, width=10)
        self.julia_real.insert(0, "-0.4")
        self.julia_real.grid(row=0, column=1)
        
        ttk.Label(self.julia_frame, text="Imag:").grid(row=1, column=0)
        self.julia_imag = ttk.Entry(self.julia_frame, width=10)
        self.julia_imag.insert(0, "0.6")
        self.julia_imag.grid(row=1, column=1)
        
        # Parameters
        params_frame = ttk.LabelFrame(control_frame, text="Parameters")
        params_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(params_frame, text="Max Iterations:").pack()
        self.max_iter_scale = ttk.Scale(
            params_frame, from_=50, to=2000,
            orient=tk.HORIZONTAL, command=self.on_param_change
        )
        self.max_iter_scale.set(256)
        self.max_iter_scale.pack(fill=tk.X)
        self.max_iter_label = ttk.Label(params_frame, text="256")
        self.max_iter_label.pack()
        
        ttk.Label(params_frame, text="Resolution:").pack()
        self.resolution = ttk.Combobox(
            params_frame,
            values=["400x400", "600x600", "800x800", "1200x1200"],
            state="readonly"
        )
        self.resolution.set("600x600")
        self.resolution.pack()
        
        # Colormap selection
        ttk.Label(control_frame, text="Colormap:").pack()
        self.colormap = ttk.Combobox(
            control_frame,
            values=["fractal_default", "fractal_fire", "fractal_ice", 
                   "fractal_psychedelic", "viridis", "plasma", "hot"],
            state="readonly"
        )
        self.colormap.set("fractal_default")
        self.colormap.pack()
        self.colormap.bind("<<ComboboxSelected>>", self.on_colormap_change)
        
        # Presets
        preset_frame = ttk.LabelFrame(control_frame, text="Presets")
        preset_frame.pack(fill=tk.X, pady=5)
        
        presets = [
            "Full Set", "Seahorse Valley", "Elephant Valley",
            "Spiral", "Mini Mandelbrot"
        ]
        for preset in presets:
            btn = ttk.Button(
                preset_frame, text=preset,
                command=lambda p=preset: self.load_preset(p)
            )
            btn.pack(fill=tk.X, pady=2)
        
        # Action buttons
        action_frame = ttk.Frame(control_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            action_frame, text="Regenerate",
            command=self.generate_and_display
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            action_frame, text="Save Image",
            command=self.save_image
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            action_frame, text="Reset View",
            command=self.reset_view
        ).pack(fill=tk.X, pady=2)
        
        # Navigation
        nav_frame = ttk.Frame(control_frame)
        nav_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(nav_frame, text="◄ Back", command=self.go_back).pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )
        ttk.Button(nav_frame, text="Forward ►", command=self.go_forward).pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )
        
        # Info display
        self.info_label = ttk.Label(
            control_frame,
            text="Click to zoom in\nRight-click to zoom out",
            justify=tk.CENTER
        )
        self.info_label.pack(pady=10)
        
        # Right panel - Display
        display_frame = ttk.Frame(main_frame)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.figure = Figure(figsize=(8, 8))
        self.ax = self.figure.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.figure, display_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
    
    def generate_and_display(self):
        """Generate fractal and display it."""
        # Get parameters
        width, height = map(int, self.resolution.get().split('x'))
        max_iter = int(self.max_iter_scale.get())

        if not hasattr(self, 'current_centre'):
            self.current_centre = -0.5 + 0j
            self.current_L = 3.0

        self._ensure_generator(width, height, max_iter)
        self.generator.generate(centre=self.current_centre, L=self.current_L)
        
        # Display
        self.ax.clear()
        image = np.log1p(self.generator.get_image())
        
        from ..visualization.colormaps import PREDEFINED_COLORMAPS
        cmap = PREDEFINED_COLORMAPS.get(
            self.colormap.get(),
            self.colormap.get()
        )
        
        self.ax.imshow(image, cmap=cmap, origin='lower')
        self.ax.axis('off')
        self.canvas.draw()
        
        # Update info
        self.update_info()
    
    def on_click(self, event):
        """Handle mouse click for zooming."""
        if event.inaxes != self.ax:
            return
        
        if event.button == 1:  # Left click - zoom in
            zoom_factor = 2.0
        elif event.button == 3:  # Right click - zoom out
            zoom_factor = 0.5
        else:
            return
        
        # Save current state to history
        self.save_to_history()
        
        # Calculate new centre
        width = self.generator.width
        height = self.generator.height
        
        x_frac = event.xdata / width
        y_frac = event.ydata / height
        
        bounds = self.generator.bounds
        width_complex = bounds[1] - bounds[0]
        height_complex = bounds[3] - bounds[2]
        
        click_real = bounds[0] + width_complex * x_frac
        click_imag = bounds[2] + height_complex * y_frac
        
        self.current_centre = complex(click_real, click_imag)
        self.current_L = self.current_L / zoom_factor
        
        self.generate_and_display()
    
    def on_scroll(self, event):
        """Handle mouse scroll for zooming."""
        if event.inaxes != self.ax:
            return
        
        self.save_to_history()
        
        if event.button == 'up':
            self.current_L /= 1.1
        else:
            self.current_L *= 1.1
        
        self.generate_and_display()
    
    def on_param_change(self, value):
        """Update parameter labels."""
        self.max_iter_label.config(text=str(int(float(value))))
    
    def on_colormap_change(self, event):
        """Regenerate with new colormap."""
        self.generate_and_display()
    
    def on_fractal_change(self, event):
        """Change fractal type."""
        fractal_type = self.fractal_type.get()
        
        if fractal_type == "Julia":
            self.julia_frame.pack(fill=tk.X, pady=5)
        else:
            self.julia_frame.pack_forget()
        
        self.reset_view()

    def _ensure_generator(self, width: int, height: int, max_iter: int):
        """Create or update the generator for the selected fractal type."""
        from ..core.generators import JuliaGenerator, MandelbrotGenerator

        fractal_type = self.fractal_type.get()
        if fractal_type == "Julia":
            C = complex(float(self.julia_real.get()), float(self.julia_imag.get()))
            if not isinstance(self.generator, JuliaGenerator):
                self.generator = JuliaGenerator(C, width=width, height=height, max_iter=max_iter)
            else:
                self.generator.width = width
                self.generator.height = height
                self.generator.max_iter = max_iter
                self.generator.set_constant(C)
            return

        if not isinstance(self.generator, MandelbrotGenerator):
            self.generator = MandelbrotGenerator(width=width, height=height, max_iter=max_iter)
        else:
            self.generator.width = width
            self.generator.height = height
            self.generator.max_iter = max_iter
    
    def load_preset(self, preset_name: str):
        """Load a preset location."""
        from ..examples.gallery import FractalGallery
        
        presets = {
            "Full Set": ('full_set', FractalGallery.MANDELBROT_LOCATIONS),
            "Seahorse Valley": ('seahorse_valley', FractalGallery.MANDELBROT_LOCATIONS),
            "Elephant Valley": ('elephant_valley', FractalGallery.MANDELBROT_LOCATIONS),
            "Spiral": ('spiral', FractalGallery.MANDELBROT_LOCATIONS),
            "Mini Mandelbrot": ('mini_mandelbrot', FractalGallery.MANDELBROT_LOCATIONS)
        }
        
        if preset_name in presets:
            key, locations = presets[preset_name]
            params = locations[key]
            self.current_centre = params['centre']
            self.current_L = params['L']
            self.generate_and_display()
    
    def save_to_history(self):
        """Save current state to history."""
        state = (self.current_centre, self.current_L)
        
        # Remove forward history
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        self.history.append(state)
        self.history_index = len(self.history) - 1
    
    def go_back(self):
        """Navigate back in history."""
        if self.history_index > 0:
            self.history_index -= 1
            self.current_centre, self.current_L = self.history[self.history_index]
            self.generate_and_display()
    
    def go_forward(self):
        """Navigate forward in history."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_centre, self.current_L = self.history[self.history_index]
            self.generate_and_display()
    
    def reset_view(self):
        """Reset to default view."""
        self.current_centre = -0.5 + 0j
        self.current_L = 3.0
        self.history = []
        self.history_index = -1
        self.generate_and_display()
    
    def save_image(self):
        """Save current fractal as image."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            from ..utils.export import export_fractal
            export_fractal(
                self.generator.get_image(),
                filename,
                cmap=self.colormap.get(),
                dpi=300
            )
            messagebox.showinfo("Success", f"Image saved to {filename}")
    
    def update_info(self):
        """Update information display."""
        info_text = f"Centre: {self.current_centre:.6f}\n"
        info_text += f"Scale: {self.current_L:.2e}\n"
        info_text += f"Resolution: {self.generator.width}x{self.generator.height}\n"
        info_text += f"Max Iter: {self.generator.max_iter}"
        self.info_label.config(text=info_text)


def launch_gui():
    """Launch the interactive GUI application."""
    root = tk.Tk()
    app = FractalExplorerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
