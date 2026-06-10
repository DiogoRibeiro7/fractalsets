"""Command-line interface for rendering fractals."""

import argparse
from typing import Iterable, Optional

from .core.generators import BurningShipGenerator, JuliaGenerator, MandelbrotGenerator
from .examples.gallery import FractalGallery
from .utils.export import export_fractal
from .visualization.animator import FractalAnimator


def build_parser() -> argparse.ArgumentParser:
    """Build the fractalsets CLI parser."""
    parser = argparse.ArgumentParser(prog="fractalsets-render")
    parser.add_argument(
        "--fractal",
        choices=["mandelbrot", "julia", "burning-ship"],
        default="mandelbrot",
        help="Fractal type to render.",
    )
    parser.add_argument("--output", help="Output image path.")
    parser.add_argument("--width", type=int, default=800, help="Output width in pixels.")
    parser.add_argument("--height", type=int, default=800, help="Output height in pixels.")
    parser.add_argument(
        "--max-iter", type=int, default=256, help="Maximum iteration count."
    )
    parser.add_argument(
        "--centre-real", type=float, default=-0.5, help="Centre real coordinate."
    )
    parser.add_argument(
        "--centre-imag", type=float, default=0.0, help="Centre imaginary coordinate."
    )
    parser.add_argument("--L", type=float, default=3.0, help="View side length.")
    parser.add_argument("--xmin", type=float, help="Minimum real bound.")
    parser.add_argument("--xmax", type=float, help="Maximum real bound.")
    parser.add_argument("--ymin", type=float, help="Minimum imaginary bound.")
    parser.add_argument("--ymax", type=float, help="Maximum imaginary bound.")
    parser.add_argument("--cmap", default="fractal_default", help="Colormap to use.")
    parser.add_argument("--dpi", type=int, default=300, help="Export DPI.")
    parser.add_argument("--fps", type=int, default=30, help="Animation frames per second.")
    parser.add_argument(
        "--no-log-scale",
        action="store_true",
        help="Disable logarithmic normalization during export.",
    )
    parser.add_argument(
        "--no-smooth",
        action="store_true",
        help="Disable smooth iteration coloring.",
    )
    parser.add_argument("--preset", help="Named preset for the selected fractal type.")
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List presets for the selected fractal type and exit.",
    )
    parser.add_argument(
        "--animate",
        choices=["zoom", "julia-morph"],
        help="Render an animation instead of a single image.",
    )
    parser.add_argument(
        "--frames",
        type=int,
        default=60,
        help="Number of frames for animation modes.",
    )
    parser.add_argument(
        "--zoom-factor",
        type=float,
        default=1.05,
        help="Per-frame zoom factor for zoom animations.",
    )
    parser.add_argument(
        "--julia-end-real",
        type=float,
        help="Julia morph target constant real part.",
    )
    parser.add_argument(
        "--julia-end-imag",
        type=float,
        help="Julia morph target constant imaginary part.",
    )
    parser.add_argument("--julia-real", type=float, help="Julia constant real part.")
    parser.add_argument("--julia-imag", type=float, help="Julia constant imaginary part.")
    return parser


def _get_presets_for_fractal(fractal: str):
    """Return preset map for a fractal type."""
    if fractal == "julia":
        return FractalGallery.JULIA_CONSTANTS
    if fractal == "burning-ship":
        return FractalGallery.BURNING_SHIP_LOCATIONS
    return FractalGallery.MANDELBROT_LOCATIONS


def _validate_bounds(args: argparse.Namespace):
    """Validate optional explicit bounds."""
    bounds = (args.xmin, args.xmax, args.ymin, args.ymax)
    provided = [value is not None for value in bounds]
    if any(provided) and not all(provided):
        raise ValueError("Explicit bounds require --xmin, --xmax, --ymin, and --ymax together.")
    if args.animate == "zoom" and args.xmin is not None:
        raise ValueError("Zoom animation does not support explicit bounds; use centre/L or a preset.")


def _resolve_preset(args: argparse.Namespace):
    """Resolve an optional preset name."""
    if not args.preset:
        return None

    presets = _get_presets_for_fractal(args.fractal)
    if args.preset not in presets:
        raise ValueError(f"Unknown preset '{args.preset}' for fractal type '{args.fractal}'.")
    return presets[args.preset]


def _build_generator(args: argparse.Namespace):
    """Create the generator requested by CLI arguments."""
    smooth = not args.no_smooth
    common = {
        "width": args.width,
        "height": args.height,
        "max_iter": args.max_iter,
        "smooth": smooth,
    }

    if args.fractal == "julia":
        preset = _resolve_preset(args)
        if preset is not None:
            constant = preset
        elif args.julia_real is None or args.julia_imag is None:
            raise ValueError(
                "Julia rendering requires --julia-real and --julia-imag, or a Julia --preset."
            )
        else:
            constant = complex(args.julia_real, args.julia_imag)
        return JuliaGenerator(C=constant, **common)

    if args.fractal == "burning-ship":
        return BurningShipGenerator(**common)

    return MandelbrotGenerator(**common)


def _generate_image(generator, args: argparse.Namespace):
    """Generate the fractal image from CLI arguments."""
    _validate_bounds(args)
    if args.xmin is not None:
        return generator.generate(
            xmin=args.xmin,
            xmax=args.xmax,
            ymin=args.ymin,
            ymax=args.ymax,
        )

    preset = _resolve_preset(args)
    if preset is not None:
        if args.fractal == "julia":
            return generator.generate(centre=0 + 0j, L=3.0)
        return generator.generate(centre=preset["centre"], L=preset["L"])

    centre = complex(args.centre_real, args.centre_imag)
    return generator.generate(centre=centre, L=args.L)


def _resolve_view(args: argparse.Namespace):
    """Resolve the centre and side length for single-image and zoom rendering."""
    preset = _resolve_preset(args)
    if preset is not None and args.fractal != "julia":
        return preset["centre"], preset["L"]
    return complex(args.centre_real, args.centre_imag), args.L


def _run_animation(generator, args: argparse.Namespace) -> int:
    """Run an animation mode from CLI arguments."""
    animator = FractalAnimator(generator, fps=args.fps, dpi=args.dpi)

    if args.animate == "zoom":
        centre, start_L = _resolve_view(args)
        animator.create_zoom_animation(
            target=centre,
            num_frames=args.frames,
            zoom_factor=args.zoom_factor,
            start_L=start_L,
            output_path=args.output,
            cmap=args.cmap,
        )
        return 0

    if args.animate == "julia-morph":
        if args.fractal != "julia":
            raise ValueError("Julia morph animation requires --fractal julia.")
        if args.julia_end_real is None or args.julia_end_imag is None:
            raise ValueError(
                "Julia morph animation requires --julia-end-real and --julia-end-imag."
            )
        animator.create_julia_morph(
            start_C=generator.C,
            end_C=complex(args.julia_end_real, args.julia_end_imag),
            num_frames=args.frames,
            output_path=args.output,
            cmap=args.cmap,
        )
        return 0

    raise ValueError(f"Unsupported animation mode '{args.animate}'.")


def _list_presets(args: argparse.Namespace):
    """Print presets for the selected fractal type."""
    for name in sorted(_get_presets_for_fractal(args.fractal)):
        print(name)


def main(argv: Optional[Iterable[str]] = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.list_presets:
        _list_presets(args)
        return 0
    if not args.output:
        parser.error("--output is required unless --list-presets is used.")

    try:
        generator = _build_generator(args)
        if args.animate:
            return _run_animation(generator, args)
        image = _generate_image(generator, args)
    except ValueError as exc:
        parser.error(str(exc))

    export_fractal(
        image,
        args.output,
        cmap=args.cmap,
        log_scale=not args.no_log_scale,
        dpi=args.dpi,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
