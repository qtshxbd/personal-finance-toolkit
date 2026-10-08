"""Compound interest and savings-growth calculations.

Rates are expressed as decimals (5% -> 0.05). Contributions are made once per
compounding period, at the end of the period unless stated otherwise.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


def _validate(principal: float, annual_rate: float, years: float, periods_per_year: int) -> None:
    if principal < 0:
        raise ValueError("principal must be non-negative")
    if annual_rate < 0:
        raise ValueError("annual_rate must be non-negative")
    if years < 0:
        raise ValueError("years must be non-negative")
    if periods_per_year < 1:
        raise ValueError("periods_per_year must be at least 1")


def future_value(
    principal: float,
    annual_rate: float,
    years: float,
    periods_per_year: int = 12,
    contribution: float = 0.0,
    contribution_at_start: bool = False,
) -> float:
    """Value of an account after `years`, with optional recurring contributions.

    Uses FV = P(1 + r)^n + C * ((1 + r)^n - 1) / r, where r is the periodic rate
    and n the number of periods. Contributions at the start of each period
    (an annuity due) earn one extra period of interest.
    """
    _validate(principal, annual_rate, years, periods_per_year)
    if contribution < 0:
        raise ValueError("contribution must be non-negative")

    r = annual_rate / periods_per_year
    n = periods_per_year * years
    if r == 0:
        return principal + contribution * n

    growth = (1 + r) ** n
    contributions_value = contribution * (growth - 1) / r
    if contribution_at_start:
        contributions_value *= 1 + r
    return principal * growth + contributions_value


def continuous_future_value(principal: float, annual_rate: float, years: float) -> float:
    """Future value under continuous compounding: P * e^(rt)."""
    _validate(principal, annual_rate, years, 1)
    return principal * math.exp(annual_rate * years)


def effective_annual_rate(nominal_rate: float, periods_per_year: int) -> float:
    """Convert a nominal annual rate to the effective annual rate (APY)."""
    _validate(0, nominal_rate, 0, periods_per_year)
    return (1 + nominal_rate / periods_per_year) ** periods_per_year - 1


def years_to_reach(
    target: float, principal: float, annual_rate: float, periods_per_year: int = 12
) -> float:
    """Years for a lump sum to grow to `target` with no further contributions."""
    _validate(principal, annual_rate, 0, periods_per_year)
    if principal == 0 or annual_rate == 0:
        raise ValueError("principal and annual_rate must be positive to grow")
    if target < principal:
        raise ValueError("target must be at least the principal")
    periodic = math.log(1 + annual_rate / periods_per_year)
    return math.log(target / principal) / (periods_per_year * periodic)


def rule_of_72(annual_rate: float) -> float:
    """Quick estimate of the years needed to double money at `annual_rate`."""
    if annual_rate <= 0:
        raise ValueError("annual_rate must be positive")
    return 72 / (annual_rate * 100)


@dataclass(frozen=True)
class YearSummary:
    year: int
    start_balance: float
    contributions: float
    interest: float
    end_balance: float


def growth_schedule(
    principal: float,
    annual_rate: float,
    years: int,
    periods_per_year: int = 12,
    contribution: float = 0.0,
) -> list[YearSummary]:
    """Year-by-year breakdown of an account's growth (end-of-period contributions)."""
    _validate(principal, annual_rate, years, periods_per_year)
    if contribution < 0:
        raise ValueError("contribution must be non-negative")
    if int(years) != years:
        raise ValueError("years must be a whole number for a yearly schedule")

    r = annual_rate / periods_per_year
    balance = principal
    schedule = []
    for year in range(1, int(years) + 1):
        start = balance
        interest_total = 0.0
        for _ in range(periods_per_year):
            interest = balance * r
            interest_total += interest
            balance += interest + contribution
        schedule.append(
            YearSummary(
                year=year,
                start_balance=start,
                contributions=contribution * periods_per_year,
                interest=interest_total,
                end_balance=balance,
            )
        )
    return schedule
