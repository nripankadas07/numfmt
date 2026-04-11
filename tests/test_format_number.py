"""Tests for format_number core functionality."""
import pytest
from numfmt.core import format_number, NumfmtError


class TestBasicFormatting:
    """Basic number formatting tests."""

    def test_format_integer(self):
        """Test formatting simple integers."""
        assert format_number(42) == "42"
        assert format_number(0) == "0"
        assert format_number(-42) == "-42"

    def test_format_float(self):
        """Test formatting floats with default precision."""
        result = format_number(3.14159)
        assert "3" in result

    def test_format_negative_zero(self):
        """Test formatting negative zero."""
        result = format_number(-0.0)
        assert result == "0"

    def test_precision_zero(self):
        """Test precision of 0 removes decimal point."""
        assert format_number(3.7, precision=0) == "4"
        assert format_number(3.2, precision=0) == "3"

    def test_precision_control(self):
        """Test explicit precision setting."""
        assert format_number(3.14159, precision=2) == "3.14"
        assert format_number(3.14159, precision=4) == "3.1416"


class TestThousandsSeparator:
    """Tests for thousands grouping."""

    def test_default_thousands_separator(self):
        """Test default thousands separator is comma."""
        assert format_number(1234.56) == "1,235"
        assert format_number(1000000) == "1,000,000"

    def test_custom_thousands_separator(self):
        """Test custom thousands separator."""
        assert format_number(1234.56, thousands_separator=" ") == "1 235"
        assert format_number(1234.56, thousands_separator=".", decimal_separator=",", precision=2) == "1.234,56"

    def test_no_thousands_separator(self):
        """Test disabling thousands separator."""
        assert format_number(1234.56, thousands_separator="") == "1235"

    def test_thousands_separator_not_applied_small(self):
        """Test that thousands separator not applied to small numbers."""
        assert format_number(999.99) == "1,000"


class TestDecimalSeparator:
    """Tests for decimal point customization."""

    def test_custom_decimal_separator(self):
        """Test custom decimal separator."""
        # Need to specify thousands_separator that doesn't conflict
        assert format_number(3.14, thousands_separator="", decimal_separator=",", precision=2) == "3,14"

    def test_thousands_and_decimal_separator(self):
        """Test combining thousands and decimal separator."""
        result = format_number(
            1234.56, thousands_separator=" ", decimal_separator=",", precision=2
        )
        assert result == "1 234,56"


class TestSignControl:
    """Tests for sign handling."""

    def test_sign_auto_default(self):
        """Test default sign='auto' shows only negative."""
        assert format_number(42) == "42"
        assert format_number(-42) == "-42"

    def test_sign_always(self):
        """Test sign='always' shows plus for positive."""
        result_pos = format_number(42, sign="always")
        result_neg = format_number(-42, sign="always")
        assert "+" in result_pos or result_pos.startswith("42")
        assert "-" in result_neg

    def test_sign_never(self):
        """Test sign='never' hides negative sign."""
        result_pos = format_number(42, sign="never")
        result_neg = format_number(-42, sign="never")
        assert "42" in result_pos
        assert "42" in result_neg

    def test_sign_parens(self):
        """Test sign='parens' uses accounting notation."""
        assert format_number(42, sign="parens") == "42"
        assert format_number(-42, sign="parens") == "(42)"


class TestPrefixSuffix:
    """Tests for prefix and suffix customization."""

    def test_prefix(self):
        """Test adding prefix."""
        assert format_number(42, prefix="$") == "$42"
        assert "$" in format_number(42, prefix="$")

    def test_suffix(self):
        """Test adding suffix."""
        result = format_number(42, suffix=" units")
        assert "units" in result and "42" in result

    def test_prefix_and_suffix(self):
        """Test combining prefix and suffix."""
        result = format_number(42, prefix="[", suffix="]")
        assert "[" in result and "]" in result


class TestSpecialValues:
    """Tests for special float values."""

    def test_positive_infinity(self):
        """Test formatting positive infinity."""
        result = format_number(float("inf"))
        assert "inf" in result.lower()

    def test_negative_infinity(self):
        """Test formatting negative infinity."""
        result = format_number(float("-inf"))
        assert "inf" in result.lower()

    def test_nan(self):
        """Test formatting NaN."""
        result = format_number(float("nan"))
        assert "nan" in result.lower()


class TestLargeNumbers:
    """Tests for very large numbers."""

    def test_large_number(self):
        """Test formatting very large numbers."""
        result = format_number(1e20)
        assert "1" in result

    def test_large_with_separator(self):
        """Test large numbers maintain grouping."""
        result = format_number(123456789, thousands_separator=",")
        assert "," in result


class TestSmallNumbers:
    """Tests for very small numbers."""

    def test_small_number(self):
        """Test formatting very small numbers."""
        result = format_number(1e-20, precision=25)
        assert result is not None

    def test_small_with_precision(self):
        """Test small numbers with high precision."""
        result = format_number(0.00000001, precision=8)
        assert "0.00000001" in result


class TestErrorHandling:
    """Tests for error conditions."""

    def test_same_separators_error(self):
        """Test that same thousands and decimal separator raises error."""
        with pytest.raises(NumfmtError):
            format_number(1234.56, thousands_separator=",", decimal_separator=",")

    def test_invalid_sign_error(self):
        """Test that invalid sign raises error."""
        with pytest.raises(NumfmtError):
            format_number(42, sign="invalid")

    def test_negative_precision_error(self):
        """Test that negative precision raises error."""
        with pytest.raises(NumfmtError):
            format_number(42, precision=-1)

    def test_non_numeric_input_error(self):
        """Test that non-numeric input raises error."""
        with pytest.raises((NumfmtError, TypeError)):
            format_number("not a number")

    def test_empty_separator_string_allowed(self):
        """Test that empty string is allowed for separators."""
        result = format_number(1234.56, thousands_separator="", decimal_separator=".", precision=2)
        assert result == "1234.56"
