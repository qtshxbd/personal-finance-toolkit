"""Loan payment and amortization calculations for fixed-rate loans."""

from __future__ import annotations

from dataclasses import dataclass

_BALANCE_TOLERANCE = 1e-9


@dataclass(frozen=True)
class Payment:
    number: int
    payment: float
    principal: float
    interest: float
    balance: float


@dataclass(frozen=True)
class PayoffComparison:
    base_payments: int
    new_payments: int
    payments_saved: int
    base_interest: float
    new_interest: float
    interest_saved: float


def _num_payments(years: float, payments_per_year: int) -> int:
    n = years * payments_per_year
    if abs(n - round(n)) > 1e-9:
        raise ValueError("years * payments_per_year must be a whole number of payments")
    return int(round(n))


def _validate(principal: float, annual_rate: float, years: float, payments_per_year: int) -> None:
    if principal <= 0:
        raise ValueError("principal must be positive")
    if annual_rate < 0:
        raise ValueError("annual_rate must be non-negative")
    if years <= 0:
        raise ValueError("years must be positive")
    if payments_per_year < 1:
        raise ValueError("payments_per_year must be at least 1")


def payment_amount(
    principal: float, annual_rate: float, years: float, payments_per_year: int = 12
) -> float:
    """Fixed payment that pays off the loan exactly: P * r / (1 - (1 + r)^-n)."""
    _validate(principal, annual_rate, years, payments_per_year)
    n = _num_payments(years, payments_per_year)
    r = annual_rate / payments_per_year
    if r == 0:
        return principal / n
    return principal * r / (1 - (1 + r) ** -n)


def amortization_schedule(
    principal: float,
    annual_rate: float,
    years: float,
    payments_per_year: int = 12,
    extra_payment: float = 0.0,
) -> list[Payment]:
    """Payment-by-payment breakdown of interest, principal, and remaining balance.

    `extra_payment` is added to every scheduled payment and goes entirely to
    principal, which shortens the loan. The final payment is reduced so the
    balance lands exactly on zero.
    """
    if extra_payment < 0:
        raise ValueError("extra_payment must be non-negative")
    scheduled = payment_amount(principal, annual_rate, years, payments_per_year)
    n = _num_payments(years, payments_per_year)
    r = annual_rate / payments_per_year

    balance = principal
    schedule = []
    number = 0
    while balance > _BALANCE_TOLERANCE and number < n:
        number += 1
        interest = balance * r
        principal_paid = min(scheduled + extra_payment - interest, balance)
        balance -= principal_paid
        if balance < _BALANCE_TOLERANCE:
            balance = 0.0
        schedule.append(
            Payment(
                number=number,
                payment=principal_paid + interest,
                principal=principal_paid,
                interest=interest,
                balance=balance,
            )
        )
    return schedule


def total_interest(schedule: list[Payment]) -> float:
    """Total interest paid over a schedule."""
    return sum(p.interest for p in schedule)


def compare_extra_payment(
    principal: float,
    annual_rate: float,
    years: float,
    extra_payment: float,
    payments_per_year: int = 12,
) -> PayoffComparison:
    """How many payments and how much interest an extra recurring payment saves."""
    base = amortization_schedule(principal, annual_rate, years, payments_per_year)
    faster = amortization_schedule(
        principal, annual_rate, years, payments_per_year, extra_payment=extra_payment
    )
    base_interest = total_interest(base)
    new_interest = total_interest(faster)
    return PayoffComparison(
        base_payments=len(base),
        new_payments=len(faster),
        payments_saved=len(base) - len(faster),
        base_interest=base_interest,
        new_interest=new_interest,
        interest_saved=base_interest - new_interest,
    )
