"""Statement/code coverage tests for laundry_service.py.

Run with:
    python -m coverage erase
    python -m coverage run -m pytest -q CodeCoverageTest_laundry_service.py
    python -m coverage report -m
"""

import pytest

from laundry_service import extra_weight_charge, order_acceptable, dropoff_status


def test_unknown_garment_type_raises_value_error():
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("shoes", 4, "standard", False)


def test_negative_weight_raises_value_error():
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -1, "standard", False)


def test_regular_standard_extra_weight_charge():
    # Regular includes 5 kg; 7 kg means 2 extra kg at 30 per kg.
    assert extra_weight_charge("regular", 7, "standard", False) == 60


def test_member_allowance_and_express_rate():
    # A regular member gets 2 extra included kg (7 kg total); 9 kg leaves 2 extra.
    assert extra_weight_charge("regular", 9, "express", True) == 100
    # Also exercise the member allowance when no extra charge is due.
    assert extra_weight_charge("regular", 7, "standard", True) == 0


def test_bedding_member_does_not_get_extra_allowance_and_high_express_rate():
    # Bedding remains at 8 kg included. 19 kg leaves 11 extra kg.
    # Express high-overage rate: 50 + 15 + 10 = 75 per kg.
    assert extra_weight_charge("bedding", 19, "express", True) == 825


def test_order_acceptable_paths():
    assert order_acceptable(10, 20, False) is True
    assert order_acceptable(10, 5, True) is True
    assert order_acceptable(30, 20, False) is False


def test_dropoff_status_paths():
    assert dropoff_status(100, False, False) == "accepted"
    assert dropoff_status(50, False, False) == "late"
    assert dropoff_status(30, False, False) == "rejected"
    # Exercise the bedding cutoff and additional express cutoff adjustment.
    assert dropoff_status(120, True, True) == "accepted"
