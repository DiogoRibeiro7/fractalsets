"""Tests for non-interactive GUI controller logic."""

from fractalsets.core.generators import (
    BurningShipGenerator,
    JuliaGenerator,
    MandelbrotGenerator,
)
from fractalsets.gui.interactive_explorer import FractalExplorerGUI


class StubValue:
    """Minimal stand-in for Tk widgets exposing get/set or config."""

    def __init__(self, value=None):
        self.value = value
        self.config_calls = []

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

    def config(self, **kwargs):
        self.config_calls.append(kwargs)


class StubFrame:
    """Minimal stand-in for a Tk frame."""

    def __init__(self):
        self.pack_calls = []
        self.forget_calls = 0

    def pack(self, *args, **kwargs):
        self.pack_calls.append((args, kwargs))

    def pack_forget(self):
        self.forget_calls += 1


class StubButton:
    """Minimal stand-in for a Tk button used in preset refresh tests."""

    def __init__(self, parent, text=None, command=None):
        self.parent = parent
        self.text = text
        self.command = command
        self.destroyed = False
        self.pack_calls = []

    def pack(self, *args, **kwargs):
        self.pack_calls.append((args, kwargs))

    def destroy(self):
        self.destroyed = True


def make_gui():
    """Create a GUI instance without constructing a Tk window."""
    gui = FractalExplorerGUI.__new__(FractalExplorerGUI)
    gui.generator = None
    gui.history = []
    gui.history_index = -1
    gui.fractal_type = StubValue("Mandelbrot")
    gui.julia_real = StubValue("-0.4")
    gui.julia_imag = StubValue("0.6")
    gui.info_label = StubValue()
    gui.max_iter_label = StubValue()
    gui.julia_frame = StubFrame()
    gui.preset_frame = object()
    gui.preset_buttons = []
    return gui


class TestGUIHelpers:
    """Test GUI controller methods without opening a window."""

    def test_get_preset_names_for_mandelbrot(self):
        gui = make_gui()

        preset_names = gui._get_preset_names()

        assert preset_names == [
            "Full Set",
            "Seahorse Valley",
            "Elephant Valley",
            "Spiral",
            "Mini Mandelbrot",
        ]

    def test_get_preset_names_for_burning_ship(self):
        gui = make_gui()
        gui.fractal_type.set("Burning Ship")

        preset_names = gui._get_preset_names()

        assert preset_names == ["Full Set", "Classic Ship", "Harbor"]

    def test_refresh_presets_replaces_buttons(self, monkeypatch):
        gui = make_gui()
        stale = StubButton(None, text="stale")
        gui.preset_buttons = [stale]
        created = []

        def fake_button(parent, text=None, command=None):
            button = StubButton(parent, text=text, command=command)
            created.append(button)
            return button

        monkeypatch.setattr(
            "fractalsets.gui.interactive_explorer.ttk.Button",
            fake_button,
        )

        gui._refresh_presets()

        assert stale.destroyed is True
        assert [button.text for button in created] == gui._get_preset_names()
        assert gui.preset_buttons == created

    def test_ensure_generator_creates_mandelbrot(self):
        gui = make_gui()

        gui._ensure_generator(width=40, height=50, max_iter=64)

        assert isinstance(gui.generator, MandelbrotGenerator)
        assert gui.generator.width == 40
        assert gui.generator.height == 50
        assert gui.generator.max_iter == 64

    def test_ensure_generator_creates_julia(self):
        gui = make_gui()
        gui.fractal_type.set("Julia")

        gui._ensure_generator(width=40, height=50, max_iter=64)

        assert isinstance(gui.generator, JuliaGenerator)
        assert gui.generator.C == complex(-0.4, 0.6)

    def test_ensure_generator_creates_burning_ship(self):
        gui = make_gui()
        gui.fractal_type.set("Burning Ship")

        gui._ensure_generator(width=40, height=50, max_iter=64)

        assert isinstance(gui.generator, BurningShipGenerator)
        assert gui.generator.max_iter == 64

    def test_load_preset_updates_view(self):
        gui = make_gui()
        calls = []
        gui.generate_and_display = lambda: calls.append("render")

        gui.load_preset("Seahorse Valley")

        assert gui.current_centre == -0.745 + 0.1j
        assert gui.current_L == 0.01
        assert calls == ["render"]

    def test_load_burning_ship_preset_updates_view(self):
        gui = make_gui()
        gui.fractal_type.set("Burning Ship")
        calls = []
        gui.generate_and_display = lambda: calls.append("render")

        gui.load_preset("Classic Ship")

        assert gui.current_centre == -1.75 - 0.03j
        assert gui.current_L == 0.08
        assert calls == ["render"]

    def test_save_to_history_trims_forward_entries(self):
        gui = make_gui()
        gui.history = [(0 + 0j, 3.0), (1 + 0j, 2.0), (2 + 0j, 1.0)]
        gui.history_index = 1
        gui.current_centre = -0.5 + 0j
        gui.current_L = 0.5

        gui.save_to_history()

        assert gui.history == [(0 + 0j, 3.0), (1 + 0j, 2.0), (-0.5 + 0j, 0.5)]
        assert gui.history_index == 2

    def test_go_back_and_forward_navigate_history(self):
        gui = make_gui()
        gui.history = [(0 + 0j, 3.0), (-0.5 + 0j, 1.5)]
        gui.history_index = 1
        calls = []
        gui.generate_and_display = lambda: calls.append((gui.current_centre, gui.current_L))

        gui.go_back()
        gui.go_forward()

        assert calls == [(0 + 0j, 3.0), (-0.5 + 0j, 1.5)]

    def test_reset_view_sets_mandelbrot_defaults(self):
        gui = make_gui()
        calls = []
        gui.generate_and_display = lambda: calls.append("render")
        gui.history = [("x", "y")]
        gui.history_index = 0

        gui.reset_view()

        assert gui.current_centre == -0.5 + 0j
        assert gui.current_L == 3.0
        assert gui.history == []
        assert gui.history_index == -1
        assert calls == ["render"]

    def test_reset_view_sets_burning_ship_defaults(self):
        gui = make_gui()
        gui.fractal_type.set("Burning Ship")
        calls = []
        gui.generate_and_display = lambda: calls.append("render")

        gui.reset_view()

        assert gui.current_centre == -0.5 - 0.5j
        assert gui.current_L == 4.0
        assert calls == ["render"]

    def test_update_info_formats_label_text(self):
        gui = make_gui()
        gui.current_centre = -0.5 + 0.25j
        gui.current_L = 0.125
        gui.generator = MandelbrotGenerator(width=64, height=32, max_iter=128)

        gui.update_info()

        text = gui.info_label.config_calls[-1]["text"]
        assert "Centre:" in text
        assert "Resolution: 64x32" in text
        assert "Max Iter: 128" in text

    def test_on_param_change_updates_label(self):
        gui = make_gui()

        gui.on_param_change("128.8")

        assert gui.max_iter_label.config_calls[-1]["text"] == "128"

    def test_on_fractal_change_toggles_julia_controls(self):
        gui = make_gui()
        refresh_calls = []
        reset_calls = []
        gui._refresh_presets = lambda: refresh_calls.append("refresh")
        gui.reset_view = lambda: reset_calls.append("reset")

        gui.fractal_type.set("Julia")
        gui.on_fractal_change(None)
        gui.fractal_type.set("Mandelbrot")
        gui.on_fractal_change(None)

        assert len(gui.julia_frame.pack_calls) == 1
        assert gui.julia_frame.forget_calls == 1
        assert refresh_calls == ["refresh", "refresh"]
        assert reset_calls == ["reset", "reset"]
