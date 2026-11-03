"""Branch coverage tests for laundry_service.py.

Run with:
    python -m coverage erase
    python -m coverage run --branch -m pytest -q BranchCoverageTest_laundry_service.py
    python -m coverage report -m
"""

import pytest

from laundry_service import extra_weight_charge, order_acceptable, dropoff_status


@pytest.mark.parametrize(
    "garment_type,weight,speed,is_member,expected",
    [
        ("regular", 5, "standard", False, 0),       # extra <= 0; non-member
        ("regular", 7, "standard", True, 0),        # member allowance; extra <= 0
        ("regular", 8, "standard", True, 30),       # member allowance; standard rate
        ("bedding", 9, "standard", True, 30),       # member condition true, bedding check false
        ("regular", 7, "express", False, 100),      # non-standard rate; <= 10 extra
        ("regular", 16, "standard", False, 495),    # > 10 extra; standard surcharge
        ("regular", 16, "express", False, 825),     # > 10 extra; express surcharge
    ],
)
def test_extra_weight_charge_branch_combinations(
    garment_type, weight, speed, is_member, expected
):
    assert extra_weight_charge(garment_type, weight, speed, is_member) == expected


def test_extra_weight_charge_invalid_input_branches():
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("unknown", 1, "standard", False)
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -0.1, "standard", False)


@pytest.mark.parametrize(
    "weight,items,is_delicate,expected",
    [
        (10, 5, True, True),    # delicate branch, item limit true
        (10, 6, True, False),   # delicate branch, item limit false
        (26, 10, False, False), # non-delicate; weight limit exceeded
        (25, 40, False, True),  # non-delicate; weight allowed; item limit true
        (25, 41, False, False), # non-delicate; weight allowed; item limit false
    ],
)
def test_order_acceptable_branch_outcomes(weight, items, is_delicate, expected):
    assert order_acceptable(weight, items, is_delicate) is expected


@pytest.mark.parametrize(
    "minutes,has_bedding,is_express,expected",
    [
        (60, False, False, "accepted"),  # no bedding/no express; at cutoff
        (40, False, False, "late"),      # between cutoff-20 and cutoff
        (39, False, False, "rejected"),  # below late window
        (90, True, False, "accepted"),   # bedding raises cutoff to 90
        (120, False, True, "accepted"),  # express raises cutoff by 30
        (100, True, True, "late"),       # bedding + express; within late window
        (69, True, True, "rejected"),    # bedding + express; below late window
    ],
)
def test_dropoff_status_branch_outcomes(minutes, has_bedding, is_express, expected):
    assert dropoff_status(minutes, has_bedding, is_express) == expected
