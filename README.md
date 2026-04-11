# numfmt

Locale-free number formatter supporting currency, percent, and scientific notation. Zero dependencies.

## Features

- Format numbers as decimal, currency, percent, or scientific notation
- Customizable thousands and decimal separators
- Support for accounting notation (negative values in parentheses)
- No locale dependencies or system calls
- Comprehensive error handling
- Type-safe with full type hints
- Production-ready with >80% test coverage

## Installation

```bash
pip install numfmt
```

## Quick Start

```python
from numfmt import format_number, format_currency, format_percent, format_scientific

# Basic decimal formatting
format_number(1234.56)  # "1,234.56"

# Currency formatting
format_currency(1234.56)  # "$1,234.56"
format_currency(1234.56, symbol="€")  # "€1,234.56"

# Percentage formatting
format_percent(0.123)  # "12.30%"
format_percent(0.123, precision=1)  # "12.3%"

# Scientific notation
format_scientific(1234.56)  # "1.23e+03"
```

## Usage Examples

### Basic Number Formatting

```python
from numfmt import format_number

# Default formatting
format_number(42)  # "42"
format_number(3.14159, precision=2)  # "3.14"

# Custom separators
format_number(1234.56, thousands_separator=" ", decimal_separator=",")
# "1 234,56"

# No thousands separator
format_number(1234.56, thousands_separator="")  # "1234.56"
```

### Sign Control

```python
# Auto (default) - only show negative sign
format_number(-42)  # "-42"
format_number(42)  # "42"

# Always show sign
format_number(42, sign="always")  # "+42"

# Never show sign
format_number(-42, sign="never")  # "42"

# Accounting notation (parentheses for negative)
format_number(-42, sign="parens")  # "(42)"
```

### Prefix and Suffix

```python
format_number(100, prefix="$", suffix=" units")  # "$100 units"
format_number(0.5, prefix="[", suffix="]")  # "[0.50]"
```

### Currency Formatting

```python
from numfmt import format_currency

# Default (USD)
format_currency(1234.56)  # "$1,234.56"

# Euro with custom thousands separator
format_currency(1234.56, symbol="€", thousands_separator=" ")
# "€1 234.56"

# Symbol after the amount
format_currency(1234.56, symbol="CHF", symbol_position="after")
# "1,234.56CHF"

# Accounting notation for negative values
format_currency(-1234.56, sign="parens")  # "($1,234.56)"
```

### Percentage Formatting

```python
from numfmt import format_percent

# Decimal to percent (0.5 = 50%)
format_percent(0.5)  # "50.00%"
format_percent(0.123)  # "12.30%"

# Custom precision
format_percent(0.123, precision=1)  # "12.3%"
format_percent(0.333, precision=0)  # "33%"

# Large percentages
format_percent(1.5)  # "150.00%"
format_percent(0.001, precision=3)  # "0.100%"
```

### Scientific Notation

```python
from numfmt import format_scientific

# Basic scientific notation
format_scientific(1234.56)  # "1.23e+03"
format_scientific(0.0001)  # "1.00e-04"

# Custom precision
format_scientific(1.23456, precision=3)  # "1.235e+00"

# Negative numbers
format_scientific(-1234.56)  # "-1.23e+03"
```

## API Reference

### `format_number(value, style="decimal", **options) -> str`

Format a number with customizable options.

**Parameters:**
- `value` (int|float): Number to format
- `style` (str): Format style - "decimal", "currency", "percent", "scientific" (default: "decimal")
- `precision` (int): Number of decimal places (default: 2)
- `thousands_separator` (str): Character for grouping thousands (default: ",")
- `decimal_separator` (str): Character for decimal point (default: ".")
- `sign` (str): Sign display mode:
  - "auto": Show sign only for negative values (default)
  - "always": Always show sign (+/-)
  - "never": Never show sign
  - "parens": Use parentheses for negative values (accounting)
- `prefix` (str): String to prepend to result (default: "")
- `suffix` (str): String to append to result (default: "")

**Returns:** Formatted number as string

**Raises:** `NumfmtError` for invalid arguments

### `format_currency(value, symbol="$", symbol_position="before", **options) -> str`

Format a number as currency.

**Parameters:**
- `value` (int|float): Amount to format
- `symbol` (str): Currency symbol (default: "$")
- `symbol_position` (str): Position of symbol - "before" or "after" (default: "before")
- `precision` (int): Decimal places (default: 2)
- `thousands_separator` (str): Character for grouping (default: ",")
- `decimal_separator` (str): Decimal character (default: ".")
- `sign` (str): Sign display mode (see `format_number`)
- `prefix` (str): Additional prefix (default: "")
- `suffix` (str): Additional suffix (default: "")

**Returns:** Formatted currency string

**Raises:** `NumfmtError` for invalid arguments

### `format_percent(value, **options) -> str`

Format a number as a percentage.

**Parameters:**
- `value` (int|float): Decimal value (0.5 = 50%)
- `precision` (int): Decimal places (default: 2)
- `thousands_separator` (str): Character for grouping (default: ",")
- `decimal_separator` (str): Decimal character (default: ".")
- `sign` (str): Sign display mode (see `format_number`)
- `prefix` (str): Additional prefix (default: "")
- `suffix` (str): Additional suffix (default: "")

**Returns:** Formatted percent string

**Raises:** `NumfmtError` for invalid arguments

### `format_scientific(value, **options) -> str`

Format a number in scientific notation.

**Parameters:**
- `value` (int|float): Number to format
- `precision` (int): Significant digits after decimal (default: 2)
- `thousands_separator` (str): Character for grouping (default: ",")
- `decimal_separator` (str): Decimal character (default: ".")
- `sign` (str): Sign display mode (see `format_number`)
- `prefix` (str): Additional prefix (default: "")
- `suffix` (str): Additional suffix (default: "")

**Returns:** Scientific notation string

**Raises:** `NumfmtError` for invalid arguments

### `NumfmtError`

Exception raised for formatting errors (invalid arguments, type errors, etc.)

## Error Handling

```python
from numfmt import format_number, NumfmtError

try:
    format_number(1234, thousands_separator=",", decimal_separator=",")
except NumfmtError as e:
    print(f"Formatting error: {e}")
    # Output: Formatting error: thousands_separator and decimal_separator cannot be the same
```

## Running Tests

Install development dependencies:

```bash
pip install numfmt[dev]
```

Run tests with coverage:

```bash
pytest
```

For detailed coverage report:

```bash
pytest --cov=numfmt --cov-report=html
```

View the HTML coverage report:

```bash
open htmlcov/index.html
```

## Design Principles

- **Locale-free**: No system locale detection or dependencies
- **Type-safe**: Full type hints for all public APIs
- **Zero dependencies**: Pure Python standard library only
- **Simple API**: Intuitive function names and parameters
- **Comprehensive**: Supports common formatting styles (decimal, currency, percent, scientific)
- **Robust**: Handles edge cases (infinity, NaN, very large/small numbers)

## License

MIT License - see LICENSE file for details

## Author

Nripanka Das
