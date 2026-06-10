"""Command-line interface for rendering fractals."""

import argparse
from typing import Iterable, Optional

from .core.generators import BurningShipGenerator, JuliaGenerator, MandelbrotGenerator
from .utils.export import export_fractal


def build_parser() -> argparse.ArgumentParser:
    """Build the fractalsets CLI parser."""
    parser = argparse.ArgumentParser(prog="fractalsets-render")
    parser.add_argument(
        "--fractal",
        choices=["mandelbrot", "julia", "burning-ship"],
        default="mandelbrot",
        help="Fractal type to render.",
    )
    parser.add_argument("--output", required=True, help="Output image path.")
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
    parser.add_argument("--julia-real", type=float, help="Julia constant real part.")
    parser.add_argument("--julia-imag", type=float, help="Julia constant imaginary part.")
    return parser


def _validate_bounds(args: argparse.Namespace):
    """Validate optional explicit bounds."""
    bounds = (args.xmin, args.xmax, args.ymin, args.ymax)
    provided = [value is not None for value in bounds]
    if any(provided) and not all(provided):
        raise ValueError("Explicit bounds require --xmin, --xmax, --ymin, and --ymax together.")


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
        if args.julia_real is None or args.julia_imag is None:
            raise ValueError("Julia rendering requires --julia-real and --julia-imag.")
        return JuliaGenerator(C=complex(args.julia_real, args.julia_imag), **common)

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

    centre = complex(args.centre_real, args.centre_imag)
    return generator.generate(centre=centre, L=args.L)


def main(argv: Optional[Iterable[str]] = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        generator = _build_generator(args)
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
