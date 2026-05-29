"""Custom context processors."""

# pylint: disable=unused-argument

from pathlib import Path
import tomllib


def build_date(request):
    """Injects build date into templates."""
    build_date_file = Path(__file__).parent / "BUILD_DATE"
    return {"build_date": build_date_file.read_text()}


def build_version(request):
    """Injects build version into templates."""
    version = ""
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject, "rb") as f:
        version = f"v{tomllib.load(f)["project"]["version"]}"
    return {"version": version}
