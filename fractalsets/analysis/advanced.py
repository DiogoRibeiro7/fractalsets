"""Advanced mathematical analysis of fractals."""

import numpy as np
from typing import Dict, List, Optional, Tuple
from scipy import ndimage


class FractalAnalyzer:
    """Advanced mathematical analysis tools for fractals."""

    @staticmethod
    def detect_boundary(image: np.ndarray, threshold: float = 0.9) -> np.ndarray:
        """Detect fractal boundary using edge detection."""
        max_value = np.max(image)
        if max_value <= 0:
            return np.zeros_like(image, dtype=bool)

        normalized = image / max_value
        edges_x = ndimage.sobel(normalized, axis=0)
        edges_y = ndimage.sobel(normalized, axis=1)
        boundary = np.hypot(edges_x, edges_y)
        return boundary > (threshold * np.max(boundary))

    @staticmethod
    def calculate_hausdorff_dimension(
        image: np.ndarray,
        box_sizes: Optional[List[int]] = None,
    ) -> Tuple[float, Dict]:
        """Calculate Hausdorff dimension using box-counting."""
        max_value = np.max(image)
        if max_value <= 0:
            return 0.0, {
                "box_sizes": [],
                "counts": [],
                "coefficients": np.array([0.0, 0.0]),
                "r_squared": 1.0,
            }

        if box_sizes is None:
            max_size = min(image.shape) // 4
            if max_size < 2:
                return 0.0, {
                    "box_sizes": [],
                    "counts": [],
                    "coefficients": np.array([0.0, 0.0]),
                    "r_squared": 1.0,
                }
            box_sizes = [2**i for i in range(1, int(np.log2(max_size)))]

        binary = (image > 0.5 * max_value).astype(int)
        counts = []
        for size in box_sizes:
            count = 0
            for i in range(0, binary.shape[0], size):
                for j in range(0, binary.shape[1], size):
                    box = binary[i:i + size, j:j + size]
                    if np.sum(box) > 0:
                        count += 1
            counts.append(count)

        valid_pairs = [(size, count) for size, count in zip(box_sizes, counts) if count > 0]
        if len(valid_pairs) < 2:
            return 0.0, {
                "box_sizes": box_sizes,
                "counts": counts,
                "coefficients": np.array([0.0, 0.0]),
                "r_squared": 1.0,
            }

        valid_sizes = [size for size, _ in valid_pairs]
        valid_counts = [count for _, count in valid_pairs]
        coeffs = np.polyfit(np.log(valid_sizes), np.log(valid_counts), 1)
        dimension = -coeffs[0]
        details = {
            "box_sizes": box_sizes,
            "counts": counts,
            "coefficients": coeffs,
            "r_squared": calculate_r_squared(valid_sizes, valid_counts, coeffs),
        }
        return dimension, details

    @staticmethod
    def compute_lyapunov_exponent(
        C: complex,
        iterations: int = 1000,
        samples: int = 100,
    ) -> float:
        """Compute a Lyapunov exponent estimate for a Julia set."""
        lyapunov_sum = 0.0
        for _ in range(samples):
            z = complex(np.random.uniform(-2, 2), np.random.uniform(-2, 2))
            local_sum = 0.0
            for n in range(iterations):
                z = z**2 + C
                if abs(z) > 2:
                    break
                derivative = abs(2 * z)
                if derivative > 0:
                    local_sum += np.log(derivative)
            if n > 0:
                lyapunov_sum += local_sum / n
        return lyapunov_sum / samples

    @staticmethod
    def find_periodic_points(
        image: np.ndarray,
        bounds: Tuple[float, float, float, float],
        max_period: int = 10,
        tolerance: float = 1e-6,
    ) -> Dict[int, List[complex]]:
        """Find periodic points of different periods."""
        xmin, xmax, ymin, ymax = bounds
        h, w = image.shape
        periodic_points = {p: [] for p in range(1, max_period + 1)}

        for i in range(0, h, 10):
            for j in range(0, w, 10):
                x = xmin + (xmax - xmin) * j / w
                y = ymin + (ymax - ymin) * i / h
                c = complex(x, y)
                if image[i, j] < 0.5 * np.max(image):
                    z = 0
                    trajectory = []
                    for _ in range(max_period * 2):
                        z = z**2 + c
                        trajectory.append(z)
                    for period in range(1, max_period + 1):
                        if len(trajectory) >= period * 2:
                            if abs(trajectory[period] - trajectory[0]) < tolerance:
                                periodic_points[period].append(c)
                                break
        return periodic_points

    @staticmethod
    def compute_multifractal_spectrum(
        image: np.ndarray,
        q_range: Tuple[float, float] = (-5, 5),
        num_q: int = 50,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Compute a multifractal spectrum."""
        q_values = np.linspace(q_range[0], q_range[1], num_q)
        Dq_values = []
        total = np.sum(image)
        if total <= 0:
            return q_values, np.zeros_like(q_values, dtype=np.float64)

        prob = image / total

        for q in q_values:
            if q == 1:
                entropy = -np.sum(prob * np.log(prob + 1e-10))
                Dq_values.append(entropy)
            else:
                partition = np.sum(prob**q)
                if partition > 0:
                    Dq = np.log(partition) / ((q - 1) * np.log(2))
                    Dq_values.append(Dq)
                else:
                    Dq_values.append(0)

        return q_values, np.array(Dq_values)

    @staticmethod
    def detect_symmetries(image: np.ndarray) -> Dict[str, float]:
        """Detect coarse image symmetries."""
        h, w = image.shape
        symmetries = {}
        max_value = np.max(image)
        if max_value <= 0:
            return {
                "vertical": 1.0,
                "horizontal": 1.0,
                "rotational_180": 1.0,
            }

        left = image[:, : w // 2]
        right = np.fliplr(image[:, w // 2 :])
        min_width = min(left.shape[1], right.shape[1])
        v_diff = np.mean(np.abs(left[:, :min_width] - right[:, :min_width]))
        symmetries["vertical"] = 1 - v_diff / max_value

        top = image[: h // 2, :]
        bottom = np.flipud(image[h // 2 :, :])
        min_height = min(top.shape[0], bottom.shape[0])
        h_diff = np.mean(np.abs(top[:min_height, :] - bottom[:min_height, :]))
        symmetries["horizontal"] = 1 - h_diff / max_value

        rotated = np.rot90(image, 2)
        r_diff = np.mean(np.abs(image - rotated))
        symmetries["rotational_180"] = 1 - r_diff / max_value
        return symmetries

    @staticmethod
    def compute_correlation_dimension(
        points: np.ndarray,
        r_values: Optional[np.ndarray] = None,
    ) -> Tuple[float, Dict]:
        """Compute a correlation dimension estimate."""
        if r_values is None:
            max_dist = np.max(np.sqrt(np.sum((points[:, None] - points) ** 2, axis=2)))
            r_values = np.logspace(np.log10(max_dist / 100), np.log10(max_dist), 50)

        N = len(points)
        correlations = []
        for r in r_values:
            distances = np.sqrt(np.sum((points[:, None] - points) ** 2, axis=2))
            count = np.sum(distances < r) - N
            correlation = count / (N * (N - 1))
            correlations.append(correlation)

        valid = np.array(correlations) > 0
        log_r = np.log(r_values[valid])
        log_C = np.log(np.array(correlations)[valid])
        coeffs = np.polyfit(log_r, log_C, 1)
        dimension = coeffs[0]
        details = {
            "r_values": r_values,
            "correlations": correlations,
            "dimension": dimension,
        }
        return dimension, details

    @staticmethod
    def extract_contours(
        image: np.ndarray,
        levels: Optional[List[float]] = None,
    ) -> List[np.ndarray]:
        """Extract contour lines at different iteration levels."""
        max_value = np.max(image)
        min_value = np.min(image)
        if max_value <= min_value:
            return []

        if levels is None:
            levels = np.linspace(0.1, 0.9, 9) * max_value

        try:
            import cv2
        except ImportError:
            from skimage import measure

            all_contours = []
            for level in levels:
                all_contours.extend(measure.find_contours(image, level))
            return all_contours

        normalized = (
            (image - min_value) / (max_value - min_value) * 255
        ).astype(np.uint8)

        all_contours = []
        for level in levels:
            threshold_level = int(level / max_value * 255)
            _, binary = cv2.threshold(
                normalized, threshold_level, 255, cv2.THRESH_BINARY
            )
            contours, _ = cv2.findContours(
                binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
            )
            all_contours.extend(contours)
        return all_contours

    @staticmethod
    def compute_entropy(image: np.ndarray, num_bins: int = 256) -> float:
        """Compute Shannon entropy of the fractal image."""
        hist, _ = np.histogram(image, bins=num_bins, density=True)
        hist = hist[hist > 0]
        return -np.sum(hist * np.log2(hist))

    @staticmethod
    def analyze_self_similarity(
        image: np.ndarray,
        scale_factors: List[float] = [2, 4, 8],
    ) -> Dict[float, float]:
        """Analyze self-similarity at different scales."""
        from skimage.transform import resize

        similarities = {}
        for scale in scale_factors:
            h, w = image.shape
            new_h, new_w = h // scale, w // scale
            start_h = h // 2 - new_h // 2
            start_w = w // 2 - new_w // 2
            center = image[start_h:start_h + new_h, start_w:start_w + new_w]
            resized = resize(center, image.shape, anti_aliasing=True)
            correlation = np.corrcoef(image.flatten(), resized.flatten())[0, 1]
            similarities[scale] = correlation
        return similarities


class BifurcationAnalyzer:
    """Analyze bifurcations in parameter space."""

    @staticmethod
    def generate_bifurcation_diagram(
        param_range: Tuple[float, float],
        num_points: int = 1000,
        iterations: int = 500,
        last_n: int = 100,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Generate a logistic-map bifurcation diagram."""
        r_values = np.linspace(param_range[0], param_range[1], num_points)
        all_params = []
        all_values = []

        for r in r_values:
            x = 0.5
            for _ in range(iterations - last_n):
                x = r * x * (1 - x)
            for _ in range(last_n):
                x = r * x * (1 - x)
                all_params.append(r)
                all_values.append(x)

        return np.array(all_params), np.array(all_values)

    @staticmethod
    def find_feigenbaum_constant(bifurcations: List[float]) -> float:
        """Estimate the Feigenbaum constant from bifurcation points."""
        if len(bifurcations) < 3:
            return None

        ratios = []
        for i in range(len(bifurcations) - 2):
            d1 = bifurcations[i + 1] - bifurcations[i]
            d2 = bifurcations[i + 2] - bifurcations[i + 1]
            if d2 != 0:
                ratios.append(d1 / d2)
        return np.mean(ratios) if ratios else None


def calculate_r_squared(x, y, coeffs):
    """Calculate R² for a polynomial fit."""
    y_pred = np.polyval(coeffs, np.log(x))
    ss_res = np.sum((np.log(y) - y_pred) ** 2)
    ss_tot = np.sum((np.log(y) - np.mean(np.log(y))) ** 2)
    return 1 - (ss_res / ss_tot)


class OrbitAnalyzer:
    """Analyze orbits of individual points."""

    @staticmethod
    def compute_orbit(
        z0: complex,
        C: complex,
        max_iter: int = 1000,
    ) -> Tuple[List[complex], int]:
        """Compute the orbit of a point."""
        orbit = [z0]
        z = z0
        for i in range(max_iter):
            z = z**2 + C
            orbit.append(z)
            if abs(z) > 2:
                return orbit, i
        return orbit, max_iter

    @staticmethod
    def classify_orbit(orbit: List[complex]) -> str:
        """Classify orbit behavior."""
        if len(orbit) < 100:
            return "escaping"

        last_100 = orbit[-100:]
        for period in range(1, 50):
            matches = 0
            for i in range(len(last_100) - period):
                if abs(last_100[i] - last_100[i + period]) < 1e-6:
                    matches += 1
            if matches > len(last_100) * 0.8:
                return f"periodic-{period}"

        if all(abs(z) < 2 for z in last_100):
            return "quasi-periodic"
        return "chaotic"

    @staticmethod
    def plot_orbit(
        orbit: List[complex],
        output_path: Optional[str] = None,
    ):
        """Plot the orbit in the complex plane."""
        import matplotlib.pyplot as plt

        real = [z.real for z in orbit]
        imag = [z.imag for z in orbit]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        ax1.plot(real, imag, "b-", alpha=0.5, linewidth=0.5)
        ax1.scatter(real[0], imag[0], c="green", s=100, label="Start", zorder=5)
        ax1.scatter(real[-1], imag[-1], c="red", s=100, label="End", zorder=5)
        ax1.set_xlabel("Real")
        ax1.set_ylabel("Imaginary")
        ax1.set_title("Orbit in Complex Plane")
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.axis("equal")

        ax2.plot(range(len(real)), real, label="Real part", alpha=0.7)
        ax2.plot(range(len(imag)), imag, label="Imaginary part", alpha=0.7)
        ax2.set_xlabel("Iteration")
        ax2.set_ylabel("Value")
        ax2.set_title("Orbit Time Series")
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=150)
        return fig
