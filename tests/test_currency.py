"""Tests for currency formatting."""
import pytest
from numfmt.core import format_currency, NumfmtError


class TestBasicCurrency:
    """Basic currency formatting tests."""

    def test_default_currency(self):
        """Test default currency symbol."""
        assert "$" in format_currency(42)
        assert "42" in format_currency(42)

    def test_custom_currency_symbol(self):
        """Test custom currency symbol."""
        assert "â¬" in format_currency(42, symbol="â¬")
        assert "Â£" in format_currency(42, symbol="Â£")

    def test_currency_precision_default(self):
        """Test default precision for currency (2 decimals)."""
        result = format_currency(3.1)
        assert "3.10" in result or "3,10" in result


class TestCurrencyPositioning:
    """Tests for currency symbol positioning."""

    def test_symbol_before_default(self):
        """Test symbol positioned before by default."""
        result = format_currency(42)
        assert result.startswith("$") or result.startswith(" $")

    def test_symbol_before_explicit(self):
        """Test symbol positioned before explicitly."""
        result = format_currency(42, symbol_position="before")
        idx_symbol = result.index("$")
        idx_number = result.index("42")
        assert idx_symbol < idx_number

    def test_symbol_after(self):
        """Test symbol positioned after."""
        result = format_currency(42, symbol_position="after")
        idx_symbol = result.index("$")
        idx_number = result.index("42")
        assert idx_number < idx_symbol

    def test_symbol_position_invalid_error(self):
        """Test invalid symbol position raises error."""
        with pytest.raises(NumfmtError):
            format_currency(42, symbol_position="invalid")


class TestCurrencyNegative:
    """Tests for negative currency values."""

    def test_negative_with_minus(self):
        """Test negative currency with minus sign."""
        result = format_currency(-42)
        assert "-" in result or "(" in result

    def test_negative_with_parens(self):
        """Test negative currency with accounting notation."""
        result = format_currency(-42, sign="parens")
        assert "(" in result
        assert ")" in result

    def test_negative_never_sign(self):
        """Test negative currency without sign."""
        result = format_currency(-42, sign="never")
        assert result.count("-") == 0
        assert "42" in result


class TestCurrencyThousands:
    """Tests for currency with thousands separator."""

    def test_large_currency_with_separator(self):
        """Test large currency amounts have thousands separator."""
        result = format_currency(1234567.89)
        assert "," in result or " " in result

    def test_custom_thousands_in_currency(self):
        """Test custom thousands separator in currency."""
        result = format_currency(1234.56, thousands_separator=" ")
        assert "1 234" in result


class TestCurrencyInternational:
    """Tests for international currency symbols."""

    def test_euro_currency(self):
        """Test Euro currency formatting."""
        result = format_currency(100, symbol="â¬")
        assert "â¬" in result
        assert "100" in result

    def test_yen_currency(self):
        """Test Japanese Yen formatting."""
        result = format_currency(1000, symbol="Â¥", precision=0)
        assert "Â¥" in result
        assert "1,000" in result

    def test_pound_currency(self):
        """Test British Pound formatting."""
        result = format_currency(42.50, symbol="Â£")
        assert "Â£" in result
        assert "42.50" in result


class TestCurrencyEdgeCases:
    """Tests for currency edge cases."""

    def test_zero_currency(self):
        """Test zero currency value."""
        result = format_currency(0)
        assert "$" in result
        assert "0" in result

    def test_currency_with_prefix_suffix(self):
        """Test currency with additional prefix/suffix."""
        result = format_currency(42, prefix="[", suffix="]")
        assert "[" in result
        assert "]" in result

    def test_currency_no_symbol(self):
        """Test currency with empty symbol."""
        result = format_currency(42, symbol="")
        assert "42" in result
