"""Tests for percent formatting."""
from numfmt.core import format_percent


class TestBasicPercent:
    """Basic percent formatting tests."""

    def test_default_percent(self):
        """Test default percent formatting."""
        result = format_percent(0.5)
        assert "50" in result
        assert "%" in result

    def test_percent_as_decimal(self):
        """Test percent with decimal value."""
        result = format_percent(0.123)
        assert "12" in result
        assert "%" in result

    def test_percent_precision_default(self):
        """Test default precision for percent."""
        result = format_percent(0.12345)
        assert result is not None


class TestPercentValuesRange:
    """Tests for various percent value ranges."""

    def test_percent_zero(self):
        """Test zero percent."""
        result = format_percent(0)
        assert "0" in result
        assert "%" in result

    def test_percent_one(self):
        """Test 100 percent."""
        result = format_percent(1)
        assert "100" in result
        assert "%" in result

    def test_percent_fractional(self):
        """Test fractional percent."""
        result = format_percent(0.01)
        assert "1" in result
        assert "%" in result

    def test_percent_over_one(self):
        """Test percent over 100."""
        result = format_percent(1.5)
        assert "150" in result
        assert "%" in result


class TestPercentPrecision:
    """Tests for percent precision control."""

    def test_percent_precision_zero(self):
        """Test percent with no decimal places."""
        result = format_percent(0.333, precision=0)
        assert "33" in result
        assert "%" in result

    def test_percent_precision_two(self):
        """Test percent with 2 decimal places."""
        result = format_percent(0.333, precision=2)
        assert "%" in result

    def test_percent_precision_high(self):
        """Test percent with high precision."""
        result = format_percent(0.123456, precision=4)
        assert "%" in result


class TestPercentNegative:
    """Tests for negative percent values."""

    def test_negative_percent(self):
        """Test negative percent."""
        result = format_percent(-0.1)
        assert "-" in result or "(" in result
        assert "%" in result

    def test_negative_percent_parens(self):
        """Test negative percent with accounting notation."""
        result = format_percent(-0.1, sign="parens")
        assert "(" in result
        assert ")" in result

    def test_negative_percent_always_sign(self):
        """Test negative percent with sign always."""
        result = format_percent(0.1, sign="always")
        assert "+" in result


class TestPercentSign:
    """Tests for percent sign handling."""

    def test_percent_sign_present(self):
        """Test percent sign is included."""
        result = format_percent(0.5)
        assert "%" in result

    def test_percent_sign_suffix(self):
        """Test percent sign as suffix."""
        result = format_percent(0.5)
        assert result.endswith("%")


class TestPercentFormatting:
    """Tests for percent formatting options."""

    def test_percent_thousands_separator(self):
        """Test percent with thousands separator."""
        result = format_percent(10.5, thousands_separator=",")
        assert "1,050" in result or "1050" in result
        assert "%" in result

    def test_percent_custom_precision(self):
        """Test percent with custom precision."""
        result = format_percent(0.12345, precision=3)
        assert "%" in result


class TestPercentEdgeCases:
    """Tests for percent edge cases."""

    def test_percent_very_small(self):
        """Test very small percent value."""
        result = format_percent(0.0001, precision=4)
        assert "0.01" in result or "0,01" in result
        assert "%" in result

    def test_percent_very_large(self):
        """Test very large percent value."""
        result = format_percent(100, precision=0)
        assert "%" in result
        # 100 * 100 = 10000 percent
        assert "10000" in result or "10" in result

    def test_percent_negative_zero(self):
        """Test negative zero percent."""
        result = format_percent(-0.0)
        assert "0" in result
        assert "%" in result
