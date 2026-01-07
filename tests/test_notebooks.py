"""
Pytest tests for executing Jupyter notebooks.

These tests execute each notebook using nbclient and verify it runs without errors.
Run with: pytest tests/test_notebooks.py -v
"""
import os
import pytest
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

# Get the repository root directory
REPO_ROOT = Path(__file__).parent.parent

# Directories to ignore when searching for notebooks
IGNORE_DIRS = {
    ".ipynb_checkpoints",
    ".venv",
    "venv",
    ".git",
    ".github",
    "__pycache__",
    ".idea",
    ".vscode",
}

# Discover all notebooks in the repository
NOTEBOOKS = [
    nb for nb in REPO_ROOT.glob("**/*_disra.ipynb")
    if not any(ignored in nb.parts for ignored in IGNORE_DIRS)
]


def get_notebook_id(notebook_path: Path) -> str:
    """Generate a readable test ID from the notebook path."""
    return str(notebook_path.relative_to(REPO_ROOT))


@pytest.mark.parametrize("notebook", NOTEBOOKS, ids=get_notebook_id)
def test_notebook_execution(notebook):
    """
    Test that a notebook executes without errors.

    This test reads the notebook, executes all cells, and fails if any cell
    raises an exception.
    """
    assert notebook.exists(), f"Notebook {notebook} does not exist"

    # Read the notebook
    with open(notebook, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # Change to the notebook's directory so relative paths work
    original_dir = os.getcwd()
    notebook_dir = notebook.parent
    os.chdir(notebook_dir)

    try:
        # Create a client to execute the notebook
        client = NotebookClient(
            nb,
            timeout=600,  # 10 minute timeout per cell
            kernel_name="python3",
            resources={"metadata": {"path": str(notebook_dir)}},
        )

        # Execute the notebook
        client.execute()

    except CellExecutionError as e:
        pytest.fail(f"Notebook {notebook.name} failed during execution:\n{e}")
    finally:
        os.chdir(original_dir)
