"""
CodeCoverageTest_visa_application.py
Test suite designed for Line Coverage Analysis of visa_application.py
Achieves 100% line coverage (statements executed), meeting the >=90% requirement.
"""

import pytest
from visa_application import visa_fee, documents_complete, application_status


# --- Tests for visa_fee ---

def test_visa_fee_unknown_visa_type():
    """Test unknown visa type raises ValueError (covers lines 5-6)."""
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("work", 1, "standard", "B")


def test_visa_fee_invalid_entries():
    """Test negative entries raises ValueError (covers lines 7-8)."""
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "standard", "B")


def test_visa_fee_no_extra_entries():
    """Test entries within included count returns 0 (covers lines 13-14)."""
    assert visa_fee("tourist", 1, "standard", "B") == 0


def test_visa_fee_standard_extra_entries():
    """Test standard speed rate calculation when extra <= 5 (covers lines 17-18, 23)."""
    # Business included = 3, entries = 4 -> extra = 1, rate = 40 -> fee = 40
    assert visa_fee("business", 4, "standard", "B") == 40


def test_visa_fee_express_high_extra_entries_nationality_a():
    """Test express speed with extra > 5 and nationality A (covers lines 10-11, 15-16, 19-22, 23)."""
    # Tourist included = 1 + 1 (nationality A) = 2, entries = 8 -> extra = 6 (> 5)
    # Express rate = 100 + 20 + 10 = 130 -> fee = 6 * 130 = 780
    assert visa_fee("tourist", 8, "express", "A") == 780


# --- Tests for documents_complete ---

def test_documents_complete_renewal():
    """Test renewal with forms filed >= 1 returns True (covers lines 27-28)."""
    assert documents_complete(1, 0, is_renewal=True) is True


def test_documents_complete_insufficient_photos():
    """Test non-renewal with photos < 2 returns False (covers lines 29-30)."""
    assert documents_complete(3, 1, is_renewal=False) is False


def test_documents_complete_standard_valid():
    """Test non-renewal with valid forms and photos returns True (covers line 31)."""
    assert documents_complete(3, 2, is_renewal=False) is True


# --- Tests for application_status ---

def test_application_status_open_express():
    """Test express open status (covers lines 35-36, 41-42)."""
    # Express cutoff = 10, days_left = 10 >= 10 -> "open"
    assert application_status(10, is_express=True, is_peak_season=False) == "open"


def test_application_status_closing_standard_peak():
    """Test standard speed closing during peak season (covers lines 37-38, 39-40, 43-44)."""
    # Standard cutoff = 30 + 15 = 45. days_left = 35 >= (45 - 15) -> "closing"
    assert application_status(35, is_express=False, is_peak_season=True) == "closing"


def test_application_status_closed_standard():
    """Test standard speed closed status (covers line 45)."""
    # Standard cutoff = 30. days_left = 5 < 15 -> "closed"
    assert application_status(5, is_express=False, is_peak_season=False) == "closed"
