import math

import pytest

from finance_toolkit import (
    continuous_future_value,
    effective_annual_rate,
    future_value,
    growth_schedule,
    rule_of_72,
    years_to_reach,
)


def test_annual_compounding_lump_sum():
    assert future_value(1000, 0.05, 10, periods_per_year=1) == pytest.approx(1628.894627)


def test_monthly_compounding_beats_annual():
    monthly = future_value(1000, 0.05, 10, periods_per_year=12)
    annual = future_value(1000, 0.05, 10, periods_per_year=1)
    assert monthly == pytest.approx(1647.009498)
    assert monthly > annual


def test_monthly_contributions_end_of_period():
    assert future_value(0, 0.05, 10, contribution=100) == pytest.approx(15528.23, abs=0.01)


def test_contributions_at_start_earn_one_more_period():
    end = future_value(0, 0.05, 10, contribution=100)
    start = future_value(0, 0.05, 10, contribution=100, contribution_at_start=True)
    assert start == pytest.approx(end * (1 + 0.05 / 12))


def test_zero_rate_is_simple_sum():
    assert future_value(1000, 0.0, 10, contribution=100) == pytest.approx(13000)


def test_zero_years_returns_principal():
    assert future_value(1000, 0.07, 0) == pytest.approx(1000)


def test_continuous_compounding():
    assert continuous_future_value(1000, 0.05, 10) == pytest.approx(1000 * math.e**0.5)


def test_continuous_is_upper_bound_on_discrete():
    assert continuous_future_value(1000, 0.05, 10) > future_value(1000, 0.05, 10, 365)


@pytest.mark.parametrize(
    "nominal, periods, expected",
    [(0.12, 12, 0.126825), (0.12, 1, 0.12), (0.06, 4, 0.061364)],
)
def test_effective_annual_rate(nominal, periods, expected):
    assert effective_annual_rate(nominal, periods) == pytest.approx(expected, abs=1e-6)


def test_years_to_double():
    assert years_to_reach(2000, 1000, 0.06, periods_per_year=1) == pytest.approx(11.8957, abs=1e-4)


def test_years_to_reach_round_trips_with_future_value():
    years = years_to_reach(5000, 1000, 0.08)
    assert future_value(1000, 0.08, years) == pytest.approx(5000)


def test_rule_of_72_is_close_to_exact_doubling_time():
    estimate = rule_of_72(0.08)
    exact = years_to_reach(2, 1, 0.08, periods_per_year=1)
    assert estimate == pytest.approx(9)
    assert abs(estimate - exact) < 0.1


def test_growth_schedule_matches_closed_form():
    schedule = growth_schedule(5000, 0.06, 5, contribution=200)
    assert len(schedule) == 5
    assert schedule[-1].end_balance == pytest.approx(future_value(5000, 0.06, 5, contribution=200))


def test_growth_schedule_years_chain_together():
    schedule = growth_schedule(1000, 0.04, 3, contribution=50)
    for previous, current in zip(schedule, schedule[1:]):
        assert current.start_balance == pytest.approx(previous.end_balance)
    for row in schedule:
        assert row.end_balance == pytest.approx(row.start_balance + row.contributions + row.interest)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"principal": -1, "annual_rate": 0.05, "years": 1},
        {"principal": 100, "annual_rate": -0.05, "years": 1},
        {"principal": 100, "annual_rate": 0.05, "years": -1},
        {"principal": 100, "annual_rate": 0.05, "years": 1, "periods_per_year": 0},
        {"principal": 100, "annual_rate": 0.05, "years": 1, "contribution": -10},
    ],
)
def test_future_value_rejects_invalid_input(kwargs):
    with pytest.raises(ValueError):
        future_value(**kwargs)


def test_years_to_reach_rejects_target_below_principal():
    with pytest.raises(ValueError):
        years_to_reach(500, 1000, 0.05)


def test_growth_schedule_requires_whole_years():
    with pytest.raises(ValueError):
        growth_schedule(1000, 0.05, 2.5)
