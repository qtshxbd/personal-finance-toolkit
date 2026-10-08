"""Personal Finance Toolkit: compound interest, loan amortization, and budgeting."""

from .budget import Budget, CategorySummary, Expense, fifty_thirty_twenty
from .interest import (
    YearSummary,
    continuous_future_value,
    effective_annual_rate,
    future_value,
    growth_schedule,
    rule_of_72,
    years_to_reach,
)
from .loans import (
    Payment,
    PayoffComparison,
    amortization_schedule,
    compare_extra_payment,
    payment_amount,
    total_interest,
)

__version__ = "1.0.0"

__all__ = [
    "Budget",
    "CategorySummary",
    "Expense",
    "Payment",
    "PayoffComparison",
    "YearSummary",
    "amortization_schedule",
    "compare_extra_payment",
    "continuous_future_value",
    "effective_annual_rate",
    "fifty_thirty_twenty",
    "future_value",
    "growth_schedule",
    "payment_amount",
    "rule_of_72",
    "total_interest",
    "years_to_reach",
]
