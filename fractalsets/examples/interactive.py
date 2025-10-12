"""Interactive fractal explorer utilities."""

from typing import Optional


class InteractiveFractalExplorer:
    """
    Interactive fractal exploration with click-to-zoom.

    Note: Requires matplotlib with an interactive backend.
    """
    def __init__(self, generator, initial_bounds=None):
        self.generator = generator
        self.history = []
        self.current_image = None

        if initial_bounds:
            self.generator.generate(xmin=initial_bounds[0], xmax=initial_bounds[1],
                                    ymin=initial_bounds[2], ymax=initial_bounds[3])
        else:
            self.generator.generate()

        self.current_image = self.generator.get_image()
        self.history.append(self.generator.bounds)

    def on_click(self, event, zoom_factor: float = 2.0):
        """Handle mouse click for zooming (left in, right out)."""
        if event.inaxes and event.button == 1:  # Left click
            bounds = self.generator.bounds
            width = bounds[1] - bounds[0]
            height = bounds[3] - bounds[2]
            x_frac = event.xdata / self.generator.width
            y_frac = event.ydata / self.generator.height
            centre = complex(bounds[0] + width * x_frac,
                             bounds[2] + height * y_frac)
            self.generator.zoom(centre, zoom_factor)
            self.current_image = self.generator.get_image()
            self.history.append(self.generator.bounds)
            return True
        elif event.button == 3:  # Right click - zoom out
            if len(self.history) > 1:
                self.history.pop()
                bounds = self.history[-1]
                self.generator.generate(xmin=bounds[0], xmax=bounds[1],
                                        ymin=bounds[2], ymax=bounds[3])
                self.current_image = self.generator.get_image()
                return True
        return False
