# 📅 Monthly Maintenance Reminder

Hello! This is your automated monthly reminder to maintain the **FractalSets** package.

## 🎯 Monthly Checklist

### Code Quality
- [ ] Review and merge pending pull requests
- [ ] Close or update stale issues
- [ ] Run full test suite: `pytest tests/ -v`
- [ ] Check code coverage
- [ ] Review and update type hints

### Documentation
- [ ] Update README.md with new features
- [ ] Review and update docstrings
- [ ] Update CHANGELOG.md
- [ ] Check that all examples run correctly
- [ ] Update API documentation if needed

### Package Health
- [ ] Check dependencies for updates
- [ ] Test with latest NumPy, Matplotlib, Numba versions
- [ ] Verify package installs correctly: `pip install -e .`
- [ ] Run setup.py check: `python setup.py check`
- [ ] Check for security vulnerabilities

### FractalSets Specific
- [ ] Test all fractal generators (Mandelbrot, Julia)
- [ ] Verify visualization colormaps work correctly
- [ ] Check performance benchmarks
- [ ] Test gallery examples
- [ ] Verify export functionality
- [ ] Test on multiple Python versions (3.8, 3.9, 3.10, 3.11)

### Community & Growth
- [ ] Respond to community questions/issues
- [ ] Review GitHub Discussions (if enabled)
- [ ] Update project roadmap
- [ ] Consider blog post or tutorial
- [ ] Share updates on social media

### Release Management
- [ ] Review version number
- [ ] Update CHANGELOG.md if releasing
- [ ] Consider creating a new release if significant changes
- [ ] Tag release: `git tag -a vX.Y.Z -m "Release X.Y.Z"`

## 📊 Quick Commands
```bash
# Run tests
pytest tests/ -v --cov=fractalsets

# Check package
python setup.py check

# Build distribution
python setup.py sdist bdist_wheel

# Test installation
pip install -e .

# Run examples
python -m fractalsets.examples.advanced_examples

# Check code style
black fractalsets/
flake8 fractalsets/
```