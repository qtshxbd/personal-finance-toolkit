import pytest

from finance_toolkit import (
    amortization_schedule,
    compare_extra_payment,
    payment_amount,
    total_interest,
)


def test_thirty_year_mortgage_payment():
    assert payment_amount(200_000, 0.06, 30) == pytest.approx(1199.10, abs=0.01)


def test_zero_interest_loan_splits_evenly():
    assert payment_amount(12_000, 0.0, 1) == pytest.approx(1000)


def test_schedule_has_one_row_per_payment():
    schedule = amortization_schedule(10_000, 0.05, 3)
    assert len(schedule) == 36
    assert [p.number for p in schedule] == list(range(1, 37))


def test_schedule_ends_at_zero_and_repays_principal():
    schedule = amortization_schedule(25_000, 0.07, 5)
    assert schedule[-1].balance == 0
    assert sum(p.principal for p in schedule) == pytest.approx(25_000)


def test_first_payment_interest_is_one_period_of_rate():
    schedule = amortization_schedule(200_000, 0.06, 30)
    assert schedule[0].interest == pytest.approx(1000)


def test_interest_share_shrinks_over_time():
    schedule = amortization_schedule(50_000, 0.05, 10)
    interest = [p.interest for p in schedule]
    assert interest == sorted(interest, reverse=True)


def test_each_row_balances():
    schedule = amortization_schedule(15_000, 0.045, 4)
    for payment in schedule:
        assert payment.payment == pytest.approx(payment.principal + payment.interest)


def test_total_interest_equals_payments_minus_principal():
    schedule = amortization_schedule(30_000, 0.06, 5)
    paid = sum(p.payment for p in schedule)
    assert total_interest(schedule) == pytest.approx(paid - 30_000)


def test_extra_payment_shortens_loan_and_saves_interest():
    result = compare_extra_payment(200_000, 0.06, 30, extra_payment=200)
    assert result.base_payments == 360
    assert result.new_payments < result.base_payments
    assert result.payments_saved == result.base_payments - result.new_payments
    assert result.interest_saved > 0
    assert result.interest_saved == pytest.approx(result.base_interest - result.new_interest)


def test_final_payment_with_extra_is_reduced_to_remaining_balance():
    schedule = amortization_schedule(10_000, 0.05, 3, extra_payment=150)
    regular = schedule[0].payment
    assert schedule[-1].payment <= regular
    assert schedule[-1].balance == 0


def test_quarterly_payments():
    schedule = amortization_schedule(8_000, 0.08, 2, payments_per_year=4)
    assert len(schedule) == 8
    assert schedule[-1].balance == 0


@pytest.mark.parametrize(
    "args",
    [(0, 0.05, 5), (-100, 0.05, 5), (1000, -0.01, 5), (1000, 0.05, 0)],
)
def test_payment_amount_rejects_invalid_input(args):
    with pytest.raises(ValueError):
        payment_amount(*args)


def test_rejects_fractional_number_of_payments():
    with pytest.raises(ValueError):
        payment_amount(1000, 0.05, 1.03)


def test_rejects_negative_extra_payment():
    with pytest.raises(ValueError):
        amortization_schedule(1000, 0.05, 1, extra_payment=-5)
