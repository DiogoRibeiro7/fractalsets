"""Setup script for FractalSets package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fractalsets",
    version="1.0.0",
    author="Diogo Ribeiro",
    author_email="dfr@esmad.ipp.pt",
    description="A comprehensive Python package for generating and visualizing Mandelbrot and Julia set fractals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DiogoRibeiro7/fractalsets",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.20.0",
        "matplotlib>=3.3.0",
        "Pillow>=8.0.0",
    ],
    extras_require={
        "performance": ["numba>=0.59,<0.62"],
        "analysis": [
            "scipy>=1.10",
            "scikit-learn>=1.3",
            "scikit-image>=0.21",
            "opencv-python>=4.8",
        ],
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "sphinx>=4.0",
        ],
        "all": [
            "numba>=0.59,<0.62",
            "scipy>=1.10",
            "scikit-learn>=1.3",
            "scikit-image>=0.21",
            "opencv-python>=4.8",
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "sphinx>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fractalsets-demo=fractalsets.examples.advanced_examples:run_all_examples",
            "fractalsets-gallery=fractalsets.examples.gallery:FractalGallery.showcase",
            "fractalsets-render=fractalsets.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
