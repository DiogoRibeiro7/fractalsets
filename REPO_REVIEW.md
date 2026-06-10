# Repository Review

## Summary

The repository has a solid core for Mandelbrot/Julia generation and basic plotting, but it is not yet aligned as a reliable distributable package. The main issues are packaging/runtime breakage, public API drift, and documentation claiming features that are either not exported, not packaged, or not implemented end to end.

## Findings

### 1. Import-time dependency handling is brittle and currently breaks package import

- `fractalsets/core/iterators.py:4` imports `numba` unconditionally at module import time.
- `requirements.txt:4` makes `numba` a hard dependency, while `pyproject.toml:35` and `setup.py:38` describe it as optional under `performance`.
- In the current environment, `import fractalsets` fails because the installed `numba` build is incompatible with the installed NumPy version. This also causes `pytest` collection to fail before any tests run.

Why this matters:
- Users cannot rely on `import fractalsets` succeeding unless they happen to have a compatible NumPy/Numba combination.
- The package metadata is internally inconsistent about whether `numba` is required or optional.

What to improve:
- Make `numba` an actual optional acceleration dependency with a pure-NumPy fallback.
- If `numba` remains required, pin compatible `numpy`/`numba` ranges in every dependency entry point consistently.
- Add an install/import smoke test in CI.

### 2. The documented API does not match the packaged API

- `README.md:152` documents `from fractalsets.gui import launch_gui`, but `fractalsets/gui` has no `__init__.py`, so it is not a normal packaged submodule.
- `README.md:161` and `README.md:226` document `from fractalsets.animation import FractalAnimator`, but there is no `fractalsets/animation.py` or `fractalsets/animation/` package. The implementation currently lives at `fractalsets/visualization/animator.py`.
- `README.md:176` documents `from fractalsets.visualization import Fractal3DRenderer`, but `fractalsets/visualization/__init__.py:1` does not re-export that class.
- `README.md:241` and `README.md:261` document `fractalsets.analysis`, but the implementation is in `analysis/advanced_analysis.py`, outside the installable package.
- `fractalsets/__init__.py:5` exports only a subset of the surface described in the README.

Why this matters:
- New users following the README will hit import errors even if the dependency issue is fixed.
- The project currently behaves more like a source tree than a stable library API.

What to improve:
- Decide the supported public import surface and implement it explicitly.
- Add `__init__.py` files where needed and re-export documented classes/functions.
- Move installable features under `fractalsets/` or stop documenting them as package APIs.

### 3. Packaging metadata and repository metadata are stale or placeholder-quality

- `pyproject.toml:45-48` still points to `yourusername/fractalsets`.
- `setup.py:12` uses `dev@fractalsets.org`, while `pyproject.toml` names a different author/contact.
- `README.md:68`, `README.md:202`, and `README.md:521` claim Docker support and a Jupyter tutorial, but those assets are not present in this repository snapshot.
- `README.md:66` claims full type hint support, but there is little validation around the higher-level modules and the codebase is not type-checked.
- `README.md` claims 145+ tests and 85% coverage, while the current `tests/` directory contains 39 test functions and the suite does not currently collect successfully in this environment.

Why this matters:
- Users and contributors cannot trust the advertised state of the project.
- Package index metadata and documentation will look unfinished.

What to improve:
- Remove placeholders and align author/contact/URLs across packaging files.
- Reduce README claims to what is demonstrably shipped and tested.
- Add CI-generated badges only for metrics that are actually produced.

### 4. Exporting with the default/custom fractal colormaps is broken

- `fractalsets/utils/export.py:21` uses `plt.get_cmap(cmap)`.
- The GUI defaults to names such as `fractal_default` and `fractal_fire` in `fractalsets/gui/interactive_explorer.py`.
- Those custom names are defined only in `fractalsets/visualization/colormaps.py`; they are not Matplotlib-registered colormap names.

Why this matters:
- Saving an image from the GUI with its default custom colormap selection can fail at runtime.
- The plotting path and the export path do not share the same colormap resolution logic.

What to improve:
- Reuse `PREDEFINED_COLORMAPS` in `export_fractal`.
- Add tests that export with custom fractal colormap names, not just built-in Matplotlib colormaps.

### 5. “Advanced analysis” is not packaged and has undeclared heavy dependencies

- `analysis/advanced_analysis.py:5-6` imports `scipy` and `sklearn`.
- It also imports `cv2` at `analysis/advanced_analysis.py:258` and `skimage` at `analysis/advanced_analysis.py:294`.
- None of those appear in `pyproject.toml` or `requirements.txt`.
- `analysis/advanced_analysis.py:6` imports `DBSCAN`, but it is not used in the file.

Why this matters:
- Even if moved under the package, these features would fail for users unless optional extras are declared and documented.
- The current location outside `fractalsets/` means these APIs are not available through normal installation anyway.

What to improve:
- Move analysis code into an installable subpackage, or explicitly treat it as experimental/not shipped.
- Declare optional extras such as `analysis`, `gui`, and `video`.
- Remove dead imports and split heavyweight dependencies behind feature-level imports.

### 6. The GUI advertises an unimplemented fractal type

- `fractalsets/gui/interactive_explorer.py:52` exposes `Burning Ship` in the selector.
- The repository does not currently provide a `BurningShipGenerator`, and the README itself still lists Burning Ship as not done at `README.md:527`.

Why this matters:
- The UI currently promises functionality the backend does not support.
- This creates avoidable runtime branching and contributor confusion.

What to improve:
- Either implement Burning Ship fully or remove it from the shipped GUI until the backend exists.

### 7. Test coverage is concentrated only on the simplest core paths

- Tests currently cover generators, iterators, and utility helpers.
- There are no tests for `visualization/animator.py`, `visualization/renderer_3d.py`, `gui/interactive_explorer.py`, example entry points, packaging/import contracts, or documented README imports.

Why this matters:
- The least stable parts of the project are the least validated.
- Regressions in the advertised user-facing features will slip through easily.

What to improve:
- Add smoke tests for documented imports and console entry points.
- Add non-interactive tests for export, animation frame generation, and 3D renderer shape/return contracts.
- Add at least one packaging/install test in CI.

## Priority Improvements

1. Fix package import reliability by resolving the `numpy`/`numba` contract and adding a fallback path or strict compatible pins.
2. Define the real public API and align the README, package exports, and on-disk module layout.
3. Move shipped features under `fractalsets/` and add missing `__init__.py` files for installable subpackages.
4. Fix export/GUI colormap interoperability.
5. Split optional features into extras like `performance`, `analysis`, `gui`, and `video`, with explicit dependency declarations.
6. Add CI checks for `import fractalsets`, `pip install .`, and the README code snippets that are meant to be supported.

## Feature Ideas Worth Implementing

### High-value product features

- **Burning Ship generator**: this is already hinted at in the GUI and roadmap, so it is the cleanest next fractal to add.
- **Arbitrary-precision deep zoom**: use `mpmath` or a perturbation-based renderer so deep zoom examples are mathematically credible beyond float precision.
- **Progressive/tiled rendering**: generate previews quickly, then refine tiles for high-resolution exports without freezing the GUI.
- **Bookmarkable explorations**: save/load view state including center, scale, max iterations, colormap, and fractal type.
- **CLI interface**: support commands like `fractalsets render ...` for batch rendering and automation.
- **Parameter sweeps**: generate Julia galleries or iteration/zoom batches from config files.

### Engineering features

- **Benchmark suite**: turn `.benchmarks/` into a maintained benchmark workflow comparing pure Python, NumPy, and Numba paths.
- **Golden-image regression tests**: verify representative renders do not drift unexpectedly.
- **Documentation examples as tests**: execute supported README snippets in CI.
- **Structured config objects**: replace ad hoc parameter passing with dataclasses or typed config models for generators/export/animations.

## Overall Assessment

The core numerical and plotting pieces are a reasonable foundation, but the repo needs one cleanup pass focused on packaging, API consistency, and truthfulness of documentation before adding many more features. Once that baseline is fixed, the best next feature is Burning Ship plus a proper CLI or progressive-render workflow, because both add visible user value without requiring the repo to overextend into many half-packaged subsystems.
