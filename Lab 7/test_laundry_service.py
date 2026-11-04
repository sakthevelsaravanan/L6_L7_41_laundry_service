from hypothesis import given, strategies as st
from laundry_service import parse_order, weight_average, payable_charge

@given(st.text() | st.none())
def test_parse_order_no_crash(s):

@given(st.text() | st.none())
def test_weight_average_no_crash(s):

@given(st.text() | st.none())
def test_payable_charge_no_crash(s):
