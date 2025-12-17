"""
Pytest configuration for notebook tests.
"""
import os
import pytest


def pytest_configure(config):
    """Configure pytest for notebook testing."""
    # Add custom markers
    config.addinivalue_line(
        "markers", "notebook: mark test as a notebook execution test"
    )


@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    """
    Change to the notebook's directory before running it.

    This ensures that relative paths in notebooks (like data files)
    are resolved correctly.
    """
    # Only apply to notebook tests (when using --nbmake)
    if hasattr(request, 'fspath') and request.fspath:
        notebook_dir = os.path.dirname(request.fspath)
        if notebook_dir:
            monkeypatch.chdir(notebook_dir)
