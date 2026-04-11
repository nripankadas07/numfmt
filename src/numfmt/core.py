"""Core number formatting module for numfmt."""
import math
from typing import Optional, Union


class NumfmtError(Exception):
    """Exception raised for formatting errors."""

    pass


def _validate_format_args(
    thousands_sep: str, decimal_sep: str, sign: str, precision: Optional[int]
) -> None:
    """Validate format arguments."""
    if thousands_sep == decimal_sep and thousands_sep != "":
        raise NumfmtError(
            "thousands_separator and decimal_separator cannot be the same"
        )
    if sign not in ("auto", "always", "never", "parens"):
        raise NumfmtError(f"Invalid sign: {sign}")
    if precision is not None and precision < 0:
        raise NumfmtError("precision must be non-negative")


def _coerce_to_float(value: Union[int, float]) -> float:
    """Coerce value to float."""
    try:
        return float(value)
    except (TypeError, ValueError) as e:
        raise NumfmtError(f"Invalid numeric value: {value}") from e


def _format_special(value: float, prefix: str, suffix: str) -> str:
    """Format special values (inf, nan)."""
    if math.isnan(value):
        return f"{prefix}nan{suffix}"
    sign_char = "-" if value < 0 else ""
    return f"{prefix}{sign_char}inf{suffix}"


def format_number(
    value: Union[int, float],
    style: str = "decimal",
    precision: Optional[int] = None,
    thousands_separator: str = ",",
    decimal_separator: str = ".",
    sign: str = "auto",
    prefix: str = "",
    suffix: str = "",
) -> str:
    """Format a number with customizable options.

    Args:
        value: Number to format.
        style: Format style ("decimal", "currency", "percent", "scientific").
        precision: Number of decimal places.
        thousands_separator: Character for grouping (default ",").
        decimal_separator: Character for decimal point (default ".").
        sign: Sign display ("auto", "always", "never", "parens").
        prefix: String to prepend to result.
        suffix: String to append to result.

    Returns:
        Formatted string.

    Raises:
        NumfmtError: For invalid arguments.
    """
    _validate_format_args(thousands_separator, decimal_separator, sign, precision)
    value = _coerce_to_float(value)
    if math.isnan(value) or math.isinf(value):
        return _format_special(value, prefix, suffix)
    if precision is None:
        precision = 0 if style == "decimal" else 2
    formatted = _format_abs_number(
        abs(value), precision, thousands_separator, decimal_separator
    )
    formatted = _apply_sign(formatted, value < 0, sign)
    return f"{prefix}{formatted}{suffix}"


def format_currency(
    value: Union[int, float],
    symbol: str = "$",
    symbol_position: str = "before",
    precision: Optional[int] = None,
    thousands_separator: str = ",",
    decimal_separator: str = ".",
    sign: str = "auto",
    prefix: str = "",
    suffix: str = "",
) -> str:
    """Format a number as currency.

    Args:
        value: Amount to format.
        symbol: Currency symbol (default "$").
        symbol_position: Position of symbol ("before" or "after").
        precision: Decimal places (default 2).
        thousands_separator: Grouping character (default ",").
        decimal_separator: Decimal character (default ".").
        sign: Sign display ("auto", "always", "never", "parens").
        prefix: Additional prefix.
        suffix: Additional suffix.

    Returns:
        Formatted currency string.

    Raises:
        NumfmtError: For invalid arguments.
    """
    if symbol_position not in ("before", "after"):
        raise NumfmtError(f"Invalid symbol_position: {symbol_position}")
    if precision is None:
        precision = 2
    formatted = format_number(
        value,
        style="currency",
        precision=precision,
        thousands_separator=thousands_separator,
        decimal_separator=decimal_separator,
        sign=sign,
    )
    result = _position_symbol(formatted, symbol, symbol_position)
    return f"{prefix}{result}{suffix}"


def format_percent(
    value: Union[int, float],
    precision: Optional[int] = None,
    thousands_separator: str = ",",
    decimal_separator: str = ".",
    sign: str = "auto",
    prefix: str = "",
    suffix: str = "",
) -> str:
    """Format a number as a percentage.

    Args:
        value: Decimal value (0.5 = 50%).
        precision: Decimal places (default 2).
        thousands_separator: Grouping character (default ",").
        decimal_separator: Decimal character (default ".").
        sign: Sign display ("auto", "always", "never", "parens").
        prefix: Additional prefix.
        suffix: Additional suffix.

    Returns:
        Formatted percent string.
    """
    if precision is None:
        precision = 2
    formatted = format_number(
        value * 100,
        style="percent",
        precision=precision,
        thousands_separator=thousands_separator,
        decimal_separator=decimal_separator,
        sign=sign,
        suffix="%",
    )
    return f"{prefix}{formatted}{suffix}"


def format_scientific(
    value: Union[int, float],
    precision: Optional[int] = None,
    thousands_separator: str = ",",
    decimal_separator: str = ".",
    sign: str = "auto",
    prefix: str = "",
    suffix: str = "",
) -> str:
    """Format a number in scientific notation.

    Args:
        value: Number to format.
        precision: Significant digits after decimal (default 2).
        thousands_separator: Grouping character (default ",").
        decimal_separator: Decimal character (default ".").
        sign: Sign display ("auto", "always", "never", "parens").
        prefix: Additional prefix.
        suffix: Additional suffix.

    Returns:
        Scientific notation string.
    """
    value = _coerce_to_float(value)
    if math.isnan(value) or math.isinf(value):
        return _format_special(value, prefix, suffix)
    if precision is None:
        precision = 2
    if value == 0:
        return f"{prefix}0{suffix}"
    is_negative = value < 0
    abs_value = abs(value)
    exponent = math.floor(math.log10(abs_value))
    mantissa = abs_value / (10**exponent)
    mantissa_str = f"{mantissa:.{precision}f}".replace(".", decimal_separator)
    formatted = _format_scientific_notation(
        mantissa_str, exponent, is_negative, sign
    )
    return f"{prefix}{formatted}{suffix}"


def _format_abs_number(
    value: float, precision: int, thousands_sep: str, decimal_sep: str
) -> str:
    """Format absolute value of a number."""
    if value == 0:
        return "0"

    rounded = round(value, precision)

    if precision == 0:
        int_part = str(int(rounded))
        return _apply_thousands_separator(int_part, thousands_sep)

    str_value = f"{rounded:.{precision}f}"
    int_part, dec_part = str_value.split(".")

    int_part = _apply_thousands_separator(int_part, thousands_sep)

    if precision == 0:
        return int_part

    return f"{int_part}{decimal_sep}{dec_part}"


def _apply_thousands_separator(int_str: str, sep: str) -> str:
    """Apply thousands separator to integer part."""
    if not sep or len(int_str) <= 3:
        return int_str

    result = []
    for i, char in enumerate(reversed(int_str)):
        if i > 0 and i % 3 == 0:
            result.append(sep)
        result.append(char)

    return "".join(reversed(result))


def _apply_sign(formatted: str, is_negative: bool, sign: str) -> str:
    """Apply sign formatting."""
    if not is_negative:
        return f"+{formatted}" if sign == "always" else formatted
    if sign == "never":
        return formatted
    if sign == "parens":
        return f"({formatted})"
    return f"-{formatted}"


def _position_symbol(formatted: str, symbol: str, position: str) -> str:
    """Position currency symbol before or after number."""
    return f"{symbol}{formatted}" if position == "before" else f"{formatted}{symbol}"


def _format_scientific_notation(
    mantissa_str: str, exponent: int, is_negative: bool, sign: str
) -> str:
    """Format scientific notation with sign."""
    formatted = f"{mantissa_str}e{exponent:+d}"
    if is_negative and sign != "never":
        formatted = f"-{formatted}"
    elif sign == "always" and not is_negative:
        formatted = f"+{formatted}"
    if sign == "parens" and is_negative:
        formatted = f"({formatted.lstrip('-')})"
    return formatted
