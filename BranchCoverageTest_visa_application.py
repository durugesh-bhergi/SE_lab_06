"""
BranchCoverageTest_visa_application.py
Comprehensive test suite designed for Branch Coverage Analysis of visa_application.py
Exercises all decision branches, edge cases, and boundary conditions to achieve 100% Branch Coverage.
"""

import pytest
from visa_application import visa_fee, documents_complete, application_status


# =====================================================================
# Tests for visa_fee - Branch & Decision Coverage
# =====================================================================

def test_visa_fee_unknown_visa_type():
    """Branch: visa_type not in INCLUDED_ENTRIES (True)."""
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("transit", 2, "normal", "B")


def test_visa_fee_negative_entries():
    """Branch: entries < 0 (True)."""
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_visa_fee_extra_exact_zero():
    """Branch: extra <= 0 (True, boundary: entries == included)."""
    # Tourist included = 1, entries = 1 -> extra = 0 -> returns 0
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_visa_fee_extra_strictly_negative():
    """Branch: extra <= 0 (True, boundary: entries < included)."""
    # Tourist included = 1, entries = 0 -> extra = -1 -> returns 0
    assert visa_fee("tourist", 0, "normal", "B") == 0


def test_visa_fee_nationality_a_non_student():
    """Branch: nationality_group == 'A' and visa_type != 'student' (True and True -> True)."""
    # Tourist included = 1 + 1 = 2. entries = 4 -> extra = 2. rate = 40. fee = 80
    assert visa_fee("tourist", 4, "normal", "A") == 80


def test_visa_fee_nationality_a_student():
    """Branch: nationality_group == 'A' and visa_type != 'student' (True and False -> False)."""
    # Student included = 2 (not incremented). entries = 4 -> extra = 2. rate = 40. fee = 80
    assert visa_fee("student", 4, "normal", "A") == 80


def test_visa_fee_nationality_other_group():
    """Branch: nationality_group != 'A' (False -> False)."""
    # Business included = 3. entries = 5 -> extra = 2. rate = 40. fee = 80
    assert visa_fee("business", 5, "normal", "B") == 80


def test_visa_fee_speed_express_extra_le_5():
    """Branch: speed == 'express' (True), extra > 5 (False)."""
    # Tourist included = 1. entries = 3 -> extra = 2 (<= 5). rate = 100. fee = 200
    assert visa_fee("tourist", 3, "express", "B") == 200


def test_visa_fee_speed_normal_extra_le_5():
    """Branch: speed != 'express' (False), extra > 5 (False)."""
    # Tourist included = 1. entries = 3 -> extra = 2 (<= 5). rate = 40. fee = 80
    assert visa_fee("tourist", 3, "normal", "B") == 80


def test_visa_fee_extra_gt_5_speed_express():
    """Branch: extra > 5 (True), speed == 'express' (True)."""
    # Tourist included = 1. entries = 7 -> extra = 6 (> 5). rate = 100 + 20 + 10 = 130. fee = 6 * 130 = 780
    assert visa_fee("tourist", 7, "express", "B") == 780


def test_visa_fee_extra_gt_5_speed_normal():
    """Branch: extra > 5 (True), speed != 'express' (False) -> covers branch 21->23."""
    # Tourist included = 1. entries = 7 -> extra = 6 (> 5). rate = 40 + 20 = 60. fee = 6 * 60 = 360
    assert visa_fee("tourist", 7, "normal", "B") == 360


# =====================================================================
# Tests for documents_complete - Branch & Decision Coverage
# =====================================================================

def test_documents_complete_renewal_sufficient():
    """Branch: is_renewal (True), forms_filed >= 1 (True)."""
    assert documents_complete(1, 0, is_renewal=True) is True
    assert documents_complete(2, 0, is_renewal=True) is True


def test_documents_complete_renewal_insufficient():
    """Branch: is_renewal (True), forms_filed >= 1 (False)."""
    assert documents_complete(0, 5, is_renewal=True) is False


def test_documents_complete_non_renewal_photos_insufficient():
    """Branch: is_renewal (False), photos < 2 (True)."""
    assert documents_complete(5, 1, is_renewal=False) is False
    assert documents_complete(5, 0, is_renewal=False) is False


def test_documents_complete_non_renewal_forms_sufficient():
    """Branch: is_renewal (False), photos < 2 (False), forms_filed >= 3 (True)."""
    assert documents_complete(3, 2, is_renewal=False) is True
    assert documents_complete(4, 3, is_renewal=False) is True


def test_documents_complete_non_renewal_forms_insufficient():
    """Branch: is_renewal (False), photos < 2 (False), forms_filed >= 3 (False)."""
    assert documents_complete(2, 2, is_renewal=False) is False


# =====================================================================
# Tests for application_status - Branch & Decision Coverage
# =====================================================================

def test_application_status_express_peak_open():
    """Branch: is_express (True), is_peak (True) [cutoff=25], days >= cutoff (True)."""
    assert application_status(25, is_express=True, is_peak_season=True) == "open"
    assert application_status(30, is_express=True, is_peak_season=True) == "open"


def test_application_status_express_peak_closing():
    """Branch: is_express (True), is_peak (True) [cutoff=25], days < cutoff, days >= cutoff-15 (True)."""
    assert application_status(24, is_express=True, is_peak_season=True) == "closing"
    assert application_status(10, is_express=True, is_peak_season=True) == "closing"


def test_application_status_express_peak_closed():
    """Branch: is_express (True), is_peak (True) [cutoff=25], days < cutoff-15 (False)."""
    assert application_status(9, is_express=True, is_peak_season=True) == "closed"


def test_application_status_express_non_peak_open():
    """Branch: is_express (True), is_peak (False) [cutoff=10], days >= cutoff (True)."""
    assert application_status(10, is_express=True, is_peak_season=False) == "open"


def test_application_status_express_non_peak_closing():
    """Branch: is_express (True), is_peak (False) [cutoff=10], days < cutoff, days >= cutoff-15 (True)."""
    assert application_status(0, is_express=True, is_peak_season=False) == "closing"
    assert application_status(-5, is_express=True, is_peak_season=False) == "closing"


def test_application_status_express_non_peak_closed():
    """Branch: is_express (True), is_peak (False) [cutoff=10], days < cutoff-15 (False)."""
    assert application_status(-6, is_express=True, is_peak_season=False) == "closed"


def test_application_status_standard_peak_open():
    """Branch: is_express (False), is_peak (True) [cutoff=45], days >= cutoff (True)."""
    assert application_status(45, is_express=False, is_peak_season=True) == "open"


def test_application_status_standard_peak_closing():
    """Branch: is_express (False), is_peak (True) [cutoff=45], days < cutoff, days >= cutoff-15 (True)."""
    assert application_status(35, is_express=False, is_peak_season=True) == "closing"
    assert application_status(30, is_express=False, is_peak_season=True) == "closing"


def test_application_status_standard_peak_closed():
    """Branch: is_express (False), is_peak (True) [cutoff=45], days < cutoff-15 (False)."""
    assert application_status(29, is_express=False, is_peak_season=True) == "closed"


def test_application_status_standard_non_peak_open():
    """Branch: is_express (False), is_peak (False) [cutoff=30], days >= cutoff (True)."""
    assert application_status(30, is_express=False, is_peak_season=False) == "open"


def test_application_status_standard_non_peak_closing():
    """Branch: is_express (False), is_peak (False) [cutoff=30], days < cutoff, days >= cutoff-15 (True)."""
    assert application_status(20, is_express=False, is_peak_season=False) == "closing"
    assert application_status(15, is_express=False, is_peak_season=False) == "closing"


def test_application_status_standard_non_peak_closed():
    """Branch: is_express (False), is_peak (False) [cutoff=30], days < cutoff-15 (False)."""
    assert application_status(14, is_express=False, is_peak_season=False) == "closed"
