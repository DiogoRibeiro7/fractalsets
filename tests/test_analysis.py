"""Tests for the packaged analysis API."""

import matplotlib

matplotlib.use("Agg")

import numpy as np

from fractalsets.analysis import BifurcationAnalyzer, FractalAnalyzer, OrbitAnalyzer


class TestFractalAnalyzer:
    """Test advanced fractal analysis helpers."""

    def test_detect_boundary_shape_and_dtype(self):
        """Boundary detection should preserve image shape and return booleans."""
        image = np.random.rand(32, 32) * 100

        boundary = FractalAnalyzer.detect_boundary(image)

        assert boundary.shape == image.shape
        assert boundary.dtype == np.bool_

    def test_detect_boundary_handles_zero_image(self):
        """Boundary detection should handle an all-zero image."""
        image = np.zeros((16, 16))

        boundary = FractalAnalyzer.detect_boundary(image)

        assert boundary.shape == image.shape
        assert not np.any(boundary)

    def test_calculate_hausdorff_dimension_returns_details(self):
        """Hausdorff estimation should return both a value and detail payload."""
        image = np.random.rand(64, 64) * 100

        dimension, details = FractalAnalyzer.calculate_hausdorff_dimension(image)

        assert isinstance(dimension, float)
        assert "box_sizes" in details
        assert "counts" in details
        assert "r_squared" in details

    def test_calculate_hausdorff_dimension_zero_image(self):
        """Hausdorff estimation should handle an all-zero image."""
        dimension, details = FractalAnalyzer.calculate_hausdorff_dimension(
            np.zeros((16, 16))
        )

        assert dimension == 0.0
        assert details["counts"] == []

    def test_compute_lyapunov_exponent_returns_float(self):
        """Lyapunov estimation should return a float."""
        value = FractalAnalyzer.compute_lyapunov_exponent(
            -0.4 + 0.6j, iterations=50, samples=5
        )

        assert isinstance(value, float)

    def test_find_periodic_points_returns_period_map(self):
        """Periodic-point detection should return a map for each requested period."""
        image = np.random.rand(40, 40) * 100

        periodic_points = FractalAnalyzer.find_periodic_points(
            image,
            bounds=(-2.0, 1.0, -1.5, 1.5),
            max_period=4,
        )

        assert sorted(periodic_points.keys()) == [1, 2, 3, 4]

    def test_compute_multifractal_spectrum_shapes(self):
        """Multifractal spectrum should return aligned q and Dq arrays."""
        image = np.random.rand(32, 32) * 10

        q_values, dq_values = FractalAnalyzer.compute_multifractal_spectrum(
            image, num_q=7
        )

        assert q_values.shape == (7,)
        assert dq_values.shape == (7,)

    def test_compute_multifractal_spectrum_zero_image(self):
        """Multifractal spectrum should handle an all-zero image."""
        q_values, dq_values = FractalAnalyzer.compute_multifractal_spectrum(
            np.zeros((8, 8)), num_q=5
        )

        assert q_values.shape == (5,)
        assert np.all(dq_values == 0)

    def test_detect_symmetries_returns_expected_keys(self):
        """Symmetry detection should report the standard axes."""
        image = np.random.rand(32, 32) * 50

        symmetries = FractalAnalyzer.detect_symmetries(image)

        assert set(symmetries.keys()) == {"vertical", "horizontal", "rotational_180"}

    def test_detect_symmetries_zero_image(self):
        """Zero image should be treated as perfectly symmetric."""
        symmetries = FractalAnalyzer.detect_symmetries(np.zeros((12, 12)))

        assert symmetries["vertical"] == 1.0
        assert symmetries["horizontal"] == 1.0
        assert symmetries["rotational_180"] == 1.0

    def test_compute_correlation_dimension_returns_details(self):
        """Correlation dimension should return a value and detail payload."""
        points = np.random.rand(20, 2)

        dimension, details = FractalAnalyzer.compute_correlation_dimension(points)

        assert isinstance(dimension, float)
        assert "r_values" in details
        assert "correlations" in details

    def test_extract_contours_returns_list(self):
        """Contour extraction should return a list for non-uniform inputs."""
        image = np.zeros((32, 32), dtype=np.float64)
        image[8:24, 8:24] = 10.0

        contours = FractalAnalyzer.extract_contours(image, levels=[1.0, 5.0])

        assert isinstance(contours, list)
        assert len(contours) > 0

    def test_extract_contours_zero_image(self):
        """Contour extraction should return no contours for a uniform zero image."""
        contours = FractalAnalyzer.extract_contours(np.zeros((16, 16)))

        assert contours == []

    def test_compute_entropy_returns_float(self):
        """Entropy computation should return a float."""
        image = np.random.rand(32, 32) * 100

        entropy = FractalAnalyzer.compute_entropy(image)

        assert isinstance(entropy, float)

    def test_analyze_self_similarity_returns_requested_scales(self):
        """Self-similarity analysis should return one entry per requested scale."""
        image = np.random.rand(32, 32) * 100

        similarities = FractalAnalyzer.analyze_self_similarity(
            image, scale_factors=[2, 4]
        )

        assert set(similarities.keys()) == {2, 4}


class TestBifurcationAnalyzer:
    """Test bifurcation helpers."""

    def test_generate_bifurcation_diagram_shapes(self):
        """Bifurcation diagram output should have paired arrays."""
        params, values = BifurcationAnalyzer.generate_bifurcation_diagram(
            (2.5, 3.5), num_points=8, iterations=30, last_n=4
        )

        assert params.shape == values.shape
        assert len(params) == 32

    def test_find_feigenbaum_constant_returns_value(self):
        """Feigenbaum estimation should return a float for enough inputs."""
        value = BifurcationAnalyzer.find_feigenbaum_constant(
            [3.0, 3.4, 3.54, 3.564]
        )

        assert isinstance(value, float)

    def test_find_feigenbaum_constant_short_input(self):
        """Feigenbaum estimation should return None when there are too few points."""
        assert BifurcationAnalyzer.find_feigenbaum_constant([3.0, 3.4]) is None


class TestOrbitAnalyzer:
    """Test orbit-analysis helpers."""

    def test_compute_orbit_returns_trajectory_and_escape_iter(self):
        """Orbit computation should return both the orbit and escape iteration."""
        orbit, escape_iter = OrbitAnalyzer.compute_orbit(
            z0=0 + 0j,
            C=-0.4 + 0.6j,
            max_iter=50,
        )

        assert len(orbit) >= 1
        assert isinstance(escape_iter, int)

    def test_classify_orbit_short_sequence(self):
        """Short orbits should classify as escaping."""
        classification = OrbitAnalyzer.classify_orbit([0 + 0j] * 10)

        assert classification == "escaping"

    def test_plot_orbit_returns_figure(self):
        """Orbit plotting should return a Matplotlib figure."""
        orbit, _ = OrbitAnalyzer.compute_orbit(0 + 0j, -0.4 + 0.6j, max_iter=25)

        fig = OrbitAnalyzer.plot_orbit(orbit)

        assert fig is not None
        assert len(fig.axes) == 2
