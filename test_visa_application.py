"""
test_visa_application.py - Full Branch Coverage Test Suite
Achieves 100% Statement and 100% Branch Coverage for visa_application.py.
"""

import pytest
from visa_application import visa_fee, documents_complete, application_status


# =====================================================================
# Tests for visa_fee - Branch & Decision Coverage
# =====================================================================

def test_within_included_entries():
    """Test standard entries within included limit (returns 0)."""
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_visa_fee_unknown_visa_type():
    """Branch: visa_type not in INCLUDED_ENTRIES (True)."""
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("transit", 2, "normal", "B")


def test_visa_fee_negative_entries():
    """Branch: entries < 0 (True)."""
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_visa_fee_extra_strictly_negative():
    """Branch: extra <= 0 (True, boundary: entries < included)."""
    assert visa_fee("tourist", 0, "normal", "B") == 0


def test_visa_fee_nationality_a_non_student():
    """Branch: nationality_group == 'A' and visa_type != 'student' (True and True -> True)."""
    assert visa_fee("tourist", 4, "normal", "A") == 80


def test_visa_fee_nationality_a_student():
    """Branch: nationality_group == 'A' and visa_type != 'student' (True and False -> False)."""
    assert visa_fee("student", 4, "normal", "A") == 80


def test_visa_fee_nationality_other_group():
    """Branch: nationality_group != 'A' (False -> False)."""
    assert visa_fee("business", 5, "normal", "B") == 80


def test_visa_fee_speed_express_extra_le_5():
    """Branch: speed == 'express' (True), extra > 5 (False)."""
    assert visa_fee("tourist", 3, "express", "B") == 200


def test_visa_fee_speed_normal_extra_le_5():
    """Branch: speed != 'express' (False), extra > 5 (False)."""
    assert visa_fee("tourist", 3, "normal", "B") == 80


def test_visa_fee_extra_gt_5_speed_express():
    """Branch: extra > 5 (True), speed == 'express' (True)."""
    assert visa_fee("tourist", 7, "express", "B") == 780


def test_visa_fee_extra_gt_5_speed_normal():
    """Branch: extra > 5 (True), speed != 'express' (False) -> covers branch 21->23."""
    assert visa_fee("tourist", 7, "normal", "B") == 360


# =====================================================================
# Tests for documents_complete - Branch & Decision Coverage
# =====================================================================

def test_documents_complete():
    """Branch: is_renewal (False), photos >= 2, forms_filed >= 3 (True)."""
    assert documents_complete(3, 2, False) is True


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


def test_documents_complete_non_renewal_forms_insufficient():
    """Branch: is_renewal (False), photos < 2 (False), forms_filed >= 3 (False)."""
    assert documents_complete(2, 2, is_renewal=False) is False


# =====================================================================
# Tests for application_status - Branch & Decision Coverage
# =====================================================================

def test_application_status_express_peak_open():
    """Branch: is_express (True), is_peak (True), days >= cutoff (True)."""
    assert application_status(25, is_express=True, is_peak_season=True) == "open"
    assert application_status(30, is_express=True, is_peak_season=True) == "open"


def test_application_status_express_peak_closing():
    """Branch: is_express (True), is_peak (True), days >= cutoff-15 (True)."""
    assert application_status(24, is_express=True, is_peak_season=True) == "closing"
    assert application_status(10, is_express=True, is_peak_season=True) == "closing"


def test_application_status_express_peak_closed():
    """Branch: is_express (True), is_peak (True), days < cutoff-15 (False)."""
    assert application_status(9, is_express=True, is_peak_season=True) == "closed"


def test_application_status_express_non_peak_open():
    """Branch: is_express (True), is_peak (False), days >= cutoff (True)."""
    assert application_status(10, is_express=True, is_peak_season=False) == "open"


def test_application_status_express_non_peak_closing():
    """Branch: is_express (True), is_peak (False), days >= cutoff-15 (True)."""
    assert application_status(0, is_express=True, is_peak_season=False) == "closing"
    assert application_status(-5, is_express=True, is_peak_season=False) == "closing"


def test_application_status_express_non_peak_closed():
    """Branch: is_express (True), is_peak (False), days < cutoff-15 (False)."""
    assert application_status(-6, is_express=True, is_peak_season=False) == "closed"


def test_application_status_standard_peak_open():
    """Branch: is_express (False), is_peak (True), days >= cutoff (True)."""
    assert application_status(45, is_express=False, is_peak_season=True) == "open"


def test_application_status_standard_peak_closing():
    """Branch: is_express (False), is_peak (True), days >= cutoff-15 (True)."""
    assert application_status(35, is_express=False, is_peak_season=True) == "closing"
    assert application_status(30, is_express=False, is_peak_season=True) == "closing"


def test_application_status_standard_peak_closed():
    """Branch: is_express (False), is_peak (True), days < cutoff-15 (False)."""
    assert application_status(29, is_express=False, is_peak_season=True) == "closed"


def test_application_status_standard_non_peak_open():
    """Branch: is_express (False), is_peak (False), days >= cutoff (True)."""
    assert application_status(30, is_express=False, is_peak_season=False) == "open"


def test_application_status_standard_non_peak_closing():
    """Branch: is_express (False), is_peak (False), days >= cutoff-15 (True)."""
    assert application_status(20, is_express=False, is_peak_season=False) == "closing"
    assert application_status(15, is_express=False, is_peak_season=False) == "closing"


def test_application_status_standard_non_peak_closed():
    """Branch: is_express (False), is_peak (False), days < cutoff-15 (False)."""
    assert application_status(14, is_express=False, is_peak_season=False) == "closed"
