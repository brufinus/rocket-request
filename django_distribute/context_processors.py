"""Custom context processors."""

# pylint: disable=unused-argument

from pathlib import Path


def build_date(request):
    """Injects build date into templates."""
    build_date_file = Path(__file__).parent / "BUILD_DATE"
    return {"build_date": build_date_file.read_text()}
