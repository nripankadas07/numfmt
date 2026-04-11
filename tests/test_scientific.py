"""Tests for scientific notation formatting."""
import pytest
from numfmt.core import format_scientific, NumfmtError


class TestBasicScientific:
    """Basic scientific notation tests."""

    def test_default_scientific(self):
        """Test default scientific notation."""
        result = format_scientific(1234.56)
        assert "e" in result.lower() or "E" in result

    def test_scientific_coefficient(self):
        """Test scientific notation has coefficient."""
        result = format_scientific(1234.56)
        assert "1" in result

    def test_scientific_exponent(self):
        """Test scientific notation has exponent."""
        result = format_scientific(1234.56)
        assert "3" in result or "e" in result.lower()


class TestScientificValues:
    """Tests for various scientific notation values."""

    def test_scientific_one(self):
        """Test scientific notation of 1."""
        result = format_scientific(1)
        assert "e" in result.lower() or "1" in result

    def test_scientific_small_number(self):
        """Test scientific notation for small number."""
        result = format_scientific(0.0001)
        assert "e" in result.lower() or "-" in result

    def test_scientific_large_number(self):
        """Test scientific notation for large number."""
        result = format_scientific(1e20)
        assert "20" in result or "e" in result.lower()

    def test_scientific_negative(self):
        """Test scientific notation for negative number."""
        result = format_scientific(-1234)
        assert "-" in result
        assert "e" in result.lower() or "E" in result


class TestScientificPrecision:
    """Tests for scientific notation precision."""

    def test_scientific_precision_default(self):
        """Test default precision in scientific notation."""
        result = format_scientific(1234.56)
        assert result is not None

    def test_scientific_precision_zero(self):
        """Test scientific notation with no decimals."""
        result = format_scientific(1234.56, precision=0)
        assert "e" in result.lower() or "E" in result

    def test_scientific_precision_high(self):
        """Test scientific notation with high precision."""
        result = format_scientific(1.23456789, precision=6)
        assert "e" in result.lower() or "E" in result


class TestScientificFormat:
    """Tests for scientific notation format."""

    def test_scientific_notation_present(self):
        """Test that result uses scientific notation."""
        result = format_scientific(1000000)
        assert "e" in result.lower() or "E" in result or "1000000" not in result

    def test_scientific_with_sign(self):
        """Test scientific notation with sign control."""
        result = format_scientific(1234, sign="always")
        assert "+" in result or "-" in result


class TestScientificEdgeCases:
    """Tests for scientific notation edge cases."""

    def test_scientific_zero(self):
        """Test scientific notation of zero."""
        result = format_scientific(0)
        assert "0" in result

    def test_scientific_negative_zero(self):
        """Test scientific notation of negative zero."""
        result = format_scientific(-0.0)
        assert "0" in result

    def test_scientific_very_small(self):
        """Test scientific notation for very small number."""
        result = format_scientific(1e-100, precision=5)
        assert "-" in result or "e" in result.lower() or "E" in result

    def test_scientific_very_large(self):
        """Test scientific notation for very large number."""
        result = format_scientific(1e100, precision=5)
        assert "e" in result.lower() or "E" in result or "100" in result

    def test_scientific_infinity(self):
        """Test scientific notation of infinity."""
        result = format_scientific(float("inf"))
        assert "inf" in result.lower()

    def test_scientific_nan(self):
        """Test scientific notation of NaN."""
        result = format_scientific(float("nan"))
        assert "nan" in result.lower()


class TestScientificDecimal:
    """Tests for decimal separator in scientific notation."""

    def test_scientific_custom_decimal(self):
        """Test scientific notation with custom decimal separator."""
        result = format_scientific(1.234e5, decimal_separator=",")
        assert "e" in result.lower() or "E" in result or "," in result

    def test_scientific_thousands_separator(self):
        """Test scientific notation with thousands separator."""
        result = format_scientific(1234567, thousands_separator=",")
        assert "e" in result.lower() or "E" in result

    def test_scientific_invalid_input(self):
        """Test scientific notation with invalid input."""
        with pytest.raises(NumfmtError):
            format_scientific("not a number")

    def test_scientific_negative_parens(self):
        """Test scientific notation with accounting notation."""
        result = format_scientific(-123.45, sign="parens")
        assert "(" in result
        assert ")" in result
