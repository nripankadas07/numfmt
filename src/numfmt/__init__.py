"""numfmt: Locale-free number formatter."""
from .core import (
    NumfmtError,
    format_currency,
    format_number,
    format_percent,
    format_scientific,
)

__version__ = "1.0.0"
__author__ = "Nripanka Das"
__all__ = [
    "format_number",
    "format_currency",
    "format_percent",
    "format_scientific",
    "NumfmtError",
]
