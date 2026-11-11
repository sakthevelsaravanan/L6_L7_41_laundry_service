
from hypothesis import given, strategies as st
from laundry_service import parse_order, weight_average, payable_charge


# Test 1: parse_order
@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    try:
        parse_order(s)
    except (ValueError, TypeError):
        pass


# Test 2: weight_average
@given(st.text() | st.none())
def test_weight_average_no_crash(s):
    try:
        weight_average(s)
    except (ValueError, TypeError):
        pass


# Test 3: payable_charge
@given(st.text() | st.none())
def test_payable_charge_no_crash(s):
    try:
        payable_charge(s)
    except (ValueError, TypeError):
        pass
