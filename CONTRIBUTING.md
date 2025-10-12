# Contributing to FractalSets

Thank you for your interest in contributing to FractalSets! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming environment for all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/DiogoRibeiro7/fractalsets/issues)
2. If not, create a new issue with:

  - Clear, descriptive title
  - Steps to reproduce
  - Expected vs actual behavior
  - Python version and OS
  - Relevant code snippets or error messages

### Suggesting Enhancements

1. Check existing issues and discussions
2. Create an issue describing:

  - The enhancement goal
  - Why it would be useful
  - Possible implementation approach

### Pull Requests

1. **Fork and Clone**

  ```bash
  git clone https://github.com/yourusername/fractalsets.git
  cd fractalsets
  ```

2. **Create a Branch**

  ```bash
  git checkout -b feature/your-feature-name
  ```

3. **Set Up Development Environment**

  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -e .[dev]
  ```

4. **Make Changes**

  - Write clear, documented code
  - Follow existing code style
  - Add tests for new features
  - Update documentation

5. **Run Tests**

  ```bash
  # Run all tests
  pytest tests/ -v

  # Check coverage
  pytest tests/ --cov=fractalsets --cov-report=html

  # Format code
  black fractalsets/

  # Lint
  flake8 fractalsets/
  ```

6. **Commit Changes**

  ```bash
  git add .
  git commit -m "feat: add new fractal type"
  ```

  Use conventional commits:

  - `feat:` - New feature
  - `fix:` - Bug fix
  - `docs:` - Documentation changes
  - `test:` - Test additions/changes
  - `refactor:` - Code refactoring
  - `perf:` - Performance improvements

7. **Push and Create PR**

  ```bash
  git push origin feature/your-feature-name
  ```

  Then create a pull request on GitHub.

## Development Guidelines

### Code Style

- Follow PEP 8
- Use Black for formatting (line length: 88)
- Use meaningful variable names
- Add docstrings to all public functions/classes

Example docstring:

```python
def fractal_function(param1: int, param2: str) -> np.ndarray:
    """
    Brief description of function.

    Longer description if needed, explaining the purpose,
    algorithm, or mathematical background.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input is provided

    Example:
        >>> result = fractal_function(100, "test")
        >>> print(result.shape)
        (100, 100)
    """
    pass
```

### Testing

- Write tests for all new features
- Aim for >80% code coverage
- Test edge cases and error conditions
- Use descriptive test names

```python
def test_mandelbrot_generator_handles_zero_dimensions():
    """Test that generator raises ValueError for zero dimensions."""
    with pytest.raises(ValueError):
        gen = MandelbrotGenerator(width=0, height=100)
```

### Documentation

- Update README.md if adding user-facing features
- Add docstrings with examples
- Update API documentation
- Include mathematical background for new fractals

### Performance

- Profile before optimizing
- Use Numba JIT where appropriate
- Consider memory usage for large images
- Add benchmarks for performance-critical code

## Project Structure

```
fractalsets/
├── fractalsets/
│   ├── core/           # Core computation
│   ├── visualization/  # Plotting and colormaps
│   ├── utils/          # Utilities
│   └── examples/       # Example scripts
├── tests/              # Test suite
├── docs/               # Documentation
└── .github/            # GitHub workflows
```

## Areas Needing Help

Current priorities:

- [ ] Improve test coverage (currently ~60%)
- [ ] Add more colormap options
- [ ] Implement interactive GUI
- [ ] Add Burning Ship fractal
- [ ] Performance benchmarking
- [ ] Documentation improvements
- [ ] More example notebooks

## Questions?

- Open a [Discussion](https://github.com/DiogoRibeiro7/fractalsets/discussions)
- Email: dfr@esmad.ipp.pt

Thank you for contributing! 🌀
